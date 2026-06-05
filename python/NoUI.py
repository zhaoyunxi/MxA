import mxAutomationV6_0 as mxA
import socket
import time
class MxAInterface:
    def __init__(self):
        # MxAutomation variables
        self.AXISGROUPIDX = 1
        self.KRC_READAXISGROUP = mxA.KRC_READAXISGROUP()
        self.KRC_WRITEAXISGROUP = mxA.KRC_WRITEAXISGROUP()
        self.KRC_INITIALIZE = mxA.KRC_INITIALIZE()
        self.KRC_AUTOMATICEXTERNAL = mxA.KRC_AUTOMATICEXTERNAL()
        self.KRC_AUTOSTART = mxA.KRC_AUTOSTART()
        self.KRC_ERROR = mxA.KRC_ERROR()
        self.KRC_SETOVERRIDE = mxA.KRC_SETOVERRIDE()
        
        # Communication variables
        self.robot_ip = "127.0.0.1"
        self.robot_recv_port = 2001
        self.ctl_recv_port = 2000
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind(('127.0.0.1', self.ctl_recv_port))  # 默认 mxAutomation 端口
        self.receiver.setblocking(0)
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.input_buffer = bytearray(b'\x00') * 256
        self.output_buffer = bytearray(b'\x00') * 256
        self.counter = 1
        self.status = 0
        # AutoExternal variables
        self.ext_start = False
        self.reset = True
        self.drive_on = False
        self.conf_mess = True
        
    def read_from_robot(self):
        try:
            message, address = self.receiver.recvfrom(256)
        except socket.error:
            print("Scoket exception in readAxisGroup")
            return
        buffer = bytearray(message)
        if(len(buffer) >= 246):
            self.input_buffer = buffer
        
        # get the latest robot status
        self.KRC_READAXISGROUP.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_READAXISGROUP.KRC4_INPUT = self.input_buffer
        self.KRC_READAXISGROUP.OnCycle()
        
        if self.KRC_READAXISGROUP.ERROR:
            print("Error by Read Axis Group function block: " + str(self.KRC_READAXISGROUP.ERRORID))
            return
        
        
        return

    
    def send_to_robot(self):
        self.KRC_WRITEAXISGROUP.AXISGROUPIDX = self.AXISGROUPIDX
        self.output_buffer = self.KRC_WRITEAXISGROUP.KRC4_OUTPUT
        self.KRC_WRITEAXISGROUP.OnCycle()
        self.sender.sendto(self.output_buffer, (self.robot_ip, self.robot_recv_port))
        

    def main_loop(self):

        while True:
            
            self.read_from_robot()
            self.updateMxAInterface()
            self.send_to_robot()
            time.sleep(0.05)
            self.counter += 1
            
    def updateMxAInterface(self):
        flag = True
        self.KRC_INITIALIZE.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_INITIALIZE.OnCycle()
        # if self.status == 0:
        #     print("KRC_Initalize Error ID: ",  self.KRC_INITIALIZE.ERRORID , "Done? ", self.KRC_INITIALIZE.DONE , "status", self.status , "KRC_Version:", self.KRC_INITIALIZE.KRC_MAJOR , self.KRC_INITIALIZE.KRC_MINOR , self.KRC_INITIALIZE.KRC_REVISION, "Serial Number: ", self.KRC_INITIALIZE.KRC_SERIAL , "Absolutgenau?" , self.KRC_INITIALIZE.KRC_ABSACCUR)
        #     if self.counter <= 100:
        #         print("100 cycles waiting for krc...")
                
        # if self.status == 0 and self.KRC_INITIALIZE.DONE :
        #     self.status = 10
        #     print("KRC_Initalize Error ID: ",  self.KRC_INITIALIZE.ERRORID , "Done? ", self.KRC_INITIALIZE.DONE , "status", self.status  )
        
        self.KRC_ERROR.AXISGROUPIDX = self.AXISGROUPIDX
        self.KRC_ERROR.MESSAGERESET = self.conf_mess
        self.KRC_ERROR.OnCycle()
        
        
        # if self.status >= 10:
        self.manual_start()
    def manual_start(self):
        self.KRC_AUTOMATICEXTERNAL.AXISGROUPIDX = self.AXISGROUPIDX
        self.drive_on = not self.KRC_AUTOMATICEXTERNAL.PERI_RDY
        self.ext_start = self.KRC_AUTOMATICEXTERNAL.RC_RDY1 and not self.KRC_AUTOMATICEXTERNAL.PRO_ACT
    
        
        self.KRC_AUTOMATICEXTERNAL.EXT_START = self.ext_start
        self.KRC_AUTOMATICEXTERNAL.RESET = self.reset
        self.KRC_AUTOMATICEXTERNAL.MOVE_ENABLE = True
        
        self.KRC_AUTOMATICEXTERNAL.DRIVES_OFF = True
        self.KRC_AUTOMATICEXTERNAL.DRIVES_ON = self.drive_on
        self.KRC_AUTOMATICEXTERNAL.ENABLE_T1 = True
        self.KRC_AUTOMATICEXTERNAL.ENABLE_T2 = True
        self.KRC_AUTOMATICEXTERNAL.ENABLE_AUT = True
        self.KRC_AUTOMATICEXTERNAL.ENABLE_EXT = True
        self.KRC_AUTOMATICEXTERNAL.OnCycle()
        print("input", self.ext_start, " Reset: ", self.reset, " DriveOn: ", self.drive_on, " PeriRdy: ", self.KRC_AUTOMATICEXTERNAL.PERI_RDY, " conf_mess: ", self.conf_mess, " RC_Rdy1: ", self.KRC_AUTOMATICEXTERNAL.RC_RDY1, " ProAct: ", self.KRC_AUTOMATICEXTERNAL.PRO_ACT )
        print(krc_automaticexternal_returns_to_string(self.KRC_AUTOMATICEXTERNAL))

        if self.KRC_AUTOMATICEXTERNAL.PRO_ACT:
            self.conf_mess = False
            self.reset = False
        if self.KRC_AUTOMATICEXTERNAL.STOPMESS:
            self.conf_mess = True
    def auto_start(self):
        self.KRC_AUTOMATICEXTERNAL.AXISGROUPIDX = self.AXISGROUPIDX
        #self.KRC_AUTOMATICEXTERNAL.EXT_START = True
        #self.KRC_AUTOMATICEXTERNAL.RESET = True
        self.KRC_AUTOMATICEXTERNAL.MOVE_ENABLE = True
        self.KRC_AUTOMATICEXTERNAL.DRIVES_OFF = True
        #self.KRC_AUTOMATICEXTERNAL.DRIVES_ON = False
        #self.KRC_AUTOMATICEXTERNAL.ENABLE_T1 = True
        self.KRC_AUTOMATICEXTERNAL.ENABLE_T2 = True
        self.KRC_AUTOMATICEXTERNAL.ENABLE_AUT = True
        self.KRC_AUTOMATICEXTERNAL.ENABLE_EXT = True
        self.KRC_AUTOMATICEXTERNAL.OnCycle()
        
        self.KRC_AUTOSTART.AXISGROUPIDX = self.AXISGROUPIDX
        if self.status == 10:
            self.KRC_AUTOSTART.ExecuteReset = True
            print( "\n", "Autostart --------- > Error ID " , self.KRC_AUTOSTART._ERRORID , "DispActive" , self.KRC_AUTOSTART._DISPACTIVE , " Reset Valid??? " , self.KRC_AUTOSTART._RESETVALID ) 
            print("status: ", self.status  )
        
        if self.status == 10 and self.KRC_AUTOSTART._DISPACTIVE:
            self.KRC_AUTOSTART.ExecuteReset = False
            self.status = 14
        self.KRC_AUTOSTART.OnCycle()

