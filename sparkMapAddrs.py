"""
Author: Umaid Muhammad Zaffar
"""


# Initialize Spark Context: local multi-threads
from pyspark import SparkConf, SparkContext
from utils.block import Block


output_folder = './csv/'
import os
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def one_to_one_tx(two_lists):
    inputs = two_lists[0]
    outputs = two_lists[1]
    if len(inputs) == 0 or len(outputs) == 0:
        return []

    sum_in = 0
    # i = (val, addr)
    # o = (val, addr)
    for i in inputs:
        sum_in += i[0]

    result = []
    for i in inputs:
        for o in outputs:
            if o[0] != 0: # Insidely filter out all zero output
                result.append(((i[1], o[1]), i[0]*o[0]*1.0/sum_in, i[2]))

    return result

def parse_outputs(line):
    """
    schema:
        txhash, nid, value, addr
    :param line:
    :return (key, value):
    """
    fields = line.split(',')
    return fields[0], (int(fields[2]), fields[3])


def parse_inputs(line):
    """
    schema:
        txhash, mid, value, addr, time
    :param line:
    :return (key, value):
    """
    fields = line.split(',')
    return fields[0], (int(fields[2]), fields[3], fields[4])


def main():

    # Initialize Spark Context: local multi-threads
    conf = SparkConf().setAppName("...1")
    sc = SparkContext(conf=conf)

    inputs = sc.textFile(sys.argv[1]).map(lambda x: parse_inputs(x)).persist()
    outputs = sc.textFile(sys.argv[2]).map(lambda x: parse_outputs(x)).persist()

    final = inputs.cogroup(outputs).filter(lambda keyValue: len(keyValue[1][0]) != 0 and len(keyValue[1][1]) != 0).flatMapValues(one_to_one_tx)
   
    final.map(lambda x:x[1][0][0]+","+x[1][0][1]+","+str(x[1][1])+","+x[0]+","+x[1][2]).saveAsTextFile(output_folder+"addrs")
    print("Step 3 Completed")


    # End Program
   


if __name__ == "__main__":

    import sys
    if len(sys.argv) < 3:
        print("\n\tUSAGE:\n\t\tspark-submit spark_parser.py filename1.csv filename2.csv ...")
        sys.exit()

    import time
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
