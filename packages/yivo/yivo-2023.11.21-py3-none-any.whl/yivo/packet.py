###############################################
# The MIT License (MIT)
# Copyright (c) 2020 Kevin Walchko
# see LICENSE for full details
##############################################
from struct import Struct
from enum import IntEnum, unique # need for Errors
from .parser import YivoParser
from collections import namedtuple
from collections import UserDict

def make_Struct(payload):
    """
    [ 0, 1, 2, 3,4,    5:-2, -1]
    [h0,h1,LN,HN,T, payload, CS]
    Header: h0, h1
    N: payload length
       N = (HN << 8) + LN, max data bytes is 65,536 Bytes
         HN: High Byte
         LN: Low Byte
    T: packet type or MsgID

    Only insert the payload format and this returns: Struct(f"<2cHB{payload}B")
    """
    return Struct(f"<2cHB{payload}B")


Value = namedtuple("Value", "fmt cls")

class MsgInfo(UserDict):
    def __setitem__(self, key, value):
        if isinstance(key, int) == False or key > 255:
            raise Exception("Key must be an int <= 255")
        if isinstance(value, tuple) == False:
            raise Exception("value must be tuple")
        if isinstance(value[0], str) == False:
            raise Exception("value must contain a string and class name")
        if isinstance(value[1], type) == False:
            raise Exception("value must contain a string and class name")

        fmt = Struct(f"<2cHB{value[0]}B")
        cls = value[1]

        value = Value(fmt, cls)
        super().__setitem__(key, value)

@unique
class Errors(IntEnum):
    NONE             = 0
    INVALID_HEADER   = 1
    INVALID_LENGTH   = 2
    INVALID_CHECKSUM = 4
    INVALID_COMMAND  = 8
    INVALID_MSGID    = 16
    NO_DATA          = 32



def checksum(size,msgid,msg):
    if size == 0 and msg == None:
        return msgid

    # a,b = struct.pack('H', size)
    a = 0x00FF & size
    b = size >> 8

    cs = (a ^ b)^msgid
    # msg = [cs] + msg
    # cs = reduce(xor, msg)
    for m in msg:
        cs ^= m
    # print("cs", cs, cs.to_bytes(1,'little'))
    return cs

def chunk(msg):
    size = msg[2] + (msg[3] << 8) # messages sent little endian
    msgid = msg[4]

    if size == 0:
        payload = None
    else:
        payload = msg[5:-1]

    cs = msg[-1]
    return size, msgid, payload, cs

def num_fields(sensor):
    """Returns the number of fields in a message"""
    return len(sensor._fields)

class Yivo:
    # [ 0, 1, 2, 3,4, ..., -1]
    # [h0,h1,LN,HN,T, ..., CS]
    # Header: h0, h1
    # N = (HN << 8) + LN, max data bytes is 65,536 Bytes
    #   HN: High Byte
    #   LN: Low Byte
    # T: packet type or MsgID
    pack_cs = Struct("<B")

    def __init__(self, database, h0=b'$', h1=b'K'):
        """
        Message header can be changed (not sure why) if you need to
        by setting a new h0 and h1. They must be binary characters.
        """
        if not isinstance(h0, bytes) or not isinstance(h1, bytes):
            raise Exception(f"Invalid header bytes: {h0}({type(h0)}) {h1}({type(h1)})")
        self.header = (h0,h1,)

        if isinstance(database, MsgInfo) == False:
            raise Exception("database must be a MsgInfo")

        self.msgInfo = database
        self.valid_msgids = [int(x) for x in database.keys()]

        self.parser = YivoParser(self.header)
        self.data = None

    def pack(self, msgID, data):
        """
        Given a MsgID and a tuple of data, returns a yivo message packet
        """
        # if data is None:
        #     msg = struct.pack("<2chBB",*self.header, 0, msgID, msgID)
        # else:
        fmt, _ = self.msgInfo[msgID]
        sz = fmt.size - 6
        msg = fmt.pack(*self.header, sz, msgID, *data, 0)
        cs = checksum(sz,msgID,msg[5:-1])
        msg = msg[:-1] + self.pack_cs.pack(cs) #cs.to_bytes(1,'little')
        return msg

    def unpack(self, msg=None):
        """
        Unpacks a binary yivo packet

        Returns:
            Errors
            Message
        """
        clear = False # doesn't cleanup if failure
        if msg is None:
            msg = self.data
            clear = True

        size, msgid, payload, cs = chunk(msg)

        # print(f">> size: {size}\n id: {msgid}\n pl: {payload}\n cs: {cs}")

        val = None
        a = ord(self.header[0])
        b = ord(self.header[1])
        if (msg[0] != a) or (msg[1] != b):
            # print(msg[:2], self.header)
            return Errors.INVALID_HEADER, None

        if msgid not in self.valid_msgids:
            # print(f"invalid id: {msgid}")
            return Errors.INVALID_MSGID, None

        if (size != 0) and (size != len(payload)):
            # print(len(payload),"!=", size)
            return Errors.INVALID_LENGTH, None
        # print(size, len(payload))

        if checksum(size, msgid, payload) != cs:
            # print("checksum failure", cs, "!=", checksum(size, msgid, payload))
            return Errors.INVALID_CHECKSUM, None
        # print(cs, checksum(size, msgid, payload))

        try:
            fmt, obj = self.msgInfo[msgid]
        except KeyError:
            return Errors.INVALID_MSGID, None

        if size > 0:
            info = fmt.unpack(msg)
            # print("info", info)
            # print(type(obj))
            # if isinstance(tuple, obj): val = tuple(info[4:-1])
            # else: val = obj(*info[4:-1])
            val = obj(*info[4:-1])
        else:
            val = REQUEST(msgid)
        if clear:
            self.data = None

        return Errors.NONE, val

    def parse(self, c):
        if self.parser.parse(c):
            self.data, msgid = self.parser.get_info()
            return msgid
        return 0
