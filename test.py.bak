
def pplist(arr): #Pretty print list of lists
    for i in range(len(arr)):
        if type(arr[i]) is list:
            arr[i]=pplist(arr[i])
        else:
            arr[i]=str(arr[i])
    return arr

import os
#file.seek = go to byte in file
#   os.SEEK_SET = set the position relative to the beginning of the file
#   os.SEEK_CUR = set it relative to the current position
#   os.SEEK_END = set it relative to the end of the file
#hex(file.tell()) = pointer location
def dbg(num=False):
    global file
    print(file.tell() if num else hex(file.tell()))

import struct
#For unpacking the weird c++ datatypes
def char(data,decode=True):#1 byte
    result = struct.unpack('<c',data)[0]
    if decode:
        result = result.decode()
    return result
def uint16(data):#2 bytes
    return struct.unpack('<H',data)[0]
def uint32(data):#4 bytes
    return struct.unpack('<L',data)[0]

import json
def loadJson(file):
    js=json.load(file)
    file.close()
    return js
class ClassID: #5-7 hours of work on this class+reference table oh my god
    reference = loadJson(open('ref.json','r'))
    def __init__(self,data):  
        self.engine = hex(data[3])[2:].zfill(2).upper()
        self.grass = hex((data[2]<<4)+(data[1]>>4))[2:].zfill(3).upper() #Not class because thats reserved keyword
        self.chunk = hex(((data[1]&0x0f)<<8)+(data[0]))[2:].zfill(3).upper()
        assert self.engine in ClassID.reference['engineNames'], 'Invalid engine '+self.engine
        assert self.grass in ClassID.reference['classNames'][self.engine], 'Invalid class '+self.grass
    
    def __str__(self):
        return ClassID.reference['engineNames'][self.engine]+'/'+ClassID.reference['classNames'][self.engine][self.grass]+'/'+self.chunk
    
    #def __repr__(self):
    #    return self.__str__()
    
file = open('2022-05-10-01-13-39_Oachkatzlschwoafs on ICE_close5angle.Replay.Gbx','rb')
file.seek(0, os.SEEK_SET)

#https://wiki.xaseco.org/wiki/GBX: Header
assert file.read(3) == b'GBX'
version = uint16(file.read(2))
print('GBX file version:',version)
if version >= 3:
    _format = char(file.read(1))
    assert char(file.read(1))=='U'
    compression = char(file.read(1))
    print('Format (Binary/Text):',_format,'Body compression (Uncompressed/Compressed):',compression)
    if version >= 4:
        unknown = char(file.read(1))
    classID = ClassID(file.read(4))
    print('Class ID of main class instance:',classID)
    if version >= 6:
        userDataSize = uint32(file.read(4))
        print('User data size:',userDataSize)
        numHeaderChunks = uint32(file.read(4))
        print('numHeaderChunks:', numHeaderChunks)
        chunks = []
        chsz=0
        for i in range(numHeaderChunks):
            chunks.append([ClassID(file.read(4)),uint32(file.read(4))& 0x7fffffff]) 
            chsz+=chunks[-1][1]
        print(pplist(chunks))
        dbg()
        file.seek(chsz,os.SEEK_CUR) #Skip all data for now
        dbg()
    numNodes = uint32(file.read(4))
    print(numNodes)
#https://wiki.xaseco.org/wiki/GBX: Reference table
numExternalNodes = uint32(file.read(4))
print(numExternalNodes) 




