"""
Filename: block.py

Current Author:
    * Umaid Muhammad Zaffar (https://github.com/umaidzz)

Previous Authors:
    * Alex (https://github.com/tenthirtyone)
    * Peng Wu (https://github.com/pw2393)
"""

from utils.RawBlockProcessor import *


class BlockHeader:
    def __init__(self, blockchain, processor):
        self.pos_start = processor.getOffset()
        self.hash = double_sha256(bytes.fromhex(blockchain[0:160]))[::-1]
        ######
        self.version = processor.uint4(blockchain)
        self.previousHash = processor.hash32(blockchain)
        self.merkleHash = processor.hash32(blockchain)
        self.time = processor.uint4(blockchain)
        self.bits = processor.uint4(blockchain)
        self.nonce = processor.uint4(blockchain)


    def toString(self):
        print("Hash:\t %s" %self.hash)
        print("Version:\t %d" % self.version)
        print("Previous Hash\t %s" % self.previousHash)
        print("Merkle Root\t %s" % self.merkleHash)
        print("Time\t\t %s" % str(self.time))
        print("Difficulty\t %8x" % self.bits)
        print("Nonce\t\t %s" % self.nonce)


class Block:
    def __init__(self, rawblock):
        self.processor = RawBlockProcessor()
        self.blockheader = BlockHeader(rawblock, self.processor)
        self.txCount = 0
        self.Txs = []
        self.txCount = self.processor.varint(rawblock)

        self.Txs = []

        for i in range(0, self.txCount):
            tx = Tx(rawblock, self.processor)
            self.Txs.append(tx)
    

    def toString(self):
        print("")
        print( "Magic No: \t%8x" % self.magicNum)
        print( "Blocksize: \t", self.blocksize)
        print( "")
        print( "#" * 10 + " Block Header " + "#" * 10)
        self.blockHeader.toString()
        print( "##### Tx Count: %d" % self.txCount)
        for t in self.Txs:
            pass
            #t.toString()
            #if hashStr(t.hash) == "3ae43bb0a8e4cc3a345a7a2a688217bcb8d9f7e9001263930cd23e9b3b7364c6":
            #    raise KeyError

    def toMemory(self):
        inputrows = []
        outputrows = []
        txrows = []
        timestamp = blktime2datetime(self.blockheader.time)
        # if timestamp.startswith('2013-10-25'):
        for tx in self.Txs:
            for m, input in enumerate(tx.inputs):
                inputrows.append((hashStr(tx.hash),
                                                m,
                                                hashStr(input.prevhash),
                                                input.txOutId,
                                                timestamp))
            amount = 0
            for n, output in enumerate(tx.outputs):
                amount += output.value
                outputrows.append((hashStr(tx.hash),
                                                n,
                                                output.value,
                                                rawpk2addr(output.pubkey)))
            txrows.append((hashStr(tx.hash),
                                            amount,
                                            timestamp,
                                            tx.inCount,
                                            tx.outCount))
        return inputrows, outputrows, txrows


class Tx:
    def __init__(self, block, processor):
        self.pos_start = processor.getOffset()
        ######
        self.version = processor.uint4(block)
        self.flag_start = processor.getOffset()
        self.flag = processor.readFlag(block)
        self.flag_end= processor.getOffset()
        self.inCount = processor.varint(block)
        self.inputs = []
        for i in range(0, self.inCount):
            input = txInput(block, processor)
            self.inputs.append(input)
        self.outCount = processor.varint(block)
        self.outputs = []
        if self.outCount > 0:
            for i in range(0, self.outCount):
                output = txOutput(block, processor)
                self.outputs.append(output)

        self.wit_start = processor.getOffset()
        if(self.flag):
            for i in range(0, self.inCount):
                self.inputs[i].witness = txWitness(block, processor)
        self.wit_end = processor.getOffset()

        self.lockTime = processor.uint4(block)
        ######
        self.pos_end = processor.getOffset()

        self.hash = double_sha256(bytes.fromhex(block[self.pos_start:self.flag_start]+ block[self.flag_end:self.wit_start]+block[self.wit_end:self.pos_end]))[::-1]

    def toString(self):
        print( "")
        print( "=" * 10 + " New Transaction " + "=" * 10)
        print( "Tx Version:\t %d" % self.version)
        print( "Inputs:\t\t %d" % self.inCount)
        for i in self.inputs:
            i.toString()

        print( "Outputs:\t %d" % self.outCount)
        for o in self.outputs:
            o.toString()
        print( "Lock Time:\t %d" % self.lockTime)
        ######
        print( "Tx Hash:\t %s" % hashStr(self.hash))


class txInput:
    def __init__(self, block, processor):
        self.prevhash = processor.hash32(block)
        self.witness = ""
        self.txOutId = processor.uint4(block)
        self.scriptLen = processor.varint(block)
        self.scriptSig = processor.read(self.scriptLen, block)
        self.seqNo = processor.uint4(block)

    def toString(self):
        print( "Previous Hash:\t %s" % hashStr(self.prevhash))
        print( "Tx Out Index:\t %8x" % self.txOutId)
        print( "Script Length:\t %d" % self.scriptLen)
        print( "Script Sig:\t %s" % hashStr(self.scriptSig))
        print( "Sequence:\t %8x" % self.seqNo)


class txOutput:
    def __init__(self, block, processor):
        self.value = processor.uint8(block)
        self.scriptLen = processor.varint(block)
        self.pubkey = processor.read(self.scriptLen, block)

    def toString(self):
        print( "Value:\t\t %d" % self.value)
        print( "Script Len:\t %d" % self.scriptLen)
        print( "Pubkey:\t\t %s" % hashStr(self.pubkey))

class txWitness:
    def __init__(self, block, processor):
        self.wit_cnt = processor.varint(block)
        self.wit_comp = []
        for i in range(0, self.wit_cnt):
            witness = witnessComponent(block, processor)
            self.wit_comp.append(witness)

class witnessComponent:
    def __init__(self, block, processor):
        self.wit_len = processor.varint(block)
        self.comp = processor.read(self.wit_len, block)

