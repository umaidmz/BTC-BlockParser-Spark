#!/bin/sh
files=""
if [ ! -z "$2" ]
then  
  echo "Usage: ./spark_workflow_linux.sh filename.txt"
  exit 1
fi

if [ ! -z "$1" ]
then
  files=$1
else
  echo "Usage: Filename Missing"
  exit 1
fi

echo "Input File: $files"

echo "###### Spark Parsing Workflow Starts... ######\n"
spark-submit \
  --master local[4] \
  sparkParser.py $files &&
# Better Data Storage:
echo "###### Concatenating Parse Files to CSV... ######\n"

cat csv/inputs_mapping/part* | sed -e '/^ *$/d' > csv/inputs_mapping.csv &&
cat csv/outputs/part* | sed -e '/^ *$/d' > csv/outputs.csv &&
cat csv/transactions/part* | sed -e '/^ *$/d' > csv/transactions.csv &&
cat csv/inputs/part* | sed -e '/^ *$/d' > csv/inputs.csv &&


echo "###### Deleting Part Files... ######\n"
rm -r csv/inputs_mapping &&
rm -r csv/outputs &&
rm -r csv/transactions &&
rm -r csv/inputs &&
#
echo "\n###### Parsing Completed ######\n"

echo "###### Extracting Payer to Payee Addresses... ######\n"
spark-submit \
  --master local[4] \
  sparkMapAddrs.py csv/inputs.csv csv/outputs.csv

cat csv/addrs/part* | sed -e '/^ *$/d' > csv/addrs.csv &&
rm -r csv/addrs