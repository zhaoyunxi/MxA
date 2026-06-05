# mxA_Python_exampleV6_0.py
# 示例程序使用 mxAutomationV6.0 库

import sys
import mxAutomationV6_0 as mxA
import time 
import socket 
import threading
from queue import Queue
from dataclasses import dataclass
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QGroupBox, QPushButton, QLabel, QLineEdit, 
    QTextEdit, QSlider, QTabWidget, QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QColor

from utils import LogManager

# 数据类定义
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

# 共享数据队列
robot_data_queue = Queue(maxsize=10)
command_queue = Queue(maxsize=10)

class MxAViewModel(QObject):
    """MxAutomation V6.0 ViewModel"""
    # 自定义信号用于线程间通信
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
        self._mxA_KRC_JOGADVANCED = mxA.KRC_JOGADVANCED()
        self._mxA_KRC_MOVEAXISABSOLUTE = mxA.KRC_MOVEAXISABSOLUTE()
        self._mxA_KRC_MOVEDIRECTABSOLUTE = mxA.KRC_MOVEDIRECTABSOLUTE()
        self._mxA_KRC_MOVEDIRECTRELATIVE = mxA.KRC_MOVEDIRECTRELATIVE()
        self._mxA_KRC_MOVELINEARABSOLUTE = mxA.KRC_MOVELINEARABSOLUTE()
        self._mxA_KRC_MOVELINEARRELATIVE = mxA.KRC_MOVELINEARRELATIVE()
        self._mxA_KRC_MOVECIRCULARABSOLUTE = mxA.KRC_MOVECIRCABSOLUTE()
        self._mxA_KRC_MOVECIRCULARRELATIVE = mxA.KRC_MOVECIRCRELATIVE()
        self._mxA_KRC_AUTOSTART = mxA.KRC_AUTOSTART()
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
        self.max_read_failure = 500
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
        except socket.error:
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
        """发送数据到机器人"""
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
        #self.auto_ext()
        if self._mxA_KRC_INITIALIZE.DONE:
            self.fast_auto_ext()
        
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

        self.print_krc_autostart_properties()
    def print_krc_autostart_properties(self):
        """
        打印 _mxA_KRC_AUTOSTART 对象的所有属性（包括输入和输出）
        """
        autostart_obj = self._mxA_KRC_AUTOSTART
        
        print("="*50)
        print("KRC_AUTOSTART 属性列表:")
        print("="*50)
        
        # 输入属性 (Input Properties)
        print("输入属性 (Input):")
        print(f"  AXISGROUPIDX: {autostart_obj.AXISGROUPIDX}")
        print(f"  ExecuteReset: {autostart_obj.ExecuteReset}")
        
        # 输出属性 (Output Properties)  
        print("\n输出属性 (Output):")
        print(f"  DONE: {autostart_obj.DONE}")
        print(f"  ERROR: {autostart_obj.ERROR}")
        print(f"  ERRORID: {autostart_obj.ERRORID}")
        print(f"  BUSY: {autostart_obj.BUSY}")
        print(f"  DISPACTIVE: {autostart_obj.DISPACTIVE}")
        print(f"  RESETVALID: {autostart_obj.RESETVALID}")
        
        print("="*50)
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
            #self.logger.log_error("KRC_ERROR error ID: " + str(self._mxA_KRC_ERROR.ERRORID))
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
            print(f"Cycle number: {self.cycle_nr}")
        
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
        self.start_running = True

        
        # Create and start main loop thread
        if self.main_thread is None or not self.main_thread.is_alive():
            self.stop_event.clear()
            self.main_thread = threading.Thread(target=self.new_main_loop, daemon=True)
            self.main_thread.start()
            self.logger.log_info("Start thread")
            
        if not self.is_in_EXT():
            self.logger.log_error("Cannot enter external auto mode, please check connection and robot status!")
            return
        
        if not self.set_drive_on():
            self.logger.log_error("Cannot turn on drives, please check connection and robot status!")
            return
        
        self.confirm_msg = True

        if not self.set_motor_on():
            self.logger.log_error("Cannot turn on motors, please check connection and robot status!")
            return

        
        if not self.reset_error():
            self.logger.log_error("Cannot reset errors, please check connection and robot status!")
            return

        self.reset_start = True 
        
        if not self.isProgramRunning():
            self.logger.log_error("No program is running, please start a program on the robot!")
        else:
            self.logger.log_info("The robot is started successfully!")

        self.reset_start = False
        
        return True

    def disconnect_from_robot(self):
        """Disconnect from robot"""
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
        self.logger.log_info("Robot paused!")

    def resume_robot(self):
        """Resume robot operation"""
        self.drive_off = True
        self.logger.log_info("Robot resumed!")

    def reset_robot(self):
        """Reset robot"""
        self.logger.log_info("Robot has been reset!")

    def interrupt_robot(self):
        """Interrupt robot"""
        self.interrupt_pause = True
        self.logger.log_info("Robot has been interrupted!")

    def continue_robot(self):
        """Continue robot operation"""
        self.interrupt_pause = False
        self.continue_resume = True
        self.logger.log_info("Robot operation continued!")
    
    def confirm_error(self):
        """Confirm error"""
        self.confirm_msg = True
        self.logger.log_info("Error confirmed!")

    def send_ptp_axis_abs(self):
        """Send PTP axis absolute command"""
        self.ptp_axis_abs = True
        self.logger.log_info("PTP axis absolute command sent!")

    def send_ptp_pos_abs(self):
        """Send PTP position absolute command"""
        self.ptp_cart_abs = True
        self.logger.log_info("PTP position absolute command sent!")

    def send_ptp_pos_rel(self):
        """Send PTP position relative command"""
        self.ptp_cart_rel = True
        self.logger.log_info("PTP position relative command sent!")

    def send_lin_pos_abs(self):
        """Send LIN position absolute command"""
        self.lin_abs = True
        self.logger.log_info("LIN position absolute command sent!")

    def send_lin_pos_rel(self):
        """Send LIN position relative command"""
        self.lin_rel = True
        self.logger.log_info("LIN position relative command sent!")

    def send_circ_pos_abs(self):
        """Send CIRC position absolute command"""
        self.circ_abs = True
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
class MxAView(QMainWindow):
    """PyQt6 风格的界面视图"""
    def __init__(self, view_model: MxAViewModel):
        super().__init__()
        self.vm = view_model
        self.init_ui()
        self.setup_connections()
        
        # 定时器更新显示
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(100)  # 每100ms更新一次

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("MxAutomation V6.0 示例程序")
        self.setGeometry(100, 100, 1400, 900)
        
        # 设置样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #fafafa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px 0 5px;
                color: #333333;
            }
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #4a90e2, stop: 1 #357abd);
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #357abd, stop: 1 #2a5a8c);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #2a5a8c, stop: 1 #1f4a7a);
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #d3d3d3;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #4a90e2, stop: 1 #357abd);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                font-family: Consolas, monospace;
                font-size: 10pt;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                font-size: 10pt;
            }
            QLabel {
                font-size: 10pt;
                color: #333333;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 8px 16px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #4a90e2;
                color: white;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 顶部连接控制区域
        top_layout = self.create_top_control_panel()
        main_layout.addLayout(top_layout)
        
        # 中央内容区域
        center_layout = self.create_center_content()
        main_layout.addLayout(center_layout)
        
        # 底部日志区域
        log_layout = self.create_log_panel()
        main_layout.addLayout(log_layout)

    def create_top_control_panel(self):
        """创建顶部控制面板"""
        layout = QHBoxLayout()
        
        # 机器人 IP 输入
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("机器人 IP:"))
        self.ip_input = QLineEdit(self.vm.robot_ip)
        self.ip_input.setMaximumWidth(150)
        ip_layout.addWidget(self.ip_input)
        layout.addLayout(ip_layout)
        
        # 连接/断开按钮
        self.connect_btn = QPushButton("连接")
        self.disconnect_btn = QPushButton("断开")
        self.disconnect_btn.setEnabled(False)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.connect_btn)
        btn_layout.addWidget(self.disconnect_btn)
        layout.addLayout(btn_layout)
        
        # 覆盖率控制
        override_layout = QHBoxLayout()
        override_layout.addWidget(QLabel("覆盖率:"))
        self.override_slider = QSlider(Qt.Orientation.Horizontal)
        self.override_slider.setRange(0, 100)
        self.override_slider.setValue(self.vm.program_override)
        self.override_label = QLabel(f"{self.vm.program_override}%")
        self.override_label.setMinimumWidth(40)
        
        override_layout.addWidget(self.override_slider)
        override_layout.addWidget(self.override_label)
        layout.addLayout(override_layout)
        
        # 添加弹性空间
        layout.addStretch()
        
        return layout

    def create_center_content(self):
        """创建中心内容区域"""
        layout = QHBoxLayout()
        
        # 左侧面板 - 控制和移动命令
        left_panel = self.create_left_panel()
        layout.addLayout(left_panel)
        
        # 右侧面板 - 状态信息
        right_panel = self.create_right_panel()
        layout.addLayout(right_panel)
        
        return layout

    def create_left_panel(self):
        """创建左侧面板"""
        layout = QVBoxLayout()
        
        # 控制按钮组
        control_group = QGroupBox("控制")
        control_layout = QHBoxLayout(control_group)
        
        self.pause_btn = QPushButton("暂停")
        self.resume_btn = QPushButton("恢复")
        self.reset_btn = QPushButton("重置")
        self.interrupt_btn = QPushButton("中断")
        self.continue_btn = QPushButton("继续")
        self.confirm_error_btn = QPushButton("确认错误")
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.resume_btn)
        control_layout.addWidget(self.reset_btn)
        control_layout.addWidget(self.interrupt_btn)
        control_layout.addWidget(self.continue_btn)
        control_layout.addWidget(self.confirm_error_btn)
        
        layout.addWidget(control_group)
        
        # 移动命令按钮组
        move_group = QGroupBox("移动命令")
        move_layout = QGridLayout(move_group)
        
        self.ptp_axis_abs_btn = QPushButton("PTP 轴绝对")
        self.ptp_pos_abs_btn = QPushButton("PTP 位置绝对")
        self.ptp_pos_rel_btn = QPushButton("PTP 位置相对")
        self.lin_pos_abs_btn = QPushButton("LIN 位置绝对")
        self.lin_pos_rel_btn = QPushButton("LIN 位置相对")
        self.circ_pos_abs_btn = QPushButton("CIRC 位置绝对")
        self.circ_pos_rel_btn = QPushButton("CIRC 位置相对")
        self.splines_pos_abs_btn = QPushButton("SPLINES 位置绝对")
        self.splines_pos_rel_btn = QPushButton("SPLINES 位置相对")
        self.jog_type_btn = QPushButton("切换点动模式")
        
        move_layout.addWidget(self.ptp_axis_abs_btn, 0, 0)
        move_layout.addWidget(self.ptp_pos_abs_btn, 0, 1)
        move_layout.addWidget(self.ptp_pos_rel_btn, 0, 2)
        move_layout.addWidget(self.lin_pos_abs_btn, 1, 0)
        move_layout.addWidget(self.lin_pos_rel_btn, 1, 1)
        move_layout.addWidget(self.circ_pos_abs_btn, 1, 2)
        move_layout.addWidget(self.circ_pos_rel_btn, 2, 0)
        move_layout.addWidget(self.splines_pos_abs_btn, 2, 1)
        move_layout.addWidget(self.splines_pos_rel_btn, 2, 2)
        move_layout.addWidget(self.jog_type_btn, 2, 3)
        
        layout.addWidget(move_group)
        
        # 点动控制按钮组
        jog_group = QGroupBox("点动控制")
        jog_layout = QGridLayout(jog_group)
        
        # 创建点动按钮矩阵
        self.jog_buttons = {}
        jog_labels = [
            ("A1+", "A1-"),
            ("A2+", "A2-"),
            ("A3+", "A3-"),
            ("A4+", "A4-"),
            ("A5+", "A5-"),
            ("A6+", "A6-")
        ]
        
        for i, (pos_label, neg_label) in enumerate(jog_labels):
            pos_btn = QPushButton(pos_label)
            neg_btn = QPushButton(neg_label)
            
            # 设置按钮大小策略
            pos_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            neg_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            
            # 存储按钮引用
            self.jog_buttons[f"{pos_label}_btn"] = pos_btn
            self.jog_buttons[f"{neg_label}_btn"] = neg_btn
            
            # 连接点击事件
            pos_btn.clicked.connect(lambda checked, lbl=pos_label: self.jog_button_clicked(lbl))
            neg_btn.clicked.connect(lambda checked, lbl=neg_label: self.jog_button_clicked(lbl))
            
            jog_layout.addWidget(pos_btn, i, 0)
            jog_layout.addWidget(neg_btn, i, 1)
        
        layout.addWidget(jog_group)
        
        # 添加弹性空间
        layout.addStretch()
        
        return layout

    def create_right_panel(self):
        """创建右侧面板"""
        layout = QVBoxLayout()
        
        # 状态信息组
        status_group = QGroupBox("状态信息")
        status_layout = QGridLayout(status_group)
        
        # 错误ID
        status_layout.addWidget(QLabel("错误ID:"), 0, 0)
        self.error_id_label = QLabel(self.vm.error_id)
        self.error_id_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
        status_layout.addWidget(self.error_id_label, 0, 1)
        
        # 运行状态
        status_layout.addWidget(QLabel("运行状态:"), 1, 0)
        self.running_status_label = QLabel("停止")
        self.running_status_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
        status_layout.addWidget(self.running_status_label, 1, 1)
        
        # 循环计数
        status_layout.addWidget(QLabel("循环计数:"), 2, 0)
        self.loop_count_label = QLabel("0")
        status_layout.addWidget(self.loop_count_label, 2, 1)
        
        # 测试步骤
        status_layout.addWidget(QLabel("测试步骤:"), 3, 0)
        self.test_step_label = QLabel("0")
        status_layout.addWidget(self.test_step_label, 3, 1)
        
        layout.addWidget(status_group)
        
        # 实时数据显示
        real_time_group = QGroupBox("实时数据")
        real_time_layout = QVBoxLayout(real_time_group)
        
        # 轴位置显示
        axes_layout = QHBoxLayout()
        self.axes_display = QTextEdit()
        self.axes_display.setMaximumHeight(150)
        self.axes_display.setReadOnly(True)
        axes_layout.addWidget(QLabel("轴位置:"))
        axes_layout.addWidget(self.axes_display)
        real_time_layout.addLayout(axes_layout)
        
        # 笛卡尔位置显示
        cart_layout = QHBoxLayout()
        self.cart_display = QTextEdit()
        self.cart_display.setMaximumHeight(150)
        self.cart_display.setReadOnly(True)
        cart_layout.addWidget(QLabel("笛卡尔位置:"))
        cart_layout.addWidget(self.cart_display)
        real_time_layout.addLayout(cart_layout)
        
        layout.addWidget(real_time_group)
        
        # 添加弹性空间
        layout.addStretch()
        
        return layout

    def create_log_panel(self):
        """创建日志面板"""
        layout = QVBoxLayout()
        
        log_group = QGroupBox("日志")
        log_layout = QHBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        return layout

    def setup_connections(self):
        """设置信号连接"""
        # 连接按钮事件
        self.connect_btn.clicked.connect(self.connect_cmd)
        self.disconnect_btn.clicked.connect(self.disconnect_cmd)
        self.pause_btn.clicked.connect(self.pause_cmd)
        self.resume_btn.clicked.connect(self.resume_cmd)
        self.reset_btn.clicked.connect(self.reset_cmd)
        self.interrupt_btn.clicked.connect(self.interrupt_cmd)
        self.continue_btn.clicked.connect(self.continue_cmd)
        self.confirm_error_btn.clicked.connect(self.confirm_error_cmd)
        self.ptp_axis_abs_btn.clicked.connect(self.ptp_axis_abs_cmd)
        self.ptp_pos_abs_btn.clicked.connect(self.ptp_pos_abs_cmd)
        self.ptp_pos_rel_btn.clicked.connect(self.ptp_pos_rel_cmd)
        self.lin_pos_abs_btn.clicked.connect(self.lin_pos_abs_cmd)
        self.lin_pos_rel_btn.clicked.connect(self.lin_pos_rel_cmd)
        self.circ_pos_abs_btn.clicked.connect(self.circ_pos_abs_cmd)
        self.circ_pos_rel_btn.clicked.connect(self.circ_pos_rel_cmd)
        self.splines_pos_abs_btn.clicked.connect(self.splines_pos_abs_cmd)
        self.splines_pos_rel_btn.clicked.connect(self.splines_pos_rel_cmd)
        self.jog_type_btn.clicked.connect(self.jog_type_switch_cmd)
        
        # 覆盖率滑块事件
        self.override_slider.valueChanged.connect(self.override_changed)
        
        # 连接 ViewModel 信号
        self.vm.log_updated.connect(self.append_log)

    def connect_cmd(self):
        """处理连接按钮点击"""
        #success = self.vm.connect_to_robot()
        success = self.vm.fast_connect_to_robot()
        if success:
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
        self.update_display()

    def disconnect_cmd(self):
        """处理断开连接按钮点击"""
        self.vm.disconnect_from_robot()
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.update_display()

    def pause_cmd(self):
        """处理暂停按钮点击"""
        self.vm.pause_robot()
        self.update_display()

    def resume_cmd(self):
        """处理恢复按钮点击"""
        self.vm.resume_robot()
        self.update_display()

    def reset_cmd(self):
        """处理重置按钮点击"""
        self.vm.reset_robot()
        self.update_display()

    def interrupt_cmd(self):
        """处理中断按钮点击"""
        self.vm.interrupt_robot()
        self.update_display()

    def continue_cmd(self):
        """处理继续按钮点击"""
        self.vm.continue_robot()
        self.update_display()
    def confirm_error_cmd(self):
        """处理确认错误按钮点击"""
        self.vm.confirm_error()
        self.update_display()
    def ptp_axis_abs_cmd(self):
        """处理 PTP 轴绝对按钮点击"""
        self.vm.send_ptp_axis_abs()
        self.update_display()

    def ptp_pos_abs_cmd(self):
        """处理 PTP 位置绝对按钮点击"""
        self.vm.send_ptp_pos_abs()
        self.update_display()

    def ptp_pos_rel_cmd(self):
        """处理 PTP 位置相对按钮点击"""
        self.vm.send_ptp_pos_rel()
        self.update_display()

    def lin_pos_abs_cmd(self):
        """处理 LIN 位置绝对按钮点击"""
        self.vm.send_lin_pos_abs()
        self.update_display()

    def lin_pos_rel_cmd(self):
        """处理 LIN 位置相对按钮点击"""
        self.vm.send_lin_pos_rel()
        self.update_display()

    def circ_pos_abs_cmd(self):
        """处理 CIRC 位置绝对按钮点击"""
        self.vm.send_circ_pos_abs()
        self.update_display()

    def circ_pos_rel_cmd(self):
        """处理 CIRC 位置相对按钮点击"""
        self.vm.send_circ_pos_rel()
        self.update_display()

    def splines_pos_abs_cmd(self):
        """处理 SPLINES 位置绝对按钮点击"""
        self.vm.send_splines_pos_abs()
        self.update_display()

    def splines_pos_rel_cmd(self):
        """处理 SPLINES 位置相对按钮点击"""
        self.vm.send_splines_pos_rel()
        self.update_display()

    def jog_type_switch_cmd(self):
        """处理点动类型切换"""
        self.vm.switch_jog_type()
        
        # 根据当前点动类型更新按钮标签
        if self.vm.jog_type == 0:  # 轴模式
            labels = [("A1+", "A1-"), ("A2+", "A2-"), ("A3+", "A3-"), 
                      ("A4+", "A4-"), ("A5+", "A5-"), ("A6+", "A6-")]
        else:  # 笛卡尔模式
            labels = [("X+", "X-"), ("Y+", "Y-"), ("Z+", "Z-"), 
                      ("A+", "A-"), ("B+", "B-"), ("C+", "C-")]
        
        for i, (pos_label, neg_label) in enumerate(labels):
            self.jog_buttons[f"{pos_label}_btn"].setText(pos_label)
            self.jog_buttons[f"{neg_label}_btn"].setText(neg_label)
        
        self.update_display()

    def jog_button_clicked(self, label):
        """处理点动按钮点击"""
        # 更新 ViewModel 的点动状态
        if label == "A1+" or label == "X+":
            self.vm.x_a1_plus = True
        elif label == "A1-" or label == "X-":
            self.vm.x_a1_minus = True
        elif label == "A2+" or label == "Y+":
            self.vm.y_a2_plus = True
        elif label == "A2-" or label == "Y-":
            self.vm.y_a2_minus = True
        elif label == "A3+" or label == "Z+":
            self.vm.z_a3_plus = True
        elif label == "A3-" or label == "Z-":
            self.vm.z_a3_minus = True
        elif label == "A4+" or label == "A+":
            self.vm.a_a4_plus = True
        elif label == "A4-" or label == "A-":
            self.vm.a_a4_minus = True
        elif label == "A5+" or label == "B+":
            self.vm.b_a5_plus = True
        elif label == "A5-" or label == "B-":
            self.vm.b_a5_minus = True
        elif label == "A6+" or label == "C+":
            self.vm.c_a6_plus = True
        elif label == "A6-" or label == "C-":
            self.vm.c_a6_minus = True

    def override_changed(self, value):
        """处理覆盖率变化"""
        self.vm.program_override = value
        self.override_label.setText(f"{value}%")

    def append_log(self, message):
        """添加日志消息"""
        self.log_text.append(message)
        # 自动滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_display(self):
        """更新显示内容"""
        # 更新错误ID
        self.error_id_label.setText(str(self.vm.error_id))
        
        # 更新运行状态
        if self.vm.start_running:
            self.running_status_label.setText("运行中")
            self.running_status_label.setStyleSheet("font-weight: bold; color: #27ae60;")
        else:
            self.running_status_label.setText("已停止")
            self.running_status_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
        
        # 从队列获取机器人数据并更新显示
        try:
            while not robot_data_queue.empty():
                robot_data = robot_data_queue.get_nowait()
                
                # 更新状态标签
                self.loop_count_label.setText(str(robot_data['loop_count']))
                self.test_step_label.setText(str(robot_data['test_step']))
                
                # 更新轴位置显示
                axes_text = (
                    f"A1: {robot_data['a1']:.2f}°\n"
                    f"A2: {robot_data['a2']:.2f}°\n"
                    f"A3: {robot_data['a3']:.2f}°\n"
                    f"A4: {robot_data['a4']:.2f}°\n"
                    f"A5: {robot_data['a5']:.2f}°\n"
                    f"A6: {robot_data['a6']:.2f}°"
                )
                self.axes_display.setPlainText(axes_text)
                
                # 更新笛卡尔位置显示
                cart_text = (
                    f"X: {robot_data['x']:.2f}mm\n"
                    f"Y: {robot_data['y']:.2f}mm\n"
                    f"Z: {robot_data['z']:.2f}mm\n"
                    f"A: {robot_data['a']:.2f}°\n"
                    f"B: {robot_data['b']:.2f}°\n"
                    f"C: {robot_data['c']:.2f}°"
                )
                self.cart_display.setPlainText(cart_text)
        except:
            pass  # 队列为空

if __name__ == "__main__":
    # 创建 ViewModel 和 View
    vm = MxAViewModel()
    app = QApplication(sys.argv)
    window = MxAView(vm)
    
    # 显示窗口
    window.show()
    
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("正在停止应用程序...")
        if vm.main_thread and vm.main_thread.is_alive():
            vm.stop_event.set()
            vm.main_thread.join(timeout=2)
        print("应用程序已停止.")