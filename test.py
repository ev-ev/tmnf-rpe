
def pplist(arr): #Pretty print list of lists
    res=list(range(len(arr)))
    for i in range(len(arr)):
        if type(arr[i]) is list:
            res[i]=pplist(arr[i])
        else:
            res[i]=str(arr[i])
    return res

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
def string(ds):
    length = uint32(ds.read(4))
    return ds.read(length).decode('utf-8')

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
        self.call = '_'+self.engine+self.grass+self.chunk
        assert self.engine in ClassID.reference['engineNames'], 'Invalid engine '+self.engine
        assert self.grass in ClassID.reference['classNames'][self.engine], 'Invalid class '+self.grass
    
    def __str__(self):
        return ClassID.reference['engineNames'][self.engine]+'/'+ClassID.reference['classNames'][self.engine][self.grass]+'/'+self.chunk

    
    #def __repr__(self):
    #    return self.__str__()

import io
lookbackstring = [] #??? certified trackmania moment tm
def LookBackString(ds): #Literally kms
    if len(lookbackstring) == 0:
        assert uint32(ds.read(4)) == 3
    index = uint32(ds.read(4)) #31&30 define string type or something??
    b31_30 = index>>30
    index = index&0x3fffffff
    if index == 0:
        if b31_30 != 0:
            newString = string(ds)
            lookbackstring.append(newString)
            return newString
        else:
            assert False==True
    elif index >= 1:
        if len(lookbackstring) < index:
            if b31_30 == 2:
                return "Unassigned"
            elif b31_30 == 0:
                assert False==True
            else:
                return -1
        else:
            return lookbackstring[index-1]            
        
    
    
def Meta(ds): #Why is this a feature
    return (LookBackString(ds),LookBackString(ds),LookBackString(ds))
def readChunk(ID,data):
    if callable(getattr(ChunkReader,ID.call,None)):
        return getattr(ChunkReader,ID.call)(data)
    else:
        print(str(ID),' not implemented, skipping')
class ChunkReader:
    def _template(data):
        result = {}
        ds = io.BytesIO(data)
        #code
        ds.close()
        return result
    def _03093000(data): #Game/CGameCtnReplayRecord/000 "Version"
        result = {}
        ds = io.BytesIO(data)
        result['version'] = uint32(ds.read(4))
        if result['version'] >= 2:
            result['trackUID'], result['enviroment'], result['author']=Meta(ds)
            result['time'] = uint32(ds.read(4))
            result['nickName'] = string(ds)
            if result['version'] >= 6:
                result['driverLogin'] = string(ds)
                if version >= 8:
                    ds.seek(1,os.SEEK_CUR) #byte 1
                    result['titleUID'] = LookBackString(ds)
        ds.close()
        return result
    def _03093001(data):#Game/CGameCtnReplayRecord/001 "Community"
        result = {}
        ds = io.BytesIO(data)
        result['xml']=string(ds)
        ds.close()
        return result

fs = ['2022-05-10-01-13-39_Oachkatzlschwoafs on ICE_close5angle.Replay.Gbx',"Hawkeye Nascar_ev_ev-nya(03'10''08)_silver.Replay.Gbx"]    
file = open(fs[1],'rb')
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
        for i in range(numHeaderChunks):
            chunks.append([ClassID(file.read(4)),uint32(file.read(4))& 0x7fffffff]) 
        print(pplist(chunks))
        for ID,SIZE in chunks:
            print(ID,readChunk(ID,file.read(SIZE)))
    numNodes = uint32(file.read(4))
    print('Number of related classes:',numNodes)
#https://wiki.xaseco.org/wiki/GBX: Reference table
#numExternalNodes = uint32(file.read(4))
#print(numExternalNodes) 