def krc_automaticexternal_returns_to_string(obj):
    """
    将 KRC_AUTOMATICEXTERNAL 对象的返回属性转换为字符串
    
    Args:
        obj: KRC_AUTOMATICEXTERNAL 对象
        
    Returns:
        str: 包含所有返回属性及其值的字符串
    """
    return (
        f"VALID: {obj.VALID}, "
        f"RC_RDY1: {obj.RC_RDY1}, "
        f"ALARM_STOP: {obj.ALARM_STOP}, "
        f"USER_SAFE: {obj.USER_SAFE}, "
        f"PERI_RDY: {obj.PERI_RDY}, "
        f"ROB_CAL: {obj.ROB_CAL}, "
        f"IO_ACTCONF: {obj.IO_ACTCONF}, "
        f"STOPMESS: {obj.STOPMESS}, "
        f"INT_E_STOP: {obj.INT_E_STOP}, "
        f"PRO_ACT: {obj.PRO_ACT}, "
        f"APPL_RUN: {obj.APPL_RUN}, "
        f"PRO_MOVE: {obj.PRO_MOVE}, "
        f"ON_PATH: {obj.ON_PATH}, "
        f"NEAR_POSRET: {obj.NEAR_POSRET}, "
        f"ROB_STOPPED: {obj.ROB_STOPPED}, "
        f"T1: {obj.T1}, "
        f"T2: {obj.T2}, "
        f"AUT: {obj.AUT}, "
        f"EXT: {obj.EXT}"
    )

def main():
    mxaI = MxAInterface()
    mxaI.main_loop()


if __name__ == "__main__":
    main()