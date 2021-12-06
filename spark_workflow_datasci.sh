#!/bin/sh
files="bitcoinBlocks.txt"

if [ ! -z "$2" ]
then  
  echo "Usage: ./spark_workflow_linux.sh filename.txt"
  exit 1
fi

if [ ! -z "$1" ]
then
  files=$1
fi

echo "###### Removing Previous CSV files... ######"

hadoop fs -rm -r inputs_mapping.csv &&
hadoop fs -rm -r outputs.csv &&
hadoop fs -rm -r transactions.csv &&
hadoop fs -rm -r inputs.csv &&
hadoop fs -rm -r addrs.csv &&

echo "###### Spark Parsing Workflow Starts... ######"
spark-submit \
  --master local[4] \
  sparkParser.py $files &&

echo "###### Concatenating Parse Files to CSV... ######\n"

hadoop fs -cat csv/inputs_mapping/part* | sed -e '/^ *$/d' | hadoop fs -put - inputs_mapping.csv &&
hadoop fs -cat csv/outputs/part* | sed -e '/^ *$/d' | hadoop fs -put - outputs.csv &&
hadoop fs -cat csv/transactions/part* | sed -e '/^ *$/d' | hadoop fs -put - transactions.csv &&
hadoop fs -cat csv/inputs/part* | sed -e '/^ *$/d' | hadoop fs -put - inputs.csv &&

echo "###### Deleting Part Files... ######\n"

hadoop fs -rm -r csv/inputs_mapping &&
hadoop fs -rm -r csv/outputs &&
hadoop fs -rm -r csv/transactions &&
hadoop fs -rm -r csv/inputs &&
#
echo "\n###### Parsing Completed ######\n"

echo "###### Extracting Payer to Payee Addresses... ######\n"

spark-submit \
   --num-executors 4 --executor-cores 4 --executor-memory 24G --driver-memory 2g \
  sparkMapAddrs.py inputs.csv outputs.csv

hadoop fs -cat csv/addrs/part* | sed -e '/^ *$/d' | hadoop fs -put - addrs.csv &&
hadoop fs -rm -r csv/addrs