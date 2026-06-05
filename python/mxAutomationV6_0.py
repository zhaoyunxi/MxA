# Version Library V6.0.0  - 2025-09-12 14:05
#******************************************************************************
#// This material is the exclusive property of KUKA Deutschland GmbH.
#// Except as expressly permitted by separate agreement, this material may only
#// be used by members of the development department of KUKA Deutschland GmbH for
#// internal development purposes of KUKA Deutschland GmbH.
#//
#// Copyright (C) 2025
#// KUKA Roboter GmbH, Germany. All Rights Reserved.
#//
#//*****************************************************************************
#// Date        Programmer        Reviewer
#//             Description
#//-----------------------------------------------------------------------------
#// 2023-11-24  ZaerleM                
#//             mxAutomation3.3.3 generated on the basis of C++ lib V3.3.3
#//
#// 2025-01-13  ElHeni, Firas                
#//             mxAutomation 3.3.3 generated based on C++ lib V3.3.3
#//
#// 2025-03-17  Akos Gy                
#//             mxAutomation 4.0 compatibility modificational change
#//
#// 2025-06-11  Akos B               
#//             mxAutomation 4.0 LDD and ConveyorTech API changes
#//
#// 2025-06-12	JiangS
#//				Bugfix 379628 CheckSum Error 712 due to Python rounding error
#//
#// 2025-08-14  Daniel P
#//             Add OrderID output to blocks using ExecuteCommand
#//
#// 2025-09-12	Gergely K
#//				Add collision detection
#//
#// 2025-10-31	Aron S
#//				Update to 6.0, remove JOG_SLIN
#//				Bugfix: coordinate system reset for KRC_JOG
#//
#// 2025-11-24  Daniel P
#//             Add KRMsgNet blocks (KRC_GETALLMESSAGES, KRC_SETLANGUAGE, KRC_SETDATETIME)
#******************************************************************************
# The Python library was adapted to conform to Python versions 2.7.3 to 3.11 
# and tested using versions 2.7.3, 2.7.10, 2.7.18, 3.8, and 3.11.

from dataclasses import dataclass, field
from typing import List
import time 

KRC4_OUTPUT = bytearray(256)


#From PLCiec C++ library...

def CURTIME():
    return int(round(time.time() * 1000))

def MKTIME(sign, mseconds, seconds=0, minutes=0, hours=0, days=0):
    total_msecs = (((days * 24 + hours) * 60 + minutes) * 60 + seconds) * 1000 + mseconds
    return total_msecs if sign >= 0 else -total_msecs

class TON:
    def __init__(self):
        self.IN = False
        self.PT = 0
        self._Q = False
        self._ET = 0
        self.m_PrevIn = False
        self.m_PrevTime = 0
        self.m_Active = False

    def OnCycle(self):
        if True == self.IN and False == self.m_PrevIn:
            self.m_PrevTime = CURTIME()
            self.m_Active = True
            self.m_PrevIn = self.IN
        elif False == self.IN and True == self.m_PrevIn:
            self.m_Active = self._Q = False
            self._ET = 0
            self.m_PrevIn = self.IN
        elif self.m_Active:
            currentTime = CURTIME()
            self._ET += currentTime - self.m_PrevTime
            self.m_PrevTime = currentTime
            if self._ET > self.PT:
                self._Q = True


class R_TRIG:
    def __init__(self):
        self.CLK = False
        self._Q = False
        #self.Q = self._Q
        self.M = False

    def OnCycle(self):
        self._Q = self.CLK and not self.M
        self.M = self.CLK




def IsBitSet(byte_val, idx):
    """
    Gibt den Wert des Bits an der Position idx in byte_val zurück.
    Das Bit ganz rechts hat den Index 0.
    """
    return (byte_val & (1 << idx)) != 0

def DINT_TO_INT(value):
    # Converts the value to an integer and returns it
    return int(value)



@dataclass
class MXA_COMMAND:
    COMMANDID: int = 0
    ORDERID: int = 0
    BUFFERMODE: int = 0
    COMMANDSIZE: int = 0
    CMDPARREAL: list = field(default_factory=lambda: [0.0] * 101)
    CMDPARINT: list = field(default_factory=lambda: [0] * 51)
    CMDPARBOOL: list = field(default_factory=lambda: [False] * 51)
@dataclass
class MXA_CMD_STATE_RET:
    SR_ORDERID: int = 0
    SR_STATE: int = 0


MXA_CMD_SR_ARR = [MXA_CMD_STATE_RET() for _ in range(11)]
MXA_CMD_DATA_RET = [0.0] * 13


@dataclass
class MXA_COMMAND_STATUS:
    CMDIDRET: int = 0
    ORDERIDRET: int = 0
    TRANSMISSIONNORET: int = 0
    STATERETURN: List[MXA_CMD_STATE_RET] = field(default_factory=lambda: MXA_CMD_SR_ARR)
    CMDDATARETURN: List[float] = field(default_factory=lambda: MXA_CMD_DATA_RET)
    CMDDATARETCSKRC: int = 0
    CMDDATARETCSPLC: int = 0

@dataclass
class MXA_AUTEXT_CONTROL:
    PGNO: int = 0
    PGNO_PARITY: bool = False
    PGNO_VALID: bool = False
    EXT_START: bool = False
    MOVE_ENABLE: bool = False
    MOVE_DISABLE: bool = False
    CONF_MESS: bool = False
    DRIVESON: bool = False
    DRIVESOFF: bool = False
    BRAKETEST_REQ_EXT: bool = False
    MASTERINGTEST_REQ_EXT: bool = False


@dataclass
class MXA_AUTEXT_STATE:
    RC_RDY1: bool = False
    ALARM_STOP: bool = False
    USER_SAFE: bool = False
    PERI_RDY: bool = False
    ROB_CAL: bool = False
    IO_ACTCONF: bool = False
    STOPMESS: bool = False
    PGNO_FBIT_REFL: bool = False
    INTNOTAUS: bool = False
    PRO_ACT: bool = False
    PGNO_REQ: bool = False
    APPL_RUN: bool = False
    PRO_MOVE: bool = False
    IN_HOME: bool = False
    ON_PATH: bool = False
    NEAR_POSRET: bool = False
    ROB_STOPPED: bool = False
    T1: bool = False
    T2: bool = False
    AUT: bool = False
    EXT: bool = False
    KCP_CONNECT: bool = False
    BRAKETEST_MONTIME: bool = False
    BRAKETEST_REQ_INT: bool = False
    BRAKETEST_WORK: bool = False
    BRAKES_OK: bool = False
    BRAKETEST_WARN: bool = False
    MASTERINGTEST_REQ_INT: bool = False
    MASTERINGTESTSWITCH_OK: bool = False

@dataclass
class E6POS:
    X: float = 0.0
    Y: float = 0.0
    Z: float = 0.0
    A: float = 0.0
    B: float = 0.0
    C: float = 0.0
    STATUS: int = 0
    TURN: int = 0
    E1: float = 0.0
    E2: float = 0.0
    E3: float = 0.0
    E4: float = 0.0
    E5: float = 0.0
    E6: float = 0.0



@dataclass
class E6AXIS:
    A1: float = 0.0
    A2: float = 0.0
    A3: float = 0.0
    A4: float = 0.0
    A5: float = 0.0
    A6: float = 0.0
    E1: float = 0.0
    E2: float = 0.0
    E3: float = 0.0
    E4: float = 0.0
    E5: float = 0.0
    E6: float = 0.0


@dataclass
class MXA_KRC_STATE:
    POSACT: E6POS = field(default_factory=E6POS)
    TOOLACT: int = 0
    BASEACT: int = 0
    IPOMODEACT: int = 0
    POSACTVALID: bool = False
    AXISACT: E6AXIS = field(default_factory=E6AXIS)
    AXISACTVALID: bool = False
    OVPROACT: int = 0
    VELACT: float = 0.0
    BRAKEACTIVE: bool = False
    WORKSTATES: int = 0
    AXWORKSTATES: int = 0
    GROUPSTATE: int = 0
    ERRORID: int = 0
    ERRORIDSUB: int = 0
    ERRORIDPCOS: int = 0
    ACTIVEPOSORDERID: int = 0
    ACTIVEORDERIDB: int = 0
    HEARTBEAT: int = 0
    HEARTBEATPCOS: int = 0
    INTERRUPTSTATE: list = field(default_factory=lambda: [0] * 9)
    QUEUECOUNT: int = 0
    TOUCHUP: bool = False
    TOUCHUP_INDEX: int = 0
    IN_VAL_1TO8: int = 0
    ABORTACTIVE: bool = False


@dataclass
class MXA_JOGADVANCED:
    JOG_AD_ACTIVE: bool = False
    JOG_AD_STATE_VAL: int = 0


@dataclass
class MXA_KRC_CONTROL:
    RESET: bool = False
    OVERRIDE: int = 0
    BRAKE: bool = False
    BRAKEF: bool = False
    RELEASEBRAKE: bool = False
    SHOWTRACE: bool = False
    MESSAGERESET: bool = False
    OUT_VAL_1: bool = False
    OUT_VAL_2: bool = False
    OUT_VAL_3: bool = False
    OUT_VAL_4: bool = False
    OUT_VAL_5: bool = False
    OUT_VAL_6: bool = False
    OUT_VAL_7: bool = False
    OUT_VAL_8: bool = False
    WRITE_OUT_1TO8: bool = False



@dataclass
class AXIS_GROUP_REF:
    INITIALIZED: bool = False
    ONLINE: bool = False
    LASTORDERID: int = 0
    READAXISGROUPINIT: bool = False
    READDONE: bool = False
    INTERRORID: int = 0
    INTFBERRORID: int = 0
    HEARTBEATTO: int = 0
    PLC_MAJOR: int = 0
    PLC_MINOR: int = 0
    DEF_VEL_CP: float = 0.0
    DEF_ACC_CP: float = 0.0
    COMMAND: MXA_COMMAND = field(default_factory=MXA_COMMAND)
    CMDSTATE: MXA_COMMAND_STATUS = field(default_factory=MXA_COMMAND_STATUS)
    AUTEXTCONTROL: MXA_AUTEXT_CONTROL = field(default_factory=MXA_AUTEXT_CONTROL)
    AUTEXTSTATE: MXA_AUTEXT_STATE = field(default_factory=MXA_AUTEXT_STATE)
    KRCSTATE: MXA_KRC_STATE = field(default_factory=MXA_KRC_STATE)
    KRCCONTROL: MXA_KRC_CONTROL = field(default_factory=MXA_KRC_CONTROL)
    JOG_ADVANCED: MXA_JOGADVANCED = field(default_factory=MXA_JOGADVANCED)
    VEL_MAX_CP: float = 0.0
    ACC_MAX_CP: float = 0.0


KRC_AXISGROUPREFARR = [AXIS_GROUP_REF() for _ in range(6)]

@dataclass
class APO:

    PTP_MODE: int = 0
    CP_MODE: int = 0
    CPTP: int = 0
    CDIS: float = 0
    CORI: float = 0
    CVEL: int = 0

@dataclass
class AXBOX:
    A1_N: float = 0 
    A2_N: float = 0
    A3_N: float = 0
    A4_N: float = 0
    A5_N: float = 0
    A6_N: float = 0
    A1_P: float = 0
    A2_P: float = 0
    A3_P: float = 0
    A4_P: float = 0
    A5_P: float = 0
    A6_P: float = 0
    E1_N: float = 0
    E2_N: float = 0
    E3_N: float = 0
    E4_N: float = 0
    E5_N: float = 0
    E6_N: float = 0
    E1_P: float = 0
    E2_P: float = 0
    E3_P: float = 0
    E4_P: float = 0
    E5_P: float = 0
    E6_P: float = 0

AXIS_VEL = List[int]
BOOL_ARRAY_40 = List[bool]


@dataclass
class BOX:
    X: float = 0.0
    Y: float = 0.0
    Z: float = 0.0
    A: float = 0.0
    B: float = 0.0
    C: float = 0.0
    X1: float = 0.0
    X2: float = 0.0
    Y1: float = 0.0
    Y2: float = 0.0
    Z1: float = 0.0
    Z2: float = 0.0

@dataclass
class COORDSYS:
    TOOL: int = -1
    BASE: int = -1
    IPO_MODE: int = 0

@dataclass
class FRAME:
    X: float = 0.0
    Y: float = 0.0
    Z: float = 0.0
    A: float = 0.0
    B: float = 0.0
    C: float = 0.0



INT32_ARRAY_40 = List[int]
MXA_BUFFERMODE = int
MXA_CIRC_TYPE = int
MXA_CP_APO = int
MXA_ORI_TYPE = int
MXA_PTP_APO = int
MXA_SYNC_IO = List[bool]


@dataclass
class POSITION1:
    COORDSYS_1: COORDSYS = field(default_factory=COORDSYS)
    E6POS_1: E6POS = field(default_factory=E6POS)
    E6AXIS_1: E6AXIS = field(default_factory=E6AXIS)


POSITION_ARRAY = [POSITION1() for _ in range(100)]
REAL_ARRAY_40 = List[float]
REAL_ARRAY_12 = List[float]


#******************************************************************************
# * FUNCTION MXA_GETIO_BYTE
# ******************************************************************************/

def MXA_GETIO_BYTE(BYTEPOS, KRC4_INPUT):
   # MXA_GETIO_BYTE = False
    O = int(KRC4_INPUT[BYTEPOS])
    return O



#/******************************************************************************
# * FUNCTION MXA_GETIO_DINT
# ******************************************************************************/


def MXA_GETIO_DINT(BYTEPOS, KRC4_INPUT):
    byte1 = KRC4_INPUT[BYTEPOS]
    byte2 = KRC4_INPUT[BYTEPOS + 1]
    byte3 = KRC4_INPUT[BYTEPOS + 2]
    byte4 = KRC4_INPUT[BYTEPOS + 3]
    DWORD = (byte4 << 24) | (byte3 << 16) | (byte2 << 8) | byte1
    if DWORD >= 2**31:
        DWORD -= 2**32
    return DWORD


#/******************************************************************************
# * FUNCTION MXA_GETIO_INT
# ******************************************************************************/


def MXA_GETIO_INT(BYTEPOS, KRC4_INPUT ):

    byte1 = bin(int( KRC4_INPUT[BYTEPOS]     ) )[2:]      # convert values from byte-array to I/O, than add
    byte2 = bin(int( KRC4_INPUT[BYTEPOS + 1] ) )[2:]  

    WORD = "0b" + byte2 + byte1 
    O = int(WORD , 2)

    return O

#/******************************************************************************
# * FUNCTION MXA_GETIO_NIBBLE
#  The first 4 bits should be written to N1 and the next 4 bits to N2 should be written as INT
# ******************************************************************************/


def MXA_GETIO_NIBBLE (BYTEPOS, KRC4_INPUT):
    # Converts the integer to a binary string and removes the '0b' at the beginning
    byte = bin( KRC4_INPUT[BYTEPOS] )[2:]
    # Adds leading zeros to create an 8-bit byte
    byte = byte.zfill(8)
    # Divide the byte into the front 4 bits (N1) and the back 4 bits (N2)
    N1 = byte[:4]
    N2 = byte[4:]
    # Convert N1 and N2 to integers
    N1 = int(N1, 2)
    N2 = int(N2, 2)

    return N1, N2



#/******************************************************************************
# * FUNCTION MXA_GETIO_REAL
# ******************************************************************************/
#The struct.unpack function is used to convert the bytes of KRC4_INPUT at the BYTEPOS position into a floating point number ('f' stands for floating point number).
#The function returns a tuple with two elements: False (equivalent to (BOOL)FALSE in your C+± code) and O (the floating point number extracted from KRC4_INPUT).

import struct

def MXA_GETIO_REAL (BYTEPOS, KRC4_INPUT) :
    O = struct.unpack('f', KRC4_INPUT[BYTEPOS:BYTEPOS+4])[0]
    return O




# /******************************************************************************
#  * FUNCTION MXA_GETIO_SINT
#  ******************************************************************************/

def BYTE_TO_SINT(byte):
    if byte & 0x80:
        sint = -((byte ^ 0xFF) + 1)
        return sint
    else:
        return byte

def MXA_GETIO_SINT(BYTEPOS, KRC4_INPUT):
    B = 0
    
    B = KRC4_INPUT[BYTEPOS]
    O = BYTE_TO_SINT( B )
    return O



#/******************************************************************************
# * FUNCTION MXA_CHBIT
# ******************************************************************************/
def MXA_CHBIT(BYTEPOS, BITPOS, VAL):
    if VAL:
        KRC4_OUTPUT[BYTEPOS] |= 1 << BITPOS
    else:
        KRC4_OUTPUT[BYTEPOS] &= ~(1 << BITPOS)
    return 


#/******************************************************************************
# * FUNCTION MXA_CHBIT with return value
# ******************************************************************************/
def MXA_CHBIT2 ( BITPOS, VAL, Mod_Val ):
    if VAL:
        Mod_Val |= 1 << BITPOS
    else:
        Mod_Val &= ~(1 << BITPOS)
    return Mod_Val



#/******************************************************************************
# * FUNCTION MXA_WRITEIO_BYTE
# ******************************************************************************/


def MXA_WRITEIO_BYTE (BYTEPOS, VAL):
    KRC4_OUTPUT[BYTEPOS] = VAL & 0xFF  # INT_TO_BYTE equivalent in Python
    return





#/******************************************************************************
# * FUNCTION MXA_WRITEIO_DINT
# ******************************************************************************/
#The loop goes over all 32 bits of VAL.
#For each bit it is calculated in which byte and at which bit position it should be set in KRC4_OUTPUT.
#The bit is then set or deleted accordingly.
#The function returns False, which is equivalent to (BOOL)FALSE in your C+± code.


def MXA_WRITEIO_DINT (BYTEPOS, VAL):
    for i in range(32):
        bit = (VAL >> i) & 1
        byte_index = BYTEPOS + i // 8
        bit_index = i % 8
        if bit:
            KRC4_OUTPUT[byte_index] |= (1 << bit_index)
        else:
            KRC4_OUTPUT[byte_index] &= ~(1 << bit_index)
    return 



#/******************************************************************************
# * FUNCTION MXA_WRITEIO_DWORD
# ******************************************************************************/
# The loop goes over all 32 bits of VAL.
# For each bit it is calculated in which byte and at which bit position it should be set in KRC4_OUTPUT.
# The bit is then set or deleted accordingly.
# The function returns False, which is equivalent to (BOOL)FALSE in your C+± code.
# Please note that Python uses lists instead of arrays and indexing starts at 0.


def MXA_WRITEIO_DWORD(BYTEPOS, VAL):
    for i in range(32):
        bit = (VAL >> i) & 1
        byte_index = BYTEPOS + i // 8
        bit_index = i % 8
        if bit:
            KRC4_OUTPUT[byte_index] |= (1 << bit_index)
        else:
            KRC4_OUTPUT[byte_index] &= ~(1 << bit_index)
    return 



# /******************************************************************************
#  * FUNCTION MXA_WRITEIO_REAL
#  ******************************************************************************/
# The struct.pack function is used to convert the floating point number VAL to bytes ('f' stands for floating point number).
# The bytes are then written to KRC4_OUTPUT at the BYTEPOS position.
# The function returns False, which is equivalent to (BOOL)FALSE in your C+± code.
# Please note that Python uses lists instead of arrays and indexing starts at 0.

import struct

def MXA_WRITEIO_REAL(BYTEPOS, VAL):
    KRC4_OUTPUT[BYTEPOS:BYTEPOS+4] = struct.pack('f', VAL)
    return



# /******************************************************************************
#  * FUNCTION MXA_WRITEIO_WORD
#  ******************************************************************************/
# The loop goes over all 16 bits of VAL.
# For each bit it is calculated in which byte and at which bit position it should be set in KRC4_OUTPUT.
# The bit is then set or deleted accordingly.
# The function returns False, which is equivalent to (BOOL)FALSE in your C+± code.
# Please note that Python uses lists instead of arrays and indexing starts at 0.

def MXA_WRITEIO_WORD(BYTEPOS, VAL):
    for i in range(16):
        bit = (VAL >> i) & 1
        byte_index = BYTEPOS + i // 8
        bit_index = i % 8
        if bit:
            KRC4_OUTPUT[byte_index] |= (1 << bit_index)
        else:
            KRC4_OUTPUT[byte_index] &= ~(1 << bit_index)
    return False



# /******************************************************************************
#  * FUNCTION_BLOCK MXA_RESETCOMMAND
#  ******************************************************************************/


class MXA_RESETCOMMAND:
    def __init__(self):
        self.I = 0
        self.AXISGROUPIDX = 0

    def OnCycle(self):
        for self.I in range(1, 51):
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[self.I] = False
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[self.I] = 0
        for self.I in range(1, 101):
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[self.I] = 0.0
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID = 0
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID = 0
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.BUFFERMODE = 0
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDSIZE = 0



# /******************************************************************************
#  * FUNCTION_BLOCK MXA_GETORDERSTATE
#  ******************************************************************************/


class MXA_GETORDERSTATE:
    def __init__(self):
        self.I = 0
        self.AXISGROUPIDX = 0
        self.ORDERID = 0
        self._ORDERSTATE = 0
        self.M_ORDERSTATE = 0

    def OnCycle(self):
        self.M_ORDERSTATE = 0
        for self.I in range(1, 11):
            if (KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[self.I].SR_ORDERID == self.ORDERID) and (KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[self.I].SR_STATE > self.M_ORDERSTATE):
                self.M_ORDERSTATE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[self.I].SR_STATE
        self._ORDERSTATE = self.M_ORDERSTATE

    @property
    def ORDERSTATE(self):
        return self._ORDERSTATE



# /******************************************************************************
#  * FUNCTION_BLOCK MXA_EXECUTECOMMAND
#  ******************************************************************************/

class MXA_EXECUTECOMMAND:
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTE = False
        self.CMDID = 0
        self.BUFFERMODE = 0
        self.COMMANDSIZE = 0
        self.ENABLEDIRECTEXE = False
        self.ENABLEQUEUEEXE = False
        self.IGNOREINIT = False
        self._WRITECMDPAR = False
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._CMDSPECIFIC1 = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._READCMDDATARET = False
        self._ORDERID = 0
        self.RESETCOMMAND_1 = MXA_RESETCOMMAND()
        self.GETORDERSTATE_1 = MXA_GETORDERSTATE()
        self.M_STATE = 0
        self.M_ORDERID = 0
        self.M_EXECUTELAST = False
        self.M_RE_EXECUTE = False
        self.M_COMMANDSIZE = 0



    @property
    def WRITECMDPAR(self):
        return self._WRITECMDPAR

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def CMDSPECIFIC1(self):
        return self._CMDSPECIFIC1

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def READCMDDATARET(self):
        return self._READCMDDATARET

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self.M_RE_EXECUTE = self.EXECUTE and not self.M_EXECUTELAST
        self.M_EXECUTELAST = self.EXECUTE
        self._WRITECMDPAR = False
        self._READCMDDATARET = False
        if not self.EXECUTE:
            self.M_STATE = 0
            self.M_ORDERID = 0
            self._ERRORID = 0
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._ERRORID = 506
        else:
            if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].READDONE:
                self._ERRORID = 507
            if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].READAXISGROUPINIT:
                self._ERRORID = 508
        if self.M_RE_EXECUTE and self._ERRORID == 0:
            self.M_STATE = 1
            if (self.BUFFERMODE == 0 and not self.ENABLEDIRECTEXE) or (self.BUFFERMODE > 0 and not self.ENABLEQUEUEEXE):
                self._ERRORID = 502
            if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED:
                if not self.IGNOREINIT:
                    self._ERRORID = 508
            if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE:
                self._ERRORID = 509
        if self.M_STATE == 1 and self._ERRORID == 0:
            if self.M_RE_EXECUTE:
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].LASTORDERID += 1
                if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].LASTORDERID >= 2147483647:
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].LASTORDERID = 1
                self.M_ORDERID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].LASTORDERID
            if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.ORDERIDRET == self.M_ORDERID:
                if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDIDRET == self.CMDID:
                    if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETCSPLC == KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETCSKRC:
                        if self.BUFFERMODE == 0:
                            self.M_STATE = 15
                            self._READCMDDATARET = True
                        else:
                            self.M_STATE = 5
                    else:
                        self._ERRORID = 512
                else:
                    self._ERRORID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDIDRET * -1
                self.RESETCOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
                self.RESETCOMMAND_1.OnCycle()
            else:
                if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID == 0 and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID == 0 and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE and (KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED or self.IGNOREINIT):
                    if self.BUFFERMODE < 2 or KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.QUEUECOUNT < 80:
                        self.RESETCOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
                        self.RESETCOMMAND_1.OnCycle()
                        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID = self.M_ORDERID
                        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID = self.CMDID
                        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.BUFFERMODE = self.BUFFERMODE
                        self.M_COMMANDSIZE = self.COMMANDSIZE
                        if self.COMMANDSIZE < 1 or self.COMMANDSIZE > 3:
                            self._ERRORID = 517
                            self.M_COMMANDSIZE = 3
                        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDSIZE = self.M_COMMANDSIZE
                        self._WRITECMDPAR = True
        if 1 < self.M_STATE < 15 and self._ERRORID == 0:
            self.GETORDERSTATE_1.AXISGROUPIDX = self.AXISGROUPIDX
            self.GETORDERSTATE_1.ORDERID = self.M_ORDERID
            self.GETORDERSTATE_1.OnCycle()
            if self.GETORDERSTATE_1.ORDERSTATE > 0:
                if self.GETORDERSTATE_1.ORDERSTATE == 5 and self.M_STATE < 10:
                    self.M_STATE = 10
                if self.GETORDERSTATE_1.ORDERSTATE == 6 and self.M_STATE < 15:
                    self.M_STATE = 15
                if self.GETORDERSTATE_1.ORDERSTATE == 8 and self.M_STATE < 20:
                    self.M_STATE = 20
                if self.GETORDERSTATE_1.ORDERSTATE == 9 and self.M_STATE < 25:
                    self.M_STATE = 25
        if self._ERRORID != 0:
            self.M_STATE = self._ERRORID * -1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
        self._BUSY = self.M_STATE > 1
        self._ACTIVE = self.M_STATE == 10
        self._DONE = self.M_STATE == 15
        self._CMDSPECIFIC1 = self.M_STATE == 25
        self._ABORTED = self.M_STATE == 20
        self._ERROR = self.M_STATE < 0
        self._ORDERID = self.M_ORDERID


#/******************************************************************************
# * FUNCTION_BLOCK KRC_SETOVERRIDE
# ******************************************************************************/

class KRC_SETOVERRIDE:
    """
    The function block KRC_SetOverride sets the program override. Program override is the velocity of the robot during program execution. It is specified as a percentage of the programmed velocity. The override setting is transferred to the robot during every PLC cycle. If the override setting is changed, this change is detected by the robot and applied.

    The override is only applied in Automatic External mode so that the override can be set via the smartPAD in the test modes T1 and T2, e.g. for teaching. The program override refers to all motions of the robot system.

    This function block may only be instanced once per axis group. In the case of multiple instancing, the signals of the most recently called function block are output.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    Override (INT): Program override, can be 0 to 100%

    Returns:
    Valid (BOOL): TRUE = data are valid
    ActualOverride (INT): Current override setting, can be 0 to 100%
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    """

    def __init__(self):
        self.AXISGROUPIDX = 0
        self.OVERRIDE = 0
        self._VALID = False
        self._ACTUALOVERRIDE = 0
        self._ERROR = False
        self._ERRORID = 0


    @property
    def VALID(self):
        return self._VALID

    @property
    def ACTUALOVERRIDE(self):
        return self._ACTUALOVERRIDE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID


    def OnCycle(self):
        self._ERRORID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if 0 <= self.OVERRIDE <= 100:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OVERRIDE = self.OVERRIDE
            self._ERRORID = 0
        else:
            self._ERRORID = 504
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
        self._ACTUALOVERRIDE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.OVPROACT
        self._VALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE
        self._ERROR = self._ERRORID != 0





# /******************************************************************************
#  * FUNCTION_BLOCK KRC_ABORT
#  ******************************************************************************/

class KRC_ABORT:
    """
    The function block KRC_Abort cancels active and buffered statements and motions. The parameter Active specifies whether or not the statement is still being executed. If the robot interpreter is no longer active, this can result in the statement being transferred, but not yet fully executed. Statements and motions of function blocks without BufferMode or QueueMode that are executed cyclically are not canceled. KRC_Abort is not processed if the function block KRC_Interrupt is active. In this case, the program must first be resumed with KRC_Continue before it can be aborted with KRC_Abort.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed.
    Done (bool): TRUE = statement has been executed.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID
    
    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 2
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 1
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ABORTACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE or self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_AUTOMATICEXTERNAL
#  ******************************************************************************/



class KRC_AUTOMATICEXTERNAL:
    """
    The function block KRC_AutomaticExternal activates the Automatic External interface and reads the interface signals. The function block KRC_AutoStart can be used to simplify use of KRC_AutomaticExternal. This function block requires the Automatic External mode of the robot system. Further information about this functionality is contained in the operating and programming instructions for the KUKA System Software (KSS).

    This function block may only be instanced once per axis group. In the case of multiple instancing, the signals of the most recently called function block are output.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    MOVE_ENABLE (BOOL): TRUE = motion enable for the robot
    CONF_MESS (BOOL): TRUE = acknowledgement of error messages
    DRIVES_ON (BOOL): TRUE = activation of the robot drives
    DRIVES_OFF (BOOL): TRUE = deactivation of the robot drives
    EXT_START (BOOL): TRUE = start or continuation of robot program execution
    RESET (BOOL): Selects the mxAutomation robot program in the case of a rising edge of the signal and starts it. First, all buffered statements are aborted.
    ENABLE_T1 (BOOL): TRUE = enabling of T1 mode
    ENABLE_T2 (BOOL): TRUE = enabling of T2 mode
    ENABLE_AUT (BOOL): TRUE = enabling of Automatic mode
    ENABLE_EXT (BOOL): TRUE = enabling of Automatic External mode

    Returns:
    Valid (BOOL): TRUE = data are valid
    RC_RDY1 (BOOL): TRUE = robot controller ready for program start
    ALARM_STOP (BOOL): FALSE = robot stop by EMERGENCY STOP
    USER_SAFE (BOOL): FALSE = operator safety violated
    PERI_RDY (BOOL): TRUE = robot drives activated
    ROB_CAL (BOOL): TRUE = robot axes mastered
    IO_ACTCONF (BOOL): TRUE = Automatic External interface active
    STOPMESS (BOOL): TRUE = safety circuit interrupted (robot fault)
    INT_E_STOP (BOOL): TRUE = external EMERGENCY STOP, FALSE = EMERGENCY STOP device pressed on the smartPAD
    PRO_ACT (BOOL): TRUE = process active at robot level
    APPL_RUN (BOOL): TRUE = robot program running
    PRO_MOVE (BOOL): TRUE = synchronous robot motion active
    ON_PATH (BOOL): TRUE = robot on programmed path
    NEAR_POSRET (BOOL): TRUE = robot near most recently saved position on the programmed path (after leaving path)
    ROB_STOPPED (BOOL): TRUE = robot is at standstill
    T1 (BOOL): TRUE = operating mode T1 selected
    T2 (BOOL): TRUE = operating mode T2 selected
    AUT (BOOL): TRUE = operating mode Automatic selected
    EXT (BOOL): TRUE = operating mode Automatic External selected
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.MOVE_ENABLE = False
        self.CONF_MESS = False
        self.DRIVES_ON = False
        self.DRIVES_OFF = False
        self.EXT_START = False
        self.RESET = False
        self.ENABLE_T1 = False
        self.ENABLE_T2 = False
        self.ENABLE_AUT = False
        self.ENABLE_EXT = False
        self._VALID = False
        self._RC_RDY1 = False
        self._ALARM_STOP = False
        self._USER_SAFE = False
        self._PERI_RDY = False
        self._ROB_CAL = False
        self._IO_ACTCONF = False
        self._STOPMESS = False
        self._INT_E_STOP = False
        self._PRO_ACT = False
        self._APPL_RUN = False
        self._PRO_MOVE = False
        self._ON_PATH = False
        self._NEAR_POSRET = False
        self._ROB_STOPPED = False
        self._T1 = False
        self._T2 = False
        self._AUT = False
        self._EXT = False


    @property
    def VALID(self):
        return self._VALID

    @property
    def RC_RDY1(self):
        return self._RC_RDY1

    @property
    def ALARM_STOP(self):
        return self._ALARM_STOP

    @property
    def USER_SAFE(self):
        return self._USER_SAFE

    @property
    def PERI_RDY(self):
        return self._PERI_RDY

    @property
    def ROB_CAL(self):
        return self._ROB_CAL

    @property
    def IO_ACTCONF(self):
        return self._IO_ACTCONF

    @property
    def STOPMESS(self):
        return self._STOPMESS

    @property
    def INT_E_STOP(self):
        return self._INT_E_STOP

    @property
    def PRO_ACT(self):
        return self._PRO_ACT

    @property
    def APPL_RUN(self):
        return self._APPL_RUN

    @property
    def PRO_MOVE(self):
        return self._PRO_MOVE

    @property
    def ON_PATH(self):
        return self._ON_PATH

    @property
    def NEAR_POSRET(self):
        return self._NEAR_POSRET

    @property
    def ROB_STOPPED(self):
        return self._ROB_STOPPED

    @property
    def T1(self):
        return self._T1

    @property
    def T2(self):
        return self._T2

    @property
    def AUT(self):
        return self._AUT

    @property
    def EXT(self):
        return self._EXT



    def OnCycle(self):
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._VALID = False
            return
        self._ALARM_STOP = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.ALARM_STOP
        self._APPL_RUN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.APPL_RUN
        self._AUT = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.AUT
        self._EXT = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.EXT
        self._INT_E_STOP = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.INTNOTAUS
        self._IO_ACTCONF = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.IO_ACTCONF
        self._NEAR_POSRET = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.NEAR_POSRET
        self._ON_PATH = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.ON_PATH
        self._PERI_RDY = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PERI_RDY
        self._PRO_ACT = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PRO_ACT
        self._PRO_MOVE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PRO_MOVE
        self._RC_RDY1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.RC_RDY1
        self._ROB_CAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.ROB_CAL
        self._ROB_STOPPED = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.ROB_STOPPED
        self._STOPMESS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.STOPMESS
        self._T1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.T1
        self._T2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.T2
        self._USER_SAFE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.USER_SAFE
        self._VALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE
        if self.CONF_MESS:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.CONF_MESS = True
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.DRIVESOFF = self.DRIVES_OFF
        if self.DRIVES_ON:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.DRIVESON = True
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.EXT_START = self.EXT_START
        if self.RESET:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.RESET = True
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.MOVE_ENABLE = self.MOVE_ENABLE and ((self.ENABLE_T1 and self._T1) or not self._T1) and ((self.ENABLE_T2 and self._T2) or not self._T2) and ((self.ENABLE_AUT and self._AUT) or not self._AUT) and ((self.ENABLE_EXT and self._EXT) or not self._EXT)

# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READMXAERROR
#  ******************************************************************************/


class KRC_READMXAERROR:
    """
    The function block KRC_ReadMXAError is used to read the current error state of an axis group. Only error messages generated by the mxA interface are displayed.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.

    Returns:
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self._ERROR = False
        self._ERRORID = 0

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID


    def OnCycle(self):
        self._ERRORID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self._ERRORID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORID
        if self._ERRORID == 0:
            self._ERRORID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORIDSUB
        if self._ERRORID == 0:
            self._ERRORID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORIDPCOS
        if self._ERRORID == 0:
            self._ERRORID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID
        if self._ERRORID == 0:
            self._ERRORID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID
        self._ERROR = self._ERRORID != 0




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READACTUALAXISPOSITION
#  ******************************************************************************/

class KRC_READACTUALAXISPOSITION:
    """
    The function block KRC_ReadActualAxisPosition reads the current axis-specific robot position. This is updated cyclically.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5

    Returns:
    Valid (BOOL): TRUE = data are valid
    AxisPosition (E6AXIS): Current axis-specific robot position ($AXIS_ACT on the robot controller). The data structure E6AXIS contains all the axis positions of the axis group.
    A1 ... A6 (REAL): Current position of robot axes A1 to A6
    E1 ... E6 (REAL): Current position of external axes E1 to E6
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self._VALID = False
        self._AXISPOSITION = E6AXIS()
        self._A1 = 0
        self._A2 = 0
        self._A3 = 0
        self._A4 = 0
        self._A5 = 0
        self._A6 = 0
        self._E1 = 0
        self._E2 = 0
        self._E3 = 0
        self._E4 = 0
        self._E5 = 0
        self._E6 = 0
    
    
    @property
    def VALID(self):
        return self._VALID

    @property
    def AXISPOSITION(self):
        return self._AXISPOSITION

    @property
    def A1(self):
        return self._A1

    @property
    def A2(self):
        return self._A2

    @property
    def A3(self):
        return self._A3

    @property
    def A4(self):
        return self._A4

    @property
    def A5(self):
        return self._A5

    @property
    def A6(self):
        return self._A6

    @property
    def E1(self):
        return self._E1

    @property
    def E2(self):
        return self._E2

    @property
    def E3(self):
        return self._E3

    @property
    def E4(self):
        return self._E4

    @property
    def E5(self):
        return self._E5

    @property
    def E6(self):
        return self._E6

    def OnCycle(self):
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._VALID = False
            return
        self._AXISPOSITION = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT
        self._A1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A1
        self._A2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A2
        self._A3 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A3
        self._A4 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A4
        self._A5 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A5
        self._A6 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A6
        self._E1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E1
        self._E2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E2
        self._E3 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E3
        self._E4 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E4
        self._E5 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E5
        self._E6 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E6
        self._VALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACTVALID and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READACTUALPOSITION
#  ******************************************************************************/

class KRC_READACTUALPOSITION:
    """
    The function block KRC_ReadActualPosition reads the current Cartesian actual position of the robot. This is updated cyclically.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5

    Returns:
    Valid (BOOL): TRUE = data are valid
    Position (E6POS): Current Cartesian actual position ($POS_ACT on the robot controller). The data structure E6POS contains all components of the Cartesian actual position (position of the TCP relative to the origin of the BASE coordinate system).
    X, Y, Z (REAL): Current actual position in the X, Y, Z directions
    A, B, C (REAL): Orientation A, B, C in the current actual position
    Status (INT): Status of the current actual position
    Turn (INT): Turn of the current actual position
    Tool (INT): Number of the currently used TOOL coordinate system ($ACT_TOOL_C on the robot controller)
    Base (INT): Number of the currently used BASE coordinate system ($ACT_BASE_C on the robot controller)
    IPOMode (INT): Current interpolation mode
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self._VALID = False
        self._ACTPOSITION = E6POS()
        self._X = 0
        self._Y = 0
        self._Z = 0
        self._A = 0
        self._B = 0
        self._C = 0
        self._STATUS = 0
        self._TURN = 0
        self._TOOL = 0
        self._BASE = 0
        self._IPOMODE = 0

    @property
    def VALID(self):
        return self._VALID

    @property
    def ACTPOSITION(self):
        return self._ACTPOSITION

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @property
    def Z(self):
        return self._Z

    @property
    def A(self):
        return self._A

    @property
    def B(self):
        return self._B

    @property
    def C(self):
        return self._C

    @property
    def STATUS(self):
        return self._STATUS

    @property
    def TURN(self):
        return self._TURN

    @property
    def TOOL(self):
        return self._TOOL

    @property
    def BASE(self):
        return self._BASE

    @property
    def IPOMODE(self):
        return self._IPOMODE

    def OnCycle(self):
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._VALID = False
            return
        self._ACTPOSITION = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT
        self._X = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.X
        self._Y = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.Y
        self._Z = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.Z
        self._A = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.A
        self._B = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.B
        self._C = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.C
        self._STATUS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.STATUS
        self._TURN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.TURN
        self._TOOL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.TOOLACT
        self._BASE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.BASEACT
        self._IPOMODE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IPOMODEACT
        self._VALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACTVALID and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_MESSAGERESET
#  ******************************************************************************/

class KRC_MESSAGERESET:
    """
    The function block KRC_MessageReset resets the current error state of an axis group. Only error messages generated by the mxA interface are reset. Messages can only be reset if the robot is stationary.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    MessageReset (bool): TRUE = reset message.

    Returns:
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.MESSAGERESET = False
        self._ERROR = False
        self._ERRORID = 0
        self.I = 0

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    def OnCycle(self):
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self._ERRORID = 0
        self._ERROR = False
        if self.MESSAGERESET:
            if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID == 565:
                for self.I in range(1, 101):
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[self.I] = 0.0
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.MESSAGERESET = self.MESSAGERESET
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID = 0
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = 0





# /******************************************************************************
#  * FUNCTION_BLOCK KRC_AUTOSTART
#  ******************************************************************************/


class KRC_AUTOSTART:
    """
    The function block KRC_AutoStart automatically sets the existing signals of the KRC_AutomaticExternal function block in the correct sequence. This function block can be used to activate the Automatic External interface of the robot system without the need for in-depth knowledge of the individual steps.

    The signals for activating the Automatic External interface are checked prior to starting. If one or more signals is missing, corresponding error numbers are displayed. The following inputs must additionally be set at the function block KRC_AutomaticExternal: MOVE_ENABLE, ENABLE_T1, ENABLE_T2, ENABLE_AUT, ENABLE_EXT, DRIVES_OFF. All other inputs are set by the function block KRC_AutoStart.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteReset (BOOL): Selects the mxAutomation robot program in the case of a rising edge of the signal and starts it. The program is reset beforehand and all buffered statements are aborted.

    Returns:
    Busy (BOOL): The sequence is active but not yet completed.
    Done (BOOL): The sequence is completed.
    DispActive (BOOL): TRUE = robot program is active
    ResetValid (BOOL): TRUE = conditions for a RESET at the function block KRC_AutomaticExternal are met
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTERESET = False
        self._BUSY = False
        self._DONE = False
        self._DISPACTIVE = False
        self._RESETVALID = False
        self._ERROR = False
        self._ERRORID = 0
        self.M_STATE = 0
        self.M_CONFMESS = False
        self.M_RESET = False
        self.M_RE_EXECUTERESET = False
        self.M_EXECUTERESETLAST = False
        self.KRC_READMXAERROR_1 = KRC_READMXAERROR()
        self.KRC_MESSAGERESET_1 = KRC_MESSAGERESET()
        self.TON_ON = TON()
        self.TON_OFF = TON()
        self.TON_1 = TON()
        self.TON_2 = TON()
        self.TON_3 = TON()
        self.TON_4 = TON()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def DISPACTIVE(self):
        return self._DISPACTIVE

    @property
    def RESETVALID(self):
        return self._RESETVALID

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    def OnCycle(self):
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._ERRORID = 506
            self._ERROR = True
            return
        self._DISPACTIVE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PRO_ACT
        self._RESETVALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.EXT and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE and not self._DISPACTIVE and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.ALARM_STOP and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.USER_SAFE
        if not self.EXECUTERESET:
            self.M_STATE = 0
            self._ERRORID = 0
        self.M_RE_EXECUTERESET = self.EXECUTERESET and not self.M_EXECUTERESETLAST
        self.M_EXECUTERESETLAST = self.EXECUTERESET
        self.KRC_READMXAERROR_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_READMXAERROR_1.OnCycle()
        self.M_CONFMESS = False
        self.M_RESET = False
        self._DONE = False
        if self.M_STATE == 0:
            if self.M_RE_EXECUTERESET:
                if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED:
                    self._ERRORID = 508
                if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE:
                    self._ERRORID = 509
                if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.EXT:
                    self._ERRORID = 523
                if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.USER_SAFE:
                    self._ERRORID = 524
                if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.ALARM_STOP:
                    self._ERRORID = 525
                if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PRO_ACT:
                    self._ERRORID = 526
                if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.MOVE_ENABLE:
                    self._ERRORID = 532
                if self._ERRORID == 0:
                    self.M_STATE = 1
                else:
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
        elif self.M_STATE == 1:
            if self.KRC_READMXAERROR_1.ERRORID == 0:
                self.M_STATE = 2
            self.KRC_MESSAGERESET_1.AXISGROUPIDX = self.AXISGROUPIDX
            self.KRC_MESSAGERESET_1.MESSAGERESET = True
            self.KRC_MESSAGERESET_1.OnCycle()
        elif self.M_STATE == 2:
            if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PERI_RDY:
                self.M_STATE = 3
            else:
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.DRIVESON = True
        elif self.M_STATE == 3:
            if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.STOPMESS:
                self.M_CONFMESS = True
            else:
                self.M_STATE = 4
        elif self.M_STATE == 4:
            if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PRO_ACT:
                self.M_STATE = 5
            else:
                self.M_RESET = True
        elif self.M_STATE == 5:
            self._DONE = True
            if not self.EXECUTERESET:
                self.M_STATE = 0
        self.TON_ON.IN = (self.M_CONFMESS or self.M_RESET) and not self.TON_OFF._Q
        self.TON_ON.PT = MKTIME(1, 200)
        self.TON_ON.OnCycle()
        self.TON_OFF.IN = (self.M_CONFMESS or self.M_RESET) and self.TON_ON._Q
        self.TON_OFF.PT = MKTIME(1, 100)
        self.TON_OFF.OnCycle()
        if self.M_CONFMESS and not self.TON_ON._Q:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.CONF_MESS = True
        if self.M_RESET and not self.TON_ON._Q:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.RESET = True
        self.TON_1.IN = self.M_STATE == 1
        self.TON_1.PT = MKTIME(1, 0, 5)
        self.TON_1.OnCycle()
        self.TON_2.IN = self.M_STATE == 2
        self.TON_2.PT = MKTIME(1, 0, 5)
        self.TON_2.OnCycle()
        self.TON_3.IN = self.M_STATE == 3
        self.TON_3.PT = MKTIME(1, 0, 5)
        self.TON_3.OnCycle()
        self.TON_4.IN = self.M_STATE == 4
        self.TON_4.PT = MKTIME(1, 0, 5)
        self.TON_4.OnCycle()
        if self.TON_1._Q:
            self._ERRORID = 528
        if self.TON_2._Q:
            self._ERRORID = 527
        if self.TON_3._Q:
            self._ERRORID = 529
        if self.TON_4._Q:
            self._ERRORID = 531
        if self._ERRORID != 0:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
        self._ERROR = self._ERRORID != 0
        self._BUSY = 0 < self.M_STATE < 5



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_ERROR
#  ******************************************************************************/


class KRC_ERROR:
    """
    The function block KRC_Error collectively reads and acknowledges the current error state of the mxA interface, the error state of the robot controller and the error state of the function blocks. If more than one error has occurred in the function block at the same time, only the error number of the most recent error is displayed. Errors in a function block cause the motion enable to be canceled. If more than one error has occurred at the same time, these errors are displayed with the following priority ranking: 1. Errors of the mxA interface in the robot interpreter, 2. Errors of the mxA interface in the submit interpreter, 3. ProConOS errors, 4. Errors in the PLC, 5. Errors in a function block of the local PLC, 6. Errors in the robot controller. The function block KRC_Error contains all diagnostic function blocks, which means that this block displays all important diagnostic data.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    MessageReset (bool): Acknowledges error messages of the mxA interface and the robot controller. TRUE = reset message. Note: The messages can only be reset if the robot is stationary.

    Returns:
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    NoHeartbeatKRC (bool): The submit interpreter is not sending a life sign.
    NoHeartbeatPCOS (bool): ProConOS is not sending a life sign.
    NotOnline (bool): No connection to robot controller.
    NotInitialized (bool): No statements can be executed, as the connection has not been initialized.
    NoOpModeExt (bool): Robot is not in Automatic External mode.
    NoMoveEnable (bool): No motion enable present.
    UserSafeNotOK (bool): The operator safety is violated. The $USER_SAF signal of the Automatic External interface is not active.
    KrcErrorActive (bool): Error messages of the robot controller are active. The $STOPMESS signal of the Automatic External interface is active.
    DrivesNotReady (bool): The drives are not ready. The $PERI_RDY signal of the Automatic External interface is not active.
    NoProgActive (bool): The robot program is not active. The $PRO_ACT signal of the Automatic External interface is not active.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.MESSAGERESET = False
        self._ERROR = False
        self._ERRORID = 0
        self._NOHEARTBEATKRC = False
        self._NOHEARTBEATPCOS = False
        self._NOTONLINE = False
        self._NOTINITIALIZED = False
        self._NOOPMODEEXT = False
        self._NOMOVEENABLE = False
        self._USERSAFENOTOK = False
        self._KRCERRORACTIVE = False
        self._DRIVESNOTREADY = False
        self._NOPROGACTIVE = False
        self.KRC_READMXAERROR_1 = KRC_READMXAERROR()
        self.KRC_MESSAGERESET_1 = KRC_MESSAGERESET()
        self.TON_ON = TON()
        self.TON_OFF = TON()
        self.TON_HBSUB = TON()
        self.TON_HBPCOS = TON()
        self.ENABLETONSUBMIT = False
        self.ENABLETONPCOS = False
        self.M_HEARTBEATLAST = 0
        self.M_HEARTBEATLASTPCOS = 0



    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def NOHEARTBEATKRC(self):
        return self._NOHEARTBEATKRC

    @property
    def NOHEARTBEATPCOS(self):
        return self._NOHEARTBEATPCOS

    @property
    def NOTONLINE(self):
        return self._NOTONLINE

    @property
    def NOTINITIALIZED(self):
        return self._NOTINITIALIZED

    @property
    def NOOPMODEEXT(self):
        return self._NOOPMODEEXT

    @property
    def NOMOVEENABLE(self):
        return self._NOMOVEENABLE

    @property
    def USERSAFENOTOK(self):
        return self._USERSAFENOTOK

    @property
    def KRCERRORACTIVE(self):
        return self._KRCERRORACTIVE

    @property
    def DRIVESNOTREADY(self):
        return self._DRIVESNOTREADY

    @property
    def NOPROGACTIVE(self):
        return self._NOPROGACTIVE

    def OnCycle(self):
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False
        self.KRC_MESSAGERESET_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MESSAGERESET_1.MESSAGERESET = self.MESSAGERESET
        self.KRC_MESSAGERESET_1.OnCycle()
        self.KRC_READMXAERROR_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_READMXAERROR_1.OnCycle()
        self._ERRORID = self.KRC_READMXAERROR_1.ERRORID
        if self._ERRORID == 0:
            self.TON_ON.IN = self.MESSAGERESET and not self.TON_OFF._Q
            self.TON_ON.PT = MKTIME(1, 200)
            self.TON_ON.OnCycle()
            self.TON_OFF.IN = self.MESSAGERESET and self.TON_ON._Q
            self.TON_OFF.PT = MKTIME(1, 100)
            self.TON_OFF.OnCycle()
            if self.MESSAGERESET and not self.TON_ON._Q:
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.CONF_MESS = True
                if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PERI_RDY:
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.DRIVESON = True
            if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.STOPMESS:
                self._ERRORID = 801
        self._ERROR = self._ERRORID != 0
        self.ENABLETONSUBMIT = self.M_HEARTBEATLAST == KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT >= 0
        self.ENABLETONPCOS = self.M_HEARTBEATLASTPCOS == KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEATPCOS and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEATPCOS >= 0
        self.TON_HBSUB.IN = self.ENABLETONSUBMIT
        self.TON_HBSUB.PT = MKTIME(1, 0, 1)
        self.TON_HBSUB.OnCycle()
        self.TON_HBPCOS.IN = self.ENABLETONPCOS
        self.TON_HBPCOS.PT = MKTIME(1, 0, 1)
        self.TON_HBPCOS.OnCycle()
        self.M_HEARTBEATLAST = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT
        self.M_HEARTBEATLASTPCOS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEATPCOS
        self._NOHEARTBEATKRC = self.TON_HBSUB._Q
        self._NOHEARTBEATPCOS = self.TON_HBPCOS._Q
        self._NOTONLINE = not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE
        self._NOTINITIALIZED = not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED
        self._NOOPMODEEXT = not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.EXT
        self._NOMOVEENABLE = not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.MOVE_ENABLE or KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.MOVE_DISABLE
        self._USERSAFENOTOK = not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.USER_SAFE
        self._KRCERRORACTIVE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.STOPMESS
        self._DRIVESNOTREADY = not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PERI_RDY
        self._NOPROGACTIVE = not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PRO_ACT



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_INITIALIZE
#  ******************************************************************************/

class KRC_INITIALIZE:
    """
    The function block KRC_Initialize initializes the mxA interface on the robot
    controller. Statements cannot be transferred until the interface has been
    initialized.

    This function block may only be instanced once per axis group. In the
    case of multiple instancing, the signals of the most recently called function
    block are output.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5

    Returns:
    Done (BOOL): TRUE = initialization successfully completed
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    KRC_Serial (DINT): Serial number of the robot controller
    KRC_Major (DINT): Version identifier of the mxA interface (1st digit)
    KRC_Minor (DINT): Version identifier of the mxA interface (2nd digit)
    KRC_Revision (DINT): Version identifier of the mxA interface (3rd digit)
    KRC_AbsAccur (DINT): Version identifier of the positionally accurate robot model
    PLC_Major (DINT): Version identifier of the PLC library (1st digit)
    PLC_Minor (DINT): Version identifier of the PLC library (2nd digit)
    PLC_Revision (DINT): Version identifier of the PLC library (3rd digit)
    OrderID (int): Identifier of command instance.
    """

    def __init__(self):
        self.AXISGROUPIDX = 0
        self._DONE = False
        self._ERROR = False
        self._ERRORID = 0
        self._KRC_SERIAL = 0
        self._KRC_MAJOR = 0
        self._KRC_MINOR = 0
        self._KRC_REVISION = 0
        self._KRC_ABSACCUR = 0
        self._PLC_MAJOR = 0
        self._PLC_MINOR = 0
        self._PLC_REVISION = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.MXA_RESETCOMMAND_1 = MXA_RESETCOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def KRC_SERIAL(self):
        return self._KRC_SERIAL

    @property
    def KRC_MAJOR(self):
        return self._KRC_MAJOR

    @property
    def KRC_MINOR(self):
        return self._KRC_MINOR

    @property
    def KRC_REVISION(self):
        return self._KRC_REVISION

    @property
    def KRC_ABSACCUR(self):
        return self._KRC_ABSACCUR

    @property
    def PLC_MAJOR(self):
        return self._PLC_MAJOR

    @property
    def PLC_MINOR(self):
        return self._PLC_MINOR

    @property
    def PLC_REVISION(self):
        return self._PLC_REVISION

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._PLC_MAJOR = 6
        self._PLC_MINOR = 0
        self._PLC_REVISION = 0
        self._ORDERID = 0
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._ERRORID = 506
            self._ERROR = True
            return
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].PLC_MAJOR = self._PLC_MAJOR
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].PLC_MINOR = self._PLC_MINOR
        if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE:
            self._ERRORID = 0
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED = False
            self.MXA_RESETCOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
            self.MXA_RESETCOMMAND_1.OnCycle()
        if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID > 0 and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID != 31:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID = 0
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID = 0
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE
        self.MXA_EXECUTECOMMAND_1.CMDID = 31
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = True
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._KRC_SERIAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
            self._KRC_MAJOR = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2])
            self._KRC_MINOR = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3])
            self._KRC_REVISION = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4])
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].DEF_VEL_CP = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].DEF_ACC_CP = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self._KRC_ABSACCUR = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7])
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].VEL_MAX_CP = float(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11])
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ACC_MAX_CP = float(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12])
            
            if self._KRC_MAJOR == self._PLC_MAJOR and self._KRC_MINOR >= self._PLC_MINOR:
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED = True
            else:
                self._ERRORID = 503
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID = self._ERRORID
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        if self._ERRORID == 0:
            self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




#/******************************************************************************
# * FUNCTION_BLOCK KRC_MOVE
# ******************************************************************************/

class KRC_MOVE:
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.CMDID = 1
        self.EXECUTECMD = False
        self.MOVETYPE = 0
        self.ACTPOSITION = E6POS()
        self.AXISPOSITION = E6AXIS()
        self.CIRCHP = E6POS()
        self.VELOCITY = 0
        self.ABSOLUTEVELOCITY = 0.0
        self.ACCELERATION = 0
        self.ABSOLUTEACCELERATION = 0.0
        self.COORDINATESYSTEM = COORDSYS()
        self.ORITYPE = 0
        self.CIRCTYPE = 0
        self.CIRCANGLE = 0.0
        self.APPROXIMATE = APO()
        self.POSVALIDX = False
        self.POSVALIDY = False
        self.POSVALIDZ = False
        self.POSVALIDA = False
        self.POSVALIDB = False
        self.POSVALIDC = False
        self.POSVALIDE1 = False
        self.POSVALIDE2 = False
        self.POSVALIDE3 = False
        self.POSVALIDE4 = False
        self.POSVALIDE5 = False
        self.POSVALIDE6 = False
        self.POSVALIDS = False
        self.POSVALIDT = False
        self.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.COMMANDSIZE = 0
        self.M_VELOCITY = 0
        self.M_ACCELERATION = 0

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if self.EXECUTECMD:
            if self.VELOCITY > 0 and self.ABSOLUTEVELOCITY > 0.0:
                self._ERRORID = 520
                self._ERROR = True
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
                return
            self.M_VELOCITY = int(self.VELOCITY)
            if self.MOVETYPE in [0, 1, 6, 9, 10, 11, 16, 19, 20, 21]:
                if self.ABSOLUTEVELOCITY > 0.0:
                    self._ERRORID = 519
                    self._ERROR = True
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
                    return
            if self.ABSOLUTEVELOCITY > 0.0:
                if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].DEF_VEL_CP <= 0.0:
                    self._ERRORID = 544
                    self._ERROR = True
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
                    return
                self.M_VELOCITY = int((self.ABSOLUTEVELOCITY * -100000.0) / KRC_AXISGROUPREFARR[self.AXISGROUPIDX].DEF_VEL_CP)
            self.M_ACCELERATION = int(self.ACCELERATION)
            if self.MOVETYPE in [0, 1, 6, 9, 10, 11, 16, 19, 20, 21]:
                if self.ABSOLUTEACCELERATION > 0.0:
                    self._ERRORID = 545
                    self._ERROR = True
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
                    return

#part 2
            if self.ABSOLUTEACCELERATION > 0.0:
                if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].DEF_ACC_CP <= 0.0:
                    self._ERRORID = 546
                    self._ERROR = True
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
                    return
                self.M_ACCELERATION = int(self.ABSOLUTEACCELERATION * -100000.0 / KRC_AXISGROUPREFARR[self.AXISGROUPIDX].DEF_ACC_CP)
        if self.MOVETYPE in [7, 8, 17, 18]:
            self.COMMANDSIZE = 2
        else:
            self.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = self.CMDID
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = self.COMMANDSIZE
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.POSVALIDX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[2] = self.POSVALIDY
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[3] = self.POSVALIDZ
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[4] = self.POSVALIDA
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[5] = self.POSVALIDB
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[6] = self.POSVALIDC
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[7] = self.POSVALIDE1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[8] = self.POSVALIDE2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[9] = self.POSVALIDE3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[10] = self.POSVALIDE4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[11] = self.POSVALIDE5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[12] = self.POSVALIDE6
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[13] = self.POSVALIDS
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[14] = self.POSVALIDT
            if self.MOVETYPE in [7, 8, 17, 18]:
                for i in range(15, 29):
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[i] = True
                # part 3
                    
            if self.MOVETYPE in [0, 10, 9, 19]:
                for i in range(1, 3):
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[i] = int(0)
            else:
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.ACTPOSITION.STATUS)
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = int(self.ACTPOSITION.TURN)

            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = int(self.COORDINATESYSTEM.TOOL)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[4] = int(self.COORDINATESYSTEM.BASE)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[5] = int(self.COORDINATESYSTEM.IPO_MODE)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[6] = int(self.MOVETYPE)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[7] = self.M_VELOCITY
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[8] = self.M_ACCELERATION
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[9] = int(self.APPROXIMATE.PTP_MODE)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[10] = int(self.APPROXIMATE.CP_MODE)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[11] = int(self.APPROXIMATE.CPTP)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[12] = int(self.APPROXIMATE.CVEL)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[13] = int(self.ORITYPE)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[14] = int(self.CIRCTYPE)

            if self.MOVETYPE in [7, 8, 17, 18]:
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[15] = int(self.CIRCHP.STATUS)
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[16] = int(self.CIRCHP.TURN)

# part 4

            if self.MOVETYPE in [0, 10, 9, 19]:
                for i in range(1, 7):
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[i] = getattr(self.AXISPOSITION, f'A{i}')
                for i in range(7, 13):
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[i] = getattr(self.AXISPOSITION, f'E{i-6}')
            else:
                for i in range(1, 7):
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[i] = getattr(self.ACTPOSITION, ['X', 'Y', 'Z', 'A', 'B', 'C'][i-1])
                for i in range(7, 13):
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[i] = getattr(self.ACTPOSITION, f'E{i-6}')
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[13] = self.APPROXIMATE.CDIS
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[14] = self.APPROXIMATE.CORI
            if self.MOVETYPE in [7, 8, 17, 18]:
                for i in range(15, 27):
                    KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[i] = getattr(self.CIRCHP, ['X', 'Y', 'Z', 'A', 'B', 'C'][i-15] if i < 21 else f'E{i-20}')
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[27] = self.CIRCANGLE
        self._BUSY = self.MXA_EXECUTECOMMAND_1._BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1._ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1._DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1._ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1._ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



#/******************************************************************************
# * FUNCTION_BLOCK KRC_MOVEAXISABSOLUTE
# ******************************************************************************/

class KRC_MOVEAXISABSOLUTE:
    """
    Executes a point-to-point motion to an axis-specific end position. The axis positions are absolute.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    AxisPosition (E6AXIS): Axis-specific end position. The data structure E6AXIS contains the angle values or translation values for all axes of the axis group in the end position.
    Velocity (int): Velocity. Refers to the maximum value specified in the machine data. Default: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Refers to the maximum value specified in the machine data. Default: 0% (= acceleration is not changed).
    Approximate (APO): Approximation parameter.
    BufferMode (int): Mode in which the statement is executed. Values can be 1 (ABORTING) or 2 (BUFFERED).
    SplineMode (bool): TRUE if the motion is executed as a spline motion. FALSE if the motion is executed as a conventional point-to-point motion.

    Returns:
    Busy (bool): TRUE if the statement is currently being transferred or has already been transferred.
    Active (bool): TRUE if the motion is currently being executed.
    Done (bool): TRUE if the motion has stopped.
    Aborted (bool): TRUE if the statement/motion has been aborted.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.AXISPOSITION = E6AXIS()
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.APPROXIMATE = APO()
        self.BUFFERMODE = 0
        self.SPLINEMODE = False
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.KRC_MOVE_1 = KRC_MOVE()
        self.SWITCHMOVETYPE = 0
        self.M_CIRCHP = E6POS()
        self.M_POSITION = E6POS()
        self.M_ORITYPE = 0
        self.M_COORDINATESYSTEM = COORDSYS()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if self.SPLINEMODE:
            self.SWITCHMOVETYPE = 10
        else:
            self.SWITCHMOVETYPE = 0
        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 1
        self.KRC_MOVE_1.EXECUTECMD = self.EXECUTECMD
        self.KRC_MOVE_1.MOVETYPE = self.SWITCHMOVETYPE
        self.KRC_MOVE_1.AXISPOSITION = self.AXISPOSITION
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.ORITYPE = self.M_ORITYPE
        self.KRC_MOVE_1.APPROXIMATE = self.APPROXIMATE
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = True
        self.KRC_MOVE_1.POSVALIDT = True
        self.KRC_MOVE_1.BUFFERMODE = self.BUFFERMODE
        self.KRC_MOVE_1.OnCycle()
        self._BUSY = self.KRC_MOVE_1.BUSY
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._DONE = self.KRC_MOVE_1.DONE
        self._ABORTED = self.KRC_MOVE_1.ABORTED
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.KRC_MOVE_1.ORDERID



#/******************************************************************************
# * FUNCTION_BLOCK KRC_MOVEDIRECTABSOLUTE
# ******************************************************************************/

class KRC_MOVEDIRECTABSOLUTE:
    """
    Executes a point-to-point motion to a Cartesian end position. The coordinates of the end position are absolute. The robot moves as quickly as possible to the end position.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    Position (E6POS): Coordinates of the Cartesian end position. The data structure E6POS contains all components of the end position (= position of the TCP relative to the origin of the BASE coordinate system).
    Velocity (int): Velocity. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type and refers to the value of DEF_VEL_CP of the robot system. Default: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type and refers to the value of DEF_ACC_CP of the robot system. Default: 0% (= acceleration is not changed).
    CoordinateSystem (COORDSYS): Coordinate system to which the Cartesian coordinates of the end position refer.
    Approximate (APO): Approximation parameter.
    BufferMode (int): Mode in which the statement is executed. Values can be 1 (ABORTING) or 2 (BUFFERED).
    SplineMode (bool): TRUE if the motion is executed as a spline motion. FALSE if the motion is executed as a conventional point-to-point motion.

    Returns:
    Busy (bool): TRUE if the statement is currently being transferred or has already been transferred.
    Active (bool): TRUE if the motion is currently being executed.
    Done (bool): TRUE if the motion has stopped.
    Aborted (bool): TRUE if the statement/motion has been aborted.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.POSITION = E6POS() 
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.COORDINATESYSTEM = COORDSYS()  
        self.APPROXIMATE = APO()  
        self.BUFFERMODE = 0
        self.SPLINEMODE = False

        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.KRC_MOVE_1 = KRC_MOVE()  
        self.SWITCHMOVETYPE = 0

        self.M_CIRCHP = E6POS() 
        self.M_AXISPOSITION = E6AXIS()  
        self.M_ORITYPE = 0

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._ERRORID = 506
            self._ERROR = True
            return

        if self.SPLINEMODE:
            self.SWITCHMOVETYPE = 11
        else:
            self.SWITCHMOVETYPE = 1

        # Call FB KRC_Move_1
        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 1
        self.KRC_MOVE_1.EXECUTECMD = self.EXECUTECMD
        self.KRC_MOVE_1.MOVETYPE = self.SWITCHMOVETYPE
        self.KRC_MOVE_1.ACTPOSITION = self.POSITION
        self.KRC_MOVE_1.AXISPOSITION = self.M_AXISPOSITION
        self.KRC_MOVE_1.CIRCHP = self.M_CIRCHP
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.COORDINATESYSTEM
        self.KRC_MOVE_1.ORITYPE = self.M_ORITYPE
        self.KRC_MOVE_1.CIRCTYPE = 0
        self.KRC_MOVE_1.CIRCANGLE = 0
        self.KRC_MOVE_1.APPROXIMATE = self.APPROXIMATE
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = True
        self.KRC_MOVE_1.POSVALIDT = True
        self.KRC_MOVE_1.BUFFERMODE = self.BUFFERMODE
        self.KRC_MOVE_1.OnCycle()
        self._BUSY = self.KRC_MOVE_1.BUSY
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._DONE = self.KRC_MOVE_1.DONE
        self._ABORTED = self.KRC_MOVE_1.ABORTED
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.KRC_MOVE_1.ORDERID



#/******************************************************************************
# * FUNCTION_BLOCK KRC_WRITEDIGITALOUTPUT
# ******************************************************************************/

class KRC_WRITEDIGITALOUTPUT:
    """
    The function block KRC_WriteDigitalOutput writes a digital output or a pulse output on the robot controller. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    Number (INT): Number of the digital output (corresponds to $OUT[1 … 2048] on the robot controller), can be 1 to 2048. Note: It must be ensured that no outputs are used that are already assigned by the robot system. Example: $OUT[1025] is always TRUE.
    Value (BOOL): Value of the digital output
    Pulse (REAL): Length of the pulse, can be 0.0 s (No pulse active) to 3.0 s (Pulse interval = 0.1 s)
    bContinue (BOOL): TRUE = output written in advance run. Note: The robot controller executes programs with an advance run and a main run.
    BufferMode (INT): Mode in which the statement is executed, can be 0 (DIRECT), 1 (ABORTING), or 2 (BUFFERED)

    Returns:
    Busy (BOOL): TRUE = statement is currently being transferred or has already been transferred
    Done (BOOL): TRUE = statement has been executed
    Aborted (BOOL): TRUE = statement has been aborted
    Error (BOOL): TRUE = error in function block
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.NUMBER = 0
        self.VALUE = False
        self.PULSE = 0.0
        self.BCONTINUE = False
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 10
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.BCONTINUE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[2] = self.VALUE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.NUMBER)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.PULSE
        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



#/******************************************************************************
# * FUNCTION_BLOCK KRC_WRITESOFTEND
# ******************************************************************************/

class KRC_WRITESOFTEND:
    """
    Writes the software limit switches of the robot axes.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    A1_Min to A6_Min (float): Negative software limit switch of axis A1 to A6. Unit: mm or °.
    A1_Max to A6_Max (float): Positive software limit switch of axis A1 to A6. Unit: mm or °.
    BufferMode (int): Mode in which the statement is executed. Values can be 0 (DIRECT), 1 (ABORTING), or 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE if the statement is currently being transferred or has already been transferred.
    Done (bool): TRUE if the statement has been executed.
    Aborted (bool): TRUE if the statement has been aborted.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.A1_MIN = 0.0
        self.A1_MAX = 0.0
        self.A2_MIN = 0.0
        self.A2_MAX = 0.0
        self.A3_MIN = 0.0
        self.A3_MAX = 0.0
        self.A4_MIN = 0.0
        self.A4_MAX = 0.0
        self.A5_MIN = 0.0
        self.A5_MAX = 0.0
        self.A6_MIN = 0.0
        self.A6_MAX = 0.0
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 17
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.A1_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.A1_MAX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.A2_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.A2_MAX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.A3_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.A3_MAX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = self.A4_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = self.A4_MAX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = self.A5_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[10] = self.A5_MAX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[11] = self.A6_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[12] = self.A6_MAX
        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READAXISGROUP
#  ******************************************************************************/


class KRC_READAXISGROUP:
    """
    The function block KRC_ReadAxisGroup is used to assign the parameter
    KRC4_Input to the parameter AxisGroupIdx. The following function blocks
    always refer to the same robot system using the parameter AxisGroupIdx.

    This function block must always be called at the start of the program.
    Access to the parameter AxisGroupIdx is only permissible between the
    function blocks KRC_ReadAxisGroup and KRC_WriteAxisGroup.

    The function block may only be instanced once per axis group. In the
    case of multiple instancing, the signals of the most recently called function
    block are output.

    Parameters:
    KRC4_Input (POINTER TO BYTE): Defines the start index of the output range of the robot controller
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5

    Returns:
    ErrorID (DINT): Error number
    Error (BOOL): TRUE = error in function block
    """

    def __init__(self):
        # VAR_INPUT
        self.KRC4_INPUT = None
        self.AXISGROUPIDX = 0

        # VAR_OUTPUT (Alias Variables)
        self._ERROR = False
        self._ERRORID = 0

        # VAR
        self.MXA_RESETCOMMAND_1 = MXA_RESETCOMMAND()
        self.M_AE_RC_RDY1 = False
        self.M_AE_ALARM_STOP = False
        self.M_AE_USER_SAF = False
        self.M_AE_PERI_RDY = False
        self.M_AE_ROB_CAL = False
        self.M_AE_IO_ACTCONF = False
        self.M_AE_STOPMESS = False
        self.M_AE_PGNO_FBIT_REFL = False
        self.M_AE_INT_ESTOP = False
        self.M_AE_PRO_ACT = False
        self.M_AE_PGNO_REQ = False
        self.M_AE_APPL_RUN = False
        self.M_AE_PRO_MOVE = False
        self.M_AE_IN_HOME = False
        self.M_AE_ON_PATH = False
        self.M_AE_NEAR_POSRET = False
        self.M_AE_ROB_STOPPED = False
        self.M_AE_T1 = False
        self.M_AE_T2 = False
        self.M_AE_AUT = False
        self.M_AE_EXT = False
        self.M_BRAKETEST_MONTIME = False
        self.M_BRAKETEST_REQ_INT = False
        self.M_BRAKETEST_WORK = False
        self.M_BRAKES_OK = False
        self.M_BRAKETEST_WARN = False
        self.M_ABORTACTIVE = False
        self.M_BRAKEACTIVE = False
        self.M_KCP_CONNECT = False
        self.M_TOUCHUP = False
        self.M_MASTEST_REQ_INT = False
        self.M_MASTESTSWITCH_OK = False
        self.M_POS_ACT_VALID = False
        self.M_HEARTBEATSUBMIT = 0
        self.M_IN_VAL_1TO8 = 0
        self.M_TOUCHUP_POSNO = 0
        self.M_SR_ORDER1_ID = 0
        self.M_SR_ORDER2_ID = 0
        self.M_SR_ORDER3_ID = 0
        self.M_SR_ORDER4_ID = 0
        self.M_SR_ORDER5_ID = 0
        self.M_SR_ORDER6_ID = 0
        self.M_SR_ORDER7_ID = 0
        self.M_SR_ORDER8_ID = 0
        self.M_SR_ORDER9_ID = 0
        self.M_SR_ORDER10_ID = 0
        self.M_SR_ORDER1_STATE = 0
        self.M_SR_ORDER2_STATE = 0
        self.M_SR_ORDER3_STATE = 0
        self.M_SR_ORDER4_STATE = 0
        self.M_SR_ORDER5_STATE = 0
        self.M_SR_ORDER6_STATE = 0
        self.M_SR_ORDER7_STATE = 0
        self.M_SR_ORDER8_STATE = 0
        self.M_SR_ORDER9_STATE = 0
        self.M_SR_ORDER10_STATE = 0
        self.M_HEARTBEATPCOS = 0
        self.M_OVERRIDE = 0
        self.M_POSACT_X = 0
        self.M_POSACT_Y = 0
        self.M_POSACT_Z = 0
        self.M_POSACT_A = 0
        self.M_POSACT_B = 0
        self.M_POSACT_C = 0
        self.M_POSACT_STATUS = 0
        self.M_POSACT_TURN = 0
        self.M_TOOLACT = 0
        self.M_BASEACT = 0
        self.M_IPOMODE = 0
        self.M_AXISACT_A1 = 0
        self.M_AXISACT_A2 = 0
        self.M_AXISACT_A3 = 0
        self.M_AXISACT_A4 = 0
        self.M_AXISACT_A5 = 0
        self.M_AXISACT_A6 = 0
        self.M_AXISACT_A7 = 0
        self.M_AXISACT_A8 = 0
        self.M_AXISACT_A9 = 0
        self.M_AXISACT_A10 = 0
        self.M_AXISACT_A11 = 0
        self.M_AXISACT_A12 = 0
        self.M_VELACT = 0
        self.M_WORKSTATES = 0
        self.M_AXWORKSTATES = 0
        self.M_GROUPSTATE = 0
        self.M_ERRORID = 0
        self.M_ERRORIDSUB = 0
        self.M_ACTIVEPOSORDERID = 0
        self.M_ACTIVEORDERIDB = 0
        self.M_QUEUECOUNT = 0
        self.M_IR_STATUS1 = 0
        self.M_IR_STATUS2 = 0
        self.M_IR_STATUS3 = 0
        self.M_IR_STATUS4 = 0
        self.M_IR_STATUS5 = 0
        self.M_IR_STATUS6 = 0
        self.M_IR_STATUS7 = 0
        self.M_IR_STATUS8 = 0
        self.M_ERRORIDPCOS = 0
        self.M_FREE_FOR_WOV = 0
        self.M_TRANSMISSIONNORET = 0
        self.M_ORDERIDRET = 0
        self.M_CMDIDRET = 0
        self.M_CMDDATARETCS = 0
        self.M_RESERVE190 = 0
        self.M_CMDDATARET1 = 0
        self.M_CMDDATARET2 = 0
        self.M_CMDDATARET3 = 0
        self.M_CMDDATARET4 = 0
        self.M_CMDDATARET5 = 0
        self.M_CMDDATARET6 = 0
        self.M_CMDDATARET7 = 0
        self.M_CMDDATARET8 = 0
        self.M_CMDDATARET9 = 0
        self.M_CMDDATARET10 = 0
        self.M_CMDDATARET11 = 0
        self.M_CMDDATARET12 = 0
        self.M_RESERVE242 = 0
        self.NCHECKSUM = 0
        self.FTMP = 0
        self.NTMP1 = 0
        self.FTMP1 = 0
        self.BTMP1 = False
        self.I = 0
        self.ONF_TRIG = False
        self.ENABLETONSUBMIT = False
        self.ENABLETONPCOS = False
        self.M_INITOK = False
        self.M_HEARTBEATLAST = 0
        self.M_HEARTBEATLASTPCOS = 0
        self.HEARTBEATTO = MKTIME(1, 0, 0)
        self.TON_1_SUBMIT = TON()
        self.TON_1_PCOS = TON()
        self.TON_2 = TON()
        self.M_LASTORDERID = 0
        self.R_TRIG_1 = R_TRIG()
        self.M_CONNECTIONOK = False
        self.M_F_TRIG = False
        self.M_FIRSTCYCLES = 0
        self.RETB = False

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID


    def OnCycle(self):
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False
        if not self.M_INITOK:
            self.M_INITOK = True
            if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].READAXISGROUPINIT:
                self._ERRORID = 505
                self._ERROR = True
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID = self._ERRORID
            else:
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].READAXISGROUPINIT = True
        if self.M_FIRSTCYCLES < 100:   
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE = False
            self.M_HEARTBEATLAST = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].READAXISGROUPINIT = True
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.BRAKEF = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.BRAKE = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.RELEASEBRAKE = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.MESSAGERESET = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.BRAKETEST_REQ_EXT = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.MASTERINGTEST_REQ_EXT = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.WRITE_OUT_1TO8 = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.CONF_MESS = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.RESET = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.DRIVESON = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].READDONE = True
        if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].HEARTBEATTO <= 0:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].HEARTBEATTO = 1000
        self.HEARTBEATTO = (KRC_AXISGROUPREFARR[self.AXISGROUPIDX].HEARTBEATTO) 
        self.ENABLETONSUBMIT = self.M_HEARTBEATLAST == KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT > 0
        self.ENABLETONPCOS = self.M_HEARTBEATLASTPCOS == KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEATPCOS and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEATPCOS > 0
        if self.M_HEARTBEATLAST != KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT > 0 and self.M_HEARTBEATLASTPCOS != KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEATPCOS and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEATPCOS > 0:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE = True
        self.TON_1_SUBMIT.IN = self.ENABLETONSUBMIT
        self.TON_1_SUBMIT.PT = self.HEARTBEATTO
        self.TON_1_PCOS.IN = self.ENABLETONPCOS
        self.TON_1_PCOS.PT = self.HEARTBEATTO
        self.TON_1_SUBMIT.OnCycle()
        self.TON_1_PCOS.OnCycle()
        self.M_HEARTBEATLAST = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT
        self.M_HEARTBEATLASTPCOS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEATPCOS
        if self.TON_1_SUBMIT._Q or self.TON_1_PCOS._Q:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE = False
        ONF_TRIG = not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE and self.M_F_TRIG
        M_F_TRIG = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE
        if ONF_TRIG:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID = 510
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED = False
        self.TON_2.IN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID > 0 and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID == self.M_LASTORDERID and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID == KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.ORDERIDRET
        self.TON_2.PT = (KRC_AXISGROUPREFARR[self.AXISGROUPIDX].HEARTBEATTO * 1) 
        self.TON_2.OnCycle()
        self.M_LASTORDERID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID
        self.R_TRIG_1.CLK =  self.TON_2._Q
        self.R_TRIG_1.OnCycle()
        if  self.R_TRIG_1._Q:
            self._ERRORID = 511
            self._ERROR = True
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID = self._ERRORID
        if  self.TON_2._Q and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID == 0:
            self._ERRORID = 0
            self._ERROR = False
            self.MXA_RESETCOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
            self.MXA_RESETCOMMAND_1.OnCycle()
        self.M_AE_RC_RDY1 =      IsBitSet( self.KRC4_INPUT[0] , 0 )
        self.M_AE_ALARM_STOP =   IsBitSet( self.KRC4_INPUT[0] , 1)
        self.M_AE_USER_SAF =     IsBitSet( self.KRC4_INPUT[0],2)
        self.M_AE_PERI_RDY =     IsBitSet( self.KRC4_INPUT[0],3)
        self.M_AE_ROB_CAL = IsBitSet(self.KRC4_INPUT[0], 4)
        self.M_AE_IO_ACTCONF = IsBitSet(self.KRC4_INPUT[0], 5)
        self.M_AE_STOPMESS = IsBitSet(self.KRC4_INPUT[0], 6)
        self.M_AE_PGNO_FBIT_REFL = IsBitSet(self.KRC4_INPUT[0], 7)
        self.M_AE_INT_ESTOP = IsBitSet(self.KRC4_INPUT[1], 0)
        self.M_AE_PRO_ACT = IsBitSet(self.KRC4_INPUT[1], 1)
        self.M_AE_PGNO_REQ = IsBitSet(self.KRC4_INPUT[1], 2)
        self.M_AE_APPL_RUN = IsBitSet(self.KRC4_INPUT[1], 3)
        self.M_AE_PRO_MOVE = IsBitSet(self.KRC4_INPUT[1], 4)
        self.M_AE_IN_HOME = IsBitSet(self.KRC4_INPUT[1], 5)
        self.M_AE_ON_PATH = IsBitSet(self.KRC4_INPUT[1], 6)
        self.M_AE_NEAR_POSRET = IsBitSet(self.KRC4_INPUT[1], 7)
        self.M_AE_ROB_STOPPED = IsBitSet(self.KRC4_INPUT[2], 0)
        self.M_AE_T1 = IsBitSet(self.KRC4_INPUT[2], 1)
        self.M_AE_T2 = IsBitSet(self.KRC4_INPUT[2], 2)
        self.M_AE_AUT = IsBitSet(self.KRC4_INPUT[2], 3)
        self.M_AE_EXT = IsBitSet(self.KRC4_INPUT[2], 4)
        
        self.M_BRAKETEST_MONTIME = IsBitSet(self.KRC4_INPUT[2], 5)
        self.M_BRAKETEST_REQ_INT = IsBitSet(self.KRC4_INPUT[2], 6)
        self.M_BRAKETEST_WORK = IsBitSet(self.KRC4_INPUT[2], 7)
        self.M_BRAKES_OK = IsBitSet(self.KRC4_INPUT[3], 0)
        self.M_BRAKETEST_WARN = IsBitSet(self.KRC4_INPUT[3], 1)
        self.M_ABORTACTIVE = IsBitSet(self.KRC4_INPUT[3], 2)
        self.M_BRAKEACTIVE = IsBitSet(self.KRC4_INPUT[3], 3)
        self.M_KCP_CONNECT = IsBitSet(self.KRC4_INPUT[3], 4)
        self.M_TOUCHUP = IsBitSet(self.KRC4_INPUT[3], 5)
        self.M_MASTEST_REQ_INT = IsBitSet(self.KRC4_INPUT[3], 6)
        self.M_MASTESTSWITCH_OK = IsBitSet(self.KRC4_INPUT[3], 7)
        self.M_POS_ACT_VALID = IsBitSet(self.KRC4_INPUT[58], 0)

        self.M_HEARTBEATSUBMIT = MXA_GETIO_BYTE(4, self.KRC4_INPUT)
        self.M_IN_VAL_1TO8 = MXA_GETIO_BYTE(5, self.KRC4_INPUT)
        self.M_TOUCHUP_POSNO = MXA_GETIO_INT(6, self.KRC4_INPUT)
        self.M_SR_ORDER1_ID = MXA_GETIO_DINT(8, self.KRC4_INPUT)
        self.M_SR_ORDER2_ID = MXA_GETIO_DINT(12, self.KRC4_INPUT)
        self.M_SR_ORDER3_ID = MXA_GETIO_DINT(16, self.KRC4_INPUT)
        self.M_SR_ORDER4_ID = MXA_GETIO_DINT(20, self.KRC4_INPUT)
        self.M_SR_ORDER5_ID = MXA_GETIO_DINT(24, self.KRC4_INPUT)
        self.M_SR_ORDER6_ID = MXA_GETIO_DINT(28, self.KRC4_INPUT)
        self.M_SR_ORDER7_ID = MXA_GETIO_DINT(32, self.KRC4_INPUT)
        self.M_SR_ORDER8_ID = MXA_GETIO_DINT(36, self.KRC4_INPUT)
        self.M_SR_ORDER9_ID = MXA_GETIO_DINT(40, self.KRC4_INPUT)
        self.M_SR_ORDER10_ID = MXA_GETIO_DINT(44, self.KRC4_INPUT)
        self.M_SR_ORDER1_STATE = MXA_GETIO_BYTE(48, self.KRC4_INPUT)
        self.M_SR_ORDER2_STATE = MXA_GETIO_BYTE(49, self.KRC4_INPUT)
        self.M_SR_ORDER3_STATE = MXA_GETIO_BYTE(50, self.KRC4_INPUT)
        self.M_SR_ORDER4_STATE = MXA_GETIO_BYTE(51, self.KRC4_INPUT)
        self.M_SR_ORDER5_STATE = MXA_GETIO_BYTE(52, self.KRC4_INPUT)
        self.M_SR_ORDER6_STATE = MXA_GETIO_BYTE(53, self.KRC4_INPUT)
        self.M_SR_ORDER7_STATE = MXA_GETIO_BYTE(54, self.KRC4_INPUT)
        self.M_SR_ORDER8_STATE = MXA_GETIO_BYTE(55, self.KRC4_INPUT)
        self.M_SR_ORDER9_STATE = MXA_GETIO_BYTE(56, self.KRC4_INPUT)
        self.M_SR_ORDER10_STATE = MXA_GETIO_BYTE(57, self.KRC4_INPUT)
        self.M_HEARTBEATPCOS = MXA_GETIO_BYTE(59, self.KRC4_INPUT)
        self.M_OVERRIDE = MXA_GETIO_BYTE(60, self.KRC4_INPUT)
        self.M_POSACT_X = MXA_GETIO_REAL(61, self.KRC4_INPUT)
        self.M_POSACT_Y = MXA_GETIO_REAL(65, self.KRC4_INPUT)
        self.M_POSACT_Z = MXA_GETIO_REAL(69, self.KRC4_INPUT)
        self.M_POSACT_A = MXA_GETIO_REAL(73, self.KRC4_INPUT)
        self.M_POSACT_B = MXA_GETIO_REAL(77, self.KRC4_INPUT)
        self.M_POSACT_C = MXA_GETIO_REAL(81, self.KRC4_INPUT)
        self.M_POSACT_STATUS = MXA_GETIO_DINT(85, self.KRC4_INPUT)
        self.M_POSACT_TURN = MXA_GETIO_BYTE(89, self.KRC4_INPUT)
        self.M_TOOLACT = MXA_GETIO_SINT(90, self.KRC4_INPUT)
        self.M_BASEACT = MXA_GETIO_SINT(91, self.KRC4_INPUT)
        self.M_IPOMODE = MXA_GETIO_BYTE(92, self.KRC4_INPUT)
        self.M_AXISACT_A1 = MXA_GETIO_REAL(93, self.KRC4_INPUT)
        self.M_AXISACT_A2 = MXA_GETIO_REAL(97, self.KRC4_INPUT)
        self.M_AXISACT_A3 = MXA_GETIO_REAL(101, self.KRC4_INPUT)
        self.M_AXISACT_A4 = MXA_GETIO_REAL(105, self.KRC4_INPUT)
        self.M_AXISACT_A5 = MXA_GETIO_REAL(109, self.KRC4_INPUT)
        self.M_AXISACT_A6 = MXA_GETIO_REAL(113, self.KRC4_INPUT)
        self.M_AXISACT_A7 = MXA_GETIO_REAL(117, self.KRC4_INPUT)
        self.M_AXISACT_A8 = MXA_GETIO_REAL(121, self.KRC4_INPUT)
        self.M_AXISACT_A9 = MXA_GETIO_REAL(125, self.KRC4_INPUT)
        self.M_AXISACT_A10 = MXA_GETIO_REAL(129, self.KRC4_INPUT)
        self.M_AXISACT_A11 = MXA_GETIO_REAL(133, self.KRC4_INPUT)
        self.M_AXISACT_A12 = MXA_GETIO_REAL(137, self.KRC4_INPUT)
        self.M_VELACT = MXA_GETIO_REAL(141, self.KRC4_INPUT)
        self.M_WORKSTATES = MXA_GETIO_BYTE(155, self.KRC4_INPUT)
        self.M_AXWORKSTATES = MXA_GETIO_BYTE(156, self.KRC4_INPUT)
        self.M_GROUPSTATE = MXA_GETIO_BYTE(157, self.KRC4_INPUT)
        self.M_ERRORID = MXA_GETIO_INT(158, self.KRC4_INPUT)
        self.M_ERRORIDSUB = MXA_GETIO_INT(160, self.KRC4_INPUT)
        self.M_ACTIVEPOSORDERID = MXA_GETIO_DINT(162, self.KRC4_INPUT)
        self.M_ACTIVEORDERIDB = MXA_GETIO_DINT(166, self.KRC4_INPUT)
        self.M_QUEUECOUNT = MXA_GETIO_BYTE(170, self.KRC4_INPUT)
        self.M_IR_STATUS1, self.M_IR_STATUS2 = MXA_GETIO_NIBBLE(171, self.KRC4_INPUT)
        self.M_IR_STATUS3, self.M_IR_STATUS4 = MXA_GETIO_NIBBLE(172, self.KRC4_INPUT)
        self.M_IR_STATUS5, self.M_IR_STATUS6 = MXA_GETIO_NIBBLE(173, self.KRC4_INPUT)
        self.M_IR_STATUS7, self.M_IR_STATUS8 = MXA_GETIO_NIBBLE(174, self.KRC4_INPUT)
        self.M_ERRORIDPCOS = MXA_GETIO_BYTE(175, self.KRC4_INPUT)
        self.M_FREE_FOR_WOV = MXA_GETIO_BYTE(176, self.KRC4_INPUT)
        self.M_TRANSMISSIONNORET = MXA_GETIO_BYTE(177, self.KRC4_INPUT)
        self.M_ORDERIDRET = MXA_GETIO_DINT(178, self.KRC4_INPUT)
        self.M_CMDIDRET = MXA_GETIO_DINT(182, self.KRC4_INPUT )
        self.M_CMDDATARETCS = MXA_GETIO_DINT(186, self.KRC4_INPUT)
        self.M_RESERVE190 = MXA_GETIO_DINT(190, self.KRC4_INPUT)
        self.M_CMDDATARET1 = MXA_GETIO_REAL(194, self.KRC4_INPUT)
        self.M_CMDDATARET2 = MXA_GETIO_REAL(198, self.KRC4_INPUT)
        self.M_CMDDATARET3 = MXA_GETIO_REAL(202, self.KRC4_INPUT)
        self.M_CMDDATARET4 = MXA_GETIO_REAL(206, self.KRC4_INPUT)
        self.M_CMDDATARET5 = MXA_GETIO_REAL(210, self.KRC4_INPUT)
        self.M_CMDDATARET6 = MXA_GETIO_REAL(214, self.KRC4_INPUT)
        self.M_CMDDATARET7 = MXA_GETIO_REAL(218, self.KRC4_INPUT)
        self.M_CMDDATARET8 = MXA_GETIO_REAL(222, self.KRC4_INPUT)
        self.M_CMDDATARET9 = MXA_GETIO_REAL(226, self.KRC4_INPUT)
        self.M_CMDDATARET10 = MXA_GETIO_REAL(230, self.KRC4_INPUT)
        self.M_CMDDATARET11 = MXA_GETIO_REAL(234, self.KRC4_INPUT)
        self.M_CMDDATARET12 = MXA_GETIO_REAL(238, self.KRC4_INPUT)
        self.M_RESERVE242 = MXA_GETIO_DINT(242, self.KRC4_INPUT)


        self.M_CONNECTIONOK = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.RC_RDY1 = self.M_AE_RC_RDY1
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.ALARM_STOP = self.M_AE_ALARM_STOP
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.USER_SAFE = self.M_AE_USER_SAF
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PERI_RDY = self.M_AE_PERI_RDY
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.ROB_CAL = self.M_AE_ROB_CAL
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.IO_ACTCONF = self.M_AE_IO_ACTCONF
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.STOPMESS = self.M_AE_STOPMESS
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PGNO_FBIT_REFL = self.M_AE_PGNO_FBIT_REFL
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.INTNOTAUS = self.M_AE_INT_ESTOP
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PRO_ACT = self.M_AE_PRO_ACT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PGNO_REQ = self.M_AE_PGNO_REQ
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.APPL_RUN = self.M_AE_APPL_RUN
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PRO_MOVE = self.M_AE_PRO_MOVE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.IN_HOME = self.M_AE_IN_HOME
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.ON_PATH = self.M_AE_ON_PATH
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.NEAR_POSRET = self.M_AE_NEAR_POSRET
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.ROB_STOPPED = self.M_AE_ROB_STOPPED
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.T1 = self.M_AE_T1
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.T2 = self.M_AE_T2
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.AUT = self.M_AE_AUT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.EXT = self.M_AE_EXT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.KCP_CONNECT = self.M_KCP_CONNECT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKETEST_MONTIME = self.M_BRAKETEST_MONTIME
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKETEST_REQ_INT = self.M_BRAKETEST_REQ_INT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKETEST_WORK = self.M_BRAKETEST_WORK
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKES_OK = self.M_BRAKES_OK
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKETEST_WARN = self.M_BRAKETEST_WARN
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.MASTERINGTEST_REQ_INT = self.M_MASTEST_REQ_INT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.MASTERINGTESTSWITCH_OK = self.M_MASTESTSWITCH_OK
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACTVALID = self.M_POS_ACT_VALID and self.M_CONNECTIONOK


        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACTVALID = self.M_CONNECTIONOK
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.BRAKEACTIVE = self.M_BRAKEACTIVE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ABORTACTIVE = self.M_ABORTACTIVE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.TOUCHUP = self.M_TOUCHUP
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.TOUCHUP_INDEX = self.M_TOUCHUP_POSNO
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT = self.M_HEARTBEATSUBMIT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEATPCOS = self.M_HEARTBEATPCOS
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.OVPROACT = self.M_OVERRIDE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.QUEUECOUNT = self.M_QUEUECOUNT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.X = self.M_POSACT_X
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.Y = self.M_POSACT_Y
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.Z = self.M_POSACT_Z
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.A = self.M_POSACT_A
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.B = self.M_POSACT_B
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.C = self.M_POSACT_C
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.E1 = self.M_AXISACT_A7
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.E2 = self.M_AXISACT_A8
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.E3 = self.M_AXISACT_A9
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.E4 = self.M_AXISACT_A10
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.E5 = self.M_AXISACT_A11
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.E6 = self.M_AXISACT_A12
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.STATUS = DINT_TO_INT(self.M_POSACT_STATUS)
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT.TURN = self.M_POSACT_TURN
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.TOOLACT = self.M_TOOLACT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.BASEACT = self.M_BASEACT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IPOMODEACT = self.M_IPOMODE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A1 = self.M_AXISACT_A1
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A2 = self.M_AXISACT_A2
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A3 = self.M_AXISACT_A3
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A4 = self.M_AXISACT_A4
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A5 = self.M_AXISACT_A5
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.A6 = self.M_AXISACT_A6
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E1 = self.M_AXISACT_A7
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E2 = self.M_AXISACT_A8
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E3 = self.M_AXISACT_A9
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E4 = self.M_AXISACT_A10
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E5 = self.M_AXISACT_A11
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT.E6 = self.M_AXISACT_A12
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.VELACT = self.M_VELACT
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.WORKSTATES = self.M_WORKSTATES
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXWORKSTATES = self.M_AXWORKSTATES
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.GROUPSTATE = self.M_GROUPSTATE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORID = self.M_ERRORID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORIDSUB = self.M_ERRORIDSUB
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORIDPCOS = self.M_ERRORIDPCOS
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ACTIVEPOSORDERID = self.M_ACTIVEPOSORDERID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ACTIVEORDERIDB = self.M_ACTIVEORDERIDB
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IN_VAL_1TO8 = self.M_IN_VAL_1TO8
        if self.M_FIRSTCYCLES < 100:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORID = 0
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID = 0
            self.M_FIRSTCYCLES += 1
        if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORIDSUB = 0

        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[1].SR_ORDERID = self.M_SR_ORDER1_ID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[2].SR_ORDERID = self.M_SR_ORDER2_ID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[3].SR_ORDERID = self.M_SR_ORDER3_ID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[4].SR_ORDERID = self.M_SR_ORDER4_ID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[5].SR_ORDERID = self.M_SR_ORDER5_ID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[6].SR_ORDERID = self.M_SR_ORDER6_ID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[7].SR_ORDERID = self.M_SR_ORDER7_ID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[8].SR_ORDERID = self.M_SR_ORDER8_ID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[9].SR_ORDERID = self.M_SR_ORDER9_ID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[10].SR_ORDERID = self.M_SR_ORDER10_ID
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[1].SR_STATE = self.M_SR_ORDER1_STATE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[2].SR_STATE = self.M_SR_ORDER2_STATE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[3].SR_STATE = self.M_SR_ORDER3_STATE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[4].SR_STATE = self.M_SR_ORDER4_STATE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[5].SR_STATE = self.M_SR_ORDER5_STATE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[6].SR_STATE = self.M_SR_ORDER6_STATE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[7].SR_STATE = self.M_SR_ORDER7_STATE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[8].SR_STATE = self.M_SR_ORDER8_STATE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[9].SR_STATE = self.M_SR_ORDER9_STATE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[10].SR_STATE = self.M_SR_ORDER10_STATE
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.TRANSMISSIONNORET = self.M_TRANSMISSIONNORET


        #part


        if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID == self.M_ORDERIDRET:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDIDRET = self.M_CMDIDRET
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.ORDERIDRET = self.M_ORDERIDRET
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETCSKRC = self.M_CMDDATARETCS
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1] = self.M_CMDDATARET1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2] = self.M_CMDDATARET2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3] = self.M_CMDDATARET3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4] = self.M_CMDDATARET4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5] = self.M_CMDDATARET5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6] = self.M_CMDDATARET6
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7] = self.M_CMDDATARET7
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8] = self.M_CMDDATARET8
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9] = self.M_CMDDATARET9
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10] = self.M_CMDDATARET10
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11] = self.M_CMDDATARET11
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12] = self.M_CMDDATARET12
            
            self.NCHECKSUM = 0
            for I in range(1, 13):
                FTMP =self.convert_to_float32(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[I])

                
                if FTMP >= 0:
                    if FTMP - int(FTMP) >= 0.5:
                        NTMP1 = int(FTMP) + 1
                    else:
                        NTMP1 = int(FTMP)
                else:
                    if int(FTMP) - FTMP >= 0.5:
                        NTMP1 = int(FTMP) - 1
                    else:
                        NTMP1 = int(FTMP)

                self.NCHECKSUM ^= NTMP1


                if FTMP > 2147483500.0 or FTMP < -2147483500.0:
                    self.NCHECKSUM = 0
                

#part 3

            self.NCHECKSUM = self.NCHECKSUM ^ KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDIDRET
            self.NCHECKSUM = self.NCHECKSUM ^ KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.ORDERIDRET
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETCSPLC = self.NCHECKSUM
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.INTERRUPTSTATE[1] = self.M_IR_STATUS1
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.INTERRUPTSTATE[2] = self.M_IR_STATUS2
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.INTERRUPTSTATE[3] = self.M_IR_STATUS3
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.INTERRUPTSTATE[4] = self.M_IR_STATUS4
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.INTERRUPTSTATE[5] = self.M_IR_STATUS5
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.INTERRUPTSTATE[6] = self.M_IR_STATUS6
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.INTERRUPTSTATE[7] = self.M_IR_STATUS7
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.INTERRUPTSTATE[8] = self.M_IR_STATUS8
    def convert_to_float32(self,value):
        return struct.unpack('f', struct.pack('f', value))[0]

            



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_WRITEAXISGROUP
#  ******************************************************************************/


class KRC_WRITEAXISGROUP:
    """
    The function block KRC_WriteAxisGroup uses the parameter AxisGroupIdx
    to write the inputs to the range defined by the parameter KRC4_Output.

    This function block must always be called at the end of the program.
    Access to AxisGroupIdx is only permissible between the function blocks
    KRC_ReadAxisGroup and KRC_WriteAxisGroup.

    The function block may only be instanced once per axis group. In the
    case of multiple instancing, the signals of the most recently called function
    block are output.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    KRC4_Output (POINTER TO BYTE): Defines the start index of the input range of the robot controller

    Returns:
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    """

    def __init__(self):
        self.AXISGROUPIDX = 0
        self._KRC4_OUTPUT = KRC4_OUTPUT
        self._ERROR = False
        self._ERRORID = 0
        self.NCHECKSUM = 0
        self.I = 0
        self.LASTORDERID = 0
        self.LASTTGNUMBER = 0
        self.LASTTGTYPE = 0
        self.M_COMMANDID = 0
        self.M_ORDERID = 0
        self.M_PROFINETERR = False
        self.M_PROFINETSTATUS = 0
        self.M_ANZTELEGRAMME = 0
        self.AE_PGNO_FBIT_VAL = False
        self.AE_PGNO_BIT1_VAL = False
        self.AE_PGNO_BIT2_VAL = False
        self.AE_PGNO_BIT3_VAL = False
        self.AE_PGNO_BIT4_VAL = False
        self.AE_PGNO_BIT5_VAL = False
        self.AE_PGNO_BIT6_VAL = False
        self.AE_PGNO_BIT7_VAL = False
        self.AE_PGNO_PARITY_VAL = False
        self.AE_PGNO_VALID_VAL = False
        self.AE_EXT_START_VAL = False
        self.AE_MOVE_ENABLE_VAL = False
        self.AE_CONF_MESS_VAL = False
        self.AE_DRIVES_OFF_VAL = False
        self.AE_DRIVES_ON_VAL = False
        self.MASTEST_REQ_EXT_VAL = False
        self.BRAKETEST_REQ_EXT_VAL = False
        self.AE_RESET_VAL = False
        self.BRAKE_VAL = False
        self.BRAKE_F_VAL = False
        self.RELEASE_BRAKE_VAL = False
        self.SHOW_TRACE_VAL = False
        self.MESSAGE_RESET_VAL = False
        self.OUT_VAL_1_VAL = False
        self.OUT_VAL_2_VAL = False
        self.OUT_VAL_3_VAL = False
        self.OUT_VAL_4_VAL = False
        self.OUT_VAL_5_VAL = False
        self.OUT_VAL_6_VAL = False
        self.OUT_VAL_7_VAL = False
        self.OUT_VAL_8_VAL = False
        self.WRITE_OUT_1TO8_VAL = False
        self.JOG_ADVANCED_VAL = False
        self.ZW_JOG_AD_STATE_VAL = 0
        self.JOG_AD_STATE = 0
        self.HEARTBEAT_VAL = 0
        self.OVERRIDE_VAL = 0
        self.PLC_MAJOR_VAL = 0
        self.PLC_MINOR_VAL = 0
        self.SR_ORDER1_ID_VAL = 0
        self.SR_ORDER2_ID_VAL = 0
        self.SR_ORDER3_ID_VAL = 0
        self.SR_ORDER4_ID_VAL = 0
        self.SR_ORDER5_ID_VAL = 0
        self.SR_ORDER6_ID_VAL = 0
        self.SR_ORDER7_ID_VAL = 0
        self.SR_ORDER8_ID_VAL = 0
        self.SR_ORDER9_ID_VAL = 0
        self.SR_ORDER10_ID_VAL = 0
        self.SR_ORDER1_STATE_VAL = 0
        self.SR_ORDER2_STATE_VAL = 0
        self.SR_ORDER3_STATE_VAL = 0
        self.SR_ORDER4_STATE_VAL = 0
        self.SR_ORDER5_STATE_VAL = 0
        self.SR_ORDER6_STATE_VAL = 0
        self.SR_ORDER7_STATE_VAL = 0
        self.SR_ORDER8_STATE_VAL = 0
        self.SR_ORDER9_STATE_VAL = 0
        self.SR_ORDER10_STATE_VAL = 0
        self.CMDPAR_INT1_VAL = 0
        self.CMDPAR_INT2_VAL = 0
        self.CMDPAR_INT3_VAL = 0
        self.CMDPAR_INT4_VAL = 0
        self.CMDPAR_INT5_VAL = 0
        self.CMDPAR_INT6_VAL = 0
        self.CMDPAR_INT7_VAL = 0
        self.CMDPAR_INT8_VAL = 0
        self.CMDPAR_INT9_VAL = 0
        self.CMDPAR_INT10_VAL = 0
        self.CMDPAR_INT11_VAL = 0
        self.CMDPAR_INT12_VAL = 0
        self.CMDPAR_INT13_VAL = 0
        self.CMDPAR_INT14_VAL = 0
        self.CMDPAR_INT15_VAL = 0
        self.CMDPAR_REAL1_VAL = 0.0
        self.CMDPAR_REAL2_VAL = 0.0
        self.CMDPAR_REAL3_VAL = 0.0
        self.CMDPAR_REAL4_VAL = 0.0
        self.CMDPAR_REAL5_VAL = 0.0
        self.CMDPAR_REAL6_VAL = 0.0
        self.CMDPAR_REAL7_VAL = 0.0
        self.CMDPAR_REAL8_VAL = 0.0
        self.CMDPAR_REAL9_VAL = 0.0
        self.CMDPAR_REAL10_VAL = 0.0
        self.CMDPAR_REAL11_VAL = 0.0
        self.CMDPAR_REAL12_VAL = 0.0
        self.CMDPAR_REAL13_VAL = 0.0
        self.CMDPAR_REAL14_VAL = 0.0
        self.CMDPAR_REAL15_VAL = 0.0
        self.CHECKSUM_VAL = 0
        self.TRANSMISSIONNO1_VAL = 0
        self.TRANSMISSIONNO2_VAL = 0
        self.TRANSMISSIONTYPE_VAL = 0
        self.ORDERID_VAL = 0
        self.CMDID_VAL = 0
        self.BUFFERMODE_VAL = 0
        self.BOOLVALUES1 = 0
        self.MXA_RESETCOMMAND_1 = MXA_RESETCOMMAND()
        self.DUMMY = False
        self.FTMP = 0.0
        self.NTMP1 = 0
        self.FTMP1 = 0.0
        self.BTMP1 = False
        self.BMAXREALERR = False
    def convert_to_float32(self,value):
        return struct.unpack('f', struct.pack('f', value))[0]

    @property
    def KRC4_OUTPUT(self):
        return self._KRC4_OUTPUT

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID


    def OnCycle(self):
        self._ERRORID = 0
        self.NCHECKSUM = 0
        self.BMAXREALERR = False
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False
        if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID > 0 and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID == KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.ORDERIDRET:
            self.MXA_RESETCOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
            self.MXA_RESETCOMMAND_1.OnCycle()
        if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].READDONE:
            self._ERRORID = 507
            self._ERROR = True
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID = self._ERRORID
        else:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].READDONE = False
        self.AE_PGNO_FBIT_VAL = False
        self.AE_PGNO_BIT1_VAL = False
        self.AE_PGNO_BIT2_VAL = False
        self.AE_PGNO_BIT3_VAL = False
        self.AE_PGNO_BIT4_VAL = False
        self.AE_PGNO_BIT5_VAL = False
        self.AE_PGNO_BIT6_VAL = False
        self.AE_PGNO_BIT7_VAL = False
        self.AE_PGNO_PARITY_VAL = False
        self.AE_PGNO_VALID_VAL = False
        self.AE_EXT_START_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.EXT_START
        self.AE_MOVE_ENABLE_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.MOVE_ENABLE and not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.MOVE_DISABLE and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORID == 0 and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORIDSUB == 0 and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID == 0 and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID == 0
        self.AE_CONF_MESS_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.CONF_MESS
        self.AE_DRIVES_OFF_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.DRIVESOFF
        self.AE_DRIVES_ON_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.DRIVESON
        self.BRAKETEST_REQ_EXT_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.BRAKETEST_REQ_EXT
        self.MASTEST_REQ_EXT_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.MASTERINGTEST_REQ_EXT
        self.AE_RESET_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.RESET
        self.BRAKE_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.BRAKE
        self.BRAKE_F_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.BRAKEF
        self.RELEASE_BRAKE_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.RELEASEBRAKE
        self.SHOW_TRACE_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.SHOWTRACE
        self.MESSAGE_RESET_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.MESSAGERESET
        self.OUT_VAL_1_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_1
        self.OUT_VAL_2_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_2
        self.OUT_VAL_3_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_3
        self.OUT_VAL_4_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_4
        self.OUT_VAL_5_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_5
        self.OUT_VAL_6_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_6
        self.OUT_VAL_7_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_7
        self.OUT_VAL_8_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_8
        self.WRITE_OUT_1TO8_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.WRITE_OUT_1TO8
        self.HEARTBEAT_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT)
        self.OVERRIDE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OVERRIDE)
        self.PLC_MAJOR_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].PLC_MAJOR
        self.PLC_MINOR_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].PLC_MINOR
        self.JOG_ADVANCED_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].JOG_ADVANCED.JOG_AD_ACTIVE
        self.ZW_JOG_AD_STATE_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].JOG_ADVANCED.JOG_AD_STATE_VAL
        self.SR_ORDER1_ID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[1].SR_ORDERID
        self.SR_ORDER2_ID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[2].SR_ORDERID
        self.SR_ORDER3_ID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[3].SR_ORDERID
        self.SR_ORDER4_ID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[4].SR_ORDERID
        self.SR_ORDER5_ID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[5].SR_ORDERID
        self.SR_ORDER6_ID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[6].SR_ORDERID
        self.SR_ORDER7_ID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[7].SR_ORDERID
        self.SR_ORDER8_ID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[8].SR_ORDERID
        self.SR_ORDER9_ID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[9].SR_ORDERID
        self.SR_ORDER10_ID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[10].SR_ORDERID
        self.SR_ORDER1_STATE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[1].SR_STATE)
        self.SR_ORDER2_STATE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[2].SR_STATE)
        self.SR_ORDER3_STATE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[3].SR_STATE)
        self.SR_ORDER4_STATE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[4].SR_STATE)
        self.SR_ORDER5_STATE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[5].SR_STATE)
        self.SR_ORDER6_STATE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[6].SR_STATE)
        self.SR_ORDER7_STATE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[7].SR_STATE)
        self.SR_ORDER8_STATE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[8].SR_STATE)
        self.SR_ORDER9_STATE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[9].SR_STATE)
        self.SR_ORDER10_STATE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.STATERETURN[10].SR_STATE)
        self.JOG_AD_STATE = int(self.ZW_JOG_AD_STATE_VAL)
        if self.LASTORDERID != KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID:
            self.LASTORDERID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID
            if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID > 0:
                self.LASTTGNUMBER += 1
                if self.LASTTGNUMBER <= 0 or self.LASTTGNUMBER >= 255:
                    self.LASTTGNUMBER = 1
                self.TRANSMISSIONNO1_VAL = self.LASTTGNUMBER
                if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDSIZE == 1:
                    self.LASTTGTYPE = 1
                elif KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDSIZE == 2:
                    self.LASTTGTYPE = 2
                elif KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDSIZE == 3:
                    self.LASTTGTYPE = 4
                self.TRANSMISSIONTYPE_VAL = self.LASTTGTYPE
                self.ORDERID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID
                self.CMDID_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID)
                self.BUFFERMODE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.BUFFERMODE)

                self.BOOLVALUES1 = MXA_CHBIT2( 0 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 1 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[2] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 2 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[3] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 3 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[4] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 4 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[5] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 5 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[6] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 6 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[7] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 7 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[8] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 8 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[9] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 9 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[10] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 10 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[11] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 11 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[12] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 12 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[13] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 13 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[14] , self.BOOLVALUES1 )
                self.BOOLVALUES1 = MXA_CHBIT2( 14 ,  KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[15] , self.BOOLVALUES1 )
                
                self.CMDPAR_INT1_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1]
                self.CMDPAR_INT2_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2]
                self.CMDPAR_INT3_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3]
                self.CMDPAR_INT4_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[4]
                self.CMDPAR_INT5_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[5]
                self.CMDPAR_INT6_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[6]
                self.CMDPAR_INT7_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[7]
                self.CMDPAR_INT8_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[8]
                self.CMDPAR_INT9_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[9]
                self.CMDPAR_INT10_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[10]
                self.CMDPAR_INT11_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[11]
                self.CMDPAR_INT12_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[12]
                self.CMDPAR_INT13_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[13]
                self.CMDPAR_INT14_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[14]
                self.CMDPAR_INT15_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[15]

                self.CMDPAR_REAL1_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1]
                self.CMDPAR_REAL2_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2]
                self.CMDPAR_REAL3_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3]
                self.CMDPAR_REAL4_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4]
                self.CMDPAR_REAL5_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5]
                self.CMDPAR_REAL6_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6]
                self.CMDPAR_REAL7_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7]
                self.CMDPAR_REAL8_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8]
                self.CMDPAR_REAL9_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9]
                self.CMDPAR_REAL10_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[10]
                self.CMDPAR_REAL11_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[11]
                self.CMDPAR_REAL12_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[12]
                self.CMDPAR_REAL13_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[13]
                self.CMDPAR_REAL14_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[14]
                self.CMDPAR_REAL15_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[15]
                self.NCHECKSUM = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID)
                self.NCHECKSUM ^= int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID)
                self.NCHECKSUM ^= int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.BUFFERMODE)
                for I in range(1, 46):
                    if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[I] == True:
                        self.NCHECKSUM ^= 1
                    self.NCHECKSUM ^= int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[I])



                    FTMP =self.convert_to_float32(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[I])   
                    if FTMP >= 0: 
                        if FTMP - int(FTMP) >= 0.5:
                            NTMP1 = int(FTMP) + 1
                        else:
                            NTMP1 = int(FTMP)
                    else: 
                        if int(FTMP) -FTMP >= 0.5:
                            NTMP1 = int(FTMP) - 1
                        else:
                            NTMP1 = int(FTMP)

                    self.NCHECKSUM ^= NTMP1

                self.CHECKSUM_VAL = self.NCHECKSUM
                self.TRANSMISSIONNO2_VAL = self.LASTTGNUMBER
        if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID > 0:
                if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDSIZE > 1:
                    if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.TRANSMISSIONNORET == self.LASTTGNUMBER and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.TRANSMISSIONNORET == self.TRANSMISSIONNO1_VAL:
                        self.LASTTGNUMBER += 1
                        if self.LASTTGNUMBER <= 0 or self.LASTTGNUMBER >= 255:
                            self.LASTTGNUMBER = 1
                        self.TRANSMISSIONNO1_VAL = self.LASTTGNUMBER
                        if self.LASTTGTYPE == 2:
                            self.LASTTGTYPE = 3
                        elif self.LASTTGTYPE == 4:
                            self.LASTTGTYPE = 5
                        elif self.LASTTGTYPE == 5:
                            self.LASTTGTYPE = 6
                        self.TRANSMISSIONTYPE_VAL = self.LASTTGTYPE
                        if self.LASTTGTYPE == 3 or self.LASTTGTYPE == 5:
                            self.ORDERID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID

                            self.CMDID_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID)
                            self.BUFFERMODE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.BUFFERMODE)
                            
                            self.BOOLVALUES1 = MXA_CHBIT2(0, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[16], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(1, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[17], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(2, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[18], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(3, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[19], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(4, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[20], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(5, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[21], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(6, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[22], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(7, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[23], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(8, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[24], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(9, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[25], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(10, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[26], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(11, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[27], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(12, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[28], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(13, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[29], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(14, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[30], self.BOOLVALUES1)

                            self.CMDPAR_INT1_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[16]
                            self.CMDPAR_INT2_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[17]
                            self.CMDPAR_INT3_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[18]
                            self.CMDPAR_INT4_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[19]
                            self.CMDPAR_INT5_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[20]
                            self.CMDPAR_INT6_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[21]
                            self.CMDPAR_INT7_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[22]
                            self.CMDPAR_INT8_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[23]
                            self.CMDPAR_INT9_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[24]
                            self.CMDPAR_INT10_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[25]
                            self.CMDPAR_INT11_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[26]
                            self.CMDPAR_INT12_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[27]
                            self.CMDPAR_INT13_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[28]
                            self.CMDPAR_INT14_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[29]
                            self.CMDPAR_INT15_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[30]
                            self.CMDPAR_REAL1_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[16]
                            self.CMDPAR_REAL2_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[17]
                            self.CMDPAR_REAL3_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[18]
                            self.CMDPAR_REAL4_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[19]
                            self.CMDPAR_REAL5_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[20]
                            self.CMDPAR_REAL6_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[21]
                            self.CMDPAR_REAL7_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[22]
                            self.CMDPAR_REAL8_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[23]
                            self.CMDPAR_REAL9_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[24]
                            self.CMDPAR_REAL10_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[25]
                            self.CMDPAR_REAL11_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[26]
                            self.CMDPAR_REAL12_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[27]
                            self.CMDPAR_REAL13_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[28]
                            self.CMDPAR_REAL14_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[29]
                            self.CMDPAR_REAL15_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[30]

 

                        elif (self.LASTTGTYPE == 6):
                            self.ORDERID_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID
                            self.CMDID_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.COMMANDID)
                            self.BUFFERMODE_VAL = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.BUFFERMODE)
                            
                            self.BOOLVALUES1 = MXA_CHBIT2(0, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[31], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(1, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[32], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(2, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[33], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(3, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[34], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(4, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[35], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(5, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[36], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(6, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[37], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(7, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[38], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(8, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[39], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(9, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[40], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(10, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[41], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(11, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[42], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(12, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[43], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(13, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[44], self.BOOLVALUES1)
                            self.BOOLVALUES1 = MXA_CHBIT2(14, KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[45], self.BOOLVALUES1)


                            self.CMDPAR_INT1_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[31]
                            self.CMDPAR_INT2_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[32]
                            self.CMDPAR_INT3_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[33]
                            self.CMDPAR_INT4_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[34]
                            self.CMDPAR_INT5_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[35]
                            self.CMDPAR_INT6_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[36]
                            self.CMDPAR_INT7_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[37]
                            self.CMDPAR_INT8_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[38]
                            self.CMDPAR_INT9_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[39]
                            self.CMDPAR_INT10_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[40]
                            self.CMDPAR_INT11_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[41]
                            self.CMDPAR_INT12_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[42]
                            self.CMDPAR_INT13_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[43]
                            self.CMDPAR_INT14_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[44]
                            self.CMDPAR_INT15_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[45]

                            self.CMDPAR_REAL1_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[31]
                            self.CMDPAR_REAL2_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[32]
                            self.CMDPAR_REAL3_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[33]
                            self.CMDPAR_REAL4_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[34]
                            self.CMDPAR_REAL5_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[35]
                            self.CMDPAR_REAL6_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[36]
                            self.CMDPAR_REAL7_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[37]
                            self.CMDPAR_REAL8_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[38]
                            self.CMDPAR_REAL9_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[39]
                            self.CMDPAR_REAL10_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[40]
                            self.CMDPAR_REAL11_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[41]
                            self.CMDPAR_REAL12_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[42]
                            self.CMDPAR_REAL13_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[43]
                            self.CMDPAR_REAL14_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[44]
                            self.CMDPAR_REAL15_VAL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[45]

                        self.TRANSMISSIONNO2_VAL = self.LASTTGNUMBER




        else:
            self.TRANSMISSIONNO1_VAL = 0
            self.TRANSMISSIONTYPE_VAL = 0
            self.ORDERID_VAL = 0
            self.CMDID_VAL = 0
            self.BUFFERMODE_VAL = 0
            self.CHECKSUM_VAL = 0
            self.BOOLVALUES1 = 0
            for i in range(1, 16):
                globals()[f'self.CMDPAR_INT{i}_VAL'] = 0
            for i in range(1, 16):
                globals()[f'self.CMDPAR_REAL{i}_VAL'] = 0.0
            self.TRANSMISSIONNO2_VAL = 0
        
        MXA_CHBIT ( 0 , 0 , self.AE_PGNO_FBIT_VAL )
        MXA_CHBIT ( 0 , 1 , self.AE_PGNO_BIT1_VAL )
        MXA_CHBIT ( 0 , 2 , self.AE_PGNO_BIT2_VAL )
        MXA_CHBIT ( 0 , 3 , self.AE_PGNO_BIT3_VAL )
        MXA_CHBIT ( 0 , 4 , self.AE_PGNO_BIT4_VAL )
        MXA_CHBIT ( 0 , 5 , self.AE_PGNO_BIT5_VAL )
        MXA_CHBIT ( 0 , 6 , self.AE_PGNO_BIT6_VAL )
        MXA_CHBIT ( 0 , 7 , self.AE_PGNO_BIT7_VAL )
        MXA_CHBIT ( 1 , 0 , self.AE_PGNO_PARITY_VAL )
        MXA_CHBIT ( 1 , 1 , self.AE_PGNO_VALID_VAL )
        MXA_CHBIT ( 1 , 2 , self.AE_EXT_START_VAL )
        MXA_CHBIT ( 1 , 3 , self.AE_MOVE_ENABLE_VAL )
        MXA_CHBIT ( 1 , 4 , self.AE_CONF_MESS_VAL )
        MXA_CHBIT ( 1 , 5 , self.AE_DRIVES_OFF_VAL )
        MXA_CHBIT ( 1 , 6 , self.AE_DRIVES_ON_VAL )
        MXA_CHBIT ( 1 , 7 , self.MASTEST_REQ_EXT_VAL )
        MXA_CHBIT ( 2 , 0 , self.BRAKETEST_REQ_EXT_VAL )
        MXA_CHBIT ( 4 , 0 , self.AE_RESET_VAL )
        MXA_CHBIT ( 4 , 1 , self.BRAKE_VAL )
        MXA_CHBIT ( 4 , 2 , self.BRAKE_F_VAL )
        MXA_CHBIT ( 4 , 3 , self.RELEASE_BRAKE_VAL )
        MXA_CHBIT ( 4 , 4 , self.SHOW_TRACE_VAL )
        MXA_CHBIT ( 4 , 5 , self.MESSAGE_RESET_VAL )
        MXA_CHBIT ( 4 , 7 , self.WRITE_OUT_1TO8_VAL )
        MXA_CHBIT ( 5 , 0 , self.OUT_VAL_1_VAL )
        MXA_CHBIT ( 5 , 1 , self.OUT_VAL_2_VAL )
        MXA_CHBIT ( 5 , 2 , self.OUT_VAL_3_VAL )
        MXA_CHBIT ( 5 , 3 , self.OUT_VAL_4_VAL )
        MXA_CHBIT ( 5 , 4 , self.OUT_VAL_5_VAL )
        MXA_CHBIT ( 5 , 5 , self.OUT_VAL_6_VAL )
        MXA_CHBIT ( 5 , 6 , self.OUT_VAL_7_VAL )
        MXA_CHBIT ( 5 , 7 , self.OUT_VAL_8_VAL )
        MXA_CHBIT ( 2 , 7 , self.JOG_ADVANCED_VAL )

        MXA_WRITEIO_BYTE ( 8 , self.HEARTBEAT_VAL )
        MXA_WRITEIO_BYTE ( 9 , self.OVERRIDE_VAL )
        MXA_WRITEIO_BYTE ( 10 , self.PLC_MAJOR_VAL )
        MXA_WRITEIO_BYTE ( 11 , self.PLC_MINOR_VAL )
        MXA_WRITEIO_DINT ( 12 , self.SR_ORDER1_ID_VAL )
        MXA_WRITEIO_DINT ( 16 , self.SR_ORDER2_ID_VAL )
        MXA_WRITEIO_DINT ( 20 , self.SR_ORDER3_ID_VAL )
        MXA_WRITEIO_DINT ( 24 , self.SR_ORDER4_ID_VAL )
        MXA_WRITEIO_DINT ( 28 , self.SR_ORDER5_ID_VAL )
        MXA_WRITEIO_DINT ( 32 , self.SR_ORDER6_ID_VAL )
        MXA_WRITEIO_DINT ( 36 , self.SR_ORDER7_ID_VAL )
        MXA_WRITEIO_DINT ( 40 , self.SR_ORDER8_ID_VAL )
        MXA_WRITEIO_DINT ( 44 , self.SR_ORDER9_ID_VAL )
        MXA_WRITEIO_DINT ( 48 , self.SR_ORDER10_ID_VAL )
        MXA_WRITEIO_BYTE ( 52 , self.SR_ORDER1_STATE_VAL )
        MXA_WRITEIO_BYTE ( 53 , self.SR_ORDER2_STATE_VAL )
        MXA_WRITEIO_BYTE ( 54 , self.SR_ORDER3_STATE_VAL )
        MXA_WRITEIO_BYTE ( 55 , self.SR_ORDER4_STATE_VAL )
        MXA_WRITEIO_BYTE ( 56 , self.SR_ORDER5_STATE_VAL )
        MXA_WRITEIO_BYTE ( 57 , self.SR_ORDER6_STATE_VAL )
        MXA_WRITEIO_BYTE ( 58 , self.SR_ORDER7_STATE_VAL )
        MXA_WRITEIO_BYTE ( 59 , self.SR_ORDER8_STATE_VAL )
        MXA_WRITEIO_BYTE ( 60 , self.SR_ORDER9_STATE_VAL )
        MXA_WRITEIO_BYTE ( 61 , self.SR_ORDER10_STATE_VAL )
        MXA_WRITEIO_BYTE ( 62 , self.TRANSMISSIONNO1_VAL )
        MXA_WRITEIO_BYTE ( 63 , self.TRANSMISSIONTYPE_VAL )
        MXA_WRITEIO_DINT ( 64 , self.ORDERID_VAL )
        MXA_WRITEIO_BYTE ( 68 , self.CMDID_VAL )
        MXA_WRITEIO_BYTE ( 69 , self.BUFFERMODE_VAL )
        MXA_WRITEIO_DWORD ( 70 , self.CHECKSUM_VAL )
        MXA_WRITEIO_WORD ( 74 , self.BOOLVALUES1 )
        MXA_WRITEIO_DINT ( 76 , self.CMDPAR_INT1_VAL )
        MXA_WRITEIO_DINT ( 80 , self.CMDPAR_INT2_VAL )
        MXA_WRITEIO_DINT ( 84 , self.CMDPAR_INT3_VAL )
        MXA_WRITEIO_DINT ( 88 , self.CMDPAR_INT4_VAL )
        MXA_WRITEIO_DINT ( 92 , self.CMDPAR_INT5_VAL )
        MXA_WRITEIO_DINT ( 96 , self.CMDPAR_INT6_VAL )
        MXA_WRITEIO_DINT ( 100 , self.CMDPAR_INT7_VAL )
        MXA_WRITEIO_DINT ( 104 , self.CMDPAR_INT8_VAL )
        MXA_WRITEIO_DINT ( 108 , self.CMDPAR_INT9_VAL )
        MXA_WRITEIO_DINT ( 112 , self.CMDPAR_INT10_VAL )
        MXA_WRITEIO_DINT ( 116 , self.CMDPAR_INT11_VAL )
        MXA_WRITEIO_DINT ( 120 , self.CMDPAR_INT12_VAL )
        MXA_WRITEIO_DINT ( 124 , self.CMDPAR_INT13_VAL )
        MXA_WRITEIO_DINT ( 128 , self.CMDPAR_INT14_VAL )
        MXA_WRITEIO_DINT ( 132 , self.CMDPAR_INT15_VAL )
        MXA_WRITEIO_REAL ( 136 , self.CMDPAR_REAL1_VAL )
        MXA_WRITEIO_REAL ( 140 , self.CMDPAR_REAL2_VAL )
        MXA_WRITEIO_REAL ( 144 , self.CMDPAR_REAL3_VAL )
        MXA_WRITEIO_REAL ( 148 , self.CMDPAR_REAL4_VAL )
        MXA_WRITEIO_REAL ( 152 , self.CMDPAR_REAL5_VAL )
        MXA_WRITEIO_REAL ( 156 , self.CMDPAR_REAL6_VAL )
        MXA_WRITEIO_REAL ( 160 , self.CMDPAR_REAL7_VAL )
        MXA_WRITEIO_REAL ( 164 , self.CMDPAR_REAL8_VAL )
        MXA_WRITEIO_REAL ( 168 , self.CMDPAR_REAL9_VAL )
        MXA_WRITEIO_REAL ( 172 , self.CMDPAR_REAL10_VAL )
        MXA_WRITEIO_REAL ( 176 , self.CMDPAR_REAL11_VAL )
        MXA_WRITEIO_REAL ( 180 , self.CMDPAR_REAL12_VAL )
        MXA_WRITEIO_REAL ( 184 , self.CMDPAR_REAL13_VAL )
        MXA_WRITEIO_REAL ( 188 , self.CMDPAR_REAL14_VAL )
        MXA_WRITEIO_REAL ( 192 , self.CMDPAR_REAL15_VAL )
        MXA_WRITEIO_BYTE ( 196 , self.TRANSMISSIONNO2_VAL )
        MXA_WRITEIO_BYTE ( 3 , self.JOG_AD_STATE )


        
#/******************************************************************************
# * FUNCTION_BLOCK KRC_READACTUALVELOCITY
# ******************************************************************************/

class KRC_READACTUALVELOCITY:
    """
    The function block KRC_ReadActualVelocity reads the current actual velocity at the TCP of the robot. This is updated cyclically. The current path velocity can only be read for CP motions in program mode.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5

    Returns:
    Valid (BOOL): TRUE = data are valid
    Value (REAL): Current path velocity ($VEL_ACT on the robot controller), unit: m/s
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self._VALID = False
        self._VALUE = 0

    @property
    def VALID(self):
        return self._VALID

    @property
    def VALUE(self):
        return self._VALUE

    def OnCycle(self):
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._VALID = False
            return
        self._VALUE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.VELACT
        self._VALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE



#/******************************************************************************
# * FUNCTION_BLOCK KRC_READACTUALAXISVELOCITY
# ******************************************************************************/

class KRC_READACTUALAXISVELOCITY:
    """
    The function block KRC_ReadActualAxisVelocity reads the current axis-specific velocity of the robot. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal

    Returns:
    Done (BOOL): TRUE = statement has been executed
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    A1 ... A6 (INT): Current motor speed (-100% … +100%) of A1 … A6, relative to the maximum motor speed ($VEL_AXIS_MA on the robot controller). Note: The actual resulting speed of the robot axis ($VEL_AXIS_ACT on the robot controller) is dependent on the gear ratio.
    E1 ... E6 (INT): Current motor speed (-100% … +100%) of E1 … E6, relative to the maximum motor speed ($VEL_AXIS_MA on the robot controller). Note: The actual resulting speed of the external axis is dependent on the gear ratio.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self._DONE = False
        self._ERROR = False
        self._ERRORID = 0
        self._A1 = 0
        self._A2 = 0
        self._A3 = 0
        self._A4 = 0
        self._A5 = 0
        self._A6 = 0
        self._E1 = 0
        self._E2 = 0
        self._E3 = 0
        self._E4 = 0
        self._E5 = 0
        self._E6 = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def A1(self):
        return self._A1

    @property
    def A2(self):
        return self._A2

    @property
    def A3(self):
        return self._A3

    @property
    def A4(self):
        return self._A4

    @property
    def A5(self):
        return self._A5

    @property
    def A6(self):
        return self._A6

    @property
    def E1(self):
        return self._E1

    @property
    def E2(self):
        return self._E2

    @property
    def E3(self):
        return self._E3

    @property
    def E4(self):
        return self._E4

    @property
    def E5(self):
        return self._E5

    @property
    def E6(self):
        return self._E6

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 25
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._A1 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
            self._A2 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2])
            self._A3 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3])
            self._A4 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4])
            self._A5 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5])
            self._A6 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6])
            self._E1 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7])
            self._E2 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8])
            self._E3 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9])
            self._E4 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10])
            self._E5 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11])
            self._E6 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12])
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




#/******************************************************************************
# * FUNCTION_BLOCK KRC_READACTUALACCELERATION
# ******************************************************************************/


class KRC_READACTUALACCELERATION:
    """
    The function block KRC_ReadActualAcceleration reads the current Cartesian acceleration at the TCP of the robot. The current Cartesian acceleration about angles A, B, C is not evaluated. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal

    Returns:
    Done (BOOL): TRUE = statement has been executed
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    ACC_ABS (REAL): Current Cartesian acceleration relative to the absolute value of the overall acceleration ($ACC_CAR_ACT on the robot controller), unit: m/s2
    X, Y, Z (REAL): Current Cartesian acceleration in the X, Y, Z directions, unit: m/s2
    A, B, C (REAL): Current Cartesian acceleration about angles A, B, C, 0 m/s2 (not calculated)
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self._DONE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ACC_ABS = 0.0
        self._X = 0.0
        self._Y = 0.0
        self._Z = 0.0
        self._A = 0.0
        self._B = 0.0
        self._C = 0.0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ACC_ABS(self):
        return self._ACC_ABS

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @property
    def Z(self):
        return self._Z

    @property
    def A(self):
        return self._A

    @property
    def B(self):
        return self._B

    @property
    def C(self):
        return self._C

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 26
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._ACC_ABS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self._X = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self._Y = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self._Z = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self._A = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self._B = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self._C = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7]
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




#/******************************************************************************
# * FUNCTION_BLOCK KRC_READDIGITALINPUT
# ******************************************************************************/

class KRC_READDIGITALINPUT:
    """
    The function block KRC_ReadDigitalInput polls and reads a digital input of the robot controller. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    Number (INT): Number of the digital input (corresponds to $IN[1 … 2048] on the robot controller), can be 1 to 2048

    Returns:
    Done (BOOL): TRUE = statement has been executed
    Value (BOOL): Value of the digital input
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.NUMBER = 0
        self._DONE = False
        self._VALUE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def VALUE(self):
        return self._VALUE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 8
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.NUMBER)
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._VALUE = bool(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



#/******************************************************************************
# * FUNCTION_BLOCK KRC_READDIGITALINPUT1TO8
# ******************************************************************************/

class KRC_READDIGITALINPUT1TO8:
    """
    The function block KRC_ReadDigitalInput1To8 polls and reads the digital inputs 1 to 8 of the robot controller.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5

    Returns:
    Valid (BOOL): TRUE = data are valid
    IN1 ... IN8 (BOOL): Actual value of the digital input $IN[1] … $IN[8]
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self._VALID = False
        self._IN1 = False
        self._IN2 = False
        self._IN3 = False
        self._IN4 = False
        self._IN5 = False
        self._IN6 = False
        self._IN7 = False
        self._IN8 = False
        self._ERROR = False
        self._ERRORID = 0

    @property
    def VALID(self):
        return self._VALID

    @property
    def IN1(self):
        return self._IN1

    @property
    def IN2(self):
        return self._IN2

    @property
    def IN3(self):
        return self._IN3

    @property
    def IN4(self):
        return self._IN4

    @property
    def IN5(self):
        return self._IN5

    @property
    def IN6(self):
        return self._IN6

    @property
    def IN7(self):
        return self._IN7

    @property
    def IN8(self):
        return self._IN8

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    def OnCycle(self):
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False
        self._VALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED
        self._IN1 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IN_VAL_1TO8, 0)
        self._IN2 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IN_VAL_1TO8, 1)
        self._IN3 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IN_VAL_1TO8, 2)
        self._IN4 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IN_VAL_1TO8, 3)
        self._IN5 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IN_VAL_1TO8, 4)
        self._IN6 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IN_VAL_1TO8, 5)
        self._IN7 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IN_VAL_1TO8, 6)
        self._IN8 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IN_VAL_1TO8, 7)


#/******************************************************************************
# * FUNCTION_BLOCK KRC_READDIGITALINPUTARRAY
# ******************************************************************************/


class KRC_READDIGITALINPUTARRAY:
    """
    The function block KRC_ReadDigitalInputArray polls and reads multiple digital inputs of the robot controller. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    Startnumber (INT): Number of the 1st digital input polled (corresponds to $IN[1 … 2048] on the robot controller), can be 1 to 2048
    Length (INT): Number of inputs that are polled, can be 1 to 200. Note: If the number of inputs to be read exceeds the 1 … 2048 range, no error message is generated. Inputs outside of this range are not read.

    Returns:
    Done (BOOL): TRUE = statement has been executed
    Values (BOOL[200]): Values of the digital inputs
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.DW1 = 0
        self.DW2 = 0
        self.DW3 = 0
        self.DW4 = 0
        self.DW5 = 0
        self.DW6 = 0
        self.DW7 = 0
        self.DW8 = 0
        self.DW9 = 0
        self.DW10 = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.STARTNUMBER = 0
        self.LENGTH = 0
        self._DONE = False
        self._VALUES = [False]*201
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

    @property
    def DONE(self):
        return self._DONE

    @property
    def VALUES(self):
        return self._VALUES

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 38
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.STARTNUMBER)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = int(self.LENGTH)
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self.DW1 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
            self.DW2 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2])
            self.DW3 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3])
            self.DW4 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4])
            self.DW5 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5])
            self.DW6 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6])
            self.DW7 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7])
            self.DW8 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8])
            self.DW9 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9])
            self.DW10 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10])

            for i in range(0, 20):
                self._VALUES[i] = bool(self.DW1 & (1 << i))
            for i in range(20, 40):
                self._VALUES[i] = bool(self.DW2 & (1 << (i - 20)))
            for i in range(40, 60):
                self._VALUES[i] = bool(self.DW3 & (1 << (i - 40)))
            for i in range(60, 80):
                self._VALUES[i] = bool(self.DW4 & (1 << (i - 60)))
            for i in range(80, 100):
                self._VALUES[i] = bool(self.DW5 & (1 << (i - 80)))
            for i in range(100, 120):
                self._VALUES[i] = bool(self.DW6 & (1 << (i - 100)))
            for i in range(120, 140):
                self._VALUES[i] = bool(self.DW7 & (1 << (i - 120)))
            for i in range(140, 160):
                self._VALUES[i] = bool(self.DW8 & (1 << (i - 140)))
            for i in range(160, 180):
                self._VALUES[i] = bool(self.DW9 & (1 << (i - 160)))
            for i in range(180, 200):
                self._VALUES[i] = bool(self.DW10 & (1 << (i - 180)))
     

        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



#/******************************************************************************
# * FUNCTION_BLOCK KRC_READDIGITALOUTPUT
# ******************************************************************************/

class KRC_READDIGITALOUTPUT:
    """
    The function block KRC_ReadDigitalOutput polls and reads a digital output of the robot controller. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    Number (INT): Number of the digital output (corresponds to $OUT[1 … 2048] on the robot controller), can be 1 to 2048

    Returns:
    Done (BOOL): TRUE = statement has been executed
    Value (BOOL): Value of the digital output
    Error (BOOL): TRUE = error in function block
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.NUMBER = 0
        self._DONE = False
        self._VALUE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def VALUE(self):
        return self._VALUE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 9
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.NUMBER)
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._VALUE = bool(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



#/******************************************************************************
# * FUNCTION_BLOCK KRC_WRITEDIGITALOUTPUT1TO8
# ******************************************************************************/

class KRC_WRITEDIGITALOUTPUT1TO8:
    """
    The function block KRC_WriteDigitalOutput1To8 writes the digital outputs 1 to 8 on the robot controller. The outputs are written cyclically.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    OUT1 ... OUT8 (BOOL): Setpoint value of the output $OUT[1] … $OUT[8]

    Returns:
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.OUT1 = False
        self.OUT2 = False
        self.OUT3 = False
        self.OUT4 = False
        self.OUT5 = False
        self.OUT6 = False
        self.OUT7 = False
        self.OUT8 = False
        self._ERROR = False
        self._ERRORID = 0

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    def OnCycle(self):
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_1 = self.OUT1
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_2 = self.OUT2
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_3 = self.OUT3
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_4 = self.OUT4
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_5 = self.OUT5
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_6 = self.OUT6
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_7 = self.OUT7
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OUT_VAL_8 = self.OUT8
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.WRITE_OUT_1TO8 = True



#/******************************************************************************
# * FUNCTION_BLOCK KRC_READANALOGINPUT
# ******************************************************************************/

class KRC_READANALOGINPUT:
    """
    The function block KRC_ReadAnalogInput polls and reads an analog input of the robot controller. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    Number (INT): Number of the analog input (corresponds to $ANIN[1 … 32] on the robot controller), can be 1 to 32

    Returns:
    Done (BOOL): TRUE = statement has been executed
    Value (REAL): Value of the analog input
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.NUMBER = 0
        self._DONE = False
        self._VALUE = 0.0
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def VALUE(self):
        return self._VALUE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 11
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.NUMBER)
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._VALUE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



#/******************************************************************************
# * FUNCTION_BLOCK KRC_READANALOGOUTPUT
# ******************************************************************************/

class KRC_READANALOGOUTPUT:
    """
    The function block KRC_ReadAnalogOutput polls and reads an analog output of the robot controller. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    Number (INT): Number of the analog output (corresponds to $ANOUT[1 … 32] on the robot controller), can be 1 to 32

    Returns:
    Done (BOOL): TRUE = statement has been executed
    Value (REAL): Value of the analog output
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.NUMBER = 0
        self._DONE = False
        self._VALUE = 0.0
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def VALUE(self):
        return self._VALUE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 12
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.NUMBER)
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._VALUE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



#/******************************************************************************
# * FUNCTION_BLOCK KRC_WRITEANALOGOUTPUT
# ******************************************************************************/


class KRC_WRITEANALOGOUTPUT:
    """
    The function block KRC_WriteAnalogOutput polls and writes an analog output of the robot controller. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    Number (INT): Number of the analog output (corresponds to $ANOUT[1 … 32] on the robot controller), can be 1 to 32
    Value (REAL): Value of the analog output
    bContinue (BOOL): TRUE = output written in advance run. Note: The robot controller executes programs with an advance run and a main run.
    BufferMode (INT): Mode in which the statement is executed, can be 0 (DIRECT), 1 (ABORTING), or 2 (BUFFERED)

    Returns:
    Busy (BOOL): TRUE = statement is currently being transferred or has already been transferred
    Done (BOOL): TRUE = statement has been executed
    Aborted (BOOL): TRUE = statement has been aborted
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.NUMBER = 0
        self.VALUE = 0.0
        self.BCONTINUE = False
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 13
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.BCONTINUE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.NUMBER)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = float(self.VALUE)
        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


#/******************************************************************************
# * FUNCTION_BLOCK KRC_SETCOORDSYS
# ******************************************************************************/

class KRC_SETCOORDSYS:
    """
    The function block KRC_SetCoordSys can be used to set the tool, base and interpolation mode without having to execute a motion at the same time. This function is required, for example, to read the current position in different coordinate systems. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    CoordinateSystem (COORDSYS): Coordinate system to which the specified values refer
    BufferMode (INT): Mode in which the statement is executed, can be 1 (ABORTING), or 2 (BUFFERED)

    Returns:
    Busy (BOOL): TRUE = statement is currently being transferred or has already been transferred
    Done (BOOL): TRUE = statement has been executed
    Aborted (BOOL): TRUE = statement has been aborted
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.COORDINATESYSTEM = COORDSYS()
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 33
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = int(self.COORDINATESYSTEM.TOOL)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[4] = int(self.COORDINATESYSTEM.BASE)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[5] = int(self.COORDINATESYSTEM.IPO_MODE)
        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READTOOLDATA
#  ******************************************************************************/

class KRC_READTOOLDATA:
    """
    The function block KRC_ReadToolData reads the TOOL data of the robot. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    ToolNo (INT): Number of the TOOL coordinate system, can be 1 to 16

    Returns:
    Done (BOOL): TRUE = statement has been executed
    ToolData (FRAME): The data structure FRAME contains the following TOOL data: X, Y, Z: Origin of the TOOL coordinate system relative to the FLANGE coordinate system; A, B, C: Orientation of the TOOL coordinate system relative to the FLANGE coordinate system
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.TOOLNO = 0
        self._DONE = False
        self._TOOLDATA = FRAME()
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def TOOLDATA(self):
        return self._TOOLDATA

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 20
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.TOOLNO)
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._TOOLDATA.X = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self._TOOLDATA.Y = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self._TOOLDATA.Z = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self._TOOLDATA.A = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self._TOOLDATA.B = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self._TOOLDATA.C = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_WRITETOOLDATA
#  ******************************************************************************/

class KRC_WRITETOOLDATA:
    """
    The function block KRC_WriteToolData writes the TOOL data of the robot. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    ToolData (FRAME): The data structure FRAME contains the following TOOL data: X, Y, Z: Origin of the TOOL coordinate system relative to the FLANGE coordinate system; A, B, C: Orientation of the TOOL coordinate system relative to the FLANGE coordinate system
    ToolNo (INT): Number of the TOOL coordinate system, can be 1 to 16
    BufferMode (INT): Mode in which the statement is executed, can be 0 (DIRECT), 1 (ABORTING), or 2 (BUFFERED)

    Returns:
    Busy (BOOL): TRUE = statement is currently being transferred or has already been transferred
    Done (BOOL): TRUE = statement has been executed
    Aborted (BOOL): TRUE = statement has been aborted
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.TOOLDATA = FRAME()  
        self.TOOLNO = 0
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 21
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()  
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.TOOLNO)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.TOOLDATA.X
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.TOOLDATA.Y
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.TOOLDATA.Z
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.TOOLDATA.A
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.TOOLDATA.B
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.TOOLDATA.C
        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READBASEDATA
# ******************************************************************************/
            
class KRC_READBASEDATA:
    """
    The function block KRC_ReadBaseData reads the BASE data of the robot. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    BaseNo (INT): Number of the BASE coordinate system, can be 1 to 32

    Returns:
    Done (BOOL): TRUE = statement has been executed
    BaseData (FRAME): The data structure FRAME contains the following BASE data: X, Y, Z: Origin of the BASE coordinate system relative to the WORLD coordinate system; A, B, C: Orientation of the BASE coordinate system relative to the WORLD coordinate system
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.BASENO = 0
        self._DONE = False
        self._BASEDATA = FRAME()  
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def DONE(self):
        return self._DONE

    @property
    def BASEDATA(self):
        return self._BASEDATA

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 22
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()  
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:  
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.BASENO)
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:  
            self._BASEDATA.X = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self._BASEDATA.Y = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self._BASEDATA.Z = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self._BASEDATA.A = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self._BASEDATA.B = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self._BASEDATA.C = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID





#/******************************************************************************
# * FUNCTION_BLOCK KRC_WRITEBASEDATA
# ******************************************************************************/
            

class KRC_WRITEBASEDATA:
    """
    The function block KRC_WriteBaseData writes the BASE data of the robot. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    BaseNo (INT): Number of the BASE coordinate system, can be 1 to 32
    BaseData (FRAME): The data structure FRAME contains the following BASE data: X, Y, Z: Origin of the BASE coordinate system relative to the WORLD coordinate system; A, B, C: Orientation of the BASE coordinate system relative to the WORLD coordinate system
    BufferMode (INT): Mode in which the statement is executed, can be 0 (DIRECT), 1 (ABORTING), or 2 (BUFFERED)

    Returns:
    Busy (BOOL): TRUE = statement is currently being transferred or has already been transferred
    Done (BOOL): TRUE = statement has been executed
    Aborted (BOOL): TRUE = statement has been aborted
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.BASENO = 0
        self.BASEDATA = FRAME()  
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 23
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()  
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:  
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.BASENO)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.BASEDATA.X
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.BASEDATA.Y
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.BASEDATA.Z
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.BASEDATA.A
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.BASEDATA.B
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.BASEDATA.C
        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READLOADDATA
#  ******************************************************************************/


class KRC_READLOADDATA:
    """
    The function block KRC_ReadLoadData reads the load data of the robot (payload data or supplementary load data). Each tool of the robot controller has its own tool load data. The supplementary load data are valid for the entire robot. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    Tool (INT): Number of the TOOL coordinate system for reading the payload data or number for reading the supplementary load data, can be 1 to 16 for TOOL_DATA[1 … 16], or -1, -2, -3 for Supplementary load A1, A2, A3 respectively

    Returns:
    Done (BOOL): TRUE = statement has been executed
    M (REAL): Mass
    X, Y, Z (REAL): Position of the center of gravity relative to the flange
    A, B, C (REAL): Orientation of the principal inertia axes relative to the flange
    JX, JY, JZ (REAL): Mass moments of inertia
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.TOOL = 0
        self._DONE = False
        self._M = 0.0
        self._X = 0.0
        self._Y = 0.0
        self._Z = 0.0
        self._A = 0.0
        self._B = 0.0
        self._C = 0.0
        self._JX = 0.0
        self._JY = 0.0
        self._JZ = 0.0
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def DONE(self):
        return self._DONE

    @property
    def M(self):
        return self._M

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @property
    def Z(self):
        return self._Z

    @property
    def A(self):
        return self._A

    @property
    def B(self):
        return self._B

    @property
    def C(self):
        return self._C

    @property
    def JX(self):
        return self._JX

    @property
    def JY(self):
        return self._JY

    @property
    def JZ(self):
        return self._JZ

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 14
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()  
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:  
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.TOOL)
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:  
            self._M = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self._X = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self._Y = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self._Z = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self._A = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self._B = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self._C = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7]
            self._JX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8]
            self._JY = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self._JZ = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10]
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_WRITELOADDATA
#  ******************************************************************************/

class KRC_WRITELOADDATA:
    """
    The function block KRC_WriteLoadData writes the load data of the robot (payload data or supplementary load data). The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal
    Tool (INT): Number of the TOOL coordinate system for writing the payload data or number for writing the supplementary load data, can be 1 to 16 for TOOL_DATA[1 … 16], or -1, -2, -3 for Supplementary load A1, A2, A3 respectively
    M (REAL): Mass
    X, Y, Z (REAL): Position of the center of gravity relative to the flange
    A, B, C (REAL): Orientation of the principal inertia axes relative to the flange
    JX, JY, JZ (REAL): Mass moments of inertia
    BufferMode (INT): Mode in which the statement is executed, can be 0 (DIRECT), 1 (ABORTING), or 2 (BUFFERED)

    Returns:
    Busy (BOOL): TRUE = statement is currently being transferred or has already been transferred
    Done (BOOL): TRUE = statement has been executed
    Aborted (BOOL): TRUE = statement has been aborted
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.TOOL = 0
        self.M = 0.0
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.A = 0.0
        self.B = 0.0
        self.C = 0.0
        self.JX = 0.0
        self.JY = 0.0
        self.JZ = 0.0
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 15
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.TOOL)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.M
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.X
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.Y
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.Z
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.A
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.B
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = self.C
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = self.JX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = self.JY
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[10] = self.JZ
        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READSOFTEND
#  ******************************************************************************/

class KRC_READSOFTEND:
    """
    The function block KRC_ReadSoftEnd reads the software limit switches of the robot axes. The statement is executed in the case of a rising edge of the signal.

    Parameters:
    AxisGroupIdx (INT): Index of axis group, can be 1 to 5
    ExecuteCmd (BOOL): The statement is executed in the case of a rising edge of the signal

    Returns:
    Done (BOOL): TRUE = statement has been executed
    A1_Min ... A6_Min (REAL): Negative software limit switch of axis A1 … A6, unit: mm or °
    A1_Max ... A6_Max (REAL): Positive software limit switch of axis A1 … A6, unit: mm or °
    Error (BOOL): TRUE = error in function block
    ErrorID (DINT): Error number
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self._DONE = False
        self._A1_MIN = 0.0
        self._A1_MAX = 0.0
        self._A2_MIN = 0.0
        self._A2_MAX = 0.0
        self._A3_MIN = 0.0
        self._A3_MAX = 0.0
        self._A4_MIN = 0.0
        self._A4_MAX = 0.0
        self._A5_MIN = 0.0
        self._A5_MAX = 0.0
        self._A6_MIN = 0.0
        self._A6_MAX = 0.0
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def A1_MIN(self):
        return self._A1_MIN

    @property
    def A1_MAX(self):
        return self._A1_MAX

    @property
    def A2_MIN(self):
        return self._A2_MIN

    @property
    def A2_MAX(self):
        return self._A2_MAX

    @property
    def A3_MIN(self):
        return self._A3_MIN

    @property
    def A3_MAX(self):
        return self._A3_MAX

    @property
    def A4_MIN(self):
        return self._A4_MIN

    @property
    def A4_MAX(self):
        return self._A4_MAX

    @property
    def A5_MIN(self):
        return self._A5_MIN

    @property
    def A5_MAX(self):
        return self._A5_MAX

    @property
    def A6_MIN(self):
        return self._A6_MIN

    @property
    def A6_MAX(self):
        return self._A6_MAX

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 16
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._A1_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self._A1_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self._A2_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self._A2_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self._A3_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self._A3_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self._A4_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7]
            self._A4_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8]
            self._A5_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self._A5_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10]
            self._A6_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11]
            self._A6_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12]
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READSOFTENDEXT
#  ******************************************************************************/

class KRC_READSOFTENDEXT:
    """
    Reads the software limit switches of the external axes.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.

    Returns:
    Done (bool): TRUE if the statement has been executed.
    E1_Min to E6_Min (List[float]): Negative software limit switch of axis E1 to E6. Unit: mm or °.
    E1_Max to E6_Max (List[float]): Positive software limit switch of axis E1 to E6. Unit: mm or °.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self._DONE = False
        self._E1_MIN = 0.0
        self._E1_MAX = 0.0
        self._E2_MIN = 0.0
        self._E2_MAX = 0.0
        self._E3_MIN = 0.0
        self._E3_MAX = 0.0
        self._E4_MIN = 0.0
        self._E4_MAX = 0.0
        self._E5_MIN = 0.0
        self._E5_MAX = 0.0
        self._E6_MIN = 0.0
        self._E6_MAX = 0.0
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def E1_MIN(self):
        return self._E1_MIN

    @property
    def E1_MAX(self):
        return self._E1_MAX

    @property
    def E2_MIN(self):
        return self._E2_MIN

    @property
    def E2_MAX(self):
        return self._E2_MAX

    @property
    def E3_MIN(self):
        return self._E3_MIN

    @property
    def E3_MAX(self):
        return self._E3_MAX

    @property
    def E4_MIN(self):
        return self._E4_MIN

    @property
    def E4_MAX(self):
        return self._E4_MAX

    @property
    def E5_MIN(self):
        return self._E5_MIN

    @property
    def E5_MAX(self):
        return self._E5_MAX

    @property
    def E6_MIN(self):
        return self._E6_MIN

    @property
    def E6_MAX(self):
        return self._E6_MAX

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 18
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._E1_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self._E1_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self._E2_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self._E2_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self._E3_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self._E3_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self._E4_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7]
            self._E4_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8]
            self._E5_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self._E5_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10]
            self._E6_MIN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11]
            self._E6_MAX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12]
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID





# /******************************************************************************
#  * FUNCTION_BLOCK KRC_WRITESOFTENDEXT
#  ******************************************************************************/

class KRC_WRITESOFTENDEXT:
    """
    Writes the software limit switches of the external axes.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    E1_Min to E6_Min (float): Negative software limit switch of axis E1 to E6. Unit: mm or °.
    E1_Max to E6_Max (float): Positive software limit switch of axis E1 to E6. Unit: mm or °.
    BufferMode (int): Mode in which the statement is executed. Values can be 0 (DIRECT), 1 (ABORTING), or 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE if the statement is currently being transferred or has already been transferred.
    Done (bool): TRUE if the statement has been executed.
    Aborted (bool): TRUE if the statement has been aborted.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.E1_MIN = 0.0
        self.E1_MAX = 0.0
        self.E2_MIN = 0.0
        self.E2_MAX = 0.0
        self.E3_MIN = 0.0
        self.E3_MAX = 0.0
        self.E4_MIN = 0.0
        self.E4_MAX = 0.0
        self.E5_MIN = 0.0
        self.E5_MAX = 0.0
        self.E6_MIN = 0.0
        self.E6_MAX = 0.0
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 19
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 2
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[13] = self.E1_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[14] = self.E1_MAX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[15] = self.E2_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[16] = self.E2_MAX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[17] = self.E3_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[18] = self.E3_MAX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[19] = self.E4_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[20] = self.E4_MAX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[21] = self.E5_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[22] = self.E5_MAX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[23] = self.E6_MIN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[24] = self.E6_MAX
        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_MOVELINEARABSOLUTE
#  ******************************************************************************/

class KRC_MOVELINEARABSOLUTE:
    """
    Executes a linear motion to a Cartesian end position. The coordinates of the end position are absolute.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    Position (E6POS): Coordinates of the Cartesian end position. The data structure E6POS contains all components of the end position (= position of the TCP relative to the origin of the BASE coordinate system).
    Velocity (int): Velocity. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type and refers to the value of DEF_VEL_CP of the robot system. Default: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type and refers to the value of DEF_ACC_CP of the robot system. Default: 0% (= acceleration is not changed).
    CoordinateSystem (COORDSYS): Coordinate system to which the Cartesian coordinates of the end position refer.
    OriType (int): Orientation control of the TCP. Values can be 0 (VAR), 1 (CONSTANT), or 2 (JOINT).
    Approximate (APO): Approximation parameter.
    BufferMode (int): Mode in which the statement is executed. Values can be 1 (ABORTING) or 2 (BUFFERED).
    SplineMode (bool): TRUE if the motion is executed as a spline motion. The motion is executed as a DLIN motion if a BASE coordinate system assigned to a conveyor is selected (parameter CoordinateSystem). FALSE if the motion is executed as a conventional linear motion.

    Returns:
    Busy (bool): TRUE if the statement is currently being transferred or has already been transferred.
    Active (bool): TRUE if the motion is currently being executed.
    Done (bool): TRUE if the motion has stopped.
    Aborted (bool): TRUE if the statement/motion has been aborted.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.POSITION = E6POS()
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.COORDINATESYSTEM = COORDSYS()
        self.ORITYPE = 0
        self.APPROXIMATE = APO()
        self.BUFFERMODE = 0
        self.SPLINEMODE = False
        self._BUSY = False 
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.KRC_MOVE_1 = KRC_MOVE()
        self.SWITCHMOVETYPE = 0
        self.M_CIRCHP = E6POS()
        self.M_AXISPOSITION = E6AXIS()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if self.SPLINEMODE:
            self.SWITCHMOVETYPE = 12
        else:
            self.SWITCHMOVETYPE = 2
        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 1
        self.KRC_MOVE_1.EXECUTECMD = self.EXECUTECMD
        self.KRC_MOVE_1.MOVETYPE = self.SWITCHMOVETYPE
        self.KRC_MOVE_1.ACTPOSITION = self.POSITION
        self.KRC_MOVE_1.AXISPOSITION = self.M_AXISPOSITION
        self.KRC_MOVE_1.CIRCHP = self.M_CIRCHP
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.COORDINATESYSTEM
        self.KRC_MOVE_1.ORITYPE = self.ORITYPE
        self.KRC_MOVE_1.CIRCTYPE = 0
        self.KRC_MOVE_1.CIRCANGLE = 0
        self.KRC_MOVE_1.APPROXIMATE = self.APPROXIMATE
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = True
        self.KRC_MOVE_1.POSVALIDT = True
        self.KRC_MOVE_1.BUFFERMODE = self.BUFFERMODE
        self.KRC_MOVE_1.OnCycle()
        self._BUSY = self.KRC_MOVE_1.BUSY
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._DONE = self.KRC_MOVE_1.DONE
        self._ABORTED = self.KRC_MOVE_1.ABORTED
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.KRC_MOVE_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_MOVELINEARRELATIVE
#  ******************************************************************************/

class KRC_MOVELINEARRELATIVE:
    """
    Executes a linear motion to a relative Cartesian end position. The parameter “Position” contains the path from the current position to the end position.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    Position (E6POS): Distance between end position and current position. The end position is based on the current position. The data structure E6POS contains all components of the end position (= position of the TCP relative to the origin of the selected coordinate system).
    Velocity (int): Velocity. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type and refers to the value of DEF_VEL_CP of the robot system. Default: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type and refers to the value of DEF_ACC_CP of the robot system. Default: 0% (= acceleration is not changed).
    CoordinateSystem (COORDSYS): Coordinate system to which the Cartesian coordinates of the end position refer.
    OriType (int): Orientation control of the TCP. Values can be 0 (VAR), 1 (CONSTANT), or 2 (JOINT).
    Approximate (APO): Approximation parameter.
    BufferMode (int): Mode in which the statement is executed. Values can be 1 (ABORTING) or 2 (BUFFERED).
    SplineMode (bool): TRUE if the motion is executed as a spline motion. The motion is executed as a DLIN motion if a BASE coordinate system assigned to a conveyor is selected (parameter CoordinateSystem). FALSE if the motion is executed as a conventional linear motion.

    Returns:
    Busy (bool): TRUE if the statement is currently being transferred or has already been transferred.
    Active (bool): TRUE if the motion is currently being executed.
    Done (bool): TRUE if the motion has stopped.
    Aborted (bool): TRUE if the statement/motion has been aborted.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.POSITION = E6POS()
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.COORDINATESYSTEM = COORDSYS()
        self.ORITYPE = 0
        self.APPROXIMATE = APO()
        self.BUFFERMODE = 0
        self.SPLINEMODE = False
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.KRC_MOVE_1 = KRC_MOVE()
        self.SWITCHMOVETYPE = 0
        self.M_CIRCHP = E6POS()
        self.M_AXISPOSITION = E6AXIS()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if self.SPLINEMODE:
            self.SWITCHMOVETYPE = 15
        else:
            self.SWITCHMOVETYPE = 5
        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 1
        self.KRC_MOVE_1.EXECUTECMD = self.EXECUTECMD
        self.KRC_MOVE_1.MOVETYPE = self.SWITCHMOVETYPE
        self.KRC_MOVE_1.ACTPOSITION = self.POSITION
        self.KRC_MOVE_1.AXISPOSITION = self.M_AXISPOSITION
        self.KRC_MOVE_1.CIRCHP = self.M_CIRCHP
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.COORDINATESYSTEM
        self.KRC_MOVE_1.ORITYPE = self.ORITYPE
        self.KRC_MOVE_1.CIRCTYPE = 0
        self.KRC_MOVE_1.CIRCANGLE = 0
        self.KRC_MOVE_1.APPROXIMATE = self.APPROXIMATE
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = False
        self.KRC_MOVE_1.POSVALIDT = False
        self.KRC_MOVE_1.BUFFERMODE = self.BUFFERMODE
        self.KRC_MOVE_1.OnCycle()
        self._BUSY = self.KRC_MOVE_1.BUSY
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._DONE = self.KRC_MOVE_1.DONE
        self._ABORTED = self.KRC_MOVE_1.ABORTED
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.KRC_MOVE_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_MOVEDIRECTRELATIVE
#  ******************************************************************************/

class KRC_MOVEDIRECTRELATIVE:
    """
    Executes a point-to-point motion to a relative Cartesian end position. The parameter “Position” contains the path from the current position to the end position. This corresponds to a PTP_REL motion on the robot system.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    Position (E6POS): Distance between end position and current position. The end position is based on the current position. The data structure E6POS contains all components of the end position (= position of the TCP relative to the origin of the selected coordinate system).
    Velocity (int): Velocity. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type and refers to the value of DEF_VEL_CP of the robot system. Default: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type and refers to the value of DEF_ACC_CP of the robot system. Default: 0% (= acceleration is not changed).
    CoordinateSystem (COORDSYS): Coordinate system to which the Cartesian coordinates of the end position refer.
    Approximate (APO): Approximation parameter.
    BufferMode (int): Mode in which the statement is executed. Values can be 1 (ABORTING) or 2 (BUFFERED).
    SplineMode (bool): TRUE if the motion is executed as a spline motion. FALSE if the motion is executed as a conventional point-to-point motion.

    Returns:
    Busy (bool): TRUE if the statement is currently being transferred or has already been transferred.
    Active (bool): TRUE if the motion is currently being executed.
    Done (bool): TRUE if the motion has stopped.
    Aborted (bool): TRUE if the statement/motion has been aborted.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.POSITION = E6POS()
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.COORDINATESYSTEM = COORDSYS()
        self.APPROXIMATE = APO()
        self.BUFFERMODE = 0
        self.SPLINEMODE = False
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.KRC_MOVE_1 = KRC_MOVE()
        self.SWITCHMOVETYPE = 0
        self.M_CIRCHP = E6POS()
        self.M_AXISPOSITION = E6AXIS()
        self.M_ORITYPE = 0

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if self.SPLINEMODE:
            self.SWITCHMOVETYPE = 16
        else:
            self.SWITCHMOVETYPE = 6
        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 1
        self.KRC_MOVE_1.EXECUTECMD = self.EXECUTECMD
        self.KRC_MOVE_1.MOVETYPE = self.SWITCHMOVETYPE
        self.KRC_MOVE_1.ACTPOSITION = self.POSITION
        self.KRC_MOVE_1.AXISPOSITION = self.M_AXISPOSITION
        self.KRC_MOVE_1.CIRCHP = self.M_CIRCHP
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.COORDINATESYSTEM
        self.KRC_MOVE_1.ORITYPE = self.M_ORITYPE
        self.KRC_MOVE_1.CIRCTYPE = 0
        self.KRC_MOVE_1.CIRCANGLE = 0
        self.KRC_MOVE_1.APPROXIMATE = self.APPROXIMATE
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = False
        self.KRC_MOVE_1.POSVALIDT = False
        self.KRC_MOVE_1.BUFFERMODE = self.BUFFERMODE
        self.KRC_MOVE_1.OnCycle()
        self._BUSY = self.KRC_MOVE_1.BUSY
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._DONE = self.KRC_MOVE_1.DONE
        self._ABORTED = self.KRC_MOVE_1.ABORTED
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.KRC_MOVE_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_MOVECIRCABSOLUTE
#  ******************************************************************************/

class KRC_MOVECIRCABSOLUTE:
    """
    Executes a circular motion to a Cartesian end position. An auxiliary position must be specified in addition to the end position for the robot controller to calculate the circular motion.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    Position (E6POS): Coordinates of the Cartesian end position. The data structure E6POS contains all components of the end position (= position of the TCP relative to the origin of the BASE coordinate system).
    CircHP (E6POS): Coordinates of the Cartesian auxiliary position. The data structure E6POS contains all components of the auxiliary position (= position of the TCP relative to the origin of the BASE coordinate system).
    Angle (float): Circular angle (= overall angle of the circular motion). The circular angle makes it possible to extend the motion beyond the programmed end point or to shorten it. The actual end point thus no longer corresponds to the programmed end point. Default: 0.0°.
    Velocity (int): Velocity. Refers to the maximum value specified in the machine data. Default: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Refers to the maximum value specified in the machine data. Default: 0% (= acceleration is not changed).
    CoordinateSystem (COORDSYS): Coordinate system to which the Cartesian coordinates of the auxiliary or end position refer.
    OriType (int): Orientation control of the TCP. Values can be 0 (VAR), 1 (CONSTANT), or 2 (JOINT).
    CircType (int): Orientation control during the circular motion. Values can be 0 (BASE) or 1 (PATH).
    Approximate (APO): Approximation parameter.
    BufferMode (int): Mode in which the statement is executed. Values can be 1 (ABORTING) or 2 (BUFFERED).
    SplineMode (bool): TRUE if the motion is executed as a spline motion. FALSE if the motion is executed as a conventional circular motion.

    Returns:
    Busy (bool): TRUE if the statement is currently being transferred or has already been transferred.
    Active (bool): TRUE if the motion is currently being executed.
    Done (bool): TRUE if the motion has stopped.
    Aborted (bool): TRUE if the statement/motion has been aborted.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.POSITION = E6POS()
        self.CIRCHP = E6POS()
        self.ANGLE = 0.0
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.COORDINATESYSTEM = COORDSYS()
        self.ORITYPE = 0
        self.CIRCTYPE = 0
        self.APPROXIMATE = APO()
        self.BUFFERMODE = 0
        self.SPLINEMODE = False
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.KRC_MOVE_1 = KRC_MOVE()
        self.SWITCHMOVETYPE = 0
        self.M_COORDINATESYSTEM = COORDSYS()
        self.M_AXISPOSITION = E6AXIS()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if self.SPLINEMODE:
            self.SWITCHMOVETYPE = 17
        else:
            self.SWITCHMOVETYPE = 7
        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 1
        self.KRC_MOVE_1.EXECUTECMD = self.EXECUTECMD
        self.KRC_MOVE_1.MOVETYPE = self.SWITCHMOVETYPE
        self.KRC_MOVE_1.ACTPOSITION = self.POSITION
        self.KRC_MOVE_1.AXISPOSITION = self.M_AXISPOSITION
        self.KRC_MOVE_1.CIRCHP = self.CIRCHP
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.COORDINATESYSTEM
        self.KRC_MOVE_1.ORITYPE = self.ORITYPE
        self.KRC_MOVE_1.CIRCTYPE = self.CIRCTYPE
        self.KRC_MOVE_1.CIRCANGLE = self.ANGLE
        self.KRC_MOVE_1.APPROXIMATE = self.APPROXIMATE
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = True
        self.KRC_MOVE_1.POSVALIDT = True
        self.KRC_MOVE_1.BUFFERMODE = self.BUFFERMODE
        self.KRC_MOVE_1.OnCycle()
        self._BUSY = self.KRC_MOVE_1.BUSY
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._DONE = self.KRC_MOVE_1.DONE
        self._ABORTED = self.KRC_MOVE_1.ABORTED
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.KRC_MOVE_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_MOVECIRCRELATIVE
#  ******************************************************************************/

class KRC_MOVECIRCRELATIVE:
    """
    Executes a circular motion to a Cartesian end position. An auxiliary position must be specified in addition to the end position for the robot controller to calculate the circular motion. The coordinates of the auxiliary position and end position are relative to the current position.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    Position (E6POS): Distance between end position and current position. The end position is based on the current position. The data structure E6POS contains all components of the end position (= position of the TCP relative to the origin of the BASE coordinate system).
    CircHP (E6POS): Coordinates of the Cartesian auxiliary position (relative to the current position). The data structure E6POS contains all components of the auxiliary position (= position of the TCP relative to the origin of the BASE coordinate system).
    Angle (float): Circular angle (= overall angle of the circular motion). The circular angle makes it possible to extend the motion beyond the programmed end point or to shorten it. The actual end point thus no longer corresponds to the programmed end point. Default: 0.0°.
    Velocity (int): Velocity. Refers to the maximum value specified in the machine data. Default: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Refers to the maximum value specified in the machine data. Default: 0% (= acceleration is not changed).
    CoordinateSystem (COORDSYS): Coordinate system to which the Cartesian coordinates of the auxiliary or end position refer.
    OriType (int): Orientation control of the TCP. Values can be 0 (VAR), 1 (CONSTANT), or 2 (JOINT).
    CircType (int): Orientation control during the circular motion. Values can be 0 (BASE) or 1 (PATH).
    Approximate (APO): Approximation parameter.
    BufferMode (int): Mode in which the statement is executed. Values can be 1 (ABORTING) or 2 (BUFFERED).
    SplineMode (bool): TRUE if the motion is executed as a spline motion. FALSE if the motion is executed as a conventional circular motion.

    Returns:
    Busy (bool): TRUE if the statement is currently being transferred or has already been transferred.
    Active (bool): TRUE if the motion is currently being executed.
    Done (bool): TRUE if the motion has stopped.
    Aborted (bool): TRUE if the statement/motion has been aborted.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.POSITION = E6POS()
        self.CIRCHP = E6POS()
        self.ANGLE = 0.0
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.COORDINATESYSTEM = COORDSYS()
        self.ORITYPE = 0
        self.CIRCTYPE = 0
        self.APPROXIMATE = APO()
        self.BUFFERMODE = 0
        self.SPLINEMODE = False
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.KRC_MOVE_1 = KRC_MOVE()
        self.SWITCHMOVETYPE = 0
        self.M_COORDINATESYSTEM = COORDSYS()
        self.M_AXISPOSITION = E6AXIS()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if self.SPLINEMODE:
            self.SWITCHMOVETYPE = 18
        else:
            self.SWITCHMOVETYPE = 8
        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 1
        self.KRC_MOVE_1.EXECUTECMD = self.EXECUTECMD
        self.KRC_MOVE_1.MOVETYPE = self.SWITCHMOVETYPE
        self.KRC_MOVE_1.ACTPOSITION = self.POSITION
        self.KRC_MOVE_1.AXISPOSITION = self.M_AXISPOSITION
        self.KRC_MOVE_1.CIRCHP = self.CIRCHP
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.COORDINATESYSTEM
        self.KRC_MOVE_1.ORITYPE = self.ORITYPE
        self.KRC_MOVE_1.CIRCTYPE = self.CIRCTYPE
        self.KRC_MOVE_1.CIRCANGLE = self.ANGLE
        self.KRC_MOVE_1.APPROXIMATE = self.APPROXIMATE
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = True
        self.KRC_MOVE_1.POSVALIDT = True
        self.KRC_MOVE_1.BUFFERMODE = self.BUFFERMODE
        self.KRC_MOVE_1.OnCycle()
        self._BUSY = self.KRC_MOVE_1.BUSY
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._DONE = self.KRC_MOVE_1.DONE
        self._ABORTED = self.KRC_MOVE_1.ABORTED
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.KRC_MOVE_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_Jog
#  ******************************************************************************/

class KRC_JOG:
    """
    Executes a motion to an end position with a linear motion or a point-to-point motion. The function is always executed in ABORTING mode, i.e. all active motions and buffered statements are canceled, the robot is braked and the motion is then executed.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    MoveType (int): Motion type for Cartesian or axis-specific jogging. Values can be 0 (Axis-specific), 1 (Cartesian), 2 (Axis-specific, as spline motion), or 3 (Cartesian, as spline motion).
    Velocity (int): Velocity. Refers to the maximum value specified in the machine data. Default: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Refers to the maximum value specified in the machine data. Default: 0% (= acceleration is not changed).
    CoordinateSystem (COORDSYS): Coordinate system to which the coordinates of the end position refer.
    Increment (float): Incremental jogging. The maximum distance for incremental jogging can be limited using this parameter.
    A1_X_P, A1_X_M, A2_Y_P, A2_Y_M, A3_Z_P, A3_Z_M, A4_A_P, A4_A_M, A5_B_P, A5_B_M, A6_C_P, A6_C_M, E1_P, E1_M, E2_P, E2_M, E3_P, E3_M, E4_P, E4_M, E5_P, E5_M, E6_P, E6_M (bool): Motion instructions. The motion is started at a rising edge of the signal and stopped at a falling edge of the signal.

    Returns:
    Busy (bool): TRUE if the function block is active and waiting for a motion instruction.
    Active (bool): TRUE if the motion is currently being executed.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.MOVETYPE = 0
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.COORDINATESYSTEM = COORDSYS()
        self.INCREMENT = 0.0
        self.A1_X_P = False
        self.A1_X_M = False
        self.A2_Y_P = False
        self.A2_Y_M = False
        self.A3_Z_P = False
        self.A3_Z_M = False
        self.A4_A_P = False
        self.A4_A_M = False
        self.A5_B_P = False
        self.A5_B_M = False
        self.A6_C_P = False
        self.A6_C_M = False
        self.E1_P = False
        self.E1_M = False
        self.E2_P = False
        self.E2_M = False
        self.E3_P = False
        self.E3_M = False
        self.E4_P = False
        self.E4_M = False
        self.E5_P = False
        self.E5_M = False
        self.E6_P = False
        self.E6_M = False
        self._BUSY = False
        self._ACTIVE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.KRC_MOVE_1 = KRC_MOVE()
        self.KRC_ABORT_1 = KRC_ABORT()
        self.M_POSITION = E6POS()
        self.M_AXISPOSITION = E6AXIS()
        self.M_MOVETYPE = 0
        self.M_EXECUTECMD = False
        self.M_CMDINPUTACTIVE = False
        self.M_CMDINPUTACTIVELAST = False
        self.M_CMDINPUTACTIVECHANGED = False
        self.M_CMDINPUTCHANGED = False
        self.M_INCREMENTACTIVE = False
        self.M_MAXDELTA = 0.0
        self.M_EXECUTEABORT = False
        self.A1_X_P_LAST = False
        self.A1_X_M_LAST = False
        self.A2_Y_P_LAST = False
        self.A2_Y_M_LAST = False
        self.A3_Z_P_LAST = False
        self.A3_Z_M_LAST = False
        self.A4_A_P_LAST = False
        self.A4_A_M_LAST = False
        self.A5_B_P_LAST = False
        self.A5_B_M_LAST = False
        self.A6_C_P_LAST = False
        self.A6_C_M_LAST = False
        self.E1_P_LAST = False
        self.E1_M_LAST = False
        self.E2_P_LAST = False
        self.E2_M_LAST = False
        self.E3_P_LAST = False
        self.E3_M_LAST = False
        self.E4_P_LAST = False
        self.E4_M_LAST = False
        self.E5_P_LAST = False
        self.E5_M_LAST = False
        self.E6_P_LAST = False
        self.E6_M_LAST = False
        self.M_EXECUTECMD_FINISHED = False

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if (self.A1_X_P and self.A1_X_M) or (self.A2_Y_P and self.A2_Y_M) or (self.A3_Z_P and self.A3_Z_M) or (self.A4_A_P and self.A4_A_M) or (self.A5_B_P and self.A5_B_M) or (self.A6_C_P and self.A6_C_M) or (self.E1_P and self.E1_M) or (self.E2_P and self.E2_M) or (self.E3_P and self.E3_M) or (self.E4_P and self.E4_M) or (self.E5_P and self.E5_M) or (self.E6_P and self.E6_M):
            self._ERRORID = 548
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            self._ERROR = True
            return
        self.M_INCREMENTACTIVE = self.INCREMENT > 0.0
        if self.MOVETYPE == 0:
            self.M_MOVETYPE = 9
        elif self.MOVETYPE == 1:
            self.M_MOVETYPE = 3
        elif self.MOVETYPE == 2:
            self.M_MOVETYPE = 19
        else:
            self._ERRORID = 590
            self._ERROR = True
            return
        self.M_CMDINPUTACTIVE = self.A1_X_P or self.A1_X_M or self.A2_Y_P or self.A2_Y_M or self.A3_Z_P or self.A3_Z_M or self.A4_A_P or self.A4_A_M or self.A5_B_P or self.A5_B_M or self.A6_C_P or self.A6_C_M or self.E1_P or self.E1_M or self.E2_P or self.E2_M or self.E3_P or self.E3_M or self.E4_P or self.E4_M or self.E5_P or self.E5_M or self.E6_P or self.E6_M
        self.M_CMDINPUTACTIVECHANGED = self.M_CMDINPUTACTIVELAST != self.M_CMDINPUTACTIVE
        self.M_CMDINPUTACTIVELAST = self.M_CMDINPUTACTIVE
        if self.M_CMDINPUTACTIVECHANGED and not self.M_CMDINPUTACTIVE:
            self.M_EXECUTEABORT = True
        self.M_CMDINPUTCHANGED = False
        if self.A1_X_P != self.A1_X_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.A1_X_M != self.A1_X_M_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.A2_Y_P != self.A2_Y_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.A2_Y_M != self.A2_Y_M_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.A3_Z_P != self.A3_Z_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.A3_Z_M != self.A3_Z_M_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.A4_A_P != self.A4_A_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.A4_A_M != self.A4_A_M_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.A5_B_P != self.A5_B_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.A5_B_M != self.A5_B_M_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.A6_C_P != self.A6_C_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.A6_C_M != self.A6_C_M_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E1_P != self.E1_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E1_M != self.E1_M_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E2_P != self.E2_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E2_M != self.E2_M_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E3_P != self.E3_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E3_M != self.E3_M_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E4_P != self.E4_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E4_M != self.E4_M_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E5_P != self.E5_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E5_M != self.E5_M_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E6_P != self.E6_P_LAST:
            self.M_CMDINPUTCHANGED = True
        if self.E6_M != self.E6_M_LAST:
            self.M_CMDINPUTCHANGED = True


# part 2
        self.A1_X_P_LAST = self.A1_X_P
        self.A1_X_M_LAST = self.A1_X_M
        self.A2_Y_P_LAST = self.A2_Y_P
        self.A2_Y_M_LAST = self.A2_Y_M
        self.A3_Z_P_LAST = self.A3_Z_P
        self.A3_Z_M_LAST = self.A3_Z_M
        self.A4_A_P_LAST = self.A4_A_P
        self.A4_A_M_LAST = self.A4_A_M
        self.A5_B_P_LAST = self.A5_B_P
        self.A5_B_M_LAST = self.A5_B_M
        self.A6_C_P_LAST = self.A6_C_P
        self.A6_C_M_LAST = self.A6_C_M
        self.E1_P_LAST = self.E1_P
        self.E1_M_LAST = self.E1_M
        self.E2_P_LAST = self.E2_P
        self.E2_M_LAST = self.E2_M
        self.E3_P_LAST = self.E3_P
        self.E3_M_LAST = self.E3_M
        self.E4_P_LAST = self.E4_P
        self.E4_M_LAST = self.E4_M
        self.E5_P_LAST = self.E5_P
        self.E5_M_LAST = self.E5_M
        self.E6_P_LAST = self.E6_P
        self.E6_M_LAST = self.E6_M
        self.M_EXECUTECMD = self.M_CMDINPUTACTIVE and (not self.M_CMDINPUTCHANGED or self.M_CMDINPUTACTIVECHANGED)
        self.M_MAXDELTA = 100000.0
        self.M_AXISPOSITION.A1 = 0.0
        self.M_AXISPOSITION.A2 = 0.0
        self.M_AXISPOSITION.A3 = 0.0
        self.M_AXISPOSITION.A4 = 0.0
        self.M_AXISPOSITION.A5 = 0.0
        self.M_AXISPOSITION.A6 = 0.0
        self.M_AXISPOSITION.E1 = 0.0
        self.M_AXISPOSITION.E2 = 0.0
        self.M_AXISPOSITION.E3 = 0.0
        self.M_AXISPOSITION.E4 = 0.0
        self.M_AXISPOSITION.E5 = 0.0
        self.M_AXISPOSITION.E6 = 0.0
        self.M_POSITION.X = 0.0
        self.M_POSITION.Y = 0.0
        self.M_POSITION.Z = 0.0
        self.M_POSITION.A = 0.0
        self.M_POSITION.B = 0.0
        self.M_POSITION.C = 0.0
        self.M_POSITION.E1 = 0.0
        self.M_POSITION.E2 = 0.0
        self.M_POSITION.E3 = 0.0
        self.M_POSITION.E4 = 0.0
        self.M_POSITION.E5 = 0.0
        self.M_POSITION.E6 = 0.0
        if self.M_EXECUTECMD:
            if self.MOVETYPE == 0 or self.MOVETYPE == 2:
                if self.M_INCREMENTACTIVE:
                    if self.A1_X_P: self.M_AXISPOSITION.A1 = self.INCREMENT
                    if self.A1_X_M: self.M_AXISPOSITION.A1 = self.INCREMENT * -1
                    if self.A2_Y_P: self.M_AXISPOSITION.A2 = self.INCREMENT
                    if self.A2_Y_M: self.M_AXISPOSITION.A2 = self.INCREMENT * -1
                    if self.A3_Z_P: self.M_AXISPOSITION.A3 = self.INCREMENT
                    if self.A3_Z_M: self.M_AXISPOSITION.A3 = self.INCREMENT * -1
                    if self.A4_A_P: self.M_AXISPOSITION.A4 = self.INCREMENT
                    if self.A4_A_M: self.M_AXISPOSITION.A4 = self.INCREMENT * -1
                    if self.A5_B_P: self.M_AXISPOSITION.A5 = self.INCREMENT
                    if self.A5_B_M: self.M_AXISPOSITION.A5 = self.INCREMENT * -1
                    if self.A6_C_P: self.M_AXISPOSITION.A6 = self.INCREMENT
                    if self.A6_C_M: self.M_AXISPOSITION.A6 = self.INCREMENT * -1
                    if self.E1_P: self.M_AXISPOSITION.E1 = self.INCREMENT
                    if self.E1_M: self.M_AXISPOSITION.E1 = self.INCREMENT * -1
                    if self.E2_P: self.M_AXISPOSITION.E2 = self.INCREMENT
                    if self.E2_M: self.M_AXISPOSITION.E2 = self.INCREMENT * -1
                    if self.E3_P: self.M_AXISPOSITION.E3 = self.INCREMENT
                    if self.E3_M: self.M_AXISPOSITION.E3 = self.INCREMENT * -1
                    if self.E4_P: self.M_AXISPOSITION.E4 = self.INCREMENT
                    if self.E4_M: self.M_AXISPOSITION.E4 = self.INCREMENT * -1
                    if self.E5_P: self.M_AXISPOSITION.E5 = self.INCREMENT
                    if self.E5_M: self.M_AXISPOSITION.E5 = self.INCREMENT * -1
                    if self.E6_P: self.M_AXISPOSITION.E6 = self.INCREMENT
                    if self.E6_M: self.M_AXISPOSITION.E6 = self.INCREMENT * -1
                else:
                    if self.A1_X_P: self.M_AXISPOSITION.A1 = self.M_MAXDELTA
                    if self.A1_X_M: self.M_AXISPOSITION.A1 = self.M_MAXDELTA * -1
                    if self.A2_Y_P: self.M_AXISPOSITION.A2 = self.M_MAXDELTA
                    if self.A2_Y_M: self.M_AXISPOSITION.A2 = self.M_MAXDELTA * -1
                    if self.A3_Z_P: self.M_AXISPOSITION.A3 = self.M_MAXDELTA
                    if self.A3_Z_M: self.M_AXISPOSITION.A3 = self.M_MAXDELTA * -1
                    if self.A4_A_P: self.M_AXISPOSITION.A4 = self.M_MAXDELTA
                    if self.A4_A_M: self.M_AXISPOSITION.A4 = self.M_MAXDELTA * -1
                    if self.A5_B_P: self.M_AXISPOSITION.A5 = self.M_MAXDELTA
                    if self.A5_B_M: self.M_AXISPOSITION.A5 = self.M_MAXDELTA * -1
                    if self.A6_C_P: self.M_AXISPOSITION.A6 = self.M_MAXDELTA
                    if self.A6_C_M: self.M_AXISPOSITION.A6 = self.M_MAXDELTA * -1
                    if self.E1_P: self.M_AXISPOSITION.E1 = self.M_MAXDELTA
                    if self.E1_M: self.M_AXISPOSITION.E1 = self.M_MAXDELTA * -1
                    if self.E2_P: self.M_AXISPOSITION.E2 = self.M_MAXDELTA
                    if self.E2_M: self.M_AXISPOSITION.E2 = self.M_MAXDELTA * -1
                    if self.E3_P: self.M_AXISPOSITION.E3 = self.M_MAXDELTA
                    if self.E3_M: self.M_AXISPOSITION.E3 = self.M_MAXDELTA * -1
                    if self.E4_P: self.M_AXISPOSITION.E4 = self.M_MAXDELTA
                    if self.E4_M: self.M_AXISPOSITION.E4 = self.M_MAXDELTA * -1
                    if self.E5_P: self.M_AXISPOSITION.E5 = self.M_MAXDELTA
                    if self.E5_M: self.M_AXISPOSITION.E5 = self.M_MAXDELTA * -1
                    if self.E6_P: self.M_AXISPOSITION.E6 = self.M_MAXDELTA
                    if self.E6_M: self.M_AXISPOSITION.E6 = self.M_MAXDELTA * -1

# part 3

            if self.MOVETYPE == 1:
                    if self.M_INCREMENTACTIVE:
                        if self.A1_X_P: self.M_POSITION.X = self.INCREMENT
                        if self.A1_X_M: self.M_POSITION.X = self.INCREMENT * -1
                        if self.A2_Y_P: self.M_POSITION.Y = self.INCREMENT
                        if self.A2_Y_M: self.M_POSITION.Y = self.INCREMENT * -1
                        if self.A3_Z_P: self.M_POSITION.Z = self.INCREMENT
                        if self.A3_Z_M: self.M_POSITION.Z = self.INCREMENT * -1
                        if self.A4_A_P: self.M_POSITION.A = self.INCREMENT
                        if self.A4_A_M: self.M_POSITION.A = self.INCREMENT * -1
                        if self.A5_B_P: self.M_POSITION.B = self.INCREMENT
                        if self.A5_B_M: self.M_POSITION.B = self.INCREMENT * -1
                        if self.A6_C_P: self.M_POSITION.C = self.INCREMENT
                        if self.A6_C_M: self.M_POSITION.C = self.INCREMENT * -1
                        if self.E1_P: self.M_POSITION.E1 = self.INCREMENT
                        if self.E1_M: self.M_POSITION.E1 = self.INCREMENT * -1
                        if self.E2_P: self.M_POSITION.E2 = self.INCREMENT
                        if self.E2_M: self.M_POSITION.E2 = self.INCREMENT * -1
                        if self.E3_P: self.M_POSITION.E3 = self.INCREMENT
                        if self.E3_M: self.M_POSITION.E3 = self.INCREMENT * -1
                        if self.E4_P: self.M_POSITION.E4 = self.INCREMENT
                        if self.E4_M: self.M_POSITION.E4 = self.INCREMENT * -1
                        if self.E5_P: self.M_POSITION.E5 = self.INCREMENT
                        if self.E5_M: self.M_POSITION.E5 = self.INCREMENT * -1
                        if self.E6_P: self.M_POSITION.E6 = self.INCREMENT
                        if self.E6_M: self.M_POSITION.E6 = self.INCREMENT * -1
                    else:
                        if self.A1_X_P: self.M_POSITION.X = self.M_MAXDELTA
                        if self.A1_X_M: self.M_POSITION.X = self.M_MAXDELTA * -1
                        if self.A2_Y_P: self.M_POSITION.Y = self.M_MAXDELTA
                        if self.A2_Y_M: self.M_POSITION.Y = self.M_MAXDELTA * -1
                        if self.A3_Z_P: self.M_POSITION.Z = self.M_MAXDELTA
                        if self.A3_Z_M: self.M_POSITION.Z = self.M_MAXDELTA * -1
    
    #part 4
                        if self.A4_A_P: self.M_POSITION.A = 90.0
                        if self.A4_A_M: self.M_POSITION.A = 90.0 * -1
                        if self.A5_B_P: self.M_POSITION.B = 90.0
                        if self.A5_B_M: self.M_POSITION.B = 90.0 * -1
                        if self.A6_C_P: self.M_POSITION.C = 90.0
                        if self.A6_C_M: self.M_POSITION.C = 90.0 * -1
                        if self.E1_P: self.M_POSITION.E1 = self.M_MAXDELTA
                        if self.E1_M: self.M_POSITION.E1 = self.M_MAXDELTA * -1
                        if self.E2_P: self.M_POSITION.E2 = self.M_MAXDELTA
                        if self.E2_M: self.M_POSITION.E2 = self.M_MAXDELTA * -1
                        if self.E3_P: self.M_POSITION.E3 = self.M_MAXDELTA
                        if self.E3_M: self.M_POSITION.E3 = self.M_MAXDELTA * -1
                        if self.E4_P: self.M_POSITION.E4 = self.M_MAXDELTA
                        if self.E4_M: self.M_POSITION.E4 = self.M_MAXDELTA * -1
                        if self.E5_P: self.M_POSITION.E5 = self.M_MAXDELTA
                        if self.E5_M: self.M_POSITION.E5 = self.M_MAXDELTA * -1
                        if self.E6_P: self.M_POSITION.E6 = self.M_MAXDELTA
                        if self.E6_M: self.M_POSITION.E6 = self.M_MAXDELTA * -1


        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 1
        self.KRC_MOVE_1.EXECUTECMD = self.M_EXECUTECMD and self._ERRORID == 0 and not self.M_EXECUTEABORT
        self.KRC_MOVE_1.MOVETYPE = self.M_MOVETYPE
        self.KRC_MOVE_1.ACTPOSITION = self.M_POSITION
        self.KRC_MOVE_1.AXISPOSITION = self.M_AXISPOSITION
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.COORDINATESYSTEM
        self.KRC_MOVE_1.ORITYPE = 0
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = False
        self.KRC_MOVE_1.POSVALIDT = False
        self.KRC_MOVE_1.BUFFERMODE = 1
        self.KRC_MOVE_1.OnCycle()
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = self._ERRORID != 0
        # Call FB KRC_Abort_1
        self.KRC_ABORT_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_ABORT_1.EXECUTECMD = self.M_EXECUTEABORT
        self.KRC_ABORT_1.OnCycle()
        if self.KRC_ABORT_1.ERROR or self.KRC_ABORT_1.DONE:
            self.M_EXECUTEABORT = False
        self._ERRORID = self.KRC_ABORT_1.ERRORID
#part 6
        #KRC jog done signal and busy robot stopped
        if not self.M_CMDINPUTACTIVELAST and self.M_CMDINPUTACTIVE and self.M_EXECUTECMD:
            self._BUSY = True

        if self.M_CMDINPUTACTIVELAST and not self.M_CMDINPUTACTIVE and self._ERRORID == 0:
            self.M_EXECUTECMD_FINISHED = True

        if self.M_EXECUTECMD_FINISHED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.ROB_STOPPED:
            self.M_EXECUTECMD_FINISHED = False
            self._BUSY = False

        if self.M_EXECUTEABORT:
            self._ORDERID = self.KRC_ABORT_1.ORDERID
        elif self.M_EXECUTECMD and self._ERRORID == 0:
            self._ORDERID = self.KRC_MOVE_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_JOGTOOLRELATIVE
#  ******************************************************************************/

class KRC_JOGTOOLRELATIVE:
    """
    Executes a motion to a Cartesian end position in the TOOL coordinate system with a linear motion. The coordinates of the end position are relative to the current position.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    Position (E6POS): Distance from the target position to the current position. The target position is based on the current position. The data structure E6POS contains all components of the end position (= position of the TCP relative to the origin of the selected coordinate system).
    Velocity (int): Velocity. Refers to the maximum value specified in the machine data. Default: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Refers to the maximum value specified in the machine data. Default: 0% (= acceleration is not changed).
    CoordinateSystem (COORDSYS): Coordinate system to which the Cartesian coordinates of the end position refer.
    OriType (int): Orientation control of the TCP. Values can be 0 (VAR), 1 (CONSTANT), or 2 (JOINT).

    Returns:
    Busy (bool): TRUE if the statement is currently being transferred or has already been transferred.
    Active (bool): TRUE if the motion is currently being executed.
    Done (bool): TRUE if the motion has stopped.
    Aborted (bool): TRUE if the statement/motion has been aborted.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.POSITION = E6POS()  
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.COORDINATESYSTEM = COORDSYS()  
        self.ORITYPE = 0

        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.KRC_MOVE_1 = KRC_MOVE() 

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._ERRORID = 506
            self._ERROR = True
            return


        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 1
        self.KRC_MOVE_1.EXECUTECMD = self.EXECUTECMD
        self.KRC_MOVE_1.MOVETYPE = 4
        self.KRC_MOVE_1.ACTPOSITION = self.POSITION
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.COORDINATESYSTEM
        self.KRC_MOVE_1.ORITYPE = self.ORITYPE
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = True
        self.KRC_MOVE_1.POSVALIDT = True
        self.KRC_MOVE_1.BUFFERMODE = 1
        self.KRC_MOVE_1.OnCycle()  
        self._BUSY = self.KRC_MOVE_1.BUSY
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._DONE = self.KRC_MOVE_1.DONE
        self._ABORTED = self.KRC_MOVE_1.ABORTED
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.KRC_MOVE_1.ORDERID




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_JOGLINEARRELATIVE
#  ******************************************************************************/

class KRC_JOGLINEARRELATIVE:
    """
    Executes a motion to a Cartesian end position with a linear motion. The end position is relative to the current position. The function is always executed in ABORTING mode, i.e. all active motions and buffered statements are canceled, the robot is braked and the linear motion is then executed.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Values can range from 1 to 5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    Position (E6POS): Distance from the target position to the current position. The target position is based on the current position. The data structure E6POS contains all components of the end position (= position of the TCP relative to the origin of the selected coordinate system).
    Velocity (int): Velocity. Refers to the maximum value specified in the machine data. Default: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Refers to the maximum value specified in the machine data. Default: 0% (= acceleration is not changed).
    CoordinateSystem (COORDSYS): Coordinate system to which the Cartesian coordinates of the end position refer.
    OriType (int): Orientation control of the TCP. Values can be 0 (VAR), 1 (CONSTANT), or 2 (JOINT).

    Returns:
    Busy (bool): TRUE if the statement is currently being transferred or has already been transferred.
    Active (bool): TRUE if the motion is currently being executed.
    Done (bool): TRUE if the motion has stopped.
    Aborted (bool): TRUE if the statement/motion has been aborted.
    Error (bool): TRUE if there is an error in the function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.POSITION = E6POS()  
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.COORDINATESYSTEM = COORDSYS()  
        self.ORITYPE = 0

        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.KRC_MOVE_1 = KRC_MOVE()  

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._ERRORID = 506
            self._ERROR = True
            return

        # Call FB KRC_Move_1
        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 1
        self.KRC_MOVE_1.EXECUTECMD = self.EXECUTECMD
        self.KRC_MOVE_1.MOVETYPE = 3
        self.KRC_MOVE_1.ACTPOSITION = self.POSITION
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.COORDINATESYSTEM
        self.KRC_MOVE_1.ORITYPE = self.ORITYPE
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = True
        self.KRC_MOVE_1.POSVALIDT = True
        self.KRC_MOVE_1.BUFFERMODE = 1
        self.KRC_MOVE_1.OnCycle() 
        self._BUSY = self.KRC_MOVE_1.BUSY
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._DONE = self.KRC_MOVE_1.DONE
        self._ABORTED = self.KRC_MOVE_1.ABORTED
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.KRC_MOVE_1.ORDERID





# /******************************************************************************
#  * FUNCTION_BLOCK KRC_JOGADVANCED
#  ******************************************************************************/

class KRC_JOGADVANCED:
    """
    The function block KRC_JogAdvanced can be used to move to an end position with a linear motion or a point-to-point motion.
    The function is activated by means of the parameter JogAdvanced. The following modified values are permanently transferred 
    to the robot controller as long as the parameter JogAdvanced is activated: Tool, Base, Interpolation mode, Motion type.

    The robot interpreter cannot perform any other calculations if the output “Busy” has the value TRUE. This function block 
    cannot be used with conveyor systems.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    MoveType (int): Motion type for Cartesian or axis-specific jogging. Options: 1 (Axis-specific as a spline motion and Cartesian as a spline motion in the BASE coordinate system), 2 (Axis-specific and Cartesian as a spline motion in the TOOL coordinate system).
    Velocity (int): Velocity. Range: 0-100%. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type. Default value: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Range: 0-100%. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type. Default value: 0% (= acceleration is not changed).
    CoordinateSystem (COORDSYS): Coordinate system to which the coordinates of the end position refer.
    JogAdvanced (bool): The JogAdvanced function is activated at a rising edge of the signal and deactivated at a falling edge of the signal.
    B_A1_JA_P (bool): Motion instruction. The motion instruction is only executed if the parameter JogAdvanced is activated. The motion is started at a rising edge of the signal and stopped at a falling edge of the signal. In the case of axis-specific motion, the robot axes can be moved as far as 0.1 mm/° before the software limit switches. For this, the software limit switch values are read once when the PLC is started. The TCP can be moved along the axes of several coordinate systems. If the input signals are changed, the motion is stopped and then resumed with the modified configuration. If the positive and negative motion directions are activated simultaneously, an error number is displayed. The inputs that end in "P" (e.g. B_A2_JA_P) move in the positive direction. The inputs that end in "M" (e.g. B_A3_JA_M) move in the negative direction.
    B_A1_JA_M (bool): Similar to B_A1_JA_P but moves in the negative direction.
    B_A2_JA_P (bool): Similar to B_A1_JA_P but for the A2 axis.
    B_A2_JA_M (bool): Similar to B_A1_JA_M but for the A2 axis.
    B_A3_JA_P (bool): Similar to B_A1_JA_P but for the A3 axis.
    B_A3_JA_M (bool): Similar to B_A1_JA_M but for the A3 axis.
    B_A4_JA_P (bool): Similar to B_A1_JA_P but for the A4 axis.
    B_A4_JA_M (bool): Similar to B_A1_JA_M but for the A4 axis.
    B_A5_JA_P (bool): Similar to B_A1_JA_P but for the A5 axis.
    B_A5_JA_M (bool): Similar to B_A1_JA_M but for the A5 axis.
    B_A6_JA_P (bool): Similar to B_A1_JA_P but for the A6 axis.
    B_A6_JA_M (bool): Similar to B_A1_JA_M but for the A6 axis.
    B_E1_JA_P (bool): Similar to B_A1_JA_P but for the E1 axis.
    B_E1_JA_M (bool): Similar to B_A1_JA_M but for the E1 axis.
    B_E2_JA_P (bool): Similar to B_A1_JA_P but for the E2 axis.
    B_E2_JA_M (bool): Similar to B_A1_JA_M but for the E2 axis.
    B_E3_JA_P (bool): Similar to B_A1_JA_P but for the E3 axis.
    B_E3_JA_M (bool): Similar to B_A1_JA_M but for the E3 axis.
    B_E4_JA_P (bool): Similar to B_A1_JA_P but for the E4 axis.
    B_E4_JA_M (bool): Similar to B_A1_JA_M but for the E4 axis.
    B_E5_JA_P (bool): Similar to B_A1_JA_P but for the E5 axis.
    B_E5_JA_M (bool): Similar to B_A1_JA_M but for the E5 axis.
    B_E6_JA_P (bool): Similar to B_A1_JA_P but for the E6 axis.
    B_E6_JA_M (bool): Similar to B_A1_JA_M but for the E6 axis.
    B_X_JA_P (bool): Similar to B_A1_JA_P but for the X axis.
    B_X_JA_M (bool): Similar to B_A1_JA_M but for the X axis.
    B_Y_JA_P (bool): Similar to B_A1_JA_P but for the Y axis.
    B_Y_JA_M (bool): Similar to B_A1_JA_M but for the Y axis.
    B_Z_JA_P (bool): Similar to B_A1_JA_P but for the Z axis.
    B_Z_JA_M (bool): Similar to B_A1_JA_M but for the Z axis.
    B_A_JA_P (bool): Similar to B_A1_JA_P but for the A axis.
    B_A_JA_M (bool): Similar to B_A1_JA_M but for the A axis.
    B_B_JA_P (bool): Similar to B_A1_JA_P but for the B axis.
    B_B_JA_M (bool): Similar to B_A1_JA_M but for the B axis.
    B_C_JA_P (bool): Similar to B_A1_JA_P but for the C axis.
    B_C_JA_M (bool): Similar to B_A1_JA_M but for the C axis.

    Returns:
    Busy (bool): TRUE = function block is active and waiting for a motion instruction.
    Active (bool): TRUE = motion is currently being executed.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.MOVETYPE = 0
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.COORDINATESYSTEM = COORDSYS()
        self.JOGADVANCED = False
        self.B_A1_JA_P = False
        self.B_A1_JA_M = False
        self.B_A2_JA_P = False
        self.B_A2_JA_M = False
        self.B_A3_JA_P = False
        self.B_A3_JA_M = False
        self.B_A4_JA_P = False
        self.B_A4_JA_M = False
        self.B_A5_JA_P = False
        self.B_A5_JA_M = False
        self.B_A6_JA_P = False
        self.B_A6_JA_M = False
        self.B_E1_JA_P = False
        self.B_E1_JA_M = False
        self.B_E2_JA_P = False
        self.B_E2_JA_M = False
        self.B_E3_JA_P = False
        self.B_E3_JA_M = False
        self.B_E4_JA_P = False
        self.B_E4_JA_M = False
        self.B_E5_JA_P = False
        self.B_E5_JA_M = False
        self.B_E6_JA_P = False
        self.B_E6_JA_M = False
        self.B_X_JA_P = False
        self.B_X_JA_M = False
        self.B_Y_JA_P = False
        self.B_Y_JA_M = False
        self.B_Z_JA_P = False
        self.B_Z_JA_M = False
        self.B_A_JA_P = False
        self.B_A_JA_M = False
        self.B_B_JA_P = False
        self.B_B_JA_M = False
        self.B_C_JA_P = False
        self.B_C_JA_M = False
        self._BUSY = False
        self._ACTIVE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.JA_STATE_VAL = 0
        self.KRC_MOVE_1 = KRC_MOVE()  
        self.KRC_ABORT_1 = KRC_ABORT()  
        self.M_POSITION = E6POS()  
        self.M_AXISPOSITION = E6AXIS()  
        self.M_MOVETYPE = 0
        self.M_EXECUTEABORT = False
        self.JA_BUTTONACTIVE = False
        self.JA_BUTTONCHANGED = False
        self.JA_BUTTONLAST = False
        self.JA_MOVETYPEACTIVE = False
        self.JA_MOVETYPELAST = False
        self.JA_MOVETYPECHANGED = False
        self.JA_BASECHANGED = False
        self.JA_COORDSYSACTIVE = COORDSYS()
        self.JA_COORDSYSLAST = COORDSYS()
        self.JA_TOOLCHANGED = False
        self.JA_IPOCHANGED = False

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self.JA_BUTTONACTIVE = False
        self._BUSY = False
        self._ORDERID = 0
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].JOG_ADVANCED.JOG_AD_ACTIVE = self.JOGADVANCED
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].JOG_ADVANCED.JOG_AD_STATE_VAL = 0
        
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        if (self.B_A1_JA_P and self.B_A1_JA_M) or (self.B_A2_JA_P and self.B_A2_JA_M) or (self.B_A3_JA_P and self.B_A3_JA_M) or (self.B_A4_JA_P and self.B_A4_JA_M) or (self.B_A5_JA_P and self.B_A5_JA_M) or (self.B_A6_JA_P and self.B_A6_JA_M) or (self.B_E1_JA_P and self.B_E1_JA_M) or (self.B_E2_JA_P and self.B_E2_JA_M) or (self.B_E3_JA_P and self.B_E3_JA_M) or (self.B_E4_JA_P and self.B_E4_JA_M) or (self.B_E5_JA_P and self.B_E5_JA_M) or (self.B_E6_JA_P and self.B_E6_JA_M) or (self.B_X_JA_P and self.B_X_JA_M) or (self.B_Y_JA_P and self.B_Y_JA_M) or (self.B_Z_JA_P and self.B_Z_JA_M) or (self.B_A_JA_P and self.B_A_JA_M) or (self.B_B_JA_P and self.B_B_JA_M) or (self.B_C_JA_P and self.B_C_JA_M):
            self._ERRORID = 548
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            self._ERROR = True
            return

        if self.MOVETYPE == 1:
            self.M_MOVETYPE = 20
            self.JA_MOVETYPEACTIVE = 1
        elif self.MOVETYPE == 2:
            self.M_MOVETYPE = 21
            self.JA_MOVETYPEACTIVE = 2
        else:
            self._ERRORID = 590
            self._ERROR = True
            return
        
    
        self.JA_MOVETYPECHANGED = self.JA_MOVETYPEACTIVE != self.JA_MOVETYPELAST
        if self.JA_MOVETYPECHANGED:
            self.M_EXECUTEABORT = True

        self.JA_COORDSYSACTIVE.BASE = self.COORDINATESYSTEM.BASE
        self.JA_BASECHANGED = self.JA_COORDSYSLAST.BASE != self.JA_COORDSYSACTIVE.BASE
        if self.JA_BASECHANGED:
            self.M_EXECUTEABORT = True

        self.JA_COORDSYSACTIVE.TOOL = self.COORDINATESYSTEM.TOOL
        self.JA_TOOLCHANGED = self.JA_COORDSYSLAST.TOOL != self.JA_COORDSYSACTIVE.TOOL
        if self.JA_TOOLCHANGED:
            self.M_EXECUTEABORT = True

        self.JA_COORDSYSACTIVE.IPO_MODE = self.COORDINATESYSTEM.IPO_MODE
        self.JA_IPOCHANGED = self.JA_COORDSYSLAST.IPO_MODE != self.JA_COORDSYSACTIVE.IPO_MODE
        if self.JA_IPOCHANGED:
            self.M_EXECUTEABORT = True

        if self.JOGADVANCED:
            self.JA_BUTTONACTIVE = self.B_A1_JA_P or self.B_A1_JA_M or self.B_A2_JA_P or self.B_A2_JA_M or self.B_A3_JA_P or self.B_A3_JA_M or self.B_A4_JA_P or self.B_A4_JA_M or self.B_A5_JA_P or self.B_A5_JA_M or self.B_A6_JA_P or self.B_A6_JA_M or self.B_E1_JA_P or self.B_E1_JA_M or self.B_E2_JA_P or self.B_E2_JA_M or self.B_E3_JA_P or self.B_E3_JA_M or self.B_E4_JA_P or self.B_E4_JA_M or self.B_E5_JA_P or self.B_E5_JA_M or self.B_E6_JA_P or self.B_E6_JA_M or self.B_X_JA_P or self.B_X_JA_M or self.B_Y_JA_P or self.B_Y_JA_M or self.B_Z_JA_P or self.B_Z_JA_M or self.B_A_JA_P or self.B_A_JA_M or self.B_B_JA_P or self.B_B_JA_M or self.B_C_JA_P or self.B_C_JA_M

            if self.JA_BUTTONACTIVE:
                if self.B_A1_JA_P: self.JA_STATE_VAL = 1  # A1 +
                if self.B_A1_JA_M: self.JA_STATE_VAL = 2  # A1 -
                if self.B_A2_JA_P: self.JA_STATE_VAL = 3  # A2 +
                if self.B_A2_JA_M: self.JA_STATE_VAL = 4  # A2 -
                if self.B_A3_JA_P: self.JA_STATE_VAL = 5  # A3 +
                if self.B_A3_JA_M: self.JA_STATE_VAL = 6  # A3 -
                if self.B_A4_JA_P: self.JA_STATE_VAL = 7  # A4 +
                if self.B_A4_JA_M: self.JA_STATE_VAL = 8  # A4 -
                if self.B_A5_JA_P: self.JA_STATE_VAL = 9  # A5 +
                if self.B_A5_JA_M: self.JA_STATE_VAL = 10  # A5 -
                if self.B_A6_JA_P: self.JA_STATE_VAL = 11  # A6 +
                if self.B_A6_JA_M: self.JA_STATE_VAL = 12  # A6 -
                if self.B_E1_JA_P: self.JA_STATE_VAL = 13  # E1 +
                if self.B_E1_JA_M: self.JA_STATE_VAL = 14  # E1 -
                if self.B_E2_JA_P: self.JA_STATE_VAL = 15  # E2 +
                if self.B_E2_JA_M: self.JA_STATE_VAL = 16  # E2 -
                if self.B_E3_JA_P: self.JA_STATE_VAL = 17  # E3 +
                if self.B_E3_JA_M: self.JA_STATE_VAL = 18  # E3 -
                if self.B_E4_JA_P: self.JA_STATE_VAL = 19  # E4 +
                if self.B_E4_JA_M: self.JA_STATE_VAL = 20  # E4 -
                if self.B_E5_JA_P: self.JA_STATE_VAL = 21  # E5 +
                if self.B_E5_JA_M: self.JA_STATE_VAL = 22  # E5 -
                if self.B_E6_JA_P: self.JA_STATE_VAL = 23  # E6 +
                if self.B_E6_JA_M: self.JA_STATE_VAL = 24  # E6 -
                if self.B_X_JA_P: self.JA_STATE_VAL = 25  # X +
                if self.B_X_JA_M: self.JA_STATE_VAL = 26  # X -
                if self.B_Y_JA_P: self.JA_STATE_VAL = 27  # Y +
                if self.B_Y_JA_M: self.JA_STATE_VAL = 28  # Y -
                if self.B_Z_JA_P: self.JA_STATE_VAL = 29  # Z +
                if self.B_Z_JA_M: self.JA_STATE_VAL = 30  # Z -
                if self.B_A_JA_P: self.JA_STATE_VAL = 31  # A +
                if self.B_A_JA_M: self.JA_STATE_VAL = 32  # A -
                if self.B_B_JA_P: self.JA_STATE_VAL = 33  # B +
                if self.B_B_JA_M: self.JA_STATE_VAL = 34  # B -
                if self.B_C_JA_P: self.JA_STATE_VAL = 35  # C +
                if self.B_C_JA_M: self.JA_STATE_VAL = 36  # C -
            else:
                self.JA_STATE_VAL = 0  # Roboter stopped

#part 3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].JOG_ADVANCED.JOG_AD_STATE_VAL = self.JA_STATE_VAL
            self.JA_BUTTONCHANGED = self.JA_BUTTONLAST != self.JA_BUTTONACTIVE
            self.JA_BUTTONLAST = self.JA_BUTTONACTIVE

            if self.JA_BUTTONCHANGED and not self.JA_BUTTONACTIVE:
                self.JA_STATE_VAL = 0  # robot stopped
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].JOG_ADVANCED.JOG_AD_STATE_VAL = self.JA_STATE_VAL
    

        # Call FB KRC_Move_1
        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 1
        self.KRC_MOVE_1.EXECUTECMD = self.JOGADVANCED and self._ERRORID == 0 and not self.M_EXECUTEABORT
        self.KRC_MOVE_1.MOVETYPE = self.M_MOVETYPE
        self.KRC_MOVE_1.ACTPOSITION = self.M_POSITION
        self.KRC_MOVE_1.AXISPOSITION = self.M_AXISPOSITION
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.COORDINATESYSTEM
        self.KRC_MOVE_1.ORITYPE = 0
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = False
        self.KRC_MOVE_1.POSVALIDT = False
        self.KRC_MOVE_1.BUFFERMODE = 1
        self.KRC_MOVE_1.OnCycle( )
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = self._ERRORID !=  0   
        # Call FB KRC_Abort_1
        self.KRC_ABORT_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_ABORT_1.EXECUTECMD = self.M_EXECUTEABORT
        self.KRC_ABORT_1.OnCycle()    
        if self.KRC_ABORT_1.ERROR or self.KRC_ABORT_1.DONE:
            self.M_EXECUTEABORT = False
        self._ERRORID = self.KRC_ABORT_1.ERRORID  
        # Abort -> program jumps out of mxA_Move returns to mxA_CommandDispatcher -> Busy output reset
        if self.JOGADVANCED and not self.KRC_MOVE_1.ABORTED:
            self._BUSY = True
        elif self.JOGADVANCED and self.KRC_MOVE_1.ABORTED:
            self._BUSY = False
        if self.JOGADVANCED and (self.MOVETYPE == 1 or self.MOVETYPE == 2) and self._BUSY:
            self._ACTIVE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.PRO_MOVE 
        self.JA_MOVETYPELAST = self.JA_MOVETYPEACTIVE
        self.JA_COORDSYSLAST.BASE = self.JA_COORDSYSACTIVE.BASE
        self.JA_COORDSYSLAST.TOOL = self.JA_COORDSYSACTIVE.TOOL
        self.JA_COORDSYSLAST.IPO_MODE = self.JA_COORDSYSACTIVE.IPO_MODE 

        if self.M_EXECUTEABORT:
            self._ORDERID = self.KRC_ABORT_1.ORDERID
        elif self.JOGADVANCED and self._ERRORID == 0:
            self._ORDERID = self.KRC_MOVE_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_ABORTADVANCED
#  ******************************************************************************/

class KRC_ABORTADVANCED:
    """
    The function block KRC_AbortAdvanced cancels active and buffered statements and motions. The parameter Active specifies whether or not the statement is still being executed. If the robot interpreter is no longer active, this can result in the statement being transferred, but not yet fully executed. Statements and motions of function blocks without BufferMode or QueueMode that are executed cyclically are not canceled. The parameter BrakeReaction can be used to define the braking reaction of the robot. KRC_AbortAdvanced is not processed if the KRC_Interrupt function block is active. In this case, the program must first be resumed with KRC_Continue before it can be aborted with KRC_AbortAdvanced.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    BrakeReaction (int): Braking reaction of the robot. Options: 1 (BRAKE), 2 (BRAKE F - default), 3 (BRAKE FF).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed.
    Done (bool): TRUE = statement has been executed.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.BRAKEREACTION = 0
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.NSTATE = 0


    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        if not self.EXECUTECMD:
            self.NSTATE = 0

        # Call FB MXA_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 58
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 1
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = self.BRAKEREACTION
            self.NSTATE = 1

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ABORTACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE or self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_INTERRUPT
#  ******************************************************************************/

class KRC_INTERRUPT:
    """
    The function block KRC_Interrupt is used to stop the robot. It brakes either gently (BRAKE) or as quickly as possible (BRAKE F) from high velocities. If a BRAKE statement is active, no more statements are processed via the mxA interface. The function block KRC_Abort is also no longer processed. KRC_Abort cannot cancel the program until it has been resumed with KRC_Continue, i.e. the BRAKE statement is no longer active. While the BRAKE statement is active, the program can only be canceled by means of a RESET of the function block KRC_AutomaticExternal.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    Execute (bool): The statement is executed in the case of a rising edge of the signal. The robot program is interrupted for as long as the input Execute is set to TRUE.
    Fast (bool): TRUE = robot stops as quickly as possible, FALSE = robot stops gently.

    Returns:
    BrakeActive (bool): TRUE = statement is active and robot is waiting for enabling.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTE = False
        self.FAST = False
        self._BRAKEACTIVE = False
        self._ERROR = False
        self._ERRORID = 0


    @property
    def BRAKEACTIVE(self):
        return self._BRAKEACTIVE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    def OnCycle(self):
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        if self.EXECUTE:
            if self.FAST:
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.BRAKEF = True
            else:
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.BRAKE = True

        self._BRAKEACTIVE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.BRAKEACTIVE


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CONTINUE
#  ******************************************************************************/

class KRC_CONTINUE:
    """
    The function block KRC_Continue can be used to resume execution of a program that has been stopped by means of an interrupt. If KRC_Continue is used together with KRC_Interrupt, the input Execute for KRC_Interrupt must have the value FALSE before KRC_Continue can be executed.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    Enable (bool): The statement is executed in the case of a rising edge of the signal.

    Returns:
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.ENABLE = False
        self._ERROR = False
        self._ERRORID = 0

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID


    def OnCycle(self):
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        if self.ENABLE:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.RELEASEBRAKE = self.ENABLE


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_WAITFORINPUT
#  ******************************************************************************/

class KRC_WAITFORINPUT:
    """
    The function block KRC_WaitForInput stops the program until a digital input takes a defined value. Program execution is then resumed.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    Number (int): Number of the digital input (corresponds to $IN[1 … 2048] on the robot controller). Range: 1-2048.
    Value (bool): Value of the digital input.
    bContinue (bool): TRUE = poll input in advance run. The robot controller executes programs with an advance run and a main run.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed (robot is waiting for an input).
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.NUMBER = 0
        self.VALUE = False
        self.BCONTINUE = False
        self.BUFFERMODE = 0
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        # Call FB MXA_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 32
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.BCONTINUE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[2] = self.VALUE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.NUMBER)

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1.ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_DECLAREINTERRUPT
#  ******************************************************************************/

class KRC_DECLAREINTERRUPT:
    """
    The function block KRC_DeclareInterrupt declares an interrupt to a digital input. There are 8 predefined interrupts available for this. An interrupt can be used to stop the robot during the motion. Depending on how the Reaction parameter is configured, the robot brakes gently from high velocities (BRAKE) or as quickly as possible (BRAKE F). The remaining program sequence can be determined using a robot input or a PLC function block. If a BRAKE statement is active, no more statements are processed via the mxA interface. The function block KRC_Abort is also no longer processed. KRC_Abort cannot cancel the program until it has been resumed with KRC_Continue, i.e. the BRAKE statement is no longer active. While the BRAKE statement is active, the program can only be canceled by means of a RESET of the function block KRC_AutomaticExternal.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is buffered in the case of a rising edge of the signal.
    Interrupt (int): Number of the interrupt. Range: 1-8. Note: Number 1 is the interrupt with the highest priority.
    Input (int): Number of the digital input to which the interrupt is declared. Range: 1-2048. Note: It must be ensured that no inputs are used that are already assigned by the system. Example: $IN[1025] is always TRUE.
    InputValue (bool): TRUE = statement is executed in the case of a rising edge of the signal. FALSE = statement is executed in the case of a falling edge of the signal.
    Reaction (int): Reaction to the interrupt. Options: 0 (Brake fast and wait for the EXT_START parameter of the function block KRC_AutomaticExternal), 1 (Brake normally and wait for the EXT_START parameter of the function block KRC_AutomaticExternal), 2 (Brake fast and wait for the Input parameter), 3 (Brake normally and wait for the Input parameter), 4 (Brake fast and wait for the edge of the function block KRC_Continue), 5 (Brake normally and wait for the edge of the function block KRC_Continue), 6 (Brake fast and wait for the edge of the function block KRC_Continue and the Input parameter), 7 (Brake normally and wait for the edge of the function block KRC_Continue and the Input parameter).
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been processed. Note: The statement can no longer be aborted. Exception: Program is deselected or reset.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.INTERRUPT = 0
        self.INPUT = 0
        self.INPUTVALUE = False
        self.REACTION = 0
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        # Call FB MXA_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 5
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.INPUTVALUE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.INTERRUPT)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = int(self.REACTION)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = int(self.INPUT)

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_ACTIVATEINTERRUPT
#  ******************************************************************************/

class KRC_ACTIVATEINTERRUPT:
    """
    The function block KRC_ActivateInterrupt activates a previously declared interrupt. There are 8 predefined interrupts available for this. The function block KRC_ReadInterruptState can be used to monitor and check whether an interrupt is active.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is buffered in the case of a rising edge of the signal.
    Interrupt (int): Number of the interrupt. Range: 1-8.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been processed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.INTERRUPT = 0
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        # Call FB MXA_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 6
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.INTERRUPT)

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_DEACTIVATEINTERRUPT
#  ******************************************************************************/

class KRC_DEACTIVATEINTERRUPT:
    """
    The function block KRC_DeactivateInterrupt deactivates a previously declared interrupt. There are 8 predefined interrupts available for this.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is buffered in the case of a rising edge of the signal.
    Interrupt (int): Number of the interrupt. Range: 1-8.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.INTERRUPT = 0
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        # Call FB MXA_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 7
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.INTERRUPT)

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READINTERRUPTSTATE
#  ******************************************************************************/

class KRC_READINTERRUPTSTATE:
    """
    The function block KRC_ReadInterruptState reads the state of an interrupt. This is updated cyclically.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    Interrupt (int): Number of the interrupt. Range: 1-8.

    Returns:
    Valid (bool): TRUE = data are valid.
    Value (int): State of specified interrupt. Options: 0 (Interrupt has not been declared), 1 (Interrupt has been declared), 2 (Interrupt has been declared and activated), 3 (Interrupt has been declared and activated and has now been deactivated again), 4 (Interrupt has been triggered and is active), 5 (Interrupt has been triggered and the main program has already been resumed with the function block KRC_Continue).
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.INTERRUPT = 0
        self._VALID = False
        self._VALUE = 0
        self._ERROR = False
        self._ERRORID = 0

    @property
    def VALID(self):
        return self._VALID

    @property
    def VALUE(self):
        return self._VALUE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    def OnCycle(self):
        self._ERRORID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        if 1 <= self.INTERRUPT <= 8:
            self._VALUE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.INTERRUPTSTATE[self.INTERRUPT]
            self._VALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE
        else:
            self._VALUE = 0
            self._VALID = False



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_SETDISTANCETRIGGER
#  ******************************************************************************/

class KRC_SETDISTANCETRIGGER:
    """
    The function block KRC_SetDistanceTrigger triggers a path-related switching action in the case of PTP or LIN motions. The Trigger triggers a defined statement. The statement refers to the start point or end point of the motion block. The statement is executed parallel to the robot motion. The statement can be shifted in time. It is then not triggered exactly at the start or end point, but brought forward or delayed. Further information on triggers, on offsetting the switching point and on the offset limits can be found in the operating and programming instructions for the KUKA System Software (KSS).

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is buffered in the case of a rising edge of the signal.
    Distance (int): Switching point of the trigger. Options: 0 (Switching action at the start point), 1 (Switching action at the end point).
    Delay (int): Statement delay. Delay = 0 ms: no delay. The statement cannot be shifted freely in time. The shifts that are available depend on the value selected for Distance.
    Output (int): Number of the digital output that can be set by the switching action. Range: 1-2048. Note: It must be ensured that no outputs are used that are already assigned by the system. Example: $OUT[1025] is always TRUE.
    Value (bool): TRUE = activate output, FALSE = deactivate output.
    Pulse (float): Length of the pulse. Range: 0.0-3.0 s. Pulse interval = 0.1 s.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been processed. Note: The statement can no longer be aborted. Exception: Program is deselected or reset. The signal does not indicate whether the switching action has really been triggered.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.DISTANCE = 0
        self.DELAY = 0
        self.OUTPUT = 0
        self.VALUE = False
        self.PULSE = 0.0
        self.BUFFERMODE = 0

        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 3
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.VALUE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = self.DISTANCE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.DELAY
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = self.OUTPUT
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.PULSE

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_SETPATHTRIGGER
#  ******************************************************************************/

class KRC_SETPATHTRIGGER:
    """
    The function block KRC_SetPathTrigger triggers a path-related switching action in the case of CP motions. The Trigger triggers a defined statement. The statement refers to the end point of the motion block. The statement is executed parallel to the robot motion. The statement can be shifted in time and/or space. It is then not triggered exactly at the end point, but beforehand or afterwards. Path triggers can only be activated before CP motions. If the subsequent motion is not a CP motion, the robot controller issues an error message. Further information on triggers, on offsetting the switching point and on the offset limits can be found in the operating and programming instructions for the KUKA System Software (KSS).

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is buffered in the case of a rising edge of the signal.
    Path (float): Statement offset. If the statement is to be shifted in space, the desired distance from the end point must be specified here. If this end point is approximated, Path is the distance to the position on the approximate positioning arc closest to the end point. Path = 0.0 mm: no offset. Path > 0.0 mm: shifts the statement towards the end of the motion. Path < 0.0 mm: shifts the statement towards the start of the motion.
    Delay (int): Statement delay. Delay = 0 ms: no delay. The statement cannot be shifted freely in time. The offsets that are possible depend on the value selected for Path.
    Output (int): Number of the digital output that can be set by the switching action. Range: 1-2048. Note: It must be ensured that no outputs are used that are already assigned by the system. Example: $OUT[1025] is always TRUE.
    Value (bool): TRUE = activate output, FALSE = deactivate output.
    Pulse (float): Length of the pulse. Range: 0.0-3.0 s. Pulse interval = 0.1 s.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been processed. Note: The statement can no longer be aborted. Exception: Program is deselected or reset. The signal does not indicate whether the switching action has really been triggered.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.PATH = 0.0
        self.DELAY = 0
        self.OUTPUT = 0
        self.VALUE = False
        self.PULSE = 0.0
        self.BUFFERMODE = 0

        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 4
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.VALUE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.DELAY
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = self.OUTPUT
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.PULSE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.PATH

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READMXASTATUS
#  ******************************************************************************/

class KRC_READMXASTATUS:
    """
    The function block KRC_ReadMXAStatus reads the current state of the mxA interface.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.

    Returns:
    Status (int): Current state of the mxA interface. Options: 0 (Invalid - No function blocks can be processed. Frequent causes: Submit interpreter stopped or deselected, I/O error due to incorrect bus configuration, Robot controller not started), 1 (Error - An mxA error message is active. The error message must be reset with the function block KRC_MessageReset), 2 (ProgramStopped - Robot interpreter is not active (main program has been stopped or deselected)), 3 (StandBy - Robot interpreter is active and waiting for statements, e.g. waiting for an input), 4 (Executing - Robot interpreter is active (main program is being executed)), 5 (Aborting - Robot stopped and all statements aborted).
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self._STATUS = 0
        self._ERROR = False
        self._ERRORID = 0

    @property
    def STATUS(self):
        return self._STATUS

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    def OnCycle(self):
        self._ERRORID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE:
            self._STATUS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.GROUPSTATE
        else:
            self._STATUS = 0





# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READKRCERROR
#  ******************************************************************************/

class KRC_READKRCERROR:
    """
    The function block KRC_ReadKRCError reads the current error state of the robot controller. Only error messages generated by the robot controller are displayed. Messages can only be reset if the robot is stationary.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    Offset (int): If there are more than 10 messages in the message buffer, the desired start index of the message buffer can be selected using the offset. Example: If there are 15 messages in the message buffer, the offset must be 6 in order to read messages 6 to 15.

    Returns:
    Done (bool): TRUE = data are valid.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    STOPMESS (bool): TRUE = safety circuit is interrupted (robot fault).
    MessageCount (int): Number of messages in the message buffer.
    Message1 (int): The number of the first message in the message buffer.
    Message2 (int): The number of the second message in the message buffer.
    Message3 (int): The number of the third message in the message buffer.
    Message4 (int): The number of the fourth message in the message buffer.
    Message5 (int): The number of the fifth message in the message buffer.
    Message6 (int): The number of the sixth message in the message buffer.
    Message7 (int): The number of the seventh message in the message buffer.
    Message8 (int): The number of the eighth message in the message buffer.
    Message9 (int): The number of the ninth message in the message buffer.
    Message10 (int): The number of the tenth message in the message buffer.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.OFFSET = 0

        self._DONE = False
        self._ERROR = False
        self._ERRORID = 0
        self._STOPMESS = False
        self._MESSAGECOUNT = 0
        self._MESSAGE1 = 0
        self._MESSAGE2 = 0
        self._MESSAGE3 = 0
        self._MESSAGE4 = 0
        self._MESSAGE5 = 0
        self._MESSAGE6 = 0
        self._MESSAGE7 = 0
        self._MESSAGE8 = 0
        self._MESSAGE9 = 0
        self._MESSAGE10 = 0
        self._ORDERID = 0

        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def STOPMESS(self):
        return self._STOPMESS

    @property
    def MESSAGECOUNT(self):
        return self._MESSAGECOUNT

    @property
    def MESSAGE1(self):
        return self._MESSAGE1

    @property
    def MESSAGE2(self):
        return self._MESSAGE2

    @property
    def MESSAGE3(self):
        return self._MESSAGE3

    @property
    def MESSAGE4(self):
        return self._MESSAGE4

    @property
    def MESSAGE5(self):
        return self._MESSAGE5

    @property
    def MESSAGE6(self):
        return self._MESSAGE6

    @property
    def MESSAGE7(self):
        return self._MESSAGE7

    @property
    def MESSAGE8(self):
        return self._MESSAGE8

    @property
    def MESSAGE9(self):
        return self._MESSAGE9

    @property
    def MESSAGE10(self):
        return self._MESSAGE10

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 24
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = self.OFFSET

        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._MESSAGECOUNT = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
            self._MESSAGE1 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2])
            self._MESSAGE2 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3])
            self._MESSAGE3 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4])
            self._MESSAGE4 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5])
            self._MESSAGE5 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6])
            self._MESSAGE6 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7])
            self._MESSAGE7 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8])
            self._MESSAGE8 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9])
            self._MESSAGE9 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10])
            self._MESSAGE10 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11])

        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._STOPMESS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.STOPMESS
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_DIAG
#  ******************************************************************************/
class KRC_DIAG:
    """
    The function block KRC_Diag reads the diagnostic signals of the robot controller. The function block may only be instanced once per axis group. In the case of multiple instancing, the signals of the most recently called function block are output.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ShowTrace (bool): TRUE = activate display of the active function blocks in the message window of the KUKA smartHMI. FALSE = deactivate display of the active function blocks in the message window of the KUKA smartHMI. Note: Only activate the display for test and diagnostic purposes. If the display is active, approximate positioning is no longer possible and the cycle time of the submit interpreter is adversely affected.
    MaxSubmitCycle (int): Maximum cycle time of the submit interpreter. Default: 1 000 ms. Note: If the maximum cycle time is exceeded, the $MOVE_ENABLE signal for motion enable is reset.

    Returns:
    Valid (bool): TRUE = data are valid.
    QueueCount (int): Number of buffered statements. Range: 1-90.
    PosActValid (bool): TRUE = position data are valid (BCO).
    BrakeActive (bool): TRUE = robot is stopped by means of a BRAKE statement.
    SubmitHeartbeat (int): Heartbeat signal of the submit interpreter (counter is incremented by 1 every Submit cycle). Range: 1-245. Note: During load data determination (function block KRC_LDDstart), it is possible for the heartbeat signal of the submit interpreter to be interrupted up to 400 ms.
    SubmitCyc_Act (float): Current cycle time of the submit interpreter; unit: ms. Mean value over 1,000 ms = 1/number of cycles per second.
    SubmitCyc_Min (float): Shortest cycle time of the submit interpreter since the last broken connection; unit: ms.
    SubmitCyc_Max (float): Longest cycle time of the submit interpreter since the last broken connection; unit: ms.
    SubmitCyc_Avg (int): Mean value of the cycle time of the submit interpreter during the calculation period Avg_Duration; unit: ms.
    ActivePosOrderID (int): Order ID of the KRC_Move motion command that is currently being executed.
    ActiveOrderIDB (int): Order ID of the current KRC_Move motion command in the advance run.
    Avg_Duration (int): Duration of the current calculation period for the mean value of the cycle time; unit: ms. The calculation period is restarted after a break in the connection to the submit interpreter or, at the latest, after 60 minutes.
    ProconosHeartbeat (int): Life sign from ProConOS (counter is incremented by 1 every ProConOS cycle).
    ProconosCyc_Act (int): Current cycle time of ProConOS; unit: ms. Mean value over 1,000 ms = 1/number of cycles per second.
    ProconosCyc_Min (int): Shortest cycle time of ProConOS since the last broken connection; unit: ms.
    ProconosCyc_Max (int): Longest cycle time of ProConOS since the last broken connection; unit: ms.
    ProconosCyc_Avg (int): Mean value of the cycle time of ProConOS during the calculation period Avg_Duration; unit: ms.
    ErrorID_RI (int): Robot interpreter error number.
    ErrorID_SI (int): Submit interpreter error number.
    ErrorID_PLC (int): PLC error number.
    ErrorID_PCOS (int): ProConOS error number.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    """
    def __init__(self):
        # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.SHOWTRACE = False
        self.MAXSUBMITCYCLE = 0

        # VAR_OUTPUT
        self._VALID = False
        self._QUEUECOUNT = 0
        self._POSACTVALID = False
        self._BRAKEACTIVE = False
        self._SUBMITHEARTBEAT = 0
        self._SUBMITCYC_ACT = 0
        self._SUBMITCYC_MIN = 0
        self._SUBMITCYC_MAX = 0
        self._SUBMITCYC_AVG = 0
        self._ACTIVEPOSORDERID = 0
        self._ACTIVEORDERIDB = 0
        self._AVG_DURATION = 0
        self._PROCONOSHEARTBEAT = 0
        self._PROCONOSCYC_ACT = 0
        self._PROCONOSCYC_MIN = 0
        self._PROCONOSCYC_MAX = 0
        self._PROCONOSCYC_AVG = 0
        self._ERRORID_RI = 0
        self._ERRORID_SI = 0
        self._ERRORID_PLC = 0
        self._ERRORID_PCOS = 0
        self._ERROR = False
        self._ERRORID = 0

        # VAR
        self.TON_1SEC = TON()
        self.HBLAST = 0
        self.HBCYCDIFF = 0
        self.HBSUM = 0
        self.CYCLCNT = 0
        self.PCOSHBLAST = 0
        self.PCOSHBCYCDIFF = 0
        self.PCOSHBSUM = 0
        self.SECSUM = 0

        # VAR_TEMP
        self.HBCYCDIFF1000 = 0
        self.CYCLCNT1000 = 0
        self.PCOSHBCYCDIFF1000 = 0


    # Properties for VAR_OUTPUT
    @property
    def VALID(self):
        return self._VALID

    @property
    def QUEUECOUNT(self):
        return self._QUEUECOUNT

    @property
    def POSACTVALID(self):
        return self._POSACTVALID

    @property
    def BRAKEACTIVE(self):
        return self._BRAKEACTIVE

    @property
    def SUBMITHEARTBEAT(self):
        return self._SUBMITHEARTBEAT

    @property
    def SUBMITCYC_ACT(self):
        return self._SUBMITCYC_ACT

    @property
    def SUBMITCYC_MIN(self):
        return self._SUBMITCYC_MIN

    @property
    def SUBMITCYC_MAX(self):
        return self._SUBMITCYC_MAX

    @property
    def SUBMITCYC_AVG(self):
        return self._SUBMITCYC_AVG

    @property
    def ACTIVEPOSORDERID(self):
        return self._ACTIVEPOSORDERID

    @property
    def ACTIVEORDERIDB(self):
        return self._ACTIVEORDERIDB

    @property
    def AVG_DURATION(self):
        return self._AVG_DURATION

    @property
    def PROCONOSHEARTBEAT(self):
        return self._PROCONOSHEARTBEAT

    @property
    def PROCONOSCYC_ACT(self):
        return self._PROCONOSCYC_ACT

    @property
    def PROCONOSCYC_MIN(self):
        return self._PROCONOSCYC_MIN

    @property
    def PROCONOSCYC_MAX(self):
        return self._PROCONOSCYC_MAX

    @property
    def PROCONOSCYC_AVG(self):
        return self._PROCONOSCYC_AVG

    @property
    def ERRORID_RI(self):
        return self._ERRORID_RI

    @property
    def ERRORID_SI(self):
        return self._ERRORID_SI

    @property
    def ERRORID_PLC(self):
        return self._ERRORID_PLC

    @property
    def ERRORID_PCOS(self):
        return self._ERRORID_PCOS

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    def OnCycle(self):
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False
        KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.SHOWTRACE = self.SHOWTRACE
        if self.MAXSUBMITCYCLE > 0:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].HEARTBEATTO = self.MAXSUBMITCYCLE
        self._VALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE
        self._QUEUECOUNT = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.QUEUECOUNT
        self._POSACTVALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACTVALID
        self._BRAKEACTIVE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.BRAKEACTIVE
        self._SUBMITHEARTBEAT = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEAT
        self._PROCONOSHEARTBEAT = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.HEARTBEATPCOS
        self._ACTIVEPOSORDERID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ACTIVEPOSORDERID
        self._ACTIVEORDERIDB = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ACTIVEORDERIDB
        self._ERRORID_RI = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORID
        self._ERRORID_SI = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORIDSUB
        self._ERRORID_PCOS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.ERRORIDPCOS
        self._ERRORID_PLC = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTERRORID
        if self._ERRORID_PCOS > 0:
            self._ERRORID_PCOS = self._ERRORID_PCOS + 700
        # Call FB TON_1Sec
        self.TON_1SEC.IN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE and not self.TON_1SEC._Q
        self.TON_1SEC.PT = MKTIME(1, 0, 1)
        self.TON_1SEC.OnCycle()
        self.CYCLCNT = self.CYCLCNT + 1
        if self.HBLAST <= self._SUBMITHEARTBEAT:
            self.HBCYCDIFF = self.HBCYCDIFF + (self._SUBMITHEARTBEAT - self.HBLAST)
        else:
            self.HBCYCDIFF = self.HBCYCDIFF + ((255 - self.HBLAST) + self._SUBMITHEARTBEAT)
        self.HBLAST = self._SUBMITHEARTBEAT
        if self.PCOSHBLAST <= self._PROCONOSHEARTBEAT:
            self.PCOSHBCYCDIFF = self.PCOSHBCYCDIFF + (self._PROCONOSHEARTBEAT - self.PCOSHBLAST)
        else:
            self.PCOSHBCYCDIFF = self.PCOSHBCYCDIFF + ((255 - self.PCOSHBLAST) + self._PROCONOSHEARTBEAT)
        self.PCOSHBLAST = self._PROCONOSHEARTBEAT
        if self.TON_1SEC._Q:
            self.HBCYCDIFF1000 = self.HBCYCDIFF
            self.PCOSHBCYCDIFF1000 = self.PCOSHBCYCDIFF
            self.CYCLCNT1000 = self.CYCLCNT
            if self.HBCYCDIFF > 0:
                self._SUBMITCYC_ACT = 1000 / self.HBCYCDIFF
            else:
                self._SUBMITCYC_ACT = -1
            if self._SUBMITCYC_MIN == 0:
                self._SUBMITCYC_MIN = DINT_TO_INT(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].HEARTBEATTO)
            if self._SUBMITCYC_ACT < self._SUBMITCYC_MIN and self._SUBMITCYC_ACT > 0:
                self._SUBMITCYC_MIN = self._SUBMITCYC_ACT
            if self._SUBMITCYC_ACT > self._SUBMITCYC_MAX:
                self._SUBMITCYC_MAX = self._SUBMITCYC_ACT
            if self.PCOSHBCYCDIFF > 0:
                self._PROCONOSCYC_ACT = DINT_TO_INT((1000 / self.PCOSHBCYCDIFF) + 0.5)
            else:
                self._PROCONOSCYC_ACT = -1
            if self._PROCONOSCYC_MIN == 0:
                self._PROCONOSCYC_MIN = DINT_TO_INT(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].HEARTBEATTO)
            if self._PROCONOSCYC_ACT < self._PROCONOSCYC_MIN and self._PROCONOSCYC_ACT > 0:
                self._PROCONOSCYC_MIN = self._PROCONOSCYC_ACT
            if self._PROCONOSCYC_ACT > self._PROCONOSCYC_MAX:
                self._PROCONOSCYC_MAX = self._PROCONOSCYC_ACT
            self.HBSUM = self.HBSUM + self.HBCYCDIFF
            self.PCOSHBSUM = self.PCOSHBSUM + self.PCOSHBCYCDIFF
            self.SECSUM = self.SECSUM + 1
            self._AVG_DURATION = self.SECSUM * 1000
            if self.HBSUM > 0:
                self._SUBMITCYC_AVG = DINT_TO_INT((self._AVG_DURATION / self.HBSUM) + 0.5)
            else:
                self._SUBMITCYC_AVG = -1
            if self.PCOSHBSUM > 0:
                self._PROCONOSCYC_AVG = DINT_TO_INT(self._AVG_DURATION / self.PCOSHBSUM)
            else:
                self._PROCONOSCYC_AVG = -1
            if self.SECSUM > 3600 or self._AVG_DURATION < self.HBSUM or self._AVG_DURATION < self.PCOSHBSUM:
                self.HBSUM = 0
                self.PCOSHBSUM = 0
                self.SECSUM = 0
                self._PROCONOSCYC_MIN = 0
                self._SUBMITCYC_MIN = 0
            self.CYCLCNT = 0
            self.HBCYCDIFF = 0
            self.PCOSHBCYCDIFF = 0
        if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE:
            self._SUBMITCYC_ACT = -1
            self._SUBMITCYC_MIN = DINT_TO_INT(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].HEARTBEATTO)
            self._SUBMITCYC_MAX = -1
            self._SUBMITCYC_AVG = -1
            self._AVG_DURATION = 0
            self._PROCONOSCYC_ACT = -1
            self._PROCONOSCYC_MIN = DINT_TO_INT(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].HEARTBEATTO)
            self._PROCONOSCYC_MAX = -1
            self._PROCONOSCYC_AVG = -1



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READSYSVAR
#  ******************************************************************************/

class KRC_READSYSVAR:
    """
    The function block KRC_ReadSysVar can be used to read system variables. So far, only the system variable $ADVANCE can be read. If required for the customer-specific application, the list of readable system variables can be expanded by KUKA.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    Index (int): Index of the system variable. Currently, only 1 ($ADVANCE) is supported.

    Returns:
    Done (bool): TRUE = statement has been executed.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    Value1 (float): Value of the first component of the system variable if it is a structure type.
    Value2 (float): Value of the second component of the system variable if it is a structure type.
    Value3 (float): Value of the third component of the system variable if it is a structure type.
    Value4 (float): Value of the fourth component of the system variable if it is a structure type.
    Value5 (float): Value of the fifth component of the system variable if it is a structure type.
    Value6 (float): Value of the sixth component of the system variable if it is a structure type.
    Value7 (float): Value of the seventh component of the system variable if it is a structure type.
    Value8 (float): Value of the eighth component of the system variable if it is a structure type.
    Value9 (float): Value of the ninth component of the system variable if it is a structure type.
    Value10 (float): Value of the tenth component of the system variable if it is a structure type.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.INDEX = 0
        self._DONE = False
        self._VALUE1 = 0.0
        self._VALUE2 = 0.0
        self._VALUE3 = 0.0
        self._VALUE4 = 0.0
        self._VALUE5 = 0.0
        self._VALUE6 = 0.0
        self._VALUE7 = 0.0
        self._VALUE8 = 0.0
        self._VALUE9 = 0.0
        self._VALUE10 = 0.0
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def DONE(self):
        return self._DONE

    @property
    def VALUE1(self):
        return self._VALUE1

    @property
    def VALUE2(self):
        return self._VALUE2

    @property
    def VALUE3(self):
        return self._VALUE3

    @property
    def VALUE4(self):
        return self._VALUE4

    @property
    def VALUE5(self):
        return self._VALUE5

    @property
    def VALUE6(self):
        return self._VALUE6

    @property
    def VALUE7(self):
        return self._VALUE7

    @property
    def VALUE8(self):
        return self._VALUE8

    @property
    def VALUE9(self):
        return self._VALUE9

    @property
    def VALUE10(self):
        return self._VALUE10

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 27
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.INDEX)
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._VALUE1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self._VALUE2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self._VALUE3 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self._VALUE4 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self._VALUE5 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self._VALUE6 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self._VALUE7 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7]
            self._VALUE8 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8]
            self._VALUE9 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self._VALUE10 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10]
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_WRITESYSVAR
#  ******************************************************************************/


class KRC_WRITESYSVAR:
    """
    The function block KRC_WriteSysVar can be used to write system variables. So far, only the system variable $ADVANCE can be written. If required for the customer-specific application, the list of writable system variables can be expanded by KUKA.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    Index (int): Index of the system variable. Currently, only 1 ($ADVANCE) is supported.
    Value1 (float): Value of the first component of the system variable if it is a structure type.
    Value2 (float): Value of the second component of the system variable if it is a structure type.
    Value3 (float): Value of the third component of the system variable if it is a structure type.
    Value4 (float): Value of the fourth component of the system variable if it is a structure type.
    Value5 (float): Value of the fifth component of the system variable if it is a structure type.
    Value6 (float): Value of the sixth component of the system variable if it is a structure type.
    Value7 (float): Value of the seventh component of the system variable if it is a structure type.
    Value8 (float): Value of the eighth component of the system variable if it is a structure type.
    Value9 (float): Value of the ninth component of the system variable if it is a structure type.
    Value10 (float): Value of the tenth component of the system variable if it is a structure type.
    bContinue (bool): TRUE = write to system variable without advance run stop. Note: Only possible for specific system variables.
    BufferMode (int): Mode in which the statement is executed. Options: 0 (DIRECT), 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.INDEX = 0
        self.VALUE1 = 0.0
        self.VALUE2 = 0.0
        self.VALUE3 = 0.0
        self.VALUE4 = 0.0
        self.VALUE5 = 0.0
        self.VALUE6 = 0.0
        self.VALUE7 = 0.0
        self.VALUE8 = 0.0
        self.VALUE9 = 0.0
        self.VALUE10 = 0.0
        self.BCONTINUE = False
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND() 


    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 28
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.BCONTINUE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.INDEX)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.VALUE1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.VALUE2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.VALUE3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.VALUE4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.VALUE5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.VALUE6
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = self.VALUE7
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = self.VALUE8
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = self.VALUE9
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[10] = self.VALUE10
        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_BRAKETEST
#  ******************************************************************************/

class KRC_BRAKETEST:
    """
    The function block KRC_BrakeTest calls the program for the brake test. The brake test is started at the position at which the robot is located when the program is called. The brake test must be performed with a program override of 100% (function block KRC_SetOverride). During the brake test, all brakes are checked to see whether the wear limit has been reached. For this purpose, the robot accelerates to a defined velocity limit. Once the robot has reached the velocity, the brake is applied and the result for this braking operation is displayed. If the brake test is successful, the robot is located back at the start position at the end of the measurement. If the brake test fails, i.e. a brake has been identified as being defective, the robot moves directly to a parking position. The coordinates of the parking position must be specified in the function block.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    ParkPosition ('E6POS'): Coordinates of the Cartesian parking position. The data structure E6POS contains all components of the parking position (= position of the TCP relative to the origin of the selected coordinate system).
    ParkVelocity (int): Velocity. Range: 0-100%. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type. Default: 0% (= velocity is not changed).
    ParkAcceleration (int): Acceleration. Range: 0-100%. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type. Default: 0% (= acceleration is not changed).
    ParkCoordinateSystem ('COORDSYS'): Coordinate system to which the Cartesian coordinates of the parking position refer.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = motion is currently being executed.
    Done (bool): TRUE = motion has stopped.
    Aborted (bool): TRUE = statement/motion has been aborted.
    Result (int): Result of the brake test. Options: 0 (brake test failed - brake identified as defective or no connection to robot controller), 1 (brake test successful - no brake defective, but at least one brake has reached the wear limit), 2 (brake test successful - no brake defective or reached wear limit).
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.PARKPOSITION = E6POS()
        self.PARKVELOCITY = 0
        self.PARKACCELERATION = 0
        self.PARKCOORDINATESYSTEM = COORDSYS()
        self.BUFFERMODE = 0
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._RESULT = 0
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.KRC_MOVE_1 = KRC_MOVE()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def RESULT(self):
        return self._RESULT

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            self._RESULT = 0
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 29
        self.KRC_MOVE_1.EXECUTECMD = self.EXECUTECMD
        self.KRC_MOVE_1.MOVETYPE = 1
        self.KRC_MOVE_1.ACTPOSITION = self.PARKPOSITION
        self.KRC_MOVE_1.VELOCITY = self.PARKVELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.PARKACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.PARKCOORDINATESYSTEM
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = True
        self.KRC_MOVE_1.POSVALIDT = True
        self.KRC_MOVE_1.BUFFERMODE = self.BUFFERMODE
        self.KRC_MOVE_1.OnCycle()
        self._BUSY = self.KRC_MOVE_1.BUSY
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._DONE = self.KRC_MOVE_1.DONE
        self._ABORTED = self.KRC_MOVE_1.ABORTED
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.KRC_MOVE_1.ORDERID
        if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE:
            if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKES_OK:
                if KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKETEST_WARN:
                    self._RESULT = 1
                else:
                    self._RESULT = 2
            else:
                self._RESULT = 0
        else:
            self._RESULT = 0



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_MASREF
#  ******************************************************************************/

class KRC_MASREF:
    """
    The function block KRC_MasRef is used to execute the mastering test. After the function block has been called, the robot moves in a linear direction from the current position to the reference position. Once the robot has reached the reference position, the current axis values are compared with the axis values which have been saved in KUKA.SafeOperation. The robot then moves back to the start position (= position before the function block was called). The reference position is defined in the function block with the input parameter Position and corresponds to the reference position defined with KUKA.SafeOperation. If the deviation between the current position and the reference position is too great, the mastering test has failed.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    Position ('E6POS'): Coordinates of the Cartesian reference position. The data structure E6POS contains all components of the reference position (= position of the TCP relative to the origin of the selected coordinate system).
    Velocity (int): Velocity. Range: 0-100%. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type. Default: 0% (= velocity is not changed).
    Acceleration (int): Acceleration. Range: 0-100%. Refers to the maximum value specified in the machine data. The maximum value is dependent on the robot type. Default: 0% (= acceleration is not changed).
    CoordinateSystem ('COORDSYS'): Coordinate system to which the Cartesian coordinates of the reference position refer.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = motion is currently being executed.
    Done (bool): TRUE = motion has stopped.
    Aborted (bool): TRUE = statement/motion has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    MasRefRequest (bool): TRUE = mastering test has been requested internally by the robot controller.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.POSITION = E6POS()
        self.VELOCITY = 0
        self.ACCELERATION = 0
        self.COORDINATESYSTEM = COORDSYS()
        self.BUFFERMODE = 0
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._MASREFREQUEST = False
        self._ORDERID = 0
        self.KRC_MOVE_1 = KRC_MOVE()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def MASREFREQUEST(self):
        return self._MASREFREQUEST

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            self._MASREFREQUEST = False
            return
        self.KRC_MOVE_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_MOVE_1.CMDID = 30
        self.KRC_MOVE_1.EXECUTECMD = self.EXECUTECMD
        self.KRC_MOVE_1.MOVETYPE = 1
        self.KRC_MOVE_1.ACTPOSITION = self.POSITION
        self.KRC_MOVE_1.VELOCITY = self.VELOCITY
        self.KRC_MOVE_1.ACCELERATION = self.ACCELERATION
        self.KRC_MOVE_1.COORDINATESYSTEM = self.COORDINATESYSTEM
        self.KRC_MOVE_1.POSVALIDX = True
        self.KRC_MOVE_1.POSVALIDY = True
        self.KRC_MOVE_1.POSVALIDZ = True
        self.KRC_MOVE_1.POSVALIDA = True
        self.KRC_MOVE_1.POSVALIDB = True
        self.KRC_MOVE_1.POSVALIDC = True
        self.KRC_MOVE_1.POSVALIDE1 = True
        self.KRC_MOVE_1.POSVALIDE2 = True
        self.KRC_MOVE_1.POSVALIDE3 = True
        self.KRC_MOVE_1.POSVALIDE4 = True
        self.KRC_MOVE_1.POSVALIDE5 = True
        self.KRC_MOVE_1.POSVALIDE6 = True
        self.KRC_MOVE_1.POSVALIDS = True
        self.KRC_MOVE_1.POSVALIDT = True
        self.KRC_MOVE_1.BUFFERMODE = self.BUFFERMODE
        self.KRC_MOVE_1.OnCycle()
        self._BUSY = self.KRC_MOVE_1.BUSY
        self._ACTIVE = self.KRC_MOVE_1.ACTIVE
        self._DONE = self.KRC_MOVE_1.DONE
        self._ABORTED = self.KRC_MOVE_1.ABORTED
        self._ERRORID = self.KRC_MOVE_1.ERRORID
        self._MASREFREQUEST = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.MASTERINGTEST_REQ_INT
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.KRC_MOVE_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READSAFEOPSTATUS
#  ******************************************************************************/

class KRC_READSAFEOPSTATUS:
    """
    The function block KRC_ReadSafeOPStatus reads signals of the safety controller. This is only relevant if KUKA.SafeOperation is installed.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    MASTERINGTEST_REQ_EXT (bool): TRUE = mastering test requested by the PLC.
    BRAKETEST_REQ_EXT (bool): TRUE = brake test requested by the PLC.

    Returns:
    Valid (bool): TRUE = data are valid.
    BRAKETEST_REQ_INT (bool): TRUE = brake test requested by the safety controller.
    MASTERINGTEST_REQ_INT (bool): TRUE = mastering test requested by the safety controller.
    BRAKETEST_MONTIME (bool): TRUE = robot was stopped due to elapsed brake test monitoring time.
    BRAKETEST_WORK (bool): TRUE = brake test is currently being performed.
    BRAKES_OK (bool): Edge TRUE --> FALSE: A brake has been identified as defective.
    BRAKETEST_WARN (bool): Edge FALSE --> TRUE: At least 1 brake has been detected as having reached the wear limit.
    MASTERINGTESTSWITCH_OK (bool): TRUE = reference switch is OK.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.MASTERINGTEST_REQ_EXT = False
        self.BRAKETEST_REQ_EXT = False
        self._VALID = False
        self._BRAKETEST_REQ_INT = False
        self._MASTERINGTEST_REQ_INT = False
        self._BRAKETEST_MONTIME = False
        self._BRAKETEST_WORK = False
        self._BRAKES_OK = False
        self._BRAKETEST_WARN = False
        self._MASTERINGTESTSWITCH_OK = False
        self._ERROR = False
        self._ERRORID = 0

    @property
    def VALID(self):
        return self._VALID

    @property
    def BRAKETEST_REQ_INT(self):
        return self._BRAKETEST_REQ_INT

    @property
    def MASTERINGTEST_REQ_INT(self):
        return self._MASTERINGTEST_REQ_INT

    @property
    def BRAKETEST_MONTIME(self):
        return self._BRAKETEST_MONTIME

    @property
    def BRAKETEST_WORK(self):
        return self._BRAKETEST_WORK

    @property
    def BRAKES_OK(self):
        return self._BRAKES_OK

    @property
    def BRAKETEST_WARN(self):
        return self._BRAKETEST_WARN

    @property
    def MASTERINGTESTSWITCH_OK(self):
        return self._MASTERINGTESTSWITCH_OK

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    def OnCycle(self):
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False
        if self.MASTERINGTEST_REQ_EXT:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.MASTERINGTEST_REQ_EXT = self.MASTERINGTEST_REQ_EXT
        if self.BRAKETEST_REQ_EXT:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTCONTROL.BRAKETEST_REQ_EXT = self.BRAKETEST_REQ_EXT
        self._VALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE
        self._BRAKES_OK = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKES_OK
        self._BRAKETEST_MONTIME = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKETEST_MONTIME
        self._BRAKETEST_REQ_INT = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKETEST_REQ_INT
        self._BRAKETEST_WARN = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKETEST_WARN
        self._BRAKETEST_WORK = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.BRAKETEST_WORK
        self._MASTERINGTEST_REQ_INT = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.MASTERINGTEST_REQ_INT
        self._MASTERINGTESTSWITCH_OK = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].AUTEXTSTATE.MASTERINGTESTSWITCH_OK


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READTOUCHUPSTATE
#  ******************************************************************************/
class KRC_READTOUCHUPSTATE:
    """
    The function block KRC_ReadTouchUPState reads the current state of the TouchUp status keys on the smartPAD. In order to be able to teach points using the status keys on the smartPAD, the function block must be linked to the function block KRC_TouchUP.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.

    Returns:
    Valid (bool): TRUE = data are valid.
    TouchUP (bool): State of the TouchUp status key on the smartPAD. TRUE = TouchUp status key has been pressed.
    Index (int): Number selected using the status key on the smartPAD to teach a position. Range: 1-100.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self._VALID = False
        self._TOUCHUP = False
        self._INDEX = 0
        self._ERROR = False
        self._ERRORID = 0

    @property
    def VALID(self):
        return self._VALID

    @property
    def TOUCHUP(self):
        return self._TOUCHUP

    @property
    def INDEX(self):
        return self._INDEX

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    def OnCycle(self):
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False
        self._VALID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE
        if self._VALID:
            self._TOUCHUP = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.TOUCHUP
            self._INDEX = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.TOUCHUP_INDEX
        else:
            self._TOUCHUP = False
            self._INDEX = 0


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_TOUCHUP
#  ******************************************************************************/

class KRC_TOUCHUP:
    """
    The function block KRC_TouchUP can be used to teach a point directly in the PLC. Tool, base and interpolation mode of this point are automatically saved by the function block.

    Parameters:
    PositionArray ('POSITION_ARRAY'): Array with the taught points and the corresponding coordinate systems. Note: The array can be used directly in the PLC.
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): TRUE = the point is taught.
    Index (int): Number under which the taught point is saved in the PLC. Range: 1-100.

    Returns:
    Done (bool): TRUE = statement has been executed.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.INDEX = 0
        self._DONE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.R_TRIG_1 = R_TRIG()
        self.M_POSINDEX = 0


    @property
    def DONE(self):
        return self._DONE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ERROR = True
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if self.EXECUTECMD:
            if self.INDEX < 1 or self.INDEX > 100:
                self._ERRORID = 513
            if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE:
                self._ERRORID = 509
            if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED:
                self._ERRORID = 508
            if not KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACTVALID:
                self._ERRORID = 514
        if self._ERRORID != 0:
            self._ERROR = True
            return
        self.R_TRIG_1.CLK = self.EXECUTECMD
        self.R_TRIG_1.OnCycle()
        if self.R_TRIG_1._Q:
            POSITION_ARRAY[self.INDEX].COORDSYS_1.TOOL = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.TOOLACT
            POSITION_ARRAY[self.INDEX].COORDSYS_1.BASE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.BASEACT
            POSITION_ARRAY[self.INDEX].COORDSYS_1.IPO_MODE = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.IPOMODEACT
            POSITION_ARRAY[self.INDEX].E6POS_1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.POSACT
            POSITION_ARRAY[self.INDEX].E6AXIS_1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXISACT
            self.M_POSINDEX = self.INDEX
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 34
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = self.M_POSINDEX
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_SETADVANCE
#  ******************************************************************************/

class KRC_SETADVANCE:
    """
    The function block KRC_SetAdvance modifies the settings for the advance run. The advance run is the maximum number of motion blocks that the robot controller calculates and plans in advance during program execution. The actual number is dependent on the capacity of the computer. The advance run is required, for example, in order to be able to calculate approximate positioning motions. If the program execution is reset, the set values are reset to the default values.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is buffered in the case of a rising edge of the signal.
    Count (int): Number of functions to be transferred before the first robot motion. Range: 1-50. Default value: 2.
    MaxWaitTime (int): Maximum wait time before the beginning of program execution if the set number of functions is not reached in the parameter count. Range: 1-32,767 ms. Default value: 300 ms.
    Mode (int): Wait mode. Options: 0 (The currently set mode is not changed), 1 (If the first instruction is an approximated motion instruction, the system waits for further instructions), 2 (The system always waits for the number of set functions or for the maximum wait time to elapse). Default value: 1.
    BufferMode (int): Mode in which the statement is executed. Options: 0 (DIRECT), 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement has been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.COUNT = 0
        self.MAXWAITTIME = 0
        self.MODE = 0
        self.BUFFERMODE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 36
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = self.COUNT
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.MAXWAITTIME
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = self.MODE
        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_GETADVANCE
#  ******************************************************************************/

class KRC_GETADVANCE:
    """
    The function block KRC_GetAdvance reads the values that have been set in the function block KRC_SetAdvance.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.

    Returns:
    Done (bool): TRUE = statement has been executed.
    Count (int): Number of functions to be transferred by the PLC before the first robot motion. Range: 1-50. Default value: 2.
    MaxWaitTime (int): Maximum wait time before the beginning of program execution if the set number of functions is not reached in the parameter count. Range: 1-32,767 ms. Default value: 300 ms.
    Mode (int): Wait mode. Options: 0 (The currently set mode is not changed), 1 (If the first instruction is an approximated motion instruction, the system waits for further instructions), 2 (The system always waits for the number of set functions or for the maximum wait time to elapse). Default value: 1.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self._DONE = False
        self._COUNT = 0
        self._MAXWAITTIME = 0
        self._MODE = 0
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def DONE(self):
        return self._DONE

    @property
    def COUNT(self):
        return self._COUNT

    @property
    def MAXWAITTIME(self):
        return self._MAXWAITTIME

    @property
    def MODE(self):
        return self._MODE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 37
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._COUNT = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
            self._MAXWAITTIME = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2])
            self._MODE = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3])
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_FORWARD
#  ******************************************************************************/

class KRC_FORWARD:
    """
    The function block KRC_Forward uses specified axis angles to calculate the Cartesian robot position.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the statement at a rising edge of the signal.
    Axis_Values ('E6AXIS'): Axis-specific values that are to be converted to Cartesian coordinates. The data structure E6AXIS contains the angle values or translation values for all axes of the axis group in this position.
    CheckSoftEnd (bool): Checks whether the specified axis angles lie within the software limit switches. If not, an error number is displayed.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Position ('E6POS'): Cartesian robot position calculated from the specified axis angles.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.AXIS_VALUES = E6AXIS()
        self.CHECKSOFTEND = False
        self.BUFFERMODE = 0

        self._BUSY = False
        self._DONE = False
        self._ACTPOSITION = E6POS()
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.NSTATE = 0
        self.MXA_EXECUTECOMMAND_0 = MXA_EXECUTECOMMAND()
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.MXA_EXECUTECOMMAND_2 = MXA_EXECUTECOMMAND()
        self.NORDERID = 0
        self.ERR_STATUS = 0.0
        self.M_POSITION = E6POS()
        self.NERR = 0

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def POSITION(self):
        return self._ACTPOSITION

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._ERRORID = 506
            self._ERROR = True
            return
        elif not self.EXECUTECMD:
            self._ERRORID = 0

        if not self.EXECUTECMD:
            self.NSTATE = 0
            self.NORDERID = 0
            self.M_POSITION.X = 0.0
            self.M_POSITION.Y = 0.0
            self.M_POSITION.Z = 0.0
            self.M_POSITION.A = 0.0
            self.M_POSITION.B = 0.0
            self.M_POSITION.C = 0.0
            self.M_POSITION.STATUS = 0
            self.M_POSITION.TURN = 0
            self.M_POSITION.E1 = 0.0
            self.M_POSITION.E2 = 0.0
            self.M_POSITION.E3 = 0.0
            self.M_POSITION.E4 = 0.0
            self.M_POSITION.E5 = 0.0
            self.M_POSITION.E6 = 0.0
            self._ACTPOSITION = self.M_POSITION

        self.MXA_EXECUTECOMMAND_0.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_0.EXECUTE = self.EXECUTECMD and (self.NSTATE == 0)
        self.MXA_EXECUTECOMMAND_0.CMDID = 52
        self.MXA_EXECUTECOMMAND_0.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_0.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_0.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_0.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_0.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_0.OnCycle()

        if self.MXA_EXECUTECOMMAND_0.WRITECMDPAR and (self.NSTATE == 0):
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.CHECKSOFTEND
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.AXIS_VALUES.A1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.AXIS_VALUES.A2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.AXIS_VALUES.A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.AXIS_VALUES.A4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.AXIS_VALUES.A5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.AXIS_VALUES.A6
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = self.AXIS_VALUES.E1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = self.AXIS_VALUES.E2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = self.AXIS_VALUES.E3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[10] = self.AXIS_VALUES.E4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[11] = self.AXIS_VALUES.E5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[12] = self.AXIS_VALUES.E6
            self.NORDERID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID

#part 2
            
        if self.MXA_EXECUTECOMMAND_0.DONE and self.NSTATE == 0:
            self.NSTATE = 1
        if self.MXA_EXECUTECOMMAND_0.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_0.ERRORID
            
        #Call FB mxA_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD and self.NSTATE == 1
        self.MXA_EXECUTECOMMAND_1.CMDID = 53
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR and self.NSTATE == 1:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = 1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.NORDERID

        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET and self.NSTATE == 1:
            self.M_POSITION.X = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self.M_POSITION.Y = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self.M_POSITION.Z = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self.M_POSITION.A = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self.M_POSITION.B = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self.M_POSITION.C = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self.M_POSITION.STATUS = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7])
            self.M_POSITION.TURN = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8])
            self.ERR_STATUS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self.NSTATE = 2

        if self.MXA_EXECUTECOMMAND_1.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID

        # Call FB mxA_ExecuteCommand_2
        self.MXA_EXECUTECOMMAND_2.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_2.EXECUTE = self.EXECUTECMD and (self.NSTATE == 2 or self.NSTATE == 3)
        self.MXA_EXECUTECOMMAND_2.CMDID = 53
        self.MXA_EXECUTECOMMAND_2.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_2.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_2.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_2.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_2.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_2.OnCycle()

        if self.MXA_EXECUTECOMMAND_2.WRITECMDPAR and self.NSTATE == 2:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = 2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.NORDERID

        if self.MXA_EXECUTECOMMAND_2.READCMDDATARET and self.NSTATE == 2:
            self.M_POSITION.E1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self.M_POSITION.E2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self.M_POSITION.E3 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self.M_POSITION.E4 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self.M_POSITION.E5 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self.M_POSITION.E6 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self.NSTATE = 3

        # part 3
        if self.MXA_EXECUTECOMMAND_2.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_2.ERRORID

        self._BUSY = self.MXA_EXECUTECOMMAND_0.BUSY or self.MXA_EXECUTECOMMAND_1.BUSY or self.MXA_EXECUTECOMMAND_2.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_2.DONE

        if self.NSTATE == 3:
            self._ACTPOSITION = self.M_POSITION
            self.NERR = int(self.ERR_STATUS)

            if self.NERR == -1:
                self._ERRORID = 533
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            elif self.NERR == -3:
                self._ERRORID = 534
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            elif self.NERR == -4:
                self._ERRORID = 535
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            elif self.NERR == 1:
                self._ERRORID = 536
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            elif self.NERR == 2:
                self._ERRORID = 537
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            elif self.NERR == 0:
                self._ERRORID = 0

        self._ERROR = self._ERRORID != 0

        if self.EXECUTECMD and self.NSTATE == 0:
            self._ORDERID = self.MXA_EXECUTECOMMAND_0.ORDERID
        elif self.EXECUTECMD and self.NSTATE == 1:
            self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID
        elif self.EXECUTECMD and (self.NSTATE == 2 or self.NSTATE == 3):
            self._ORDERID = self.MXA_EXECUTECOMMAND_2.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_FORWARDADVANCED
#  ******************************************************************************/


class KRC_FORWARDADVANCED:
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.AXIS_VALUES = E6AXIS()
        self.CHECKSOFTEND = False
        self.COORDINATESYSTEM = COORDSYS()

        self._BUSY = False
        self._DONE = False
        self._ACTPOSITION = E6POS()
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.NSTATE = 0
        self.MXA_EXECUTECOMMAND_0 = MXA_EXECUTECOMMAND()
        self.NORDERID = 0
        self.ERR_STATUS = 0.0
        self.M_POSITION = E6POS()
        self.NERR = 0

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def POSITION(self):
        return self._ACTPOSITION

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if not (1 <= self.AXISGROUPIDX <= 5):
            self._ERRORID = 506
            self._ERROR = True
            return
        elif not self.EXECUTECMD:
            self._ERRORID = 0

        if not self.EXECUTECMD:
            self.NSTATE = 0
            self.NORDERID = 0
            self.M_POSITION.X = 0.0
            self.M_POSITION.Y = 0.0
            self.M_POSITION.Z = 0.0
            self.M_POSITION.A = 0.0
            self.M_POSITION.B = 0.0
            self.M_POSITION.C = 0.0
            self.M_POSITION.STATUS = 0
            self.M_POSITION.TURN = 0
            self.M_POSITION.E1 = 0.0
            self.M_POSITION.E2 = 0.0
            self.M_POSITION.E3 = 0.0
            self.M_POSITION.E4 = 0.0
            self.M_POSITION.E5 = 0.0
            self.M_POSITION.E6 = 0.0
            self._ACTPOSITION = self.M_POSITION

        self.MXA_EXECUTECOMMAND_0.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_0.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_0.CMDID = 56
        self.MXA_EXECUTECOMMAND_0.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_0.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_0.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_0.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_0.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_0.OnCycle()

        if self.MXA_EXECUTECOMMAND_0.WRITECMDPAR and self.NSTATE == 0:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.CHECKSOFTEND
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.AXIS_VALUES.A1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.AXIS_VALUES.A2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.AXIS_VALUES.A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.AXIS_VALUES.A4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.AXIS_VALUES.A5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.AXIS_VALUES.A6
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = self.AXIS_VALUES.E1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = self.AXIS_VALUES.E2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = self.AXIS_VALUES.E3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[10] = self.AXIS_VALUES.E4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[11] = self.AXIS_VALUES.E5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[12] = self.AXIS_VALUES.E6
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = int(self.COORDINATESYSTEM.TOOL)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[4] = int(self.COORDINATESYSTEM.BASE)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[5] = int(self.COORDINATESYSTEM.IPO_MODE)

# part 2
            
        if self.MXA_EXECUTECOMMAND_0.READCMDDATARET and self.NSTATE == 0:
            self.M_POSITION.X = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self.M_POSITION.Y = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self.M_POSITION.Z = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self.M_POSITION.A = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self.M_POSITION.B = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self.M_POSITION.C = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self.M_POSITION.STATUS = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7])
            self.M_POSITION.TURN = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8])
            self.M_POSITION.E1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self.M_POSITION.E2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10]
            self.M_POSITION.E3 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11]
            self.ERR_STATUS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12]
            self.NSTATE = 1

        if self.MXA_EXECUTECOMMAND_0.DONE and self.NSTATE == 1:
            self.NSTATE = 2

        if self.MXA_EXECUTECOMMAND_0.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_0.ERRORID

        self._BUSY = self.MXA_EXECUTECOMMAND_0.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_0.DONE

        if self.NSTATE == 2:
            self._ACTPOSITION = self.M_POSITION
            self.NERR = int(self.ERR_STATUS)

            if self.NERR == -1:
                self._ERRORID = 533
            elif self.NERR == -3:
                self._ERRORID = 534
            elif self.NERR == -4:
                self._ERRORID = 535
            elif self.NERR == 1:
                self._ERRORID = 536
            elif self.NERR == 2:
                self._ERRORID = 537
            elif self.NERR == 4:
                self._ERRORID = 549
            elif self.NERR == 0:
                self._ERRORID = 0

        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_0.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_INVERSE
#  ******************************************************************************/

class KRC_INVERSE:
    """
    The function block KRC_Inverse uses a specified Cartesian robot position to calculate the axis angles.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the statement at a rising edge of the signal.
    Position ('E6POS'): Cartesian robot position.
    PosValidS (bool): TRUE = The Status value contained in the Position parameter is valid. FALSE = The Status value is unknown.
    PosValidT (bool): TRUE = The Turn value contained in the Position parameter is valid. FALSE = The Turn value is unknown.
    Start_Axis ('E6Axis'): Axis-specific values at the start point of the motion. The start point is the axis-specific position from which the robot moves to the position that is to be calculated.
    CheckSoftEnd (bool): Checks whether the values from the Start_Axis parameter lie within the software limit switches. If not, an error number is displayed.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    AxisPosition ('E6AXIS'): Axis angles that have been calculated from the specified Cartesian robot position. The data structure E6AXIS contains all the axis positions of the axis group.
    Aborted (bool): TRUE = statement was aborted before it was processed in the advance run.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.POSITION = E6POS()
        self.POSVALIDS = False
        self.POSVALIDT = False
        self.START_AXIS = E6AXIS()
        self.CHECKSOFTEND = False
        self.BUFFERMODE = 0

        self._BUSY = False
        self._DONE = False
        self._AXISPOSITION = E6AXIS()
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.NSTATE = 0
        self.MXA_EXECUTECOMMAND_0 = MXA_EXECUTECOMMAND()
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.MXA_EXECUTECOMMAND_2 = MXA_EXECUTECOMMAND()
        self.NORDERID = 0
        self.ERR_STATUS = 0.0
        self.M_POSITION = E6AXIS()
        self.NERR = 0

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def AXISPOSITION(self):
        return self._AXISPOSITION

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            if not self.EXECUTECMD:
                self._ERRORID = 0

        if not self.EXECUTECMD:
            self.NSTATE = 0
            self.NORDERID = 0
            self.M_POSITION.A1 = 0.0
            self.M_POSITION.A2 = 0.0
            self.M_POSITION.A3 = 0.0
            self.M_POSITION.A4 = 0.0
            self.M_POSITION.A5 = 0.0
            self.M_POSITION.A6 = 0.0
            self.M_POSITION.E1 = 0.0
            self.M_POSITION.E2 = 0.0
            self.M_POSITION.E3 = 0.0
            self.M_POSITION.E4 = 0.0
            self.M_POSITION.E5 = 0.0
            self.M_POSITION.E6 = 0.0
            self._AXISPOSITION = self.M_POSITION

        self.MXA_EXECUTECOMMAND_0.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_0.EXECUTE = self.EXECUTECMD and self.NSTATE == 0
        self.MXA_EXECUTECOMMAND_0.CMDID = 54
        self.MXA_EXECUTECOMMAND_0.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_0.COMMANDSIZE = 2
        self.MXA_EXECUTECOMMAND_0.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_0.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_0.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_0.OnCycle()

# part 2

        if self.MXA_EXECUTECOMMAND_0.WRITECMDPAR and self.NSTATE == 0:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.CHECKSOFTEND
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[2] = self.POSVALIDS
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[3] = self.POSVALIDT
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = self.POSITION.STATUS
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.POSITION.TURN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.POSITION.X
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.POSITION.Y
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.POSITION.Z
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.POSITION.A
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.POSITION.B
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.POSITION.C
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = self.POSITION.E1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = self.POSITION.E2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = self.POSITION.E3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[10] = self.POSITION.E4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[11] = self.POSITION.E5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[12] = self.POSITION.E6
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[13] = self.START_AXIS.A1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[14] = self.START_AXIS.A2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[15] = self.START_AXIS.A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[16] = self.START_AXIS.A4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[17] = self.START_AXIS.A5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[18] = self.START_AXIS.A6
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[19] = self.START_AXIS.E1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[20] = self.START_AXIS.E2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[21] = self.START_AXIS.E3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[22] = self.START_AXIS.E4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[23] = self.START_AXIS.E5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[24] = self.START_AXIS.E6
            self.NORDERID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID

        if self.MXA_EXECUTECOMMAND_0.DONE and self.NSTATE == 0:
            self.NSTATE = 1

        if self.MXA_EXECUTECOMMAND_0.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_0.ERRORID

        # Call FB mxA_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD and self.NSTATE == 1
        self.MXA_EXECUTECOMMAND_1.CMDID = 55
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR and self.NSTATE == 1:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = 1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.NORDERID

        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET and self.NSTATE == 1:
            self.M_POSITION.A1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self.M_POSITION.A2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self.M_POSITION.A3 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self.M_POSITION.A4 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self.M_POSITION.A5 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self.M_POSITION.A6 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self.ERR_STATUS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self.NSTATE = 2

# part 3 
            
        if self.MXA_EXECUTECOMMAND_1.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID

        # Call FB mxA_ExecuteCommand_2
        self.MXA_EXECUTECOMMAND_2.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_2.EXECUTE = self.EXECUTECMD and (self.NSTATE == 2 or self.NSTATE == 3)
        self.MXA_EXECUTECOMMAND_2.CMDID = 55
        self.MXA_EXECUTECOMMAND_2.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_2.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_2.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_2.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_2.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_2.OnCycle()

        if self.MXA_EXECUTECOMMAND_2.WRITECMDPAR and self.NSTATE == 2:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = 2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.NORDERID

        if self.MXA_EXECUTECOMMAND_2.READCMDDATARET and self.NSTATE == 2:
            self.M_POSITION.E1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self.M_POSITION.E2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self.M_POSITION.E3 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self.M_POSITION.E4 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self.M_POSITION.E5 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self.M_POSITION.E6 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self.NSTATE = 3

        if self.MXA_EXECUTECOMMAND_2.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_2.ERRORID

        if self.NSTATE == 3:
            self._AXISPOSITION = self.M_POSITION
            self.NERR = int(self.ERR_STATUS)
            if self.NERR == -1:
                self._ERRORID = 538
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            elif self.NERR == -3:
                self._ERRORID = 539
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            elif self.NERR == -4:
                self._ERRORID = 540
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            elif self.NERR == 1:
                self._ERRORID = 541
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            elif self.NERR == 2:
                self._ERRORID = 542
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            elif self.NERR == 3:
                self._ERRORID = 547
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            elif self.NERR == 0:
                self._ERRORID = 0

        self._ERROR = self._ERRORID != 0
        self._BUSY = self.MXA_EXECUTECOMMAND_0.BUSY or self.MXA_EXECUTECOMMAND_1.BUSY or self.MXA_EXECUTECOMMAND_2.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_2.DONE and not self._ERROR

        if self.EXECUTECMD and self.NSTATE == 0:
            self._ORDERID = self.MXA_EXECUTECOMMAND_0.ORDERID
        elif self.EXECUTECMD and self.NSTATE == 1:
            self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID
        elif self.EXECUTECMD and (self.NSTATE == 2 or self.NSTATE == 3):
            self._ORDERID = self.MXA_EXECUTECOMMAND_2.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_INVERSEADVANCED
#  ******************************************************************************/

class KRC_INVERSEADVANCED:
    """
    The function block KRC_InverseAdvanced uses a specified Cartesian robot
    position to calculate the axis angles. The TOOL and BASE coordinate
    systems and the interpolation mode are included in the calculation.
    The function is executed automatically in BufferMode 0 and can therefore
    be used independently of the motion execution.
    The specified value for the interpolation mode must match the current
    value on the robot controller.

    Parameters:
    AxisGroupIdx (int): Index of axis group, can be from 1 to 5.
    ExecuteCmd (bool): Starts/buffers the statement at a rising edge of the signal.
    Position (E6POS): Cartesian robot position. Note: External axes E4 to E6 are not taken into consideration in the calculation.
    PosValidS (bool): TRUE = the Status value contained in the Position parameter is valid. FALSE = the Status value is unknown.
    PosValidT (bool): TRUE = the Turn value contained in the Position parameter is valid. FALSE = the Turn value is unknown.
    Start_Axis (E6Axis): Axis-specific values at the start point of the motion. The start point is the axis-specific position from which the robot moves to the position that is to be calculated.
    CheckSoftEnd (bool): Checks whether the values from the Start_Axis parameter lie within the software limit switches. If not, an error number is displayed.
    CoordinateSystem (COORDSYS): Specification of the TOOL and BASE coordinate system and the interpolation mode.

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    AxisPosition (E6AXIS): Axis angles that have been calculated from the specified Cartesian robot position. The data structure E6AXIS contains all the axis positions of the axis group.
    Aborted (bool): TRUE = statement was aborted before it was processed in the advance run.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.POSITION = E6POS()
        self.POSVALIDS = False
        self.POSVALIDT = False
        self.START_AXIS = E6AXIS()
        self.CHECKSOFTEND = False
        self.COORDINATESYSTEM = COORDSYS()

        self._BUSY = False
        self._DONE = False
        self._AXISPOSITION = E6AXIS()
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.NSTATE = 0
        self.MXA_EXECUTECOMMAND_0 = MXA_EXECUTECOMMAND()
        self.NORDERID = 0
        self.ERR_STATUS = 0.0
        self.M_POSITION = E6AXIS()
        self.NERR = 0

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def AXISPOSITION(self):
        return self._AXISPOSITION

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            if not self.EXECUTECMD:
                self._ERRORID = 0

        if not self.EXECUTECMD:
            self.NSTATE = 0
            self.NORDERID = 0
            self.M_POSITION.A1 = 0.0
            self.M_POSITION.A2 = 0.0
            self.M_POSITION.A3 = 0.0
            self.M_POSITION.A4 = 0.0
            self.M_POSITION.A5 = 0.0
            self.M_POSITION.A6 = 0.0
            self.M_POSITION.E1 = 0.0
            self.M_POSITION.E2 = 0.0
            self.M_POSITION.E3 = 0.0
            self.M_POSITION.E4 = 0.0
            self.M_POSITION.E5 = 0.0
            self.M_POSITION.E6 = 0.0
            self._AXISPOSITION = self.M_POSITION

        self.MXA_EXECUTECOMMAND_0.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_0.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_0.CMDID = 57
        self.MXA_EXECUTECOMMAND_0.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_0.COMMANDSIZE = 2
        self.MXA_EXECUTECOMMAND_0.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_0.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_0.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_0.OnCycle()

        if self.MXA_EXECUTECOMMAND_0.WRITECMDPAR and self.NSTATE == 0:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.CHECKSOFTEND
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[2] = self.POSVALIDS
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[3] = self.POSVALIDT
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = self.POSITION.STATUS
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.POSITION.TURN
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.POSITION.X
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.POSITION.Y
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.POSITION.Z
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.POSITION.A
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.POSITION.B
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.POSITION.C
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = self.POSITION.E1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = self.POSITION.E2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = self.POSITION.E3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[10] = self.POSITION.E4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[11] = self.POSITION.E5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[12] = self.POSITION.E6
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[13] = self.START_AXIS.A1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[14] = self.START_AXIS.A2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[15] = self.START_AXIS.A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[16] = self.START_AXIS.A4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[17] = self.START_AXIS.A5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[18] = self.START_AXIS.A6
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[19] = self.START_AXIS.E1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[20] = self.START_AXIS.E2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[21] = self.START_AXIS.E3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[22] = self.START_AXIS.E4
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[23] = self.START_AXIS.E5
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[24] = self.START_AXIS.E6
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = int(self.COORDINATESYSTEM.TOOL)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[4] = int(self.COORDINATESYSTEM.BASE)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[5] = int(self.COORDINATESYSTEM.IPO_MODE)


        if self.MXA_EXECUTECOMMAND_0.READCMDDATARET and self.NSTATE == 0:
            self.M_POSITION.A1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self.M_POSITION.A2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self.M_POSITION.A3 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self.M_POSITION.A4 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self.M_POSITION.A5 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self.M_POSITION.A6 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self.M_POSITION.E1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self.M_POSITION.E2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10]
            self.M_POSITION.E3 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11]
            self.ERR_STATUS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12]
            self.NSTATE = 1

        if self.MXA_EXECUTECOMMAND_0.DONE and self.NSTATE == 1:
            self.NSTATE = 2

        if self.MXA_EXECUTECOMMAND_0.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_0.ERRORID

        if self.NSTATE == 2:
            self._AXISPOSITION = self.M_POSITION
            NERR = int(self.ERR_STATUS)
            if NERR == -1:
                self._ERRORID = 538
            elif NERR == -3:
                self._ERRORID = 539
            elif NERR == -4:
                self._ERRORID = 540
            elif NERR == 1:
                self._ERRORID = 541
            elif NERR == 2:
                self._ERRORID = 542
            elif NERR == 3:
                self._ERRORID = 547
            elif NERR == 4:
                self._ERRORID = 549
            elif NERR == 0:
                self._ERRORID = 0

        self._ERROR = self._ERRORID != 0
        self._BUSY = self.MXA_EXECUTECOMMAND_0.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_0.DONE and not self._ERROR
        self._ORDERID = self.MXA_EXECUTECOMMAND_0.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_TECHFUNCTION
#  ******************************************************************************/
        
class KRC_TECHFUNCTION:
    """
    Calles and executes KRL programs in the robot interpreter or submit interpreter.
    
    Parameters:
    BOOL_DATA (list[bool]): Array of type BOOL as transfer parameter.
    INT_DATA (list[int]): Array of type DINT as transfer parameter.
    REAL_DATA (list[float]): Array of type REAL as transfer parameter.
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    TechFunctionID (int): ID for selecting the function at KRL level (SWITCH CASE ID).
    ParameterCount (int): Maximum variable index that can be used for the parameters BOOL_DATA, INT_DATA and REAL_DATA. Range: 1-40.
    BufferMode (int): Mode in which the statement is executed. Options: 0 (DIRECT), 1 (ABORTING), 2 (BUFFERED).
    
    Returns:
        - 'Busy' (bool): TRUE if statement is currently being transferred or has already been transferred.
        - 'Active' (bool): TRUE if statement is currently being executed.
        - 'Done' (bool): TRUE if statement has been executed.
        - 'Aborted' (bool): TRUE if statement has been aborted.
        - 'Error' (bool): TRUE if there is an error in function block.
        - 'ErrorID' (int): Error number.
    OrderID (int): Identifier of command instance.

    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.TECHFUNCTIONID = 0
        self.PARAMETERCOUNT = 0
        self.BUFFERMODE = 0

        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.I = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

        self.BOOL_DATA = [False]*41  # Array of BOOL
        self.INT_DATA = [0]*41  # Array of DINT
        self.REAL_DATA = [0.0]*41  # Array of REAL


    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if self.PARAMETERCOUNT < 1 or self.PARAMETERCOUNT > 40:
            self._ERRORID = 521
            self._ERROR = True
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            return
        for self.I in range(self.PARAMETERCOUNT + 1, 40):
            if self.BOOL_DATA[self.I] or self.INT_DATA[self.I] != 0 or self.REAL_DATA[self.I] != 0.0:
                self._ERRORID = 522
                self._ERROR = True
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
                return

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 35
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 3
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[41] = int(self.TECHFUNCTIONID)
            for self.I in range(1, 41):
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[self.I] = self.BOOL_DATA[self.I]
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[self.I] = self.INT_DATA[self.I]
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[self.I] = self.REAL_DATA[self.I]

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1.ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_TECHFUNCTIONADVANCED
#  ******************************************************************************/

class KRC_TECHFUNCTIONADVANCED:
    """
    Executes KRL programs in the submit interpreter. The return values of the KRL function are output in the parameter ReturnValue.
    
    Parameters:
    BOOL_DATA (list[bool]): Array of type BOOL as transfer parameter. Range: 1-40.
    INT_DATA (list[int]): Array of type DINT as transfer parameter. Range: 1-40.
    REAL_DATA (list[float]): Array of type REAL as transfer parameter. Range: 1-40.
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    TechFunctionID (int): ID for selecting the function at KRL level (SWITCH CASE ID).
    ParameterCount (int): Maximum variable index that can be used for the parameters BOOL_DATA, INT_DATA and REAL_DATA. Range: 1-40.

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    ReturnValue (list[float]): Array of type REAL as return values from the KRL function. Range: 1-12.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.TECHFUNCTIONID = 0
        self.PARAMETERCOUNT = 0

        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._RETURNVALUE = [0.0]*13  # REAL_ARRAY_12
        self._ORDERID = 0

        self.I = 0
        self.NSTATE = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

        self.BOOL_DATA = [False]*41  # Array of BOOL
        self.INT_DATA = [0]*41  # Array of DINT
        self.REAL_DATA = [0.0]*41  # Array of REAL

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def RETURNVALUE(self):
        return self._RETURNVALUE

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        if self.PARAMETERCOUNT < 1 or self.PARAMETERCOUNT > 40:
            self._ERRORID = 521
            self._ERROR = True
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
            return
        if not self.EXECUTECMD:
            self.NSTATE = 0

        for self.I in range(self.PARAMETERCOUNT + 1, 40):
            if self.BOOL_DATA[self.I] or self.INT_DATA[self.I] != 0 or self.REAL_DATA[self.I] != 0.0:
                self._ERRORID = 522
                self._ERROR = True
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self._ERRORID
                return

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 59
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 3
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[41] = int(self.TECHFUNCTIONID)
            for self.I in range(1, 41):
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[self.I] = self.BOOL_DATA[self.I]
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[self.I] = self.INT_DATA[self.I]
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[self.I] = self.REAL_DATA[self.I]

        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET and self.NSTATE == 0:
            for self.I in range(1, 13):
                self._RETURNVALUE[self.I] = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[self.I]
            self.NSTATE = 1

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1.ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE and self.NSTATE == 1
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_ACTIVATEPOSCONVERSION
#  ******************************************************************************/

class KRC_ACTIVATEPOSCONVERSION:
    """
    The function block KRC_ActivatePosConversion can be used to display the current robot position relative to the selected TOOL or BASE coordinate system or interpolation mode.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    ActivateConversion (bool): TRUE = current robot position is displayed in the selected coordinate system. FALSE = current robot position is displayed in the current coordinate system of the robot controller.
    CoordSysToDisplay (COORDSYS): Coordinate system in which the current robot position is to be displayed.

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.ACTIVATECONVERSION = False
        self.COORDSYSTODISPLAY = COORDSYS()

        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  # MXA_EXECUTECOMMAND object
        

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 68
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 2
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.ACTIVATECONVERSION
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = int(self.COORDSYSTODISPLAY.TOOL)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[4] = int(self.COORDSYSTODISPLAY.BASE)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[5] = int(self.COORDSYSTODISPLAY.IPO_MODE)

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CONVINIT
#  ******************************************************************************/

class KRC_CONVINIT:
    """
    Resetting and initializing the ConveyorTech application (initializing and activating all conveyors)

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    BufferMode (int): Mode in which the statement is executed [0: DIRECT, 1: ABORTING, 2: BUFFERED]

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """

    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.BUFFERMODE = 2

        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY
    
    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 39
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1.ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CONVSCENEEXISTS
#  ******************************************************************************/


class KRC_CONVSCENEEXISTS:
    """
    Checks whether conveyor scene with given parameters exists.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    ConveyorIndex (int):  Index of the selected conveyor [1-3]
    SceneSelection (int):  Type of scene selection, maps to [NextSyncable,Current,Next,Previous,Latest,StepScenes,AbsoluteScene]
    SceneStepOffset (int):  Step offset in case of selection type StepScenes
    SceneAbsoluteId (int):  ID of scene in case of selection type AbsoluteScene
    StartOfWorkareaOffset (float):  Offset for start of work area
    EndOfSyncAreaOffset (float):  Offset for end of sync area
    AlarmDistanceOffset (float):  Offset for alarm distance
    EndOfWorkAreaOffset (float):  Offset for end of work area

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Exists (bool): TRUE = scene with given parameters exists.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """

    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.CONVEYORINDEX = 0
        self.SCENESELECTION = 0
        self.SCENESTEPOFFSET = 0
        self.SCENEABSOLUTEID = 0
        self.STARTOFWORKAREAOFFSET = 0.0
        self.ENDOFSYNCAREAOFFSET = 0.0
        self.ALARMDISTANCEOFFSET = 0.0
        self.ENDOFWORKAREAOFFSET = 0.0

        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._EXISTS = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.MXA_EXECUTECOMMAND_1 =  MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED
    
    @property
    def EXISTS(self):
        return self._EXISTS

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 40
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.CONVEYORINDEX)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = int(self.SCENESELECTION)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = int(self.SCENESTEPOFFSET)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[4] = int(self.SCENEABSOLUTEID)
            
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.STARTOFWORKAREAOFFSET
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.ENDOFSYNCAREAOFFSET
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.ALARMDISTANCEOFFSET
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.ENDOFWORKAREAOFFSET

        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._EXISTS = bool(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CONVTRACKINGON
#  ******************************************************************************/

class KRC_CONVTRACKINGON:
    """
    Starts tracking a scene on a selected conveyor

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    ConveyorIndex (int):  Index of the selected conveyor [1-3]
    SceneSelection (int):  Type of scene selection, maps to [NextSyncable,Current,Next,Previous,Latest,StepScenes,AbsoluteScene]
    SceneStepOffset (int):  Step offset in case of selection type StepScenes
    SceneAbsoluteId (int):  ID of scene in case of selection type AbsoluteScene
    StartOfWorkareaOffset (float):  Offset for start of work area
    EndOfSyncAreaOffset (float):  Offset for end of sync area
    AlarmDistanceOffset (float):  Offset for alarm distance
    EndOfWorkAreaOffset (float):  Offset for end of work area
    RetractMotionVelocity (float):  Velocity of retraction motion in case of an interrupt
    RetractMotionAcceleration (float):  Acceleration of retraction motion in case of an interrupt
    RetractMotionVectorX (float):  X coordinate of retraction motion vector in case of an interrupt
    RetractMotionVectorY (float):  Y coordinate of retraction motion vector in case of an interrupt
    RetractMotionVectorZ (float):  Z coordinate of retraction motion vector in case of an interrupt
    BufferMode (int):  Mode in which the statement is executed [0: DIRECT, 1: ABORTING, 2: BUFFERED]

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.CONVEYORINDEX = 0
        self.SCENESELECTION = 0
        self.SCENESTEPOFFSET = 0
        self.SCENEABSOLUTEID = 0
        self.MOVETOSTANDBY = False
        self.STARTOFWORKAREAOFFSET = 0.0
        self.ENDOFSYNCAREAOFFSET = 0.0
        self.ALARMDISTANCEOFFSET = 0.0
        self.ENDOFWORKAREAOFFSET = 0.0
        self.RETRACTMOTIONVELOCITY = 0.0
        self.RETRACTMOTIONACCELERATION = 2.0
        self.RETRACTMOTIONVECTORX = 100.0
        self.RETRACTMOTIONVECTORY = 0.0
        self.RETRACTMOTIONVECTORZ = 0.0
        self.BUFFERMODE = 2

        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY
    
    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 41
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.CONVEYORINDEX)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = int(self.SCENESELECTION)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = int(self.SCENESTEPOFFSET)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[4] = int(self.SCENEABSOLUTEID)
            
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = self.MOVETOSTANDBY

            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.STARTOFWORKAREAOFFSET
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.ENDOFSYNCAREAOFFSET
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.ALARMDISTANCEOFFSET
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.ENDOFWORKAREAOFFSET
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.RETRACTMOTIONVELOCITY
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.RETRACTMOTIONACCELERATION
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = self.RETRACTMOTIONVECTORX
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = self.RETRACTMOTIONVECTORY
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = self.RETRACTMOTIONVECTORZ

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1.ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CONVTRACKINGOFF
#  ******************************************************************************/

class KRC_CONVTRACKINGOFF:
    """
    Finish tracking a workpiece on a conveyor.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    ExecuteType (int): Type of stopping mechanism, maps to [AdvanceRunStop,TrigStartPoint]
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.EXECUTIONTYPE = 0
        self.BUFFERMODE = 2

        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 42
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.EXECUTIONTYPE)

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1.ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_GETCONVSPEED
#  ******************************************************************************/

class KRC_GETCONVSPEED:
    """
    Retrieves speed of selected conveyor [mm/s]

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    ConveyorIndex (int):  Index of the selected conveyor [1-3]

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Speed (float): TRUE = speed of the selected conveyor.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.CONVEYORINDEX = 0

        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._SPEED = 0.0
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED
    
    @property
    def SPEED(self):
        return self._SPEED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 43
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.CONVEYORINDEX)

        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._SPEED = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_VECTORMOVEON
#  ******************************************************************************/

class KRC_VECTORMOVEON:
    """
    The function block KRC_VectorMoveOn is used to move a robot along a defined vector in Cartesian space. The robot is moved by an external force. The vector must be specified in relation to the TCP of the TOOL coordinate system. The last taught point before the function block is called is the root point of the vector.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    X (float): Defines the direction of the vector for translational motion. Limits: max. 200 mm in the positive and negative directions.
    Y (float): Defines the direction of the vector for translational motion. Limits: max. 200 mm in the positive and negative directions.
    Z (float): Defines the direction of the vector for translational motion. Limits: max. 200 mm in the positive and negative directions.
    A (float): Defines the direction of the vector for rotational motion. Limits: max. 30° in the positive and negative directions.
    B (float): Defines the direction of the vector for rotational motion. Limits: max. 30° in the positive and negative directions.
    C (float): Defines the direction of the vector for rotational motion. Limits: max. 30° in the positive and negative directions.
    VectorLimit (float): Permissible vector length limit. If this value is exceeded, the robot is stopped with ramp-down braking. Range: 0-30%. Default: 10%.
    MaxDuration (float): Length of time after which VectorMove is deactivated if an error has occurred. Range: 0-10000 s. Default: 100 s.
    TorqueOffsetValue (float): Defines the resistance torque of the robot (unit: Nm). The resistance torque is the torque with which the robot acts against the external force. It has the effect that the robot only begins to move when a specific amount of force is exerted. The resistance torque can be defined in addition to the holding torque. The holding torque depends on the robot position, type, size and additional load. Range: 1-200 Nm. Default: 1 Nm.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.A = 0.0
        self.B = 0.0
        self.C = 0.0
        self.VECTORLIMIT = 0.0
        self.MAXDURATION = 0.0
        self.TORQUEOFFSETVALUE = 0.0
        self.BUFFERMODE = 0

        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 44
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.X
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.Y
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.Z
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.A
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.B
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.C
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = self.VECTORLIMIT
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = self.MAXDURATION
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = self.TORQUEOFFSETVALUE

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_VECTORMOVEOFF
#  ******************************************************************************/
class KRC_VECTORMOVEOFF:
    """
    The function block KRC_VectorMoveOff is used to deactivate the motion along a vector.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.BUFFERMODE = 0

        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND() 

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 45
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_LDDCONFIG
#  ******************************************************************************/

class KRC_LDDCONFIG:
    """
    The function block KRC_LDDconfig is used to configure load data determination. 

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    LoadA3Settings (int): Defines the supplementary load on axis 3 for the robot. Options: 0 (No supplementary load), 1 (Maximum permissible load), 2 (Values from LOAD_A3_DATA defined during start-up are used), 3 (Transferred data from the function block are applied and saved in the file $config.dat).
    WarmUp (bool): Defines whether a warm-up is carried out before load data determination. TRUE = a warm-up is carried out, FALSE = no warm-up is carried out.
    M_A3 (float): Mass of the supplementary load on axis 3.
    X_A3, Y_A3, Z_A3 (float): Position of the center of mass of the supplementary load on axis 3 relative to the FLANGE coordinate system.
    A_A3, B_A3, C_A3 (float): Orientation of the center of mass of the supplementary load on axis 3 relative to the FLANGE coordinate system.
    JX_A3, JY_A3, JZ_A3 (float): Mass moments of inertia of the supplementary load on axis 3 relative to the FLANGE coordinate system.
    Mass (float): Payload. If ≤ 0, Payload is automatically determined. If > 0, Payload is already known from CAD data or a measurement.

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.LOADA3SETTINGS = 0
        self.M_A3 = 0.0
        self.X_A3 = 0.0
        self.Y_A3 = 0.0
        self.Z_A3 = 0.0
        self.A_A3 = 0.0
        self.B_A3 = 0.0
        self.C_A3 = 0.0
        self.JX_A3 = 0.0
        self.JY_A3 = 0.0
        self.JZ_A3 = 0.0
        self.MASS = 0.0

        self._BUSY = False
        self._DONE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.NORDERID = 0
        self.ERR_STATUS = 0.0
        self.NERR = 0
        self.NSTATE = 0

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if (self.AXISGROUPIDX < 1) or (self.AXISGROUPIDX > 5):
            self._ERRORID = 506
            self._ERROR = True
            return

        if not self.EXECUTECMD:
            self.NSTATE = 0

        # Execute LDD config function
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 60
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.LOADA3SETTINGS)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.M_A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.X_A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.Y_A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.Z_A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.A_A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.B_A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = self.C_A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = self.JX_A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = self.JY_A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[10] = self.JZ_A3
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[11] = self.MASS
            self.NORDERID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID

# part 2
        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self.ERR_STATUS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            print("LDD library Error-Status !!! :" , KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9] )
            self.NSTATE = 1

        if self.NSTATE == 1:
            self.NERR = int(self.ERR_STATUS)
            if self.NERR == -108:  # Internal: initializing LDD failed
                self._ERRORID = 550
            elif self.NERR == -109:  # Setting manual mass failed
                self._ERRORID = 551
            elif self.NERR == -110:  # Setting start position failed
                self._ERRORID = 552
            elif self.NERR == -111:  # Setting supplementary load failed
                self._ERRORID = 553
            elif self.NERR == -112:  # Internal: setting acceleration factor LDD failed
                self._ERRORID = 554
            elif self.NERR == -113:  # Internal: finalizing configuration failed
                self._ERRORID = 555
            elif self.NERR == -114:  #  Invalid supplementary load option selected (LoadA3Settings)
                self._ERRORID = 556
            else:
                self._ERRORID = 0

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = (self.MXA_EXECUTECOMMAND_1.DONE and (self.NSTATE == 1))
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID





# /******************************************************************************
#  * FUNCTION_BLOCK KRC_LDDTESTRUN
#  ******************************************************************************/

class KRC_LDDTESTRUN:
    
    """
    The function block KRC_LDDtestRun is used to carry out a test run without determination of the load data. The motion sequence for load data determination is carried out at low velocity. The purpose of the test run is to avoid possible collisions during load data determination. The test run before load data determination must be performed with a program override of ≤10% (function block KRC_SetOverride).

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """

    def __init__(self):
    # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False

    # VAR_OUTPUT
        self._BUSY = False
        self._DONE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

    # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.MXA_EXECUTECOMMAND_2 = MXA_EXECUTECOMMAND()
        self.NSTATE = 0
        self.NERR = 0
        self.ERR_STATUS = 0.0
        self.NORDERID = 0

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if (self.AXISGROUPIDX < 1) or (self.AXISGROUPIDX > 5):
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            if not self.EXECUTECMD:
                self._ERRORID = 0

        if not self.EXECUTECMD:
            self.NSTATE = 0
            self.NORDERID = 0

        if self.EXECUTECMD and (KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OVERRIDE > 10):
            self._ERRORID = 563
            self._ERROR = True
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            return

        # Execute LDD test function
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = (self.EXECUTECMD and self.NSTATE == 0)
        self.MXA_EXECUTECOMMAND_1.CMDID = 62
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 1
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR and self.NSTATE == 0:
            self.NORDERID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID

        if self.MXA_EXECUTECOMMAND_1.DONE and self.NSTATE == 0:
            self.NSTATE = 1

        if self.MXA_EXECUTECOMMAND_1.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID

        # Get return values if error happens
        self.MXA_EXECUTECOMMAND_2.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_2.EXECUTE = (self.EXECUTECMD and ((self.NSTATE == 1) or (self.NSTATE == 2)))
        self.MXA_EXECUTECOMMAND_2.CMDID = 63
        self.MXA_EXECUTECOMMAND_2.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_2.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_2.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_2.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_2.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_2.OnCycle()

        if self.MXA_EXECUTECOMMAND_2.WRITECMDPAR and self.NSTATE == 1:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.NORDERID

        if self.MXA_EXECUTECOMMAND_2.READCMDDATARET and self.NSTATE == 1:
            self.ERR_STATUS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self.NSTATE = 2

        if self.MXA_EXECUTECOMMAND_2.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_2.ERRORID
# part 2
        self._BUSY = (self.MXA_EXECUTECOMMAND_1.BUSY or self.MXA_EXECUTECOMMAND_2.BUSY)
        self._DONE = self.MXA_EXECUTECOMMAND_2.DONE

        if self.NSTATE == 2:
            self.NERR = int(self.ERR_STATUS)
            if self.NERR == -100:  # Internal error: Setting run mode failed
                self._ERRORID = 558
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            elif self.NERR == -101:  # Internal error: Getting number of identification runs failed
                self._ERRORID = 559
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            elif self.NERR == -102:  # Internal error: Getting starting position for next movement failed
                self._ERRORID = 560
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            elif self.NERR == -105:  # Internal error: Calculation step failed
                self._ERRORID = 561
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            else:
                self._ERRORID = 0

        self._ERROR = (self._ERRORID != 0)

        if self.EXECUTECMD and self.NSTATE == 0:
            self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID
        elif self.EXECUTECMD and (self.NSTATE == 1 or self.NSTATE == 2):
            self._ORDERID = self.MXA_EXECUTECOMMAND_2.ORDERID

# /******************************************************************************
#  * FUNCTION_BLOCK KRC_LDDSTART
#  ******************************************************************************/

class KRC_LDDSTART:
    """
    The function block KRC_LDDstart is used to perform load data determination. The load data determination must be performed with a program override of 100% (function block KRC_SetOverride).

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    Tool (int): Number of the tool for which load data determination is to be carried out. Range: 1 to maximum number of tools.

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
    # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.TOOL = 0

    # VAR_OUTPUT
        self._BUSY = False
        self._DONE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

    # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.MXA_EXECUTECOMMAND_2 = MXA_EXECUTECOMMAND()
        self.NORDERID = 0
        self.NSTATE = 0
        self.NERR = 0
        self.ERR_STATUS = 0.0

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if (self.AXISGROUPIDX < 1) or (self.AXISGROUPIDX > 5):
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            if not self.EXECUTECMD:
                self._ERRORID = 0

        if not self.EXECUTECMD:
            self.NSTATE = 0
            self.NORDERID = 0

        if self.EXECUTECMD and (KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCCONTROL.OVERRIDE < 100):
            self._ERRORID = 557
            self._ERROR = True
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            return

        # Execute LDD start function
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = (self.EXECUTECMD and self.NSTATE == 0)
        self.MXA_EXECUTECOMMAND_1.CMDID = 64
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 1
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR and self.NSTATE == 0:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.TOOL
            self.NORDERID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID

        if self.MXA_EXECUTECOMMAND_1.DONE and self.NSTATE == 0:
            self.NSTATE = 1

        if self.MXA_EXECUTECOMMAND_1.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID

        # Get return values if error happens
        self.MXA_EXECUTECOMMAND_2.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_2.EXECUTE = (self.EXECUTECMD and ((self.NSTATE == 1) or (self.NSTATE == 2)))
        self.MXA_EXECUTECOMMAND_2.CMDID = 65
        self.MXA_EXECUTECOMMAND_2.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_2.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_2.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_2.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_2.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_2.OnCycle()

        if self.MXA_EXECUTECOMMAND_2.WRITECMDPAR and self.NSTATE == 1:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.NORDERID

        if self.MXA_EXECUTECOMMAND_2.READCMDDATARET and self.NSTATE == 1:
            self.ERR_STATUS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self.NSTATE = 2

        if self.MXA_EXECUTECOMMAND_2.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_2.ERRORID

        self._BUSY = (self.MXA_EXECUTECOMMAND_1.BUSY or self.MXA_EXECUTECOMMAND_2.BUSY)
        self._DONE = self.MXA_EXECUTECOMMAND_2.DONE

# part 2
        
        if self.NSTATE == 2:
            self.NERR = int(self.ERR_STATUS)
            if self.NERR == -108:  # Internal: initializing LDD failed
                self._ERRORID = 550
            elif self.NERR == -109:  # Setting manual mass failed
                self._ERRORID = 551
            elif self.NERR == -110:  # Setting start position failed
                self._ERRORID = 552
            elif self.NERR == -111:  # Setting supplementary load failed
                self._ERRORID = 553
            elif self.NERR == -112:  # Internal: setting acceleration factor LDD failed
                self._ERRORID = 554
            elif self.NERR == -113:  # Internal: finalizing configuration failed
                self._ERRORID = 555
            elif self.NERR == -100:  # Internal error: Setting run mode failed
                self._ERRORID = 558
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            elif self.NERR == -101:  # Internal error: Getting number of identification runs failed
                self._ERRORID = 559
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            elif self.NERR == -102:  # Internal error: Getting starting position for next movement failed
                self._ERRORID = 560
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            elif self.NERR == -105:  # Internal error: Calculation step failed
                self._ERRORID = 561
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            elif self.NERR == -1:  # Internal error: Getting identified load failed
                self._ERRORID = 562
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            else:
                self._ERRORID = 0

        self._ERROR = (self._ERRORID != 0)

        if self.EXECUTECMD and self.NSTATE == 0:
            self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID
        elif self.EXECUTECMD and (self.NSTATE == 1 or self.NSTATE == 2):
            self._ORDERID = self.MXA_EXECUTECOMMAND_2.ORDERID

# /******************************************************************************
#  * FUNCTION_BLOCK KRC_LDDWRITELOAD
#  ******************************************************************************/

class KRC_LDDWRITELOAD:
    """
    The function block KRC_LDDwriteLoad assigns the determined load data to the specified tool. It is always the most recently determined load data that are used. It is thus also possible to assign the most recently determined load data to multiple tools.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is executed in the case of a rising edge of the signal.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).
    Tool (int): Number of the tool to which the load data are to be assigned. Range: 1 to maximum number of tools.

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """

    def __init__(self):
    # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.BUFFERMODE = 0
        self.TOOL = 0

    # VAR_OUTPUT
        self._BUSY = False
        self._DONE = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

    # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.MXA_EXECUTECOMMAND_2 = MXA_EXECUTECOMMAND()
        self.NORDERID = 0
        self.NSTATE = 0
        self.COPY_OF_NSTATE = 0
        self.NERR = 0
        self.ERR_STATUS = 0.0

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if (self.AXISGROUPIDX < 1) or (self.AXISGROUPIDX > 5):
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            if not self.EXECUTECMD:
                self._ERRORID = 0

        if not self.EXECUTECMD:
            self.NSTATE = 0
            self.NORDERID = 0

        # Execute LDD write load function
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = (self.EXECUTECMD and self.NSTATE == 0)
        self.MXA_EXECUTECOMMAND_1.CMDID = 66
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR and self.NSTATE == 0:
            self.NORDERID = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.ORDERID

        if self.MXA_EXECUTECOMMAND_1.DONE and self.NSTATE == 0:
            self.NSTATE = 1

        if self.MXA_EXECUTECOMMAND_1.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID

        # Get return values if error happens
        self.MXA_EXECUTECOMMAND_2.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_2.EXECUTE = (self.EXECUTECMD and ((self.NSTATE == 1) or (self.NSTATE == 2)))
        self.MXA_EXECUTECOMMAND_2.CMDID = 67
        self.MXA_EXECUTECOMMAND_2.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_2.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_2.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_2.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_2.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_2.OnCycle()

        if self.MXA_EXECUTECOMMAND_2.WRITECMDPAR and self.NSTATE == 1:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.NORDERID

        if self.MXA_EXECUTECOMMAND_2.READCMDDATARET and self.NSTATE == 1:
            self.ERR_STATUS = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self.NSTATE = 2

        if self.MXA_EXECUTECOMMAND_2.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_2.ERRORID


        self._BUSY = (self.MXA_EXECUTECOMMAND_1.BUSY or self.MXA_EXECUTECOMMAND_2.BUSY)
        self._DONE = self.MXA_EXECUTECOMMAND_2.DONE

        if self.NSTATE == 2:
            self.NERR = int(self.ERR_STATUS)
            if self.NERR == -1:  # Internal error: Getting identified load failed
                self._ERRORID = 562
                KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INTFBERRORID = self.ERRORID
            else:
                self._ERRORID = 0

        self._ERROR = (self._ERRORID != 0)

        if self.EXECUTECMD and self.NSTATE == 0:
            self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID
        elif self.EXECUTECMD and (self.NSTATE == 1 or self.NSTATE == 2):
            self._ORDERID = self.MXA_EXECUTECOMMAND_2.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_WRITEWORKSPACE
#  ******************************************************************************/

class KRC_WRITEWORKSPACE:
    """
    The function block KRC_WriteWorkspace is used to configure Cartesian (cubic) workspaces for the robot. Workspaces serve to protect the system. A maximum of 8 Cartesian workspaces can be configured at any one time. The workspaces may overlap.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    WorkspaceNo (int): Number of workspace. Range: 1-8.
    WorkspaceMode (int): Mode for workspaces. Options: 0 (#OFF), 1 (#INSIDE), 2 (#OUTSIDE), 3 (#INSIDE_STOP), 4 (#OUTSIDE_STOP).
    WorkspaceData (BOX): Data of the workspace. The data of a Cartesian workspace are specified with the following elements:
        - Origin and orientation: These elements refer to the WORLD coordinate system and are defined in the variable BOX.
            - X, Y, Z (float): Coordinates of the origin in millimeters.
            - A, B, C (float): Orientation. Range: -180 to 180 degrees.
        - Dimensions: The dimensions of a Cartesian workspace are specified with the following elements.
            - X1, X2, Y1, Y2, Z1, Z2 (float): Dimensions in millimeters.
    BufferMode (int): Mode in which the statement is executed. Options: 0 (DIRECT), 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """

    def __init__(self):
    # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.WORKSPACENO = 0
        self.WORKSPACEMODE = 0
        self.WORKSPACEDATA = BOX()
        self.BUFFERMODE = 0

    # VAR_OUTPUT
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

    # VAR
    MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if ((self.AXISGROUPIDX < 1) or (self.AXISGROUPIDX > 5)):
            self._ERRORID = 506
            self._ERROR = True
            return

        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 48
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = self.WORKSPACENO
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.WORKSPACEMODE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = self.WORKSPACEDATA.X
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = self.WORKSPACEDATA.Y
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = self.WORKSPACEDATA.Z
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = self.WORKSPACEDATA.A
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = self.WORKSPACEDATA.B
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = self.WORKSPACEDATA.C
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = self.WORKSPACEDATA.X1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = self.WORKSPACEDATA.X2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = self.WORKSPACEDATA.Y1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[10] = self.WORKSPACEDATA.Y2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[11] = self.WORKSPACEDATA.Z1
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[12] = self.WORKSPACEDATA.Z2

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID


# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READWORKSPACE
#  ******************************************************************************/

class KRC_READWORKSPACE:
    """
    The function block KRC_ReadWorkspace reads the configuration of the Cartesian workspaces for the robot.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    WorkspaceNo (int): Number of workspace. Range: 1-8.

    Returns:
    Done (bool): TRUE = statement has been executed.
    WorkspaceMode (int): Mode for workspaces. Options: 0 (#OFF), 1 (#INSIDE), 2 (#OUTSIDE), 3 (#INSIDE_STOP), 4 (#OUTSIDE_STOP).
    WorkspaceData (BOX): Data of the workspace.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
    # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.WORKSPACENO = 0

    # VAR_OUTPUT
        self._DONE = False
        self._WORKSPACEMODE = 0
        self._WORKSPACEDATA = BOX()
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

    # VAR
        self.NSTATE = 0
        self.MXA_EXECUTECOMMAND_0 = MXA_EXECUTECOMMAND()
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.M_WORKSPACEMODE = 0
        self.M_WORKSPACEDATA = BOX()

    @property
    def DONE(self):
        return self._DONE

    @property
    def WORKSPACEMODE(self):
        return self._WORKSPACEMODE

    @property
    def WORKSPACEDATA(self):
        return self._WORKSPACEDATA

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if ((self.AXISGROUPIDX < 1) or (self.AXISGROUPIDX > 5)):
            self._ERRORID = 506
            self._ERROR = True
            return

        if not self.EXECUTECMD:
            self.NSTATE = 0
            self.M_WORKSPACEMODE = 0
            self.M_WORKSPACEDATA.X = 0.0
            self.M_WORKSPACEDATA.Y = 0.0
            self.M_WORKSPACEDATA.Z = 0.0
            self.M_WORKSPACEDATA.A = 0.0
            self.M_WORKSPACEDATA.B = 0.0
            self.M_WORKSPACEDATA.C = 0.0
            self.M_WORKSPACEDATA.X1 = 0.0
            self.M_WORKSPACEDATA.X2 = 0.0
            self.M_WORKSPACEDATA.Y1 = 0.0
            self.M_WORKSPACEDATA.Y2 = 0.0
            self.M_WORKSPACEDATA.Z1 = 0.0
            self.M_WORKSPACEDATA.Z2 = 0.0
            self._WORKSPACEMODE = self.M_WORKSPACEMODE
            self._WORKSPACEDATA = self.M_WORKSPACEDATA

        # Call FB mxA_ExecuteCommand_0
        self.MXA_EXECUTECOMMAND_0.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_0.EXECUTE = (self.EXECUTECMD and (self.NSTATE == 0))
        self.MXA_EXECUTECOMMAND_0.CMDID = 49
        self.MXA_EXECUTECOMMAND_0.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_0.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_0.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_0.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_0.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_0.OnCycle()

        if (self.MXA_EXECUTECOMMAND_0.WRITECMDPAR and (self.NSTATE == 0)):
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.WORKSPACENO)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = 1

        if (self.MXA_EXECUTECOMMAND_0.READCMDDATARET and (self.NSTATE == 0)):
            self.M_WORKSPACEMODE = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
            self.NSTATE = 1

        if self.MXA_EXECUTECOMMAND_0.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_0.ERRORID

        # Call FB mxA_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = (self.EXECUTECMD and (self.NSTATE == 1))
        self.MXA_EXECUTECOMMAND_1.CMDID = 49
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if (self.MXA_EXECUTECOMMAND_1.WRITECMDPAR and (self.NSTATE == 1)):
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.WORKSPACENO)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = 2
# part 2
        if (self.MXA_EXECUTECOMMAND_1.READCMDDATARET and (self.NSTATE == 1)):
            self.M_WORKSPACEDATA.X = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self.M_WORKSPACEDATA.Y = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self.M_WORKSPACEDATA.Z = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self.M_WORKSPACEDATA.A = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self.M_WORKSPACEDATA.B = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self.M_WORKSPACEDATA.C = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self.M_WORKSPACEDATA.X1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7]
            self.M_WORKSPACEDATA.X2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8]
            self.M_WORKSPACEDATA.Y1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self.M_WORKSPACEDATA.Y2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10]
            self.M_WORKSPACEDATA.Z1 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11]
            self.M_WORKSPACEDATA.Z2 = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12]
            self.NSTATE = 2

        if self.MXA_EXECUTECOMMAND_1.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID

        self._DONE = (self.NSTATE == 2)

        if (self.NSTATE == 2):
            self._WORKSPACEMODE = self.M_WORKSPACEMODE
            self._WORKSPACEDATA = self.M_WORKSPACEDATA
            self._ERROR = 0
            self._ERRORID = 0

        self._ERROR = (self._ERRORID != 0)

        if self.EXECUTECMD and self.NSTATE == 0:
            self._ORDERID = self.MXA_EXECUTECOMMAND_0.ORDERID
        elif self.EXECUTECMD and self.NSTATE == 1:
            self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_WRITEAXWORKSPACE
#  ******************************************************************************/

class KRC_WRITEAXWORKSPACE:
    """
    The function block KRC_WriteAxWorkspace is used to configure axis-specific workspaces for the robot. These serve to protect the system. A maximum of 8 axis-specific workspaces can be configured at any one time. The workspaces may overlap.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    WorkspaceNo (int): Number of workspace. Range: 1-8.
    WorkspaceMode (int): Mode for workspaces. Options: 0 (#OFF), 1 (#INSIDE), 2 (#OUTSIDE), 3 (#INSIDE_STOP), 4 (#OUTSIDE_STOP).
    WorkspaceData (AXBOX): Data of the workspace. The data of an axis-specific workspace are defined using the following elements in the variable AXBOX.
        - Robot axes:
            - A1_N, A2_N, A3_N, A4_N, A5_N, A6_N (float): Lower limit for axis angle in mm/°.
            - A1_P, A2_P, A3_P, A4_P, A5_P, A6_P (float): Upper limit for axis angle in mm/°.
        - External axes:
            - E1_N, E2_N, E3_N, E4_N, E5_N, E6_N (float): Lower limit for axis angle in mm/°.
            - E1_P, E2_P, E3_P, E4_P, E5_P, E6_P (float): Upper limit for axis angle in mm/°.
    BufferMode (int): Mode in which the statement is executed. Options: 0 (DIRECT), 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
    # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.WORKSPACENO = 0
        self.WORKSPACEMODE = 0
        self.WORKSPACEDATA = AXBOX()
        self.BUFFERMODE = 0

    # VAR_OUTPUT
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0

    # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if ((self.AXISGROUPIDX < 1) or (self.AXISGROUPIDX > 5)):
            self._ERRORID = 506
            self._ERROR = True
            return

        # Call FB mxa_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 50
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 2
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.WORKSPACENO)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = int(self.WORKSPACEMODE)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[1] = float(self.WORKSPACEDATA.A1_N)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[2] = float(self.WORKSPACEDATA.A2_N)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[3] = float(self.WORKSPACEDATA.A3_N)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[4] = float(self.WORKSPACEDATA.A4_N)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[5] = float(self.WORKSPACEDATA.A5_N)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[6] = float(self.WORKSPACEDATA.A6_N)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[7] = float(self.WORKSPACEDATA.A1_P)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[8] = float(self.WORKSPACEDATA.A2_P)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[9] = float(self.WORKSPACEDATA.A3_P)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[10] = float(self.WORKSPACEDATA.A4_P)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[11] = float(self.WORKSPACEDATA.A5_P)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[12] = float(self.WORKSPACEDATA.A6_P)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[13] = float(self.WORKSPACEDATA.E1_N)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[14] = float(self.WORKSPACEDATA.E2_N)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[15] = float(self.WORKSPACEDATA.E3_N)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[16] = float(self.WORKSPACEDATA.E4_N)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[17] = float(self.WORKSPACEDATA.E5_N)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[18] = float(self.WORKSPACEDATA.E6_N)
# part 2
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[19] = float(self.WORKSPACEDATA.E1_P)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[20] = float(self.WORKSPACEDATA.E2_P)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[21] = float(self.WORKSPACEDATA.E3_P)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[22] = float(self.WORKSPACEDATA.E4_P)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[23] = float(self.WORKSPACEDATA.E5_P)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARREAL[24] = float(self.WORKSPACEDATA.E6_P)

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = (self._ERRORID != 0)
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READAXWORKSPACE
#  ******************************************************************************/

class KRC_READAXWORKSPACE:
    """
    The function block KRC_ReadAxWorkspace reads the configuration of the axis-specific workspaces for the robot.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    WorkspaceNo (int): Number of workspace. Range: 1-8.

    Returns:
    Done (bool): TRUE = statement has been executed.
    WorkspaceMode (int): Mode for workspaces. Options: 0 (#OFF), 1 (#INSIDE), 2 (#OUTSIDE), 3 (#INSIDE_STOP), 4 (#OUTSIDE_STOP).
    WorkspaceData (AXBOX): Data of the workspace. The data of an axis-specific workspace are defined using the following elements in the variable AXBOX.
        - Robot axes:
            - A1_N, A2_N, A3_N, A4_N, A5_N, A6_N (float): Lower limit for axis angle in mm/°.
            - A1_P, A2_P, A3_P, A4_P, A5_P, A6_P (float): Upper limit for axis angle in mm/°.
        - External axes:
            - E1_N, E2_N, E3_N, E4_N, E5_N, E6_N (float): Lower limit for axis angle in mm/°.
            - E1_P, E2_P, E3_P, E4_P, E5_P, E6_P (float): Upper limit for axis angle in mm/°.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
    # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.WORKSPACENO = 0
    
    # VAR_OUTPUT
        self._DONE = False
        self._WORKSPACEMODE = 0
        self._WORKSPACEDATA = AXBOX()
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
    
    # VAR
        self.NSTATE = 0
        self.MXA_EXECUTECOMMAND_0 = MXA_EXECUTECOMMAND()
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.MXA_EXECUTECOMMAND_2 = MXA_EXECUTECOMMAND()
        self.M_WORKSPACEMODE = 0
        self.M_WORKSPACEDATA = AXBOX()

    @property
    def DONE(self):
        return self._DONE

    @property
    def WORKSPACEMODE(self):
        return self._WORKSPACEMODE

    @property
    def WORKSPACEDATA(self):
        return self._WORKSPACEDATA

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ERRORID = 0
        self._ORDERID = 0
        if ((self.AXISGROUPIDX < 1) or (self.AXISGROUPIDX > 5)):
            self._ERRORID = 506
            self._ERROR = True
            return

        if not self.EXECUTECMD:
            self.NSTATE = 0
            self.M_WORKSPACEMODE = 0
            self.M_WORKSPACEDATA.A1_N = 0.0
            self.M_WORKSPACEDATA.A2_N = 0.0
            self.M_WORKSPACEDATA.A3_N = 0.0
            self.M_WORKSPACEDATA.A4_N = 0.0
            self.M_WORKSPACEDATA.A5_N = 0.0
            self.M_WORKSPACEDATA.A6_N = 0.0
            self.M_WORKSPACEDATA.A1_P = 0.0
            self.M_WORKSPACEDATA.A2_P = 0.0
            self.M_WORKSPACEDATA.A3_P = 0.0
            self.M_WORKSPACEDATA.A4_P = 0.0
            self.M_WORKSPACEDATA.A5_P = 0.0
            self.M_WORKSPACEDATA.A6_P = 0.0
            self.M_WORKSPACEDATA.E1_N = 0.0
            self.M_WORKSPACEDATA.E2_N = 0.0
            self.M_WORKSPACEDATA.E3_N = 0.0
            self.M_WORKSPACEDATA.E4_N = 0.0
            self.M_WORKSPACEDATA.E5_N = 0.0
            self.M_WORKSPACEDATA.E6_N = 0.0
            self.M_WORKSPACEDATA.E1_P = 0.0
            self.M_WORKSPACEDATA.E2_P = 0.0
            self.M_WORKSPACEDATA.E3_P = 0.0
            self.M_WORKSPACEDATA.E4_P = 0.0
            self.M_WORKSPACEDATA.E5_P = 0.0
            self.M_WORKSPACEDATA.E6_P = 0.0
            self._WORKSPACEDATA = self.M_WORKSPACEDATA

        # Call FB mxA_ExecuteCommand_0
        self.MXA_EXECUTECOMMAND_0.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_0.EXECUTE = (self.EXECUTECMD and (self.NSTATE == 0))
        self.MXA_EXECUTECOMMAND_0.CMDID = 51
        self.MXA_EXECUTECOMMAND_0.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_0.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_0.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_0.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_0.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_0.OnCycle()

        if (self.MXA_EXECUTECOMMAND_0.WRITECMDPAR and (self.NSTATE == 0)):
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.WORKSPACENO)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = 1

        if (self.MXA_EXECUTECOMMAND_0.READCMDDATARET and (self.NSTATE == 0)):
            self.M_WORKSPACEMODE = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
            self.NSTATE = 1

        if self.MXA_EXECUTECOMMAND_0.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_0.ERRORID

        # Call FB mxA_ExecuteCommand_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = (self.EXECUTECMD and (self.NSTATE == 1))
        self.MXA_EXECUTECOMMAND_1.CMDID = 51
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
# part 2
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if (self.MXA_EXECUTECOMMAND_1.WRITECMDPAR and (self.NSTATE == 1)):
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.WORKSPACENO)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = 2

        if (self.MXA_EXECUTECOMMAND_1.READCMDDATARET and (self.NSTATE == 1)):
            self.M_WORKSPACEDATA.A1_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self.M_WORKSPACEDATA.A2_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self.M_WORKSPACEDATA.A3_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self.M_WORKSPACEDATA.A4_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self.M_WORKSPACEDATA.A5_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self.M_WORKSPACEDATA.A6_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self.M_WORKSPACEDATA.A1_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7]
            self.M_WORKSPACEDATA.A2_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8]
            self.M_WORKSPACEDATA.A3_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self.M_WORKSPACEDATA.A4_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10]
            self.M_WORKSPACEDATA.A5_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11]
            self.M_WORKSPACEDATA.A6_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12]
            self.NSTATE = 2

        if self.MXA_EXECUTECOMMAND_1.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID

        # Call FB mxA_ExecuteCommand_2
        self.MXA_EXECUTECOMMAND_2.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_2.EXECUTE = (self.EXECUTECMD and (self.NSTATE == 2))
        self.MXA_EXECUTECOMMAND_2.CMDID = 51
        self.MXA_EXECUTECOMMAND_2.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_2.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_2.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_2.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_2.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_2.OnCycle()

        if (self.MXA_EXECUTECOMMAND_2.WRITECMDPAR and (self.NSTATE == 2)):
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.WORKSPACENO)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = 3

        if (self.MXA_EXECUTECOMMAND_2.READCMDDATARET and (self.NSTATE == 2)):
            self.M_WORKSPACEDATA.E1_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1]
            self.M_WORKSPACEDATA.E2_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2]
            self.M_WORKSPACEDATA.E3_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3]
            self.M_WORKSPACEDATA.E4_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4]
            self.M_WORKSPACEDATA.E5_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5]
            self.M_WORKSPACEDATA.E6_N = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6]
            self.M_WORKSPACEDATA.E1_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7]
            self.M_WORKSPACEDATA.E2_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8]
            self.M_WORKSPACEDATA.E3_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9]
            self.M_WORKSPACEDATA.E4_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10]
            self.M_WORKSPACEDATA.E5_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11]
            self.M_WORKSPACEDATA.E6_P = KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12]
            self.NSTATE = 3

        if self.MXA_EXECUTECOMMAND_2.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_2.ERRORID
# part 3
        self._DONE = (self.NSTATE == 3)

        if (self.NSTATE == 3):
            self._WORKSPACEMODE = self.M_WORKSPACEMODE
            self._WORKSPACEDATA = self.M_WORKSPACEDATA
            self._ERROR = False
            self._ERRORID = 0

        self._ERROR = (self._ERRORID != 0)

        if self.EXECUTECMD and self.NSTATE == 0:
            self._ORDERID = self.MXA_EXECUTECOMMAND_0.ORDERID
        elif self.EXECUTECMD and self.NSTATE == 1:
            self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID
        elif self.EXECUTECMD and self.NSTATE == 2:
            self._ORDERID = self.MXA_EXECUTECOMMAND_2.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_READWORKSTATES
#  ******************************************************************************/

class KRC_READWORKSTATES:
    """
    The function block KRC_ReadWorkstates reads the current status of the workspaces. The status of the workspaces is updated cyclically.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.

    Returns:
    Valid (bool): TRUE = data are valid.
    WORKSTATE1, WORKSTATE2, WORKSTATE3, WORKSTATE4, WORKSTATE5, WORKSTATE6, WORKSTATE7, WORKSTATE8 (bool): Status of the workspaces.
    AXWORKSTATE1, AXWORKSTATE2, AXWORKSTATE3, AXWORKSTATE4, AXWORKSTATE5, AXWORKSTATE6, AXWORKSTATE7, AXWORKSTATE8 (bool): Status of the axis-specific workspaces.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    """
    def __init__(self):
    # VAR_INPUT
        self.AXISGROUPIDX = 0

    # VAR_OUTPUT
        self._VALID = False
        self._WORKSTATE1 = False
        self._WORKSTATE2 = False
        self._WORKSTATE3 = False
        self._WORKSTATE4 = False
        self._WORKSTATE5 = False
        self._WORKSTATE6 = False
        self._WORKSTATE7 = False
        self._WORKSTATE8 = False
        self._AXWORKSTATE1 = False
        self._AXWORKSTATE2 = False
        self._AXWORKSTATE3 = False
        self._AXWORKSTATE4 = False
        self._AXWORKSTATE5 = False
        self._AXWORKSTATE6 = False
        self._AXWORKSTATE7 = False
        self._AXWORKSTATE8 = False
        self._ERROR = False
        self._ERRORID = 0

    @property
    def VALID(self):
        return self._VALID

    @property
    def WORKSTATE1(self):
        return self._WORKSTATE1

    @property
    def WORKSTATE2(self):
        return self._WORKSTATE2

    @property
    def WORKSTATE3(self):
        return self._WORKSTATE3

    @property
    def WORKSTATE4(self):
        return self._WORKSTATE4

    @property
    def WORKSTATE5(self):
        return self._WORKSTATE5

    @property
    def WORKSTATE6(self):
        return self._WORKSTATE6

    @property
    def WORKSTATE7(self):
        return self._WORKSTATE7

    @property
    def WORKSTATE8(self):
        return self._WORKSTATE8

    @property
    def AXWORKSTATE1(self):
        return self._AXWORKSTATE1

    @property
    def AXWORKSTATE2(self):
        return self._AXWORKSTATE2

    @property
    def AXWORKSTATE3(self):
        return self._AXWORKSTATE3

    @property
    def AXWORKSTATE4(self):
        return self._AXWORKSTATE4

    @property
    def AXWORKSTATE5(self):
        return self._AXWORKSTATE5

    @property
    def AXWORKSTATE6(self):
        return self._AXWORKSTATE6

    @property
    def AXWORKSTATE7(self):
        return self._AXWORKSTATE7

    @property
    def AXWORKSTATE8(self):
        return self._AXWORKSTATE8

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    def OnCycle(self):
        if ((self.AXISGROUPIDX < 1) or (self.AXISGROUPIDX > 5)):
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        self._VALID = (KRC_AXISGROUPREFARR[self.AXISGROUPIDX].ONLINE and KRC_AXISGROUPREFARR[self.AXISGROUPIDX].INITIALIZED)
        self._WORKSTATE1 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.WORKSTATES, 0)
        self._WORKSTATE2 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.WORKSTATES, 1)
        self._WORKSTATE3 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.WORKSTATES, 2)
        self._WORKSTATE4 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.WORKSTATES, 3)
        self._WORKSTATE5 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.WORKSTATES, 4)
        self._WORKSTATE6 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.WORKSTATES, 5)
        self._WORKSTATE7 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.WORKSTATES, 6)
        self._WORKSTATE8 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.WORKSTATES, 7)
        self._AXWORKSTATE1 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXWORKSTATES, 0)
        self._AXWORKSTATE2 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXWORKSTATES, 1)
        self._AXWORKSTATE3 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXWORKSTATES, 2)
        self._AXWORKSTATE4 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXWORKSTATES, 3)
        self._AXWORKSTATE5 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXWORKSTATES, 4)
        self._AXWORKSTATE6 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXWORKSTATES, 5)
        self._AXWORKSTATE7 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXWORKSTATES, 6)
        self._AXWORKSTATE8 = IsBitSet(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].KRCSTATE.AXWORKSTATES, 7)



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CDREADSTATUS
#  ******************************************************************************/

class KRC_CDREADSTATUS:
    """
    Reads variables reflecting collision detection state

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    ActiveCom (bool): TRUE = $COLLMON_ACTIVE_COM is TRUE
    ActivePro (bool): TRUE = $COLLMON_ACTIVE_PRO is TRUE
    ImprovedCollmon (bool): TRUE = $IMPROVED_COLLMON is TRUE
    ActiveDatasetIndex (int): index of active dataset
    CollisionOccurred (bool): TRUE = $COLL_ALARM is TRUE
    """
    def __init__(self):
      # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False

      # VAR_OUTPUT
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self._ACTIVECOM = False
        self._ACTIVEPRO = False
        self._IMPROVEDCOLLMON = False
        self._ACTIVEDATASETINDEX = 0
        self._COLLISIONOCCURED = False
      
      # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 69
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._ACTIVECOM = bool(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
            self._ACTIVEPRO = bool(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2])
            self._IMPROVEDCOLLMON = bool(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3])
            self._ACTIVEDATASETINDEX = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4])
            self._COLLISIONOCCURED = bool(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5])

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CDACTIVATEDATASET
#  ******************************************************************************/

class KRC_CDACTIVATEDATASET:
    """
    Activates specified collision detection dataset

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).
    DatasetIndex (int): Index of dataset selected to be activated

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
      # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.BUFFERMODE = 2
        self.DATASETINDEX = 0

      # VAR_OUTPUT
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
      
      # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 70
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.DATASETINDEX)

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1.ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CDREADDATASET
#  ******************************************************************************/

class KRC_CDREADDATASET:
    """
    Reads collision detection thresholds for jogging mode

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    DatasetIndex (int): Index of dataset desired to be read
    
    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    ThresholdA1 (int): Dataset threshold for A1
    ThresholdA2 (int): Dataset threshold for A2
    ThresholdA3 (int): Dataset threshold for A3
    ThresholdA4 (int): Dataset threshold for A4
    ThresholdA5 (int): Dataset threshold for A5
    ThresholdA6 (int): Dataset threshold for A6
    ThresholdE1 (int): Dataset threshold for E1
    ThresholdE2 (int): Dataset threshold for E2
    ThresholdE3 (int): Dataset threshold for E3
    ThresholdE4 (int): Dataset threshold for E4
    ThresholdE5 (int): Dataset threshold for E5
    ThresholdE6 (int): Dataset threshold for E6
    """
    def __init__(self):
      # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.DATASETINDEX = 0

      # VAR_OUTPUT
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self._THRESHOLDA1 = 0
        self._THRESHOLDA2 = 0
        self._THRESHOLDA3 = 0
        self._THRESHOLDA4 = 0
        self._THRESHOLDA5 = 0
        self._THRESHOLDA6 = 0
        self._THRESHOLDE1 = 0
        self._THRESHOLDE2 = 0
        self._THRESHOLDE3 = 0
        self._THRESHOLDE4 = 0
        self._THRESHOLDE5 = 0
        self._THRESHOLDE6 = 0
      
      # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 71
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._THRESHOLDA1 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
            self._THRESHOLDA2 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2])
            self._THRESHOLDA3 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3])
            self._THRESHOLDA4 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4])
            self._THRESHOLDA5 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5])
            self._THRESHOLDA6 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6])
            self._THRESHOLDE1 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7])
            self._THRESHOLDE2 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8])
            self._THRESHOLDE3 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9])
            self._THRESHOLDE4 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10])
            self._THRESHOLDE5 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11])
            self._THRESHOLDE6 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12])

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CDWRITEDATASET
#  ******************************************************************************/

class KRC_CDWRITEDATASET:
    """
    Writes data of selected collision detection dataset

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    BufferMode (int): Mode in which the statement is executed. Options: 0 (DIRECT), 1 (ABORTING), 2 (BUFFERED).
    DatasetIndex (int): Index of dataset desired to be written
    ThresholdA1 (int): Dataset threshold for A1
    ThresholdA2 (int): Dataset threshold for A2
    ThresholdA3 (int): Dataset threshold for A3
    ThresholdA4 (int): Dataset threshold for A4
    ThresholdA5 (int): Dataset threshold for A5
    ThresholdA6 (int): Dataset threshold for A6
    ThresholdE1 (int): Dataset threshold for E1
    ThresholdE2 (int): Dataset threshold for E2
    ThresholdE3 (int): Dataset threshold for E3
    ThresholdE4 (int): Dataset threshold for E4
    ThresholdE5 (int): Dataset threshold for E5
    ThresholdE6 (int): Dataset threshold for E6

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
      # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.BUFFERMODE = 2
        self.DATASETINDEX = 0
        self.THRESHOLDA1 = 150
        self.THRESHOLDA2 = 150
        self.THRESHOLDA3 = 150
        self.THRESHOLDA4 = 150
        self.THRESHOLDA5 = 150
        self.THRESHOLDA6 = 150
        self.THRESHOLDE1 = 150
        self.THRESHOLDE2 = 150
        self.THRESHOLDE3 = 150
        self.THRESHOLDE4 = 150
        self.THRESHOLDE5 = 150
        self.THRESHOLDE6 = 150

      # VAR_OUTPUT
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        
      
      # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY
   
    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 72
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.DATASETINDEX)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = int(self.THRESHOLDA1)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = int(self.THRESHOLDA2)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[4] = int(self.THRESHOLDA3)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[5] = int(self.THRESHOLDA4)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[6] = int(self.THRESHOLDA5)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[7] = int(self.THRESHOLDA6)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[8] = int(self.THRESHOLDE1)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[9] = int(self.THRESHOLDE2)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[10] = int(self.THRESHOLDE3)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[11] = int(self.THRESHOLDE4)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[12] = int(self.THRESHOLDE5)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[13] = int(self.THRESHOLDE6)

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1.ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CDRESETMAXMEASURED
#  ******************************************************************************/

class KRC_CDRESETMAXMEASURED:
    """
    Resets maximum measured collision detection monitoring values

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    BufferMode (int): Mode in which the statement is executed. Options: 0 (DIRECT), 1 (ABORTING), 2 (BUFFERED).

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
      # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.BUFFERMODE = 2

      # VAR_OUTPUT
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        
      
      # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY
   
    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 73
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1.ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CDREADMAXMEASURED
#  ******************************************************************************/

class KRC_CDREADMAXMEASURED:
    """
    Reads maximum measured collision detection monitoring values since last reset

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    
    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    MaxMeasuredA1 (int): Max measured value for A1
    MaxMeasuredA2 (int): Max measured value for A2
    MaxMeasuredA3 (int): Max measured value for A3
    MaxMeasuredA4 (int): Max measured value for A4
    MaxMeasuredA5 (int): Max measured value for A5
    MaxMeasuredA6 (int): Max measured value for A6
    MaxMeasuredE1 (int): Max measured value for E1
    MaxMeasuredE2 (int): Max measured value for E2
    MaxMeasuredE3 (int): Max measured value for E3
    MaxMeasuredE4 (int): Max measured value for E4
    MaxMeasuredE5 (int): Max measured value for E5
    MaxMeasuredE6 (int): Max measured value for E6
    """
    def __init__(self):
      # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False

      # VAR_OUTPUT
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self._MAXMEASUREDA1 = 0
        self._MAXMEASUREDA2 = 0
        self._MAXMEASUREDA3 = 0
        self._MAXMEASUREDA4 = 0
        self._MAXMEASUREDA5 = 0
        self._MAXMEASUREDA6 = 0
        self._MAXMEASUREDE1 = 0
        self._MAXMEASUREDE2 = 0
        self._MAXMEASUREDE3 = 0
        self._MAXMEASUREDE4 = 0
        self._MAXMEASUREDE5 = 0
        self._MAXMEASUREDE6 = 0
      
      # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 74
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.READCMDDATARET:
            self._MAXMEASUREDA1 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
            self._MAXMEASUREDA2 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2])
            self._MAXMEASUREDA3 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3])
            self._MAXMEASUREDA4 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4])
            self._MAXMEASUREDA5 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5])
            self._MAXMEASUREDA6 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6])
            self._MAXMEASUREDE1 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7])
            self._MAXMEASUREDE2 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8])
            self._MAXMEASUREDE3 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9])
            self._MAXMEASUREDE4 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10])
            self._MAXMEASUREDE5 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11])
            self._MAXMEASUREDE6 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12])

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CDSTARTTEACHING
#  ******************************************************************************/

class KRC_CDSTARTTEACHING:
    """
    Starts teaching collision detection threshold values with given parameters

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).
    DatasetIndex (int): Index of dataset to store result in if applied automatically when stopped
    TeachingOffset (int): Offset to use when teaching

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
      # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.BUFFERMODE = 2
        self.DATASETINDEX = 0
        self.TEACHINGOFFSET = 0

      # VAR_OUTPUT
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        
      
      # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()  

    @property
    def BUSY(self):
        return self._BUSY
   
    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 75
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = int(self.DATASETINDEX)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = int(self.TEACHINGOFFSET)

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1.ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID




# /******************************************************************************
#  * FUNCTION_BLOCK KRC_CDSTOPTEACHING
#  ******************************************************************************/

class KRC_CDSTOPTEACHING:
    """
    Stops teaching and applies values if requested

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): Starts/buffers the motion in the case of a rising edge of the signal.
    BufferMode (int): Mode in which the statement is executed. Options: 1 (ABORTING), 2 (BUFFERED).
    Apply (bool): Whether to apply measured max based on the setup configured in StartTeaching
    ApplyHigherOnly (bool): Whether to apply only measured values that are higher than the corresponding current value

    Returns:
    Busy (bool): TRUE = statement is currently being transferred or has already been transferred.
    Active (bool): TRUE = statement is currently being executed.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    TeachingResultA1 (int): Value learnt value for A1
    TeachingResultA2 (int): Value learnt value for A2
    TeachingResultA3 (int): Value learnt value for A3
    TeachingResultA4 (int): Value learnt value for A4
    TeachingResultA5 (int): Value learnt value for A5
    TeachingResultA6 (int): Value learnt value for A6
    TeachingResultE1 (int): Value learnt value for E1
    TeachingResultE2 (int): Value learnt value for E2
    TeachingResultE3 (int): Value learnt value for E3
    TeachingResultE4 (int): Value learnt value for E4
    TeachingResultE5 (int): Value learnt value for E5
    TeachingResultE6 (int): Value learnt value for E6
    """
    def __init__(self):
      # VAR_INPUT
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.BUFFERMODE = 2
        self.APPLY = False
        self.APPLYHIGHERONLY = False

      # VAR_OUTPUT
        self._BUSY = False
        self._ACTIVE = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self._TEACHINGRESULTA1 = 0
        self._TEACHINGRESULTA2 = 0
        self._TEACHINGRESULTA3 = 0
        self._TEACHINGRESULTA4 = 0
        self._TEACHINGRESULTA5 = 0
        self._TEACHINGRESULTA6 = 0
        self._TEACHINGRESULTE1 = 0
        self._TEACHINGRESULTE2 = 0
        self._TEACHINGRESULTE3 = 0
        self._TEACHINGRESULTE4 = 0
        self._TEACHINGRESULTE5 = 0
        self._TEACHINGRESULTE6 = 0
      
      # VAR
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()
        self.MXA_EXECUTECOMMAND_2 = MXA_EXECUTECOMMAND()
        self.NSTATE = 0

    @property
    def BUSY(self):
        return self._BUSY
   
    @property
    def ACTIVE(self):
        return self._ACTIVE

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return
        else:
            self._ERRORID = 0
            self._ERROR = False

        if not self.EXECUTECMD:
            self.NSTATE = 0

        # Call FB self.MXA_EXECUTECOMMAND_1
        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 76
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = self.BUFFERMODE
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[1] = bool(self.APPLY)
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARBOOL[2] = bool(self.APPLYHIGHERONLY)
            
        if self.MXA_EXECUTECOMMAND_1.DONE:
            self.NSTATE = 1

        if self.MXA_EXECUTECOMMAND_1.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID

        # Call FB self.MXA_EXECUTECOMMAND_2
        self.MXA_EXECUTECOMMAND_2.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_2.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_2.CMDID = 77
        self.MXA_EXECUTECOMMAND_2.BUFFERMODE = 0
        self.MXA_EXECUTECOMMAND_2.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_2.ENABLEDIRECTEXE = True
        self.MXA_EXECUTECOMMAND_2.ENABLEQUEUEEXE = False
        self.MXA_EXECUTECOMMAND_2.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_2.OnCycle()

        if self.MXA_EXECUTECOMMAND_2.READCMDDATARET:
            self._TEACHINGRESULTA1 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[1])
            self._TEACHINGRESULTA2 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[2])
            self._TEACHINGRESULTA3 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[3])
            self._TEACHINGRESULTA4 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[4])
            self._TEACHINGRESULTA5 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[5])
            self._TEACHINGRESULTA6 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[6])
            self._TEACHINGRESULTE1 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[7])
            self._TEACHINGRESULTE2 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[8])
            self._TEACHINGRESULTE3 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[9])
            self._TEACHINGRESULTE4 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[10])
            self._TEACHINGRESULTE5 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[11])
            self._TEACHINGRESULTE6 = int(KRC_AXISGROUPREFARR[self.AXISGROUPIDX].CMDSTATE.CMDDATARETURN[12])

        if self.MXA_EXECUTECOMMAND_2.ERROR:
            self.NSTATE = 9
            self._ERROR = True
            self._ERRORID = self.MXA_EXECUTECOMMAND_2.ERRORID

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY or self.MXA_EXECUTECOMMAND_2.BUSY
        self._ACTIVE = self.MXA_EXECUTECOMMAND_1.ACTIVE or self.MXA_EXECUTECOMMAND_2.ACTIVE
        self._DONE = self.MXA_EXECUTECOMMAND_2.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED or self.MXA_EXECUTECOMMAND_2.ABORTED
        self._ERROR = self._ERRORID != 0
        if self.EXECUTECMD and self.NSTATE == 0:
            self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID
        elif self.EXECUTECMD and ((self.NSTATE == 1) or (self.NSTATE == 2)):
            self._ORDERID = self.MXA_EXECUTECOMMAND_2.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_GETALLMESSAGES
#  ******************************************************************************/

class KRC_GETALLMESSAGES:
    """
    The function block KRC_GetAllMessages sends all the active system messages to KRMsgNet's client. For INFO type messages, the last is sent.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is buffered in the case of a rising edge of the signal.

    Returns:
    Busy (bool): TRUE = statement has been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 78
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 2 # Buffered
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_SETDATETIME
#  ******************************************************************************/

class KRC_SETDATETIME:
    """
    The function block KRC_SetDateTime changes the controller's system time.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is buffered in the case of a rising edge of the signal.
    Year (int): New year to be set.
    Month (int): New month to be set.
    Day (int): New day to be set.
    Hour (int): New hour to be set.
    Minute (int): New minute to be set.
    Second (int): New second to be set.

    Returns:
    Busy (bool): TRUE = statement has been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.YEAR = 0
        self.MONTH = 0
        self.DAY = 0
        self.HOUR = 0
        self.MINUTE = 0
        self.SECOND = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 80
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 2 # Buffered
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = self.YEAR
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[2] = self.MONTH
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[3] = self.DAY
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[4] = self.HOUR
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[5] = self.MINUTE
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[6] = self.SECOND

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID



# /******************************************************************************
#  * FUNCTION_BLOCK KRC_SETLANGUAGE
#  ******************************************************************************/

class KRC_SETLANGUAGE:
    """
    The function block KRC_SetLanguage changes the language of the controller's messages sent to KRMsgNet's client.

    Parameters:
    AxisGroupIdx (int): Index of axis group. Range: 1-5.
    ExecuteCmd (bool): The statement is buffered in the case of a rising edge of the signal.
    Language (int): ID of a supported language, currently: 1-EN, 2-DE

    Returns:
    Busy (bool): TRUE = statement has been transferred.
    Done (bool): TRUE = statement has been executed.
    Aborted (bool): TRUE = statement has been aborted.
    Error (bool): TRUE = error in function block.
    ErrorID (int): Error number.
    OrderID (int): Identifier of command instance.
    """
    def __init__(self):
        self.AXISGROUPIDX = 0
        self.EXECUTECMD = False
        self.LANGUAGE = 0
        self._BUSY = False
        self._DONE = False
        self._ABORTED = False
        self._ERROR = False
        self._ERRORID = 0
        self._ORDERID = 0
        self.MXA_EXECUTECOMMAND_1 = MXA_EXECUTECOMMAND()

    @property
    def BUSY(self):
        return self._BUSY

    @property
    def DONE(self):
        return self._DONE

    @property
    def ABORTED(self):
        return self._ABORTED

    @property
    def ERROR(self):
        return self._ERROR

    @property
    def ERRORID(self):
        return self._ERRORID

    @property
    def ORDERID(self):
        return self._ORDERID

    def OnCycle(self):
        self._ORDERID = 0
        if self.AXISGROUPIDX < 1 or self.AXISGROUPIDX > 5:
            self._ERRORID = 506
            self._ERROR = True
            return

        self.MXA_EXECUTECOMMAND_1.AXISGROUPIDX = self.AXISGROUPIDX
        self.MXA_EXECUTECOMMAND_1.EXECUTE = self.EXECUTECMD
        self.MXA_EXECUTECOMMAND_1.CMDID = 79
        self.MXA_EXECUTECOMMAND_1.BUFFERMODE = 2 # Buffered
        self.MXA_EXECUTECOMMAND_1.COMMANDSIZE = 1
        self.MXA_EXECUTECOMMAND_1.ENABLEDIRECTEXE = False
        self.MXA_EXECUTECOMMAND_1.ENABLEQUEUEEXE = True
        self.MXA_EXECUTECOMMAND_1.IGNOREINIT = False
        self.MXA_EXECUTECOMMAND_1.OnCycle()

        if self.MXA_EXECUTECOMMAND_1.WRITECMDPAR:
            KRC_AXISGROUPREFARR[self.AXISGROUPIDX].COMMAND.CMDPARINT[1] = self.LANGUAGE

        self._BUSY = self.MXA_EXECUTECOMMAND_1.BUSY
        self._DONE = self.MXA_EXECUTECOMMAND_1.DONE
        self._ABORTED = self.MXA_EXECUTECOMMAND_1.ABORTED
        self._ERRORID = self.MXA_EXECUTECOMMAND_1.ERRORID
        self._ERROR = self._ERRORID != 0
        self._ORDERID = self.MXA_EXECUTECOMMAND_1.ORDERID
