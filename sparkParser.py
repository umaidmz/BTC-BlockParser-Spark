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


def parse(blockchain):
    keyVal = blockchain.split(" ")
    rawBlock = keyVal[1]
    block = Block(rawBlock)
    print('Block: '+ str(keyVal[0]) + " Parsed")
    return block.toMemory()


def main():

    # Initialize Spark Context: local multi-threads
    conf = SparkConf().setAppName("Raw Block Parser")
    sc = SparkContext(conf=conf)


    rawBlocks = sc.textFile(sys.argv[1]).map(lambda x: parse(x))
    inputs = rawBlocks.map(lambda x: x[0]).flatMap(lambda x:x).map(lambda x:((x[2],str(x[3])), (x[0], str(x[1]), x[4])))
    outputs = rawBlocks.map(lambda x: x[1]).flatMap(lambda x:x).map(lambda x:((x[0],str(x[1])), (str(x[2]), x[3])))
    transactions = rawBlocks.map(lambda x: x[2]).flatMap(lambda x:x).map(lambda x:x[0]+","+str(x[1])+","+x[2]+","+str(x[3])+","+ str(x[4]))

    metafinal = inputs.join(outputs).persist()
    final = metafinal.values()

    #new_inputs = final.map(lambda x:(x[0][0],(int(x[1][0]), x[1][1], x[0][2])))
    new_outputs = outputs.map(lambda x:(x[0][0],(int(x[1][0]), x[1][1])))

    #new_final = new_inputs.cogroup(new_outputs).filter(lambda keyValue: len(keyValue[1][0]) != 0 and len(keyValue[1][1]) != 0).flatMapValues(one_to_one_tx)

    # Transformations and/or Actions
    rawBlocks.map(lambda x: x[0]).flatMap(lambda x:x).map(lambda x:x[0]+","+str(x[1])+","+x[2]+","+str(x[3])+","+x[4]).saveAsTextFile(output_folder+'inputs_mapping')
    rawBlocks.map(lambda x: x[1]).flatMap(lambda x:x).map(lambda x:x[0]+","+str(x[1])+","+str(x[2])+","+x[3]).saveAsTextFile(output_folder+'outputs')
    transactions.saveAsTextFile(output_folder+'transactions')
    print("Step 1 Completed")
    final.map(lambda x:x[0][0]+","+x[0][1]+","+x[1][0]+","+x[1][1]+","+x[0][2]).saveAsTextFile(output_folder+"inputs")
    print("Step 2 Completed")

    #new_final.map(lambda x:x[1][0][0]+","+x[1][0][1]+","+str(x[1][1])+","+x[0]+","+x[1][2]).saveAsTextFile(output_folder+"addrs")
    #print("Step 3 Completed")


    # End Program
   


if __name__ == "__main__":

    import sys
    if len(sys.argv) < 2:
        print("\n\tUSAGE:\n\t\tspark-submit spark_parser.py filename1.dat filename2.dat ...")
        sys.exit()

    import time
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
