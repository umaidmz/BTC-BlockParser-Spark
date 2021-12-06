"""
Author: Umaid Muhammad Zaffar
"""

from bitcoinlib.services.services import Service

class BitcoinBlockFetcher:
    def __init__(self):
        self.service = Service()
        info = self.service.getinfo()
        self.blockcount = info["blockcount"]
    
    def fetchBlock(self, num):
        return self.service.getrawblock(num)

    def saveRecentBlocks(self, num, filename):
        with open(filename, "w") as file:
            for i in range(num, 0, -1):
                blockNum = self.blockcount-i
                print("Fetching Block: "+ str(blockNum))
                file.write(str(blockNum)+" ")
                file.write(self.fetchBlock(blockNum))
                file.write("\n")

    def saveFirstBlocks(self, num, filename):
        with open(filename, "w") as file:
            for i in range(num):
                print("Fetching Block: "+ str(i))
                file.write(str(i)+" ")
                file.write(self.fetchBlock(i))
                file.write("\n")

    def saveRangeOfBlocks(self, start, num, filename):
        with open(filename, "w") as file:
            for i in range(start, start+num):
                print("Fetching Block: "+ str(i))
                file.write(str(i)+" ")
                file.write(self.fetchBlock(i))
                file.write("\n")