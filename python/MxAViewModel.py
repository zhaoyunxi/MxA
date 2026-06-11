# MxAViewModel.py
import sys
import mxAutomationV6_0 as mxA
import time 
import socket 
import threading
from queue import Queue
from dataclasses import dataclass
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal

from utils import LogManager

# Data class definitions
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
class COORDSYS:
    TOOL: int = -1
    BASE: int = -1
    IPO_MODE: int = 0

@dataclass
class APO:
    PTP_MODE: int = 0
    CP_MODE: int = 0
    CPTP: int = 0
    CDIS: float = 0.0
    CORI: float = 0.0
    CVEL: int = 0

# Shared data queues
robot_data_queue = Queue(maxsize=10)
command_queue = Queue(maxsize=10)

class MxAViewModel(QObject):
    """MxAutomation V6.0 ViewModel"""
    # Custom signals for inter-thread communication
    log_updated = pyqtSignal(str)
    robot_data_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        # Initialize the enhanced log manager
        self.logger = LogManager()
        # Connect the logger signal to the ViewModel signal
        self.logger.log_signal.connect(self.log_updated.emit)
        
        # Initialize mxAutomation V6.0 objects
        self._mxA_KRC_READAXISGROUP = mxA.KRC_READAXISGROUP()
        self._mxA_KRC_WRITEAXISGROUP = mxA.KRC_WRITEAXISGROUP()
        self._mxA_READACTUALPOSITION = mxA.KRC_READACTUALPOSITION()
        self._mxA_READACTUALAXISPOSITION = mxA.KRC_READACTUALAXISPOSITION()
        self._mxA_KRC_INITIALIZE = mxA.KRC_INITIALIZE()
        self._mxA_KRC_AUTOMATICEXTERNAL = mxA.KRC_AUTOMATICEXTERNAL()
        self._mxA_KRC_AUTOSTART = mxA.KRC_AUTOSTART()
        self._mxA_KRC_ERROR = mxA.KRC_ERROR()
        self._mxA_KRC_ABORT = mxA.KRC_ABORT()
        self._mxA_KRC_SETOVERRIDE = mxA.KRC_SETOVERRIDE()
        self._mxA_KRC_JOG = mxA.KRC_JOG()
        self._mxA_KRC_MOVEAXISABSOLUTE = mxA.KRC_MOVEAXISABSOLUTE()
    
        self._mxA_KRC_MOVEDIRECTABSOLUTE = mxA.KRC_MOVEDIRECTABSOLUTE()
        self._mxA_KRC_MOVEDIRECTRELATIVE = mxA.KRC_MOVEDIRECTRELATIVE()
        self._mxA_KRC_MOVELINEARABSOLUTE = mxA.KRC_MOVELINEARABSOLUTE()
        self._mxA_KRC_MOVELINEARRELATIVE = mxA.KRC_MOVELINEARRELATIVE()

        self._mxA_KRC_AUTOSTART = mxA.KRC_AUTOSTART()
        self._mxA_KRC_INTERRUPT = mxA.KRC_INTERRUPT()
        self._mxA_KRC_CONTINUE = mxA.KRC_CONTINUE()
        # V6.0 special functions        
        self._mxA_KRC_SETCOORDSYS = mxA.KRC_SETCOORDSYS()
        self._mxA_KRC_TECHFUNCTIONADVANCED = mxA.KRC_TECHFUNCTIONADVANCED()
        self._mxA_KRC_Diag = mxA.KRC_DIAG()
        self._mxA_KRC_Braketest = mxA.KRC_BRAKETEST()
        self._mxA_KRC_ReadSafeOPstatus = mxA.KRC_READSAFEOPSTATUS()

        # Value initialization
        self.axis_target_pos = mxA.E6AXIS() 
        self.direct_target_pos = mxA.E6POS() 
        self.CoordSys_ToolBase = mxA.COORDSYS()
        self.APO_parameter = mxA.APO()
        self.ptp_axis_abs_pos = mxA.E6AXIS(0,0,0,0,0,0)
        self.ptp_cart_abs_pos = mxA.E6POS(0,0,0,0,0,0)
        self.ptp_axis_rel_pos = mxA.E6AXIS(0,0,0,0,0,0)
        self.ptp_cart_rel_pos = mxA.E6POS(0,0,0,0,0,0)
        self.lin_abs_pos = mxA.E6POS(0,0,0,0,0,0)
        self.lin_rel_pos = mxA.E6POS(0,0,0,0,0,0)

        # Spline movement parameters
        self.spline_mode = True
        
        # Configuration parameters
        if True:  # Target position example
            self.APO_parameter.PTP_MODE = 0
            self.APO_parameter.CP_MODE = 0
            self.APO_parameter.CPTP = 50     # %
            self.APO_parameter.CDIS = 45.123 # mm
            self.APO_parameter.CORI = 2.4    # degrees
            self.APO_parameter.CVEL = 50     # %

        # Loop and UDP connection settings
        self.loops = 10000
        self.loop_Time = 0.005
        self.controller_port = 2000
        self.robot_ip = "127.0.0.1"  # Input your KLI IP address
        self.robot_recv_port = 2001
        self._axisGroupIdx = 1
        self.test_step = 0
        self.Movements_in_Spline = True
        self.read_failure_counter = 0
        self.max_read_failure = 100
        self.delay_loop = 40
        self.delay_time = 0.1
        # UDP receiver settings
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind(('127.0.0.1', self.controller_port))  # Default mxAutomation port
        self.receiver.setblocking(0)
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

        self.success = False
        self.message = ""

        self.input_buffer = bytearray(b'\x00') * 256
        self.output_to_robot = bytearray(b'\x00') * 256
        
        # Control flags
        self.start_running = False
        self.pro_active_old = False
        self.pro_active_new = False
        self.ext_start = False
        self.reset_start = False
        self.confirm_msg = False
        self.move_enable = True
        self.drive_off = True
        self.interrupt_pause = False
        self.continue_resume = False
        self.ptp_axis_abs = False
        self.ptp_cart_abs = False
        self.ptp_cart_rel = False
        self.lin_abs = False
        self.lin_rel = False
        self.circ_abs = False
        self.circ_rel = False
        self.splines_abs = False
        self.splines_rel = False
        self.ptp_array = False
        self.lin_array = False
        self.motion_array = False
        self.jog_type = 0  # 0 for axis, 1 for cartesian
        self.program_override = 30
        
        # Jog controls
        self.x_a1_plus = False
        self.y_a2_plus = False
        self.z_a3_plus = False
        self.a_a4_plus = False
        self.b_a5_plus = False
        self.c_a6_plus = False
        self.x_a1_minus = False
        self.y_a2_minus = False
        self.z_a3_minus = False
        self.a_a4_minus = False
        self.b_a5_minus = False
        self.c_a6_minus = False
        
        # Network settings
        self.axis_group_index = 1

        self.cycle_flag = False
        self.cycle_nr = 0
        
        # Main loop related
        self.main_thread = None
        self.stop_event = threading.Event()

        self.error_id = None
        self.new_log_message = ""
        self.log_messages = ""
        
    def read_from_robot(self):
        """read data from robot via UDP"""
        try:
            # NON BLOCKING
            message, address = self.receiver.recvfrom(256)
        except socket.error as e:
            self.logger.log_error("Socket exception in read_from_robot")
            return False
        buffer = bytearray(message)
        if 246 <= len(buffer) and len(buffer) <= 256:
            self.input_buffer = buffer
        else:
            self.logger.log_warning("The length of the buffer is not correct")
            return False
                
        return True

    def send_to_robot(self):    
        """send data to robot"""
        self.sender.sendto(self.output_to_robot, (self.robot_ip, self.robot_recv_port))

    def read(self):
        success = self.read_from_robot()
        if success:
            self.read_failure_counter = 0
        else:
            self.read_failure_counter += 1
            if self.read_failure_counter > self.max_read_failure:
                self.logger.log_error("Failed to read from robot")
                self.disconnect_from_robot()
                return
        self._mxA_KRC_READAXISGROUP.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_READAXISGROUP.KRC4_INPUT = self.input_buffer
        self._mxA_KRC_READAXISGROUP.OnCycle()
        
        if self._mxA_KRC_READAXISGROUP.ERROR:
            self.logger.log_error("Error by KRC_READAXISGROUP : " + str(self._mxA_KRC_READAXISGROUP.ERRORID))
            return

    def write(self):
        self._mxA_KRC_WRITEAXISGROUP.AXISGROUPIDX = self.axis_group_index
        self.output_to_robot = self._mxA_KRC_WRITEAXISGROUP.KRC4_OUTPUT
        self._mxA_KRC_WRITEAXISGROUP.OnCycle()
        self.send_to_robot()

    def update(self):
        self.initialize()
        self.error_check()
        self.auto_ext()
        self.read_real_time_data()
        self.interrupt_and_continue()
        self.move()
        self.set_override()
        self.jog()
        # if self._mxA_KRC_INITIALIZE.DONE:
        #     self.fast_auto_ext()

    def set_override(self):
        self._mxA_KRC_SETOVERRIDE.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_SETOVERRIDE.OVERRIDE = self.program_override
        self._mxA_KRC_SETOVERRIDE.OnCycle()
    
    
    def jog(self):
        self._mxA_KRC_JOG.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_JOG.MOVETYPE = self.jog_type   
        self._mxA_KRC_JOG.VELOCITY = 50 
        self._mxA_KRC_JOG.ACCELERATION = 50
        self._mxA_KRC_JOG.COORDINATESYSTEM = self.CoordSys_ToolBase
        self._mxA_KRC_JOG.INCREMENT = 0
        
        self._mxA_KRC_JOG.A1_X_P = self.x_a1_plus
        self._mxA_KRC_JOG.A1_X_M = self.x_a1_minus
        self._mxA_KRC_JOG.A2_Y_P = self.y_a2_plus
        self._mxA_KRC_JOG.A2_Y_M = self.y_a2_minus
        self._mxA_KRC_JOG.A3_Z_P = self.z_a3_plus
        self._mxA_KRC_JOG.A3_Z_M = self.z_a3_minus
        self._mxA_KRC_JOG.A4_A_P = self.a_a4_plus
        self._mxA_KRC_JOG.A4_A_M = self.a_a4_minus
        self._mxA_KRC_JOG.A5_B_P = self.b_a5_plus
        self._mxA_KRC_JOG.A5_B_M = self.b_a5_minus
        self._mxA_KRC_JOG.A6_C_P = self.c_a6_plus
        self._mxA_KRC_JOG.A6_C_M = self.c_a6_minus
        
        self._mxA_KRC_JOG.OnCycle()
        
    
    
    def move(self):
        self.ptp_move()
        self.lin_move()
    
    
    def ptp_move(self):
        self.ptp_move_axis_abs()
        self.ptp_move_axis_rel()
        self.ptp_move_cart_abs()
        self.ptp_move_cart_rel()
    def ptp_move_axis_abs(self):
        #  PTP Axis Absolute movement
        self._mxA_KRC_MOVEAXISABSOLUTE.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_MOVEAXISABSOLUTE.EXECUTECMD = self.ptp_axis_abs
        self._mxA_KRC_MOVEAXISABSOLUTE.AXISPOSITION = self.ptp_axis_abs_pos
        self._mxA_KRC_MOVEAXISABSOLUTE.VELOCITY = 50
        self._mxA_KRC_MOVEAXISABSOLUTE.ACCELERATION = 50    
        self._mxA_KRC_MOVEAXISABSOLUTE.SPLINEMODE = self.spline_mode
        self._mxA_KRC_MOVEAXISABSOLUTE.BUFFERMODE = 2
        
        self._mxA_KRC_MOVEAXISABSOLUTE.OnCycle()
        
        if self._mxA_KRC_MOVEAXISABSOLUTE.DONE or self._mxA_KRC_MOVEAXISABSOLUTE.ERROR or self._mxA_KRC_MOVEAXISABSOLUTE.ABORTED:
            self.ptp_axis_abs = False
        
    def ptp_move_axis_rel(self):
        #  PTP Axis Relative movement is not supported by MxA
        pass

    def ptp_move_cart_abs(self):
        
        # The turn and status of new position are the same with the current position
        self.ptp_cart_abs_pos.STATUS = self._mxA_READACTUALPOSITION.STATUS
        self.ptp_cart_abs_pos.TURN = self._mxA_READACTUALPOSITION.TURN
        
        #  PTP Cartesian Absolute movement
        self._mxA_KRC_MOVEDIRECTABSOLUTE.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_MOVEDIRECTABSOLUTE.EXECUTECMD = self.ptp_cart_abs
        self._mxA_KRC_MOVEDIRECTABSOLUTE.POSITION = self.ptp_cart_abs_pos
        self._mxA_KRC_MOVEDIRECTABSOLUTE.VELOCITY = 50
        self._mxA_KRC_MOVEDIRECTABSOLUTE.ACCELERATION = 50
        self._mxA_KRC_MOVEDIRECTABSOLUTE.BUFFERMODE = 2
        self._mxA_KRC_MOVEDIRECTABSOLUTE.SPLINEMODE = self.spline_mode
        
        self._mxA_KRC_MOVEDIRECTABSOLUTE.OnCycle()
        
        if self._mxA_KRC_MOVEDIRECTABSOLUTE.DONE or self._mxA_KRC_MOVEDIRECTABSOLUTE.ERROR or self._mxA_KRC_MOVEDIRECTABSOLUTE.ABORTED:
            self.ptp_cart_abs = False
        
        
    def ptp_move_cart_rel(self):
        # The turn and status of new position are the same with the current position
        # self.ptp_cart_abs_pos.STATUS = self._mxA_READACTUALPOSITION.STATUS
        # self.ptp_cart_abs_pos.TURN = self._mxA_READACTUALPOSITION.TURN
        
        #  PTP Cartesian Absolute movement
        self._mxA_KRC_MOVEDIRECTRELATIVE.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_MOVEDIRECTRELATIVE.EXECUTECMD = self.ptp_cart_rel
        self._mxA_KRC_MOVEDIRECTRELATIVE.POSITION = self.ptp_cart_rel_pos
        self._mxA_KRC_MOVEDIRECTRELATIVE.VELOCITY = 50
        self._mxA_KRC_MOVEDIRECTRELATIVE.ACCELERATION = 50
        self._mxA_KRC_MOVEDIRECTRELATIVE.BUFFERMODE = 2
        self._mxA_KRC_MOVEDIRECTRELATIVE.SPLINEMODE = self.spline_mode
        
        self._mxA_KRC_MOVEDIRECTRELATIVE.OnCycle()
        
        if self._mxA_KRC_MOVEDIRECTRELATIVE.DONE or self._mxA_KRC_MOVEDIRECTRELATIVE.ERROR or self._mxA_KRC_MOVEDIRECTRELATIVE.ABORTED:
            self.ptp_cart_abs = False
    
    def lin_move(self):
        self.lin_move_cart_abs()
        self.lin_move_cart_rel()
    
    def lin_move_cart_abs(self):
        
        self._mxA_KRC_MOVELINEARABSOLUTE.AXISGROUPIDX = self._axisGroupIdx
        self._mxA_KRC_MOVELINEARABSOLUTE.EXECUTECMD = self.lin_abs
        self._mxA_KRC_MOVELINEARABSOLUTE.POSITION = self.lin_abs_pos
        self._mxA_KRC_MOVELINEARABSOLUTE.VELOCITY = 50
        self._mxA_KRC_MOVELINEARABSOLUTE.ACCELERATION = 50
        self._mxA_KRC_MOVELINEARABSOLUTE.BUFFERMODE = 2
        self._mxA_KRC_MOVELINEARABSOLUTE.OnCycle()
        
        if self._mxA_KRC_MOVELINEARABSOLUTE.DONE or self._mxA_KRC_MOVELINEARABSOLUTE.ERROR or self._mxA_KRC_MOVELINEARABSOLUTE.ABORTED:
            self.lin_abs = False

    def lin_move_cart_rel(self):
        
        self._mxA_KRC_MOVELINEARRELATIVE.AXISGROUPIDX = self._axisGroupIdx
        self._mxA_KRC_MOVELINEARRELATIVE.EXECUTECMD = self.lin_rel
        self._mxA_KRC_MOVELINEARRELATIVE.POSITION = self.lin_rel_pos
        self._mxA_KRC_MOVELINEARRELATIVE.VELOCITY = 50
        self._mxA_KRC_MOVELINEARRELATIVE.ACCELERATION = 50
        self._mxA_KRC_MOVELINEARRELATIVE.BUFFERMODE = 2
        self._mxA_KRC_MOVELINEARRELATIVE.OnCycle()
        if self._mxA_KRC_MOVELINEARRELATIVE.DONE or self._mxA_KRC_MOVELINEARRELATIVE.ERROR or self._mxA_KRC_MOVELINEARRELATIVE.ABORTED:
            self.lin_rel = False
    def interrupt_and_continue(self):
        
        self._mxA_KRC_INTERRUPT.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_INTERRUPT.EXECUTE = self.interrupt_pause
        self._mxA_KRC_INTERRUPT.FAST = True
        self._mxA_KRC_INTERRUPT.OnCycle()
        
        
        self._mxA_KRC_CONTINUE.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_CONTINUE.ENABLE = self.continue_resume        
        self._mxA_KRC_CONTINUE.OnCycle()
        if(self.continue_resume and not self._mxA_KRC_INTERRUPT.BRAKEACTIVE):
            self.continue_resume = False
        
        
    def read_real_time_data(self):
        
        self._mxA_READACTUALAXISPOSITION.AXISGROUPIDX = self.axis_group_index
        self._mxA_READACTUALAXISPOSITION.OnCycle()
        
        self._mxA_READACTUALPOSITION.AXISGROUPIDX = self.axis_group_index
        self._mxA_READACTUALPOSITION.OnCycle()
        
    def fast_auto_ext(self):
        # Note that the conf_mess of KRC_AUTOMATICEXTERNAL is useless,  which can not confirm the message.
        # the error message must be confirmed by the KRC_ERROR
        self._mxA_KRC_AUTOMATICEXTERNAL.AXISGROUPIDX = self.axis_group_index

        self._mxA_KRC_AUTOMATICEXTERNAL.MOVE_ENABLE = self.move_enable
        self._mxA_KRC_AUTOMATICEXTERNAL.DRIVES_OFF = self.drive_off
        #self._mxA_KRC_AUTOMATICEXTERNAL.MOVE_ENABLE = True
        #self._mxA_KRC_AUTOMATICEXTERNAL.DRIVES_OFF = True
        self._mxA_KRC_AUTOMATICEXTERNAL.ENABLE_T1 = True
        self._mxA_KRC_AUTOMATICEXTERNAL.ENABLE_T2 = True
        self._mxA_KRC_AUTOMATICEXTERNAL.ENABLE_AUT = True
        self._mxA_KRC_AUTOMATICEXTERNAL.ENABLE_EXT = True
        
        self._mxA_KRC_AUTOMATICEXTERNAL.OnCycle()
        
        self._mxA_KRC_AUTOSTART.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_AUTOSTART.ExecuteReset = self.reset_start
        self._mxA_KRC_AUTOSTART.OnCycle()
        
        
        if self._mxA_KRC_AUTOSTART.DISPACTIVE:
            self.reset_start = False
            self.pro_active_new = True
        else:
            self.pro_active_new = False

    def fast_connect_to_robot(self):
        """Connect to robot"""
        self.cycle_flag = True
        self.start_running = True

        
        # Create and start main loop thread
        if self.main_thread is None or not self.main_thread.is_alive():
            self.stop_event.clear()
            self.main_thread = threading.Thread(target=self.new_main_loop, daemon=True)
            self.main_thread.start()
            self.logger.log_info("Start thread")
        
        self.move_enable = True
        self.drive_off = True
        self.reset_start = True
        return True

    def auto_ext(self):
        
        # Note that the conf_mess of KRC_AUTOMATICEXTERNAL is useless,  which can not confirm the message.
        # the error message must be confirmed by the KRC_ERROR
        self._mxA_KRC_AUTOMATICEXTERNAL.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_AUTOMATICEXTERNAL.EXT_START = self.ext_start
        self._mxA_KRC_AUTOMATICEXTERNAL.RESET = self.reset_start
        self._mxA_KRC_AUTOMATICEXTERNAL.MOVE_ENABLE = self.move_enable
        self._mxA_KRC_AUTOMATICEXTERNAL.DRIVES_OFF = self.drive_off
        self._mxA_KRC_AUTOMATICEXTERNAL.DRIVES_ON = False  # ?
        self._mxA_KRC_AUTOMATICEXTERNAL.ENABLE_T1 = True
        self._mxA_KRC_AUTOMATICEXTERNAL.ENABLE_T2 = True
        self._mxA_KRC_AUTOMATICEXTERNAL.ENABLE_AUT = True
        self._mxA_KRC_AUTOMATICEXTERNAL.ENABLE_EXT = True
        
        self._mxA_KRC_AUTOMATICEXTERNAL.OnCycle()
        
        if self._mxA_KRC_AUTOMATICEXTERNAL.PRO_ACT:
            self.pro_active_new = True
            #self.confirm_msg = False
        else:
            self.pro_active_new = False
        # print("ext_start: " + str(self._mxA_KRC_AUTOMATICEXTERNAL.EXT_START) + " reset_start: " + str(self._mxA_KRC_AUTOMATICEXTERNAL.RESET) + " move_enable: " + str(self._mxA_KRC_AUTOMATICEXTERNAL.MOVE_ENABLE) + " drive_off: " + str(self._mxA_KRC_AUTOMATICEXTERNAL.DRIVES_OFF) + " peri_rdy: " + str(self._mxA_KRC_AUTOMATICEXTERNAL.PERI_RDY) + " rc_rdy1: " + str(self._mxA_KRC_AUTOMATICEXTERNAL.RC_RDY1) + " pro_act: " + str(self._mxA_KRC_AUTOMATICEXTERNAL.PRO_ACT) )
        # print(self.krc_automaticexternal_returns_to_string(self._mxA_KRC_AUTOMATICEXTERNAL))

    

    
    def initialize(self):
        self._mxA_KRC_INITIALIZE.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_INITIALIZE.OnCycle()
        if self._mxA_KRC_INITIALIZE.ERROR:
            self.logger.log_error("KRC_INITIALIZE error ID: " + str(self._mxA_KRC_INITIALIZE.ERRORID))

    def error_check(self):
        """
            self._mxA_KRC_ERROR.AXISGROUPIDX = self.axis_group_index
            self._mxA_KRC_ERROR.OnCycle()
            
            if self._mxA_KRC_ERROR.ERROR:
                self.logger.log_error("KRC_ERROR error ID: " + str(self._mxA_KRC_ERROR.ERRORID))
                self.error_id = self._mxA_KRC_ERROR.ERRORID
            else:
                self.error_id = 0
            
            self._mxA_KRC_ERROR.MESSAGERESET = self.confirm_msg
            self._mxA_KRC_ERROR.OnCycle()
            
            the codes above is written by the original idea from me, we will find out that it is equivalent to the following
            code if the source of confirm_msg is UI.
        """
        self._mxA_KRC_ERROR.AXISGROUPIDX = self.axis_group_index
        self._mxA_KRC_ERROR.MESSAGERESET = self.confirm_msg
        self._mxA_KRC_ERROR.OnCycle()
        
        if self._mxA_KRC_ERROR.ERROR:            
            self.error_id = self._mxA_KRC_ERROR.ERRORID
        else:
            self.error_id = 0
            self.confirm_msg = False

    def new_main_loop(self):
        
        while self.cycle_flag:
            time.sleep(self.loop_Time)
            self.read()
            self.update()
            self.write()
            self.cycle_nr += 1
            #print(f"Cycle number: {self.cycle_nr}")
        
    def is_in_EXT(self):
        for i in range(self.delay_loop):
            if (self._mxA_KRC_AUTOMATICEXTERNAL.EXT and self.cycle_nr > 0):
                break
            time.sleep(self.delay_time)
        return self._mxA_KRC_AUTOMATICEXTERNAL.EXT

    # def set_drive_off(self):
    #     self.drive_off = True
    
    def set_drive_on(self):
        for i in range(self.delay_loop):
            self.drive_off = True
            if(self._mxA_KRC_AUTOMATICEXTERNAL.PERI_RDY):
                break
            time.sleep(self.delay_time)
        return self._mxA_KRC_AUTOMATICEXTERNAL.PERI_RDY
    
    def set_motor_on(self):
        for i in range(self.delay_loop):
            self.move_enable = True
            if (self._mxA_KRC_AUTOMATICEXTERNAL.RC_RDY1):
                break
            time.sleep(self.delay_time)
        return self._mxA_KRC_AUTOMATICEXTERNAL.RC_RDY1

    def reset_error(self):
        for i in range(self.delay_loop):
            self.confirm_msg = True
            if (not self._mxA_KRC_ERROR.ERROR):
                break
            time.sleep(self.delay_time)
        return not self._mxA_KRC_ERROR.ERROR

    def isProgramRunning(self):
        """Check if program is running"""
        for i in range(self.delay_loop):
            if (self._mxA_KRC_AUTOMATICEXTERNAL.PRO_ACT):
                break
            time.sleep(self.delay_time)
        return self._mxA_KRC_AUTOMATICEXTERNAL.PRO_ACT
    
    def connect_to_robot(self):
        """Connect to robot"""
        self.cycle_flag = True
        # Create and start main loop thread
        if self.main_thread is None or not self.main_thread.is_alive():
            self.stop_event.clear()
            self.main_thread = threading.Thread(target=self.new_main_loop, daemon=True)
            self.main_thread.start()
            self.logger.log_info("Start thread")
            
        if not self.is_in_EXT():
            self.logger.log_error("Cannot enter external auto mode, please check connection and robot status!")
            return
        else:
            self.logger.log_info("Robot is in external auto mode")
            
        if not self.set_drive_on():
            self.logger.log_error("Cannot turn on drives, please check connection and robot status!")
            return
        else:
            self.logger.log_info("Drives are turned on")
            
        self.confirm_msg = True
        if not self.set_motor_on():
            self.logger.log_error("Cannot turn on motors, please check connection and robot status!")
            return
        else:
            self.logger.log_info("Motors are turned on")
        
        if not self.reset_error():
            self.logger.log_error("Cannot reset errors, please check connection and robot status!")
            return
        else:
            self.logger.log_info("Errors are reset")
            
        self.reset_start = True 
        
        if not self.isProgramRunning():
            self.logger.log_error("No program is running, please start a program on the robot!")
        else:
            self.logger.log_info("The robot is started successfully!")

            self.start_running = True

        self.reset_start = False
        
        return True

    def disconnect_from_robot(self):
        """Disconnect from robot"""

        # Stop the robot by switching off drive
        self.drive_off = False
        for i in range(self.delay_loop):
            if (not self._mxA_KRC_AUTOMATICEXTERNAL.PRO_ACT):
                break
            time.sleep(self.delay_time)
            
        if self._mxA_KRC_AUTOMATICEXTERNAL.PRO_ACT:
            self.logger.log_error("Cannot stop the robot, please check connection and robot status!")
        else:
            self.logger.log_info("Robot has been stopped successfully!")
        
        self.cycle_flag = False
        self.start_running = False
        self.pro_active_new = False
        
        # Stop main loop thread
        if self.main_thread and self.main_thread.is_alive():
            self.stop_event.set()
            self.main_thread.join(timeout=2)  # Wait up to 2 seconds for thread to end
            self.main_thread = None
        
        # Close network connections
        try:
            self.receiver.close()
        except:
            pass
        
        self.logger.log_info("Successfully disconnected from robot!")

    def pause_robot(self):
        """Pause robot"""
        self.drive_off = False
        for i in range(self.delay_loop):
            if (not self._mxA_KRC_AUTOMATICEXTERNAL.PRO_ACT):
                break
            time.sleep(self.delay_time)
        
        if (self._mxA_KRC_AUTOMATICEXTERNAL.PRO_ACT):
            self.logger.log_error("Cannot pause the robot, please check connection and robot status!")
        else:
            self.logger.log_info("Robot paused successfully!")  


    def resume_robot(self):
        """Resume robot operation"""
        if not self.is_in_EXT():
            self.logger.log_error("Cannot resume robot, Robot is not in EXT mode!")
            return 
        
        if not self.set_drive_on():
            self.logger.log_error("Cannot turn on drives,  drive is off")
            return

        self.confirm_msg = True
        
        if not self.set_motor_on():
            self.logger.log_error("Cannot turn on motors,  move enable is invalid")
            return

        self.ext_start = True
        
        if not self.isProgramRunning():
            self.logger.log_error("Failed to resume robot")
        else:
            self.logger.log_info("resume robot successfully!")


        self.ext_start = False
        
        return True
        

    def reset_robot(self):
        if not self.is_in_EXT():
            self.logger.log_error("Cannot reset robot, Robot is not in EXT mode!")
            return
            
        if not self.set_drive_on():
            self.logger.log_error("Cannot reset robot, robot drive is off!")
            return

            
        self.confirm_msg = True
        if not self.set_motor_on():
            self.logger.log_error("Cannot reset robot, robot drive is off!")
            return

        
        if not self.reset_error():
            self.logger.log_error("Cannot reset errors, there are errors in robot!")
            return

            
        self.reset_start = True 
        
        if not self.isProgramRunning():
            self.logger.log_error("Cannot reset program, please start a program on the robot!")
        else:
            self.logger.log_info("The robot is started successfully!")

            self.start_running = True

        self.reset_start = False
        
        return True

    def interrupt_robot(self):
        """Interrupt robot"""
        self.interrupt_pause = True
        time.sleep(0.05)
        self.logger.log_info("Robot has been interrupted!")

    def continue_robot(self):
        """Continue robot operation"""
        self.interrupt_pause = False
        time.sleep(0.05)
        self.continue_resume = True
        self.logger.log_info("Robot operation continued!")
    
    def confirm_error(self):
        """Confirm error"""
        self.confirm_msg = True
        self.logger.log_info("Error confirmed!")

    def send_ptp_axis_abs(self, axis_data: E6AXIS):
        """Send PTP axis absolute command"""
        self.ptp_axis_abs = True
        self.ptp_axis_abs_pos = axis_data
        self.logger.log_info("PTP axis absolute command sent!")
    
    def send_ptp_axis_rel(self, axis_data: E6AXIS):
        """Send PTP axis relative command"""
        self.logger.log_error("This movement type is not supported by mxAutomation!")

    def send_ptp_pos_abs(self, pos_data: E6POS):
        """Send PTP position absolute command"""
        self.ptp_cart_abs = True
        self.ptp_cart_abs_pos = pos_data
        self.logger.log_info("PTP position absolute command sent!")

    def send_ptp_pos_rel(self, pos_data: E6POS):
        """Send PTP position relative command"""
        self.ptp_cart_rel = True
        self.ptp_cart_rel_pos = pos_data
        self.logger.log_info("PTP position relative command sent!")

    def send_lin_pos_abs(self, pos_data: E6POS):
        """Send LIN position absolute command"""
        self.lin_abs = True
        self.lin_abs_pos = pos_data
        self.logger.log_info("LIN position absolute command sent!")

    def send_lin_pos_rel(self, pos_data: E6POS):
        """Send LIN position relative command"""
        self.lin_rel = True
        self.lin_rel_pos = pos_data
        self.logger.log_info("LIN position relative command sent!")

    def send_circ_pos_abs(self, pos_data: E6POS):
        """Send CIRC position absolute command"""
        self.circ_abs = True
        self.circ_abs_pos = pos_data
        self.logger.log_info("CIRC position absolute command sent!")

    def send_circ_pos_rel(self):
        """Send CIRC position relative command"""
        self.circ_rel = True
        self.logger.log_info("CIRC position relative command sent!")

    def send_splines_pos_abs(self):
        """Send SPLINES position absolute command"""
        self.splines_abs = True
        self.logger.log_info("SPLINES position absolute command sent!")

    def send_splines_pos_rel(self):
        """Send SPLINES position relative command"""
        self.splines_rel = True
        self.logger.log_info("SPLINES position relative command sent!")