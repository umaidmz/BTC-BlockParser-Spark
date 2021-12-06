# RawBTCBlockParser-Spark

## Author: Umaid Muhammad Zaffar

## Introduction

This tool was developed as a project for Data Intensive Distributed Computing CS 651 taught by Dr. Ali Abedi. Beginners to Cryptocurrency Analysis find it a challenging task to collect bitcoin raw data without downloading bitcoin core. Therefore, the usual approach is to lookup websites such as blockchain.info and fetch binary data. In this tool, I automated this process that provides raw block and stores them in a format that would be scalable to HDFS. In this way we avoid downloading bitcoin-core and parse raw blocks. The implementations stemmed from a previous work (https://github.com/pw2393/spark-bitcoin-parser) with the following improvements:


1. Uses Python3 instead of Python2
2. Independant of bitcoin-core which is requires alot of time to download
3. Provides an end to end implementation to fetch raw data and parse it
4. <b>Scalable to Hadoop Distributed File System</b>
5. Parsing updated according to the latest bitcoin protocol


## How to Run?

The following steps are required to successfully run this tool on your linux/ hadoop cluster.

### Data Collection
We must prepare the data so that we can input it into spark. For that we should avoid sequential reading of files because that will not be scalable to HDFS and it would be required to download bitcoin-core (which I totally wanted to avoid because it was taking 3 days 😔). I used bitcoinlib (https://bitcoinlib.readthedocs.io/en/latest/#) to fetch raw data and store that raw data in a key value format where key is block height and value is the raw data. I have done so in prepareBlocks.py and now I will take you through it.<br><br>

        usage: prepareBlocks.py [-h] [-n NUM] [-s START] [-r RANGE] [-f FILE] [-e ENV]

        Prepare Blocks for Apache Spark

        optional arguments:
        -h, --help            show this help message and exit
        -n NUM, --num NUM     Number of Blocks to be parsed
        -s START, --start START
                                Start block for parsing
        -r RANGE, --range RANGE
                                Specifies if we want range
        -f FILE, --file FILE  Filename where to save data
        -e ENV, --env ENV     Environment of the module

Fetch 10 most recent blocks:

        ./prepareBlocks.py -n 10

Fetch 10 blocks starting from genesis (first) block:

        ./prepareBlocks.py -n 10 -s 511114

Fetch 10  blocks starting from 511114 block:

        ./prepareBlocks.py -n 10 -s 511114 -r True

Fetch 10  blocks starting from 511114 block and store it to myData.txt:

        ./prepareBlocks.py -n 10 -s 511114 -r True -f myData.txt

Fetch 10  blocks starting from 511114 block, store it to myData.txt and copy it to HDFS:

        ./prepareBlocks.py -n 10 -s 511114 -r True -f myData.txt -e hdfs

### Data Parsing:

Now we have each line of data representing each block so we can use spark to process these files that can be used in HDFS as well. I followed the protocol (https://en.bitcoin.it/wiki/Protocol_documentation) to parse the data. Remember, witness transactions were introduced after 2017 and are not included in tx hash.

<b>Linux:</b> <br>

Use myData.txt in previous step and input it to this command.

        ./spark_workflow_linux.sh myData.txt

<b>HDFS:</b> <br>

Use myData.txt in previous step and input it to this command.

        ./spark_workflow_datasci.sh myData.txt


### Output:
Output Folder: csv/
Credits: https://github.com/pw2393/spark-bitcoin-parser
Output CSV Files | Schema
------ | ------
transactions.csv  | tx_hash tx_value, timestamp, num_inputs, num_outputs
outputs.csv  | tx_hash, output_index, output_value, output_address
inputs_mapping.csv  |  tx_hash, input_index, prev_tx_hash, output_index
inputs.csv  | tx_hash, input_index, input_value, input_address, time
addrs.csv  | payer_address, payee_address, value, tx_hash, time

### For Testing:

you can check out how I started this module in tests folder where the ipynb file contains my initial progress.
