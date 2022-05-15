import os
#file.seek = go to byte in file
#   os.SEEK_SET = set the position relative to the beginning of the file
#   os.SEEK_CUR = set it relative to the current position
#   os.SEEK_END = set it relative to the end of the file
#hex(file.tell()) = pointer location
def dbg():
    global file
    print(hex(file.tell()))

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
    classID = uint32(file.read(4))
    print('Class ID of main class instance:',classID)
    if version >= 6:
        userDataSize = uint32(file.read(4))
        print('User data size:',userDataSize)
        userData = {'numHeaderChunks':uint32(file.read(4)),
                    'HeaderEntry':[uint32(file.read(4)),uint32(file.read(4))]
                    }
        print(userData)
print('\n\n\nend')



