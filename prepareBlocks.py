#!/usr/bin/python3
"""
Umaid Muhammad Zaffar

Sample usage: ./prepareBlocks -n 10
"""


from utils.BitcoinBlockFetcher import BitcoinBlockFetcher
import argparse
from subprocess import call

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare Blocks for Apache Spark")
    parser.add_argument('-n','--num',help="Number of Blocks to be parsed",type=int,default=10)
    parser.add_argument('-s','--start',help="Start block for parsing",type=int,default=-1)
    parser.add_argument('-r','--range',help="Specifies if we want range",type=bool,default=False)
    parser.add_argument('-f', '--file', help='Filename where to save data',type=str,default='bitcoinBlocks.txt')
    parser.add_argument('-e', '--env', help='Environment of the module',type=str,default='linux')

    args=parser.parse_args()
    try:
        blockFetcher = BitcoinBlockFetcher()
        if(args.start != -1 and args.range):
            print("Fetching Range of Blocks")
            blockFetcher.saveRangeOfBlocks(args.start, args.num, args.file)
        elif(args.start != -1):          
            print("Fetching First Blocks")
            blockFetcher.saveFirstBlocks(args.num+1, args.file)
        elif(args.start == -1 and not(args.range)):
            print("Fetching Recent Blocks")
            blockFetcher.saveRecentBlocks(args.num, args.file)
        else:
            print("usage: both start and range must be set or neither should be set")            
        if(args.env != "linux"):
            call("hadoop", "fs", "-put", args.file)

    except Exception as e:
        print(e)
    
    
