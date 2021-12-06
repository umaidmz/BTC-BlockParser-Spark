"""
Filename: block.py
Author:
    * Umaid Muhammad Zaffar (https://github.com/umaidzz)
"""

import hashlib

def rawpk2hash160(pk_script):
    """
    Locate the raw 20-byte hash160 value of a public key right after 0x14
    """
    head = pk_script.find(b'\x14') + 1
    return pk_script[head:head + 20]


def hashStr(bytesArray):
    return bytesArray.hex()

def reverseHex(value):
    return bytes.fromhex(value)[::-1].hex()

def rawpk2addr(pk_script):
    """
    Convert a raw bitcoin block script of public key to a common address
    """
    import utils.base58  # reference program: base58.py
    return utils.base58.hash_160_to_bc_address(rawpk2hash160(pk_script))

def blktime2datetime(blktime):
    """
    Convert a bitcoin block timestamp integer to a datetime string.
    Note that current timestamp as seconds since 1970-01-01T00:00 UTC.
    """
    from datetime import timedelta, datetime
    d = datetime(1970, 1, 1, 0, 0, 0) + timedelta(days=int(blktime) / 86400, seconds=int(blktime) % 86400)
    return d.strftime('%Y-%m-%dT%H:%M:%S')

def double_sha256(bytebuffer):
    """
    Dual SHA256 on raw byte string
    """
    return hashlib.sha256(hashlib.sha256(bytebuffer).digest()).digest()

class RawBlockProcessor:
    def __init__(self):
        self.offset = 0
    
    def getOffset(self):
        return self.offset
    
    def setOffset(self, value):
        self.offset = value
    
    def uint1(self, block):
        o = self.offset
        val = reverseHex(block[o:o+2])
        self.offset+=2
        return int(val, 16)

    def uint2(self, block):
        o = self.offset
        val = reverseHex(block[o:o+4])
        self.offset+=4
        return int(val, 16)

    def uint4(self, block):
        o = self.offset
        val = reverseHex(block[o:o+8])
        self.offset+=8
        return int(val, 16)

    def uint8(self, block):
        o = self.offset
        val = reverseHex(block[o:o+16])
        self.offset+=16
        return int(val, 16)
    
    def hash32(self, block):
        o = self.offset
        val = reverseHex(block[o:o+64])
        self.offset+=64
        return bytes.fromhex(val)
    
    def varint(self, block):
        o = self.offset
        if(int(block[o:o+2], 16) < int("fd", 16)):
            self.setOffset(o+2)
            return int(reverseHex(block[o:o+2]),16)
        elif(int(block[o:o+2], 16) == int("fd", 16)):
            self.setOffset(o+6)
            return int(reverseHex(block[o+2:o+6]),16)
        elif(int(block[o:o+2], 16) == int("fe", 16)):
            self.setOffset(o+10)
            return int(reverseHex(block[o+2:o+10]),16)
        elif(int(block[o:o+2], 16) == int("ff", 16)):
            self.setOffset(o+18)
            return int(reverseHex(block[o+2:o+18]),16)
    
    def read(self, len, block):
        o = self.offset
        val = block[o:o+(len*2)]
        self.offset+=(len*2)
        return bytes.fromhex(val)
    
    def readFlag(self, block):
        o = self.offset
        if(bool(int(block[o:o+2], 16))):
            return False
        else:
            self.setOffset(o+4)
            return True

    
    

