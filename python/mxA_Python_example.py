
#2024-06-06 
import mxAutomation_3 as mxA
import time 
import socket 
from sys import version_info
major = version_info[0]
minor = version_info[1]
micro = version_info[2]
if major == 2:
    # We are using Python 2.x
    from Tkinter import *
    import Tkinter as tk
    import ttk
    import ScrolledText as scrolledtext
elif major == 3:
    # We are using Python 3.x
    from tkinter import *
    import tkinter as tk 
    from tkinter import ttk
    from tkinter import scrolledtext


_mxA_KRC_READAXISGROUP = mxA.KRC_READAXISGROUP()
_mxA_KRC_WRITEAXISGROUP = mxA.KRC_WRITEAXISGROUP()
_mxA_READACTUALPOSITION = mxA.KRC_READACTUALPOSITION()
_mxA_READACTUALAXISPOSITION = mxA.KRC_READACTUALAXISPOSITION()
_mxA_KRC_INITIALIZE = mxA.KRC_INITIALIZE()
_mxA_KRC_AUTOMATICEXTERNAL = mxA.KRC_AUTOMATICEXTERNAL()
_mxA_KRC_AUTOSTART = mxA.KRC_AUTOSTART()
_mxA_KRC_ERROR = mxA.KRC_ERROR()
_mxA_KRC_ABORT = mxA.KRC_ABORT()
_mxA_KRC_SETOVERRIDE = mxA.KRC_SETOVERRIDE()
_mxA_KRC_JOGADVANCED = mxA.KRC_JOGADVANCED()
_mxA_KRC_MOVEAXISABSOLUTE = mxA.KRC_MOVEAXISABSOLUTE()
_mxA_KRC_MOVEDIRECTABSOLUTE = mxA.KRC_MOVEDIRECTABSOLUTE()
_mxA_KRC_INVERSE = mxA.KRC_INVERSEADVANCED()
#Special Functions
_mxA_KRC_SETCOORDSYS = mxA.KRC_SETCOORDSYS()
_mxA_KRC_TECHFUNCTIONADVANCED = mxA.KRC_TECHFUNCTIONADVANCED()
_mxA_KRC_Diag = mxA.KRC_DIAG()
_mxA_KRC_Braketest = mxA.KRC_BRAKETEST()
_mxA_KRC_ReadSafeOPstatus = mxA.KRC_READSAFEOPSTATUS()

#Value Initialization 
axis_target_pos = mxA.E6AXIS() 
direct_target_pos = mxA.E6POS() 
CoordSys_ToolBase = mxA.COORDSYS()
APO_parameter = mxA.APO()


if True:  # target positions e.g. 
    APO_parameter.PTP_MODE = 0
    APO_parameter.CP_MODE = 0
    APO_parameter.CPTP = 50     # in %
    APO_parameter.CDIS = 45.123 # in mm
    APO_parameter.CORI = 2.4  # in degree
    APO_parameter.CVEL = 50  # in %

#Loops and UDP Connection
loops = 10000
loop_Time = 0.15
UDP_IP = "172.31.1.147"  # enter here your KLI IP adress
_axisGroupIdx = 1
test_step = 0
Movements_in_Spline = True

#UDP receiver setup
receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind(('127.0.0.1', 2000))  # default mxAutomation port
receiver.setblocking(0)
success = False
message = ""

input_buffer = bytearray(b'\x00') * 256
output_to_robot = bytearray(b'\x00') * 256

#Read from Robot
def readfrom_robot():
    global input_buffer
    try:
        message, address = receiver.recvfrom(256)
    except socket.error:
        return
    buffer = bytearray(message)
    input_buffer = buffer
    if(len(buffer) < 256):
        print("ERROR receiving buffer")
        return
    
#Send to Robot
# -*- coding: utf-8 -*-
def sendto_robot():    
    global UDP_IP
    UDP_PORT = 2001  #Default mxAutomation port
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sender.sendto(output_to_robot, (UDP_IP, UDP_PORT))

#Update mxA Interface
def update_mxAutomation_interface():
    readfrom_robot()
    _mxA_KRC_READAXISGROUP.OnCycle()  #Reads the data from incoming byte array
    _mxA_READACTUALAXISPOSITION.OnCycle()
    _mxA_READACTUALPOSITION.OnCycle()
    _mxA_KRC_ERROR.OnCycle()
    _mxA_KRC_ABORT.OnCycle()
    _mxA_KRC_SETOVERRIDE.OnCycle()
    _mxA_KRC_AUTOMATICEXTERNAL.OnCycle()
    _mxA_KRC_SETCOORDSYS.OnCycle()
    _mxA_KRC_AUTOSTART.OnCycle()
    _mxA_KRC_INITIALIZE.OnCycle()
    _mxA_KRC_JOGADVANCED.OnCycle() 
    _mxA_KRC_MOVEAXISABSOLUTE.OnCycle()
    _mxA_KRC_MOVEDIRECTABSOLUTE.OnCycle()
    _mxA_KRC_TECHFUNCTIONADVANCED.OnCycle()
    _mxA_KRC_Diag.OnCycle()
    _mxA_KRC_ReadSafeOPstatus.OnCycle()
    _mxA_KRC_Braketest.OnCycle()
    _mxA_KRC_WRITEAXISGROUP.OnCycle()  #Writes data to the outbound byte array
    _mxA_KRC_INVERSE.OnCycle()
    sendto_robot()


class HMI:

    #Setting IP Function
    def setIP(self):
        global UDP_IP
        IP_STRING = self.ipEntry.get()
        print(IP_STRING)
        try:
            #IP valid?
            socket.inet_aton(IP_STRING)
            UDP_IP = IP_STRING
        except socket.error:
            print("ERROR parsing IP")
    
    #Jogging value Change
    def changeValue(self, n, newValue):
        if n == "X -":
            print("CHANGING X-")
            _mxA_KRC_JOGADVANCED.B_X_JA_M = newValue
        elif n == "X +":
            _mxA_KRC_JOGADVANCED.B_X_JA_P = newValue
        elif n == "Y -":
            _mxA_KRC_JOGADVANCED.B_Y_JA_M = newValue
        elif n == "Y +":
            _mxA_KRC_JOGADVANCED.B_Y_JA_P = newValue
        elif n == "Z -":
            _mxA_KRC_JOGADVANCED.B_Z_JA_M = newValue
        elif n == "Z +":
            _mxA_KRC_JOGADVANCED.B_Z_JA_P = newValue
        elif n == "A -":
            _mxA_KRC_JOGADVANCED.B_A_JA_M = newValue
        elif n == "A +":
            _mxA_KRC_JOGADVANCED.B_A_JA_P = newValue
        elif n == "B -":
            _mxA_KRC_JOGADVANCED.B_B_JA_M = newValue
        elif n == "B +":
            _mxA_KRC_JOGADVANCED.B_B_JA_P = newValue
        elif n == "C -":
            _mxA_KRC_JOGADVANCED.B_C_JA_M = newValue
        elif n == "C +":
            _mxA_KRC_JOGADVANCED.B_C_JA_P = newValue
        elif n == "A1 -":
            _mxA_KRC_JOGADVANCED.B_A1_JA_M = newValue
        elif n == "A1 +":
            _mxA_KRC_JOGADVANCED.B_A1_JA_P = newValue
        elif n == "A2 -":
            _mxA_KRC_JOGADVANCED.B_A2_JA_M = newValue
        elif n == "A2 +":
            _mxA_KRC_JOGADVANCED.B_A2_JA_P = newValue
        elif n == "A3 -":
            _mxA_KRC_JOGADVANCED.B_A3_JA_M = newValue
        elif n == "A3 +":
            _mxA_KRC_JOGADVANCED.B_A3_JA_P = newValue
        elif n == "A4 -":
            _mxA_KRC_JOGADVANCED.B_A4_JA_M = newValue
        elif n == "A4 +":
            _mxA_KRC_JOGADVANCED.B_A4_JA_P = newValue
        elif n == "A5 -":
            _mxA_KRC_JOGADVANCED.B_A5_JA_M = newValue
        elif n == "A5 +":
            _mxA_KRC_JOGADVANCED.B_A5_JA_P = newValue
        elif n == "A6 -":
            _mxA_KRC_JOGADVANCED.B_A6_JA_M = newValue
        elif n == "A6 +":
            _mxA_KRC_JOGADVANCED.B_A6_JA_P = newValue
        else:
            self.messages_scrolledtext.insert(INSERT, "ERROR reading jogging input\n")

    #Jogging Button Press and Release functions
    def JoggingButtonPress(self, event, name):
        print("Pressed a Jogging button")
        print(event)
        print(name)
        self.changeValue(name, True)
            
    def JoggingButtonRelease(self, event, name):
        print("Released a Jogging button")
        print(event)
        print(name)
        self.changeValue(name, False)

    #Autostart            
    def Autostart(self):
        _mxA_KRC_AUTOSTART.EXECUTERESET = True

    #Error Reset  
    def ErrorReset_Press(self, event):
        _mxA_KRC_ERROR.MESSAGERESET = True
        self.messages_scrolledtext.insert(INSERT, "-> MESSAGERESET set to {}\n".format(_mxA_KRC_ERROR.MESSAGERESET))

    def ErrorReset_Release(self, event):
        _mxA_KRC_ERROR.MESSAGERESET = False  
        self.messages_scrolledtext.insert(INSERT, "-> MESSAGERESET set to {}\n".format(_mxA_KRC_ERROR.MESSAGERESET))

    #Ext_Start 
    def Ext_StartSet(self, event):
        _mxA_KRC_AUTOMATICEXTERNAL.EXT_START = True 
        self.messages_scrolledtext.insert(INSERT, "-> Ext_Start button pressed\n")

    def Ext_StartReset(self, event):
        _mxA_KRC_AUTOMATICEXTERNAL.EXT_START = False
        self.messages_scrolledtext.insert(INSERT, "-> Ext_Start button released\n")

    #Set Coordinate System
    def SetCoordys(self):
        _mxA_KRC_SETCOORDSYS.EXECUTECMD = True
        CoordSys_ToolBase.TOOL = int(self.ToolCoordsys_entry.get())
        CoordSys_ToolBase.BASE = int(self.BaseCoordsys_entry.get())
        CoordSys_ToolBase.IPO_MODE = self.IPOCoordsys_combobox.get()
        self.messages_scrolledtext.insert(INSERT, "-> Coordsys values has been Set\n")

    #Brake Tests
    def StartBraketest_Press(self, event):
        _mxA_KRC_Braketest.EXECUTECMD = True
        self.messages_scrolledtext.insert(INSERT, "-> Braketest Start button pressed\n")
    
    def StartBraketest_Release(self, event):
        _mxA_KRC_Braketest.EXECUTECMD = False
        self.messages_scrolledtext.insert(INSERT, "-> Braketest Start button released\n")

    def ReqBraketest_Press(self, event):
        _mxA_KRC_ReadSafeOPstatus.BRAKETEST_REQ_EXT = True
        self.messages_scrolledtext.insert(INSERT, "-> Request Brake test pressed\n")
    
    def ReqBraketest_Release(self, event):
        _mxA_KRC_ReadSafeOPstatus.BRAKETEST_REQ_EXT = False
        self.messages_scrolledtext.insert(INSERT, "-> Request Brake test released\n")

    #Tech Function Advanced  
    def TechFctAdv_Button_Press(self, event):
        _mxA_KRC_TECHFUNCTIONADVANCED.EXECUTECMD = True
    
    def TechFctAdv_Button_Release(self, event):
        _mxA_KRC_TECHFUNCTIONADVANCED.EXECUTECMD = False
  
    #Move Axis Absolute Function 
    def MoveAxisAbsolute(self):
        _mxA_KRC_MOVEAXISABSOLUTE.EXECUTECMD = True
        _mxA_KRC_MOVEAXISABSOLUTE.AXISGROUPIDX = _axisGroupIdx
        _mxA_KRC_MOVEAXISABSOLUTE.APPROXIMATE = APO_parameter
        _mxA_KRC_MOVEAXISABSOLUTE.BUFFERMODE = 2

        axis_target_pos.A1 = float(self.A1axis_entry.get())
        axis_target_pos.A2 = float(self.A2axis_entry.get())
        axis_target_pos.A3 = float(self.A3axis_entry.get())
        axis_target_pos.A4 = float(self.A4axis_entry.get())
        axis_target_pos.A5 = float(self.A5axis_entry.get())
        axis_target_pos.A6 = float(self.A6axis_entry.get())

        axis_target_pos.E1 = float(self.E1axis_entry.get())
        axis_target_pos.E2 = float(self.E2axis_entry.get())
        axis_target_pos.E3 = float(self.E3axis_entry.get())
        axis_target_pos.E4 = float(self.E4axis_entry.get())
        axis_target_pos.E5 = float(self.E5axis_entry.get())
        axis_target_pos.E6 = float(self.E6axis_entry.get()) 

        self.messages_scrolledtext.insert(INSERT, "-> MOVEAXISABSOLUTE.EXECUTECMD: {}\n".format(_mxA_KRC_MOVEAXISABSOLUTE.EXECUTECMD))

      
    #Move Direct Absolute Function 
    def MoveDirectAbsolute(self):
        _mxA_KRC_MOVEDIRECTABSOLUTE.EXECUTECMD = True
        _mxA_KRC_MOVEDIRECTABSOLUTE.AXISGROUPIDX = _axisGroupIdx
        _mxA_KRC_MOVEDIRECTABSOLUTE.APPROXIMATE = APO_parameter
        _mxA_KRC_MOVEDIRECTABSOLUTE.SPLINEMODE = Movements_in_Spline
        _mxA_KRC_MOVEDIRECTABSOLUTE.BUFFERMODE = 2
        
        direct_target_pos.X = float(self.Xdirect_entry.get())
        direct_target_pos.Y = float(self.Ydirect_entry.get())
        direct_target_pos.Z = float(self.Zdirect_entry.get())
        direct_target_pos.A = float(self.Adirect_entry.get())
        direct_target_pos.B = float(self.Bdirect_entry.get())
        direct_target_pos.C = float(self.Cdirect_entry.get())

        direct_target_pos.E1 = float(self.E1direct_entry.get())
        direct_target_pos.E2 = float(self.E2direct_entry.get())
        direct_target_pos.E3 = float(self.E3direct_entry.get())
        direct_target_pos.E4 = float(self.E4direct_entry.get())
        direct_target_pos.E5 = float(self.E5direct_entry.get())
        direct_target_pos.E6 = float(self.E6direct_entry.get()) 
 
        direct_target_pos.STATUS = -1
        direct_target_pos.TURN = -1
        

        self.messages_scrolledtext.insert(INSERT, "-> MOVEDIRECTABSOLUTE.EXECUTECMD: {}\n".format(_mxA_KRC_MOVEDIRECTABSOLUTE.EXECUTECMD))

    #Toggle Buttons
    def MoveEnableT1_Toggle(self):
        if self.moveenablet1_checkbutton_state.get() == 1:
            _mxA_KRC_AUTOMATICEXTERNAL.ENABLE_T1 = True
            self.messages_scrolledtext.insert(INSERT, "-> Enable T1 Move: {}\n".format(_mxA_KRC_AUTOMATICEXTERNAL.ENABLE_T1))

              
        else:
             _mxA_KRC_AUTOMATICEXTERNAL.ENABLE_T1 = False
             self.messages_scrolledtext.insert(INSERT, "-> Enable T1 Move: {}\n".format(_mxA_KRC_AUTOMATICEXTERNAL.ENABLE_T1))


    def activateJogAdvanced_Toggle(self):
        if self.activate_jog_advanced.get() == 1:
            _mxA_KRC_JOGADVANCED.JOGADVANCED = True
            self.jog_advanced_checkbutton.configure(fg="green")
            self.messages_scrolledtext.insert(INSERT, "-> JogAdvanced: {} \n".format(_mxA_KRC_JOGADVANCED.JOGADVANCED))


        else:
            _mxA_KRC_JOGADVANCED.JOGADVANCED = False
            self.jog_advanced_checkbutton.configure(fg="red")
            self.messages_scrolledtext.insert(INSERT, "-> JogAdvanced: {} \n".format(_mxA_KRC_JOGADVANCED.JOGADVANCED))

    
    #Message Scrollbox Clear
    def clearmessages(self):
        self.messages_scrolledtext.delete(1.0, END)

    #Show Trace function
    def showTrace(self):

        if self.showTrace_Button["bg"] == "light green":
           _mxA_KRC_Diag.SHOWTRACE = False
           self.showTrace_Button["bg"] = "SystemButtonFace"

        else:
           _mxA_KRC_Diag.SHOWTRACE = True
           self.showTrace_Button["bg"] = "light green"
           
    #Abort function 
    def abort(self):
        _mxA_KRC_ABORT.EXECUTECMD = True
        self.messages_scrolledtext.insert(INSERT, "-> ABORT.EXECUTECMD: {}\n".format(_mxA_KRC_ABORT.EXECUTECMD))



    #Setting up the GUI 
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MxAutomation Test Run")
        self.root.geometry("950x650")
        self.root.maxsize(950, 650)
        self.root.minsize(950, 650)

    #Frames in Root
        self.main_frame = tk.Frame(self.root, borderwidth = 1, width = 50, height = 70, relief = "flat",)
        self.main_frame.grid(row=0, column=0, sticky = "nwe", padx = 5, pady = 10)

        self.side_frame = tk.Frame(self.root, borderwidth = 1, width = 50, height = 70, relief = "flat", )
        self.side_frame.grid(row=0, column=1, sticky = "nwe", padx = 3, pady = 10)

        self.robotstate_frame = tk.Frame(self.main_frame, borderwidth=1, width=40, height=20, relief="solid")
        self.robotstate_frame.grid(row=0, column=0, padx = 10, pady = 10, sticky="nw")

        self.override_frame = tk.Frame(self.main_frame, borderwidth=1, width = 30, height = 70, relief = "flat")
        self.override_frame.grid(row=1, column=0, padx = 10, pady = 5, sticky="nw")

        self.buttons_frame = tk.Frame(self.main_frame, borderwidth=1, width = 30, height = 70, relief = "flat")
        self.buttons_frame.grid(row=2, column=0, padx = 10, pady = 5, sticky="nw")

        self.messages_frame = tk.Frame(self.main_frame, borderwidth=1, width = 50, height = 10, relief = "flat")
        self.messages_frame.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = "nswe")

        self.tab_frame = tk.Frame(self.side_frame, borderwidth=1, width = 70, height = 10, relief = "solid")
        self.tab_frame.grid(row = 0, column = 0, padx = 3, pady = 5, sticky = "nwe")

        self.position_frame = tk.Frame(self.side_frame, borderwidth=1, width = 70, height = 50, relief = "solid", bg = "white" )
        self.position_frame.grid(row=2, column=0, padx = 3, pady = 5,  sticky="nwe")

    #Creating Tabs
        self.tabs = ttk.Notebook(self.tab_frame)

    #Tabs in the Tab Frame 
        self.SetCoordsysTab = ttk.Frame(self.tabs)
        self.MoveAxisTab = ttk.Frame(self.tabs)
        self.MoveDirectTab = ttk.Frame(self.tabs)
        self.JoggingTab = ttk.Frame(self.tabs)
        self.TechFunctionTab = ttk.Frame(self.tabs)
        self.SafeOPTab = ttk.Frame(self.tabs)

    #Adding the Tabs 
        self.tabs.add(self.SetCoordsysTab, text='Set Coordsys')
        self.tabs.add(self.MoveAxisTab, text='Move Axis Abs')
        self.tabs.add(self.MoveDirectTab, text='Move Direct Abs')
        self.tabs.add(self.JoggingTab, text='Jogging')
        self.tabs.add(self.TechFunctionTab, text ='TechFunction Adv')
        self.tabs.add(self.SafeOPTab, text='Safe OP')

    #Making it visible
        self.tabs.pack(expand = 1, fill="both")

    #Widgets in Main Frame
        self.robotstate_label = tk.Label(self.robotstate_frame, text = "State of the Robot: ")
        self.robotstate_label.grid(row=0, column=0, padx=10, pady =10)

        self.robotstateS_label = tk.Label(self.robotstate_frame, text = "   S   ", borderwidth=2, relief="solid", activebackground="Grey")
        self.robotstateS_label.grid(row=0, column=1, padx=10, pady =10, ipadx = 10, ipady = 10, sticky="we")

        self.robotstateI_label = tk.Label(self.robotstate_frame, text = "   I   ", borderwidth=2, relief="solid", activebackground="Grey")
        self.robotstateI_label.grid(row=0, column=2, padx=10, pady =10, ipadx = 10, ipady = 10)

        self.robotstateR_label = tk.Label(self.robotstate_frame, text = "   R   ", borderwidth=2, relief="solid", activebackground="Grey")
        self.robotstateR_label.grid(row=0, column=3, padx=10, pady =10, ipadx = 10, ipady = 10)

        self.robotstateExt_label = tk.Label(self.robotstate_frame, text = "   EXT   ", borderwidth=2, relief="solid", activebackground="Grey")
        self.robotstateExt_label.grid(row=0, column=4, padx=8, pady = 8, ipadx = 6, ipady = 10)

        self.IP_label = tk.Label(self.override_frame, text = "IP Address:  ")
        self.IP_label.grid(row=1, column=0, sticky= "w", pady = 10)

        self.ipEntry = tk.Entry(self.override_frame)
        self.ipEntry.insert(tk.END, "172.31.1.147")
        self.ipEntry.grid(row=1, column=1,  ipadx = 10, sticky = "w")

        self.buttonSubmitIP = tk.Button(self.override_frame, text="Set IP", width = 12, command = self.setIP)
        self.buttonSubmitIP.grid(row=1, column=2, sticky = "w", padx= 5)

        self.slider_label = tk.Label(self.override_frame, text="Override Value:      ")
        self.slider_label.grid(row=2,column=0, sticky="sw", pady = 5)

        self.override_value = tk.DoubleVar()
        self.slider = tk.Scale(self.override_frame, from_=0, to=100, orient = tk.HORIZONTAL, variable=self.override_value)
        self.slider.set(1)
        self.slider.grid(row=2, column=1, ipadx = 20, sticky = "w")

        self.moveenablet1_checkbutton_state = tk.BooleanVar(value=False)
        self.moveenablet1_checkbutton = tk.Checkbutton(self.override_frame, text="Move Enable T1", variable = self.moveenablet1_checkbutton_state, command=self.MoveEnableT1_Toggle)
        self.moveenablet1_checkbutton.grid(row=2, column=2, sticky = "ws")
        
    #Buttons in Button Frame
        self.AutostartButton = tk.Button(self.buttons_frame, text="Auto Start",width = 12, command=self.Autostart)
        self.AutostartButton.grid(row=0, column=0, sticky="w", padx = 5, pady = 3)

        self.ErrorReset_Button = tk.Button(self.buttons_frame, width = 12, text="Error Reset")
        self.ErrorReset_Button.grid(row=0, column=1, sticky = "w", padx = 5, pady = 3)
        self.ErrorReset_Button.bind('<ButtonPress>', self.ErrorReset_Press)
        self.ErrorReset_Button.bind('<ButtonRelease>', self.ErrorReset_Release)

        self.Ext_StartButton = tk.Button(self.buttons_frame, text="Ext Start", width = 12)
        self.Ext_StartButton.grid(row=0, column=2, sticky = "w", padx = 5, pady = 3)
        self.Ext_StartButton.bind('<ButtonPress>', self.Ext_StartSet)
        self.Ext_StartButton.bind('<ButtonRelease>', self.Ext_StartReset)
        
        self.AbortButton = tk.Button(self.buttons_frame, text="Abort", width = 12, command = self.abort)
        self.AbortButton.grid(row=1, column=0, sticky = "w", padx = 5, pady = 3)   

        self.showTrace_Button = tk.Button(self.buttons_frame, width = 12, text="Show Trace", command = self.showTrace, bg = "SystemButtonFace")
        self.showTrace_Button.grid(row=1, column=1, sticky = "w", padx = 5, pady = 3)


    #Message Scrolled Texts
        self.messages_label = tk.Label(self.messages_frame, text="Messages: ",font = ("Segoe UI", 10, "bold"))
        self.messages_label.grid(row=0, column = 0, sticky="nw")

        self.messages_scrolledtext = scrolledtext.ScrolledText(self.messages_frame, width = 50, height=19)
        self.messages_scrolledtext.grid(row=1,column=0, sticky = "nwe")

        self.clearmessages_Button = tk.Button(self.messages_frame, text = "Clear Messages", command=self.clearmessages)
        self.clearmessages_Button.grid(row=2, column = 0, sticky="nw")


    #Position Display in Position Frame  
        self.OutputConsole_label = tk.Label(self.side_frame, text ="\nOutput Console: ", font = ("Segoe UI", 10, "bold"))
        self.OutputConsole_label.grid(row=1, column=0, sticky = "w")
        
        self.errorNr_label = tk.Label(self.position_frame, text="",bg = "white", activeforeground="black")
        self.errorNr_label.grid(row=0, column=0, sticky = "w")

        self.toolbasepos_label = tk.Label(self.position_frame, bg="white")
        self.toolbasepos_label.grid(row=1, column=0, sticky = "w")

        self.currentposition1_label = tk.Label(self.position_frame, bg = "white")
        self.currentposition1_label.grid(row=2, column=0, sticky = "w")
        self.currentposition2_label = tk.Label(self.position_frame, bg = "white")
        self.currentposition2_label.grid(row=3, column=0, sticky = "w")

        self.cart1_label = tk.Label(self.position_frame, text = "Cart: ", bg = "white")
        self.cart1_label.grid(row=4, column=0, sticky = "nw")
        self.cart2_label = tk.Label(self.position_frame, bg = "white")
        self.cart2_label.grid(row=5, column=0, sticky = "w")

        self.loop_counter_label = tk.Label(self.position_frame, text="", bg="white")
        self.loop_counter_label.grid(row=0, column=1, sticky = "w")

        self.test_step_label = tk.Label(self.position_frame, bg="white")
        self.test_step_label.grid(row=0, column=2, sticky = "w")

        self.statusturn_label = tk.Label(self.position_frame, bg="white")
        self.statusturn_label.grid(row=1, column=1, sticky = "w") 
    

    #Widgets in Side Frame
    #-----------Set Coordinate System Tab-----------
        self.SetCoordys_frame = tk.Frame(self.SetCoordsysTab, borderwidth = 1, relief = "flat", width = 40, height=50)
        self.SetCoordys_frame.grid(row = 0, column=0, sticky = "nw", pady = 10)

        #Frame 1 
        self.ToolCoordsys_label = tk.Label(self.SetCoordys_frame, text="Set Tool Coordsys: ")
        self.ToolCoordsys_label.grid(row = 0, column=0, padx=5, pady = 10)

        self.ToolCoordsys_variable = tk.IntVar()
        self.ToolCoordsys_entry  = tk.Entry(self.SetCoordys_frame, width=4, textvariable=self.ToolCoordsys_variable)
        self.ToolCoordsys_entry.grid(row=0, column = 1, padx=5, pady = 10, ipadx=10)

        self.BaseCoordsys_label = tk.Label(self.SetCoordys_frame, text="Set Base Coordsys: ")
        self.BaseCoordsys_label.grid(row = 1, column=0, padx=5, pady = 10)

        self.BaseCoordsys_variable = tk.IntVar()
        self.BaseCoordsys_entry  = tk.Entry(self.SetCoordys_frame, width=4, textvariable=self.BaseCoordsys_variable)
        self.BaseCoordsys_entry.grid(row=1, column = 1, padx=5, pady = 10, ipadx=10)

        self.IPOCoordsys_label = tk.Label(self.SetCoordys_frame, text="Set IPO Mode: ")
        self.IPOCoordsys_label.grid(row = 2, column=0, padx=5, pady = 10)

        self.IPOCoordsys_variable = tk.IntVar()
        self.IPOCoordsys_combobox  = ttk.Combobox(self.SetCoordys_frame, width=4, textvariable=self.IPOCoordsys_variable)
        self.IPOCoordsys_combobox["values"] = (0,1)
        self.IPOCoordsys_combobox.current(0)
        self.IPOCoordsys_combobox.grid(row=2, column=1, padx=5, pady = 10)

        self.SetCoordsys_Button = tk.Button(self.SetCoordys_frame, text = "Set Coordsys Values", command=self.SetCoordys)
        self.SetCoordsys_Button.grid(row = 3, column=0, padx=15, pady = 10)

    #-----------Move Axis Absolute Tab-----------
        #-----------Move Axis Absolute Tab Frames-----------
        self.Axis_frame = tk.Frame(self.MoveAxisTab, borderwidth = 1, relief = "flat", width = 40, height=50)
        self.Axis_frame.grid(row = 0, column=0, sticky = "nw", ipadx = 10, pady = 5)
        
        self.Axis2_frame = tk.Frame(self.MoveAxisTab, borderwidth = 1, relief = "flat", width = 40, height=50)
        self.Axis2_frame.grid(row = 0, column=4, sticky = "nw", ipadx = 10, pady = 5)

        self.Axis3_frame = tk.Frame(self.MoveAxisTab, borderwidth = 1, relief = "flat")
        self.Axis3_frame.grid(row = 8, column=0, pady = 10, sticky = "nw")
        
        self.Axis4_frame = tk.Frame(self.MoveAxisTab, borderwidth = 1, relief = "flat")
        self.Axis4_frame.grid(row = 9, column=0, pady = 10, sticky = 'nw')

        #Frame 1
        self.A1axis_label = tk.Label(self.Axis_frame, text = "A1:")
        self.A1axis_label.grid(row = 0, column=0, padx=5)

        self.AxisAbsoluteA1_variable = tk.DoubleVar()
        self.A1axis_entry = tk.Entry(self.Axis_frame, width=4, textvariable=self.AxisAbsoluteA1_variable)
        self.A1axis_entry.grid(row=0, column = 1, padx=5)
        
        

        self.A2axis_label = tk.Label(self.Axis_frame, text = "A2:")
        self.A2axis_label.grid(row = 1, column=0, padx=5)
        
        self.AxisAbsoluteA2_variable = tk.DoubleVar()
        self.A2axis_entry = tk.Entry(self.Axis_frame, width=4, textvariable=self.AxisAbsoluteA2_variable)
        self.A2axis_entry.grid(row=1, column = 1, padx=5)
        
        

        self.A3axis_label = tk.Label(self.Axis_frame, text = "A3:")
        self.A3axis_label.grid(row = 2, column=0, padx=5)
        
        self.AxisAbsoluteA3_variable = tk.DoubleVar()
        self.A3axis_entry = tk.Entry(self.Axis_frame, width=4, textvariable=self.AxisAbsoluteA3_variable)
        self.A3axis_entry.grid(row=2, column = 1, padx=5)
        
        

        self.A4axis_label = tk.Label(self.Axis_frame, text = "A4:")
        self.A4axis_label.grid(row = 3, column=0, padx=5)
        
        self.AxisAbsoluteA4_variable = tk.DoubleVar()
        self.A4axis_entry = tk.Entry(self.Axis_frame, width=4, textvariable=self.AxisAbsoluteA4_variable)
        self.A4axis_entry.grid(row=3, column = 1, padx=5)
        
        

        self.A5axis_label = tk.Label(self.Axis_frame, text = "A5:")
        self.A5axis_label.grid(row = 4, column=0, padx=5)
        
        self.AxisAbsoluteA5_variable = tk.DoubleVar()
        self.A5axis_entry = tk.Entry(self.Axis_frame, width=4, textvariable=self.AxisAbsoluteA5_variable)
        self.A5axis_entry.grid(row=4, column = 1, padx=5)
        
        
        
        self.A6axis_label = tk.Label(self.Axis_frame, text = "A6:")
        self.A6axis_label.grid(row = 5, column=0, padx=5)
        
        self.AxisAbsoluteA6_variable = tk.DoubleVar()
        self.A6axis_entry = tk.Entry(self.Axis_frame, width=4, textvariable=self.AxisAbsoluteA6_variable)
        self.A6axis_entry.grid(row=5, column = 1, padx=5)
        

        #Frame 2
        self.E1axis_label = tk.Label(self.Axis2_frame, text = "E1:")
        self.E1axis_label.grid(row = 0, column=0, padx=5)

        self.AxisAbsoluteE1_variable = tk.DoubleVar()
        self.E1axis_entry = tk.Entry(self.Axis2_frame, width=4, textvariable=self.AxisAbsoluteE1_variable)
        self.E1axis_entry.grid(row=0, column = 1, padx=5)
        
        

        self.E2axis_label = tk.Label(self.Axis2_frame, text = "E2:")
        self.E2axis_label.grid(row = 1, column=0, padx=5)
      
        self.AxisAbsoluteE2_variable = tk.DoubleVar()
        self.E2axis_entry = tk.Entry(self.Axis2_frame, width=4, textvariable=self.AxisAbsoluteE2_variable)
        self.E2axis_entry.grid(row=1, column = 1, padx=5)
        
        
        
        self.E3axis_label = tk.Label(self.Axis2_frame, text = "E3:")
        self.E3axis_label.grid(row = 2, column=0, padx=5)
       
        self.AxisAbsoluteE3_variable = tk.DoubleVar()
        self.E3axis_entry = tk.Entry(self.Axis2_frame, width=4, textvariable=self.AxisAbsoluteE3_variable)
        self.E3axis_entry.grid(row=2, column = 1, padx=5)
        
        

        self.E4axis_label = tk.Label(self.Axis2_frame, text = "E4:")
        self.E4axis_label.grid(row = 3, column=0, padx=5)

        self.AxisAbsoluteE4_variable = tk.DoubleVar()
        self.E4axis_entry = tk.Entry(self.Axis2_frame, width=4, textvariable=self.AxisAbsoluteE4_variable)
        self.E4axis_entry.grid(row=3, column = 1, padx=5)
        
        

        self.E5axis_label = tk.Label(self.Axis2_frame, text = "E5:")
        self.E5axis_label.grid(row=4, column=0, padx=5)

        self.AxisAbsoluteE5_variable = tk.DoubleVar()
        self.E5axis_entry = tk.Entry(self.Axis2_frame, width=4, textvariable=self.AxisAbsoluteE5_variable)
        self.E5axis_entry.grid(row=4, column = 1, padx=5)
        
        

        self.E6axis_label = tk.Label(self.Axis2_frame, text = "E6:")
        self.E6axis_label.grid(row = 5, column=0, padx=5)

        self.AxisAbsoluteE6_variable = tk.DoubleVar()
        self.E6axis_entry = tk.Entry(self.Axis2_frame, width=4, textvariable=self.AxisAbsoluteE6_variable)
        self.E6axis_entry.grid(row=5, column = 1, padx=5)
        

        #Frame 3
        self.MoveAxis_Button = tk.Button(self.Axis3_frame, text = "Move to Axis Position Directly", command = self.MoveAxisAbsolute)  
        self.MoveAxis_Button.grid(row=0, column=0, padx=5)


        #Frame 4 
        #Axis Absolute Active Status
        self.AxisActiveLabel = tk.Label(self.Axis4_frame, text = "Active:")
        self.AxisActiveLabel.grid(row=0,column=0, padx=1, pady = 5, sticky = 'w')

        self.AxisActiveStatusCanvas = tk.Canvas(self.Axis4_frame, width=20, height=20)
        self.AxisActiveStatusCanvas.grid(row=0,column=1, pady = 5, sticky = 'w')
        self.AxisActiveStatusLed = self.AxisActiveStatusCanvas.create_oval(5, 5, 15, 15)

        #Axis Absolute Done Status 
        self.AxisDoneLabel = tk.Label(self.Axis4_frame, text = "Done:")
        self.AxisDoneLabel.grid(row=0,column=2, padx=1, pady = 5, sticky = 'w')

        self.AxisDoneStatusCanvas = tk.Canvas(self.Axis4_frame, width=20, height=20)
        self.AxisDoneStatusCanvas.grid(row=0,column=3, pady = 5, sticky = 'w')
        self.AxisDoneStatusLed = self.AxisDoneStatusCanvas.create_oval(5, 5, 15, 15)

    #-----------Move Direct Absolute Tab-----------
        #-----------Move Direct Absolute Tab Frames-----------
        self.Direct_frame = tk.Frame(self.MoveDirectTab, borderwidth = 1, relief = "flat", width = 40, height=50)
        self.Direct_frame.grid(row = 0, column=0, sticky = "nw", ipadx = 10, pady = 5)
        
        self.Direct2_frame = tk.Frame(self.MoveDirectTab, borderwidth = 1, relief = "flat", width = 40, height=50)
        self.Direct2_frame.grid(row = 0, column=2, sticky = "nw", ipadx = 10, pady = 5)

        self.Direct3_frame = tk.Frame(self.MoveDirectTab, borderwidth = 1, relief = "flat")
        self.Direct3_frame.grid(row = 8, column=0, pady = 10, sticky = "nw")

        self.Direct4_frame = tk.Frame(self.MoveDirectTab, borderwidth = 1, relief = "flat")
        self.Direct4_frame.grid(row = 9, column=0, pady = 10, sticky = 'nw')

        #Frame 1  
        self.Xdirect_label = tk.Label(self.Direct_frame, text = "X:")
        self.Xdirect_label.grid(row = 0, column=0, padx=5, sticky = "w")
        
        self.DirectAbsoluteX_variable = tk.DoubleVar()
        self.Xdirect_entry = tk.Entry(self.Direct_frame, width=4, textvariable=self.DirectAbsoluteX_variable)
        self.Xdirect_entry.grid(row=0, column = 1, padx=5)

     
        self.Ydirect_label = tk.Label(self.Direct_frame, text = "Y:")
        self.Ydirect_label.grid(row = 1, column=0, padx=5)

        self.DirectAbsoluteY_variable = tk.DoubleVar()
        self.Ydirect_entry = tk.Entry(self.Direct_frame, width=4, textvariable=self.DirectAbsoluteY_variable)
        self.Ydirect_entry.grid(row=1, column = 1, padx=5)


        self.Zdirect_label = tk.Label(self.Direct_frame, text = "Z:")
        self.Zdirect_label.grid(row = 2, column=0, padx=5)

        self.DirectAbsoluteZ_variable = tk.DoubleVar()
        self.Zdirect_entry = tk.Entry(self.Direct_frame, width=4, textvariable=self.DirectAbsoluteZ_variable)
        self.Zdirect_entry.grid(row=2, column = 1, padx=5)


        self.Adirect_label = tk.Label(self.Direct_frame, text = "A:")
        self.Adirect_label.grid(row = 3, column=0, padx=5)

        self.DirectAbsoluteA_variable = tk.DoubleVar()
        self.Adirect_entry = tk.Entry(self.Direct_frame, width=4, textvariable=self.DirectAbsoluteA_variable)
        self.Adirect_entry.grid(row=3, column = 1, padx=5)


        self.Bdirect_label = tk.Label(self.Direct_frame, text = "B:")
        self.Bdirect_label.grid(row = 4, column=0, padx=5)

        self.DirectAbsoluteB_variable = tk.DoubleVar()
        self.Bdirect_entry = tk.Entry(self.Direct_frame, width=4, textvariable=self.DirectAbsoluteB_variable)
        self.Bdirect_entry.grid(row=4, column = 1, padx=5)


        self.Cdirect_label = tk.Label(self.Direct_frame, text = "C:")
        self.Cdirect_label.grid(row = 5, column=0, padx=5)

        self.DirectAbsoluteC_variable = tk.DoubleVar()
        self.Cdirect_entry = tk.Entry(self.Direct_frame, width=4, textvariable=self.DirectAbsoluteC_variable)
        self.Cdirect_entry.grid(row=5, column = 1, padx=5)


        #Frame 2
        self.E1direct_label = tk.Label(self.Direct2_frame, text = "E1:")
        self.E1direct_label.grid(row = 0, column=0, padx=5)

        self.DirectAbsoluteE1_variable = tk.DoubleVar()
        self.E1direct_entry = tk.Entry(self.Direct2_frame, width=4, textvariable=self.DirectAbsoluteE1_variable)
        self.E1direct_entry.grid(row=0, column = 1, padx=5)


        self.E2direct_label = tk.Label(self.Direct2_frame, text = "E2:")
        self.E2direct_label.grid(row = 1, column=0, padx=5)

        self.DirectAbsoluteE2_variable = tk.DoubleVar()
        self.E2direct_entry = tk.Entry(self.Direct2_frame, width=4, textvariable=self.DirectAbsoluteE2_variable)
        self.E2direct_entry.grid(row=1, column = 1, padx=5)

        
        self.E3direct_label = tk.Label(self.Direct2_frame, text = "E3:")
        self.E3direct_label.grid(row = 2, column=0, padx=5)

        self.DirectAbsoluteE3_variable = tk.DoubleVar()
        self.E3direct_entry = tk.Entry(self.Direct2_frame, width=4, textvariable=self.DirectAbsoluteE3_variable)
        self.E3direct_entry.grid(row=2, column = 1, padx=5)


        self.E4direct_label = tk.Label(self.Direct2_frame, text = "E4:")
        self.E4direct_label.grid(row = 3, column=0, padx=5)

        self.DirectAbsoluteE4_variable = tk.DoubleVar()
        self.E4direct_entry = tk.Entry(self.Direct2_frame, width=4, textvariable=self.DirectAbsoluteE4_variable)
        self.E4direct_entry.grid(row=3, column = 1, padx=5)


        self.E5direct_label = tk.Label(self.Direct2_frame, text = "E5:")
        self.E5direct_label.grid(row=4, column=0, padx=5)

        self.DirectAbsoluteE5_variable = tk.DoubleVar()
        self.E5direct_entry = tk.Entry(self.Direct2_frame, width=4, textvariable=self.DirectAbsoluteE5_variable)
        self.E5direct_entry.grid(row=4, column = 1, padx=5)


        self.E6direct_label = tk.Label(self.Direct2_frame, text = "E6:")
        self.E6direct_label.grid(row = 5, column=0, padx=5)

        self.DirectAbsoluteE6_variable = tk.DoubleVar()
        self.E6direct_entry = tk.Entry(self.Direct2_frame, width=4, textvariable=self.DirectAbsoluteE6_variable)
        self.E6direct_entry.grid(row=5, column = 1, padx=5)
        

        #Frame 3
        self.Movedirect_Button = tk.Button(self.Direct3_frame, text = "Move to Position Directly", command = self.MoveDirectAbsolute)
        self.Movedirect_Button.grid(row=0, column=0, padx=5)
        

        #Frame 4 
        #Direct Absolute Active Status
        self.DirectActiveLabel = tk.Label(self.Direct4_frame, text = "Active:")
        self.DirectActiveLabel.grid(row=0,column=0, padx=1, pady = 5, sticky = 'w')

        self.DirectActiveStatusCanvas = tk.Canvas(self.Direct4_frame, width=20, height=20)
        self.DirectActiveStatusCanvas.grid(row=0,column=1, pady = 5, sticky = 'w')

        self.DirectActiveStatusLed = self.DirectActiveStatusCanvas.create_oval(5, 5, 15, 15)
        
        #Direct Absolute Done Status
        self.DirectDoneLabel = tk.Label(self.Direct4_frame, text = "Done:")
        self.DirectDoneLabel.grid(row=0,column=2,  padx=1, pady = 5, sticky = 'w')

        self.DirectDoneStatusCanvas = tk.Canvas(self.Direct4_frame, width=20, height=20)
        self.DirectDoneStatusCanvas.grid(row=0,column=3, pady = 5, sticky = 'w')
        self.DirectDoneStatusLed = self.DirectDoneStatusCanvas.create_oval(5, 5, 15, 15)


    #------------------Jogging Tab------------------
        #Jogging Buttons
        self.variables = ["A1 -", "A1 +", "X -", "X +", "A2 -", "A2 +", "Y -", "Y +", "A3 -", "A3 +", "Z -",  "Z +", "A4 -", "A4 +", "A -", "A +", "A5 -", "A5 +", "B -", "B +",  "A6 -", "A6 +", "C -", "C +"]
        self.buttons = []

        #Frames in Jogging Tab
        self.jog_frame = tk.Frame(self.JoggingTab, borderwidth = 1, relief = "flat", width = 30, height=50)
        self.jog_frame.grid(row = 0, column=0, pady = 10)
        
        self.jog2_frame = tk.Frame(self.JoggingTab, borderwidth = 1, relief = "flat", width = 30, height=50)
        self.jog2_frame.grid(row = 0, column=1, pady = 10, padx = 10, sticky = "n")
        
        #Frame 1 
        for i, var in enumerate(self.variables):
            button = tk.Button(self.jog_frame, text=var, bg= "#D3D3D3")
            button.grid(row=i//4, column=i%4, padx=10, pady = 1)
            button.bind("<ButtonPress>", lambda event, button_name=var: self.JoggingButtonPress(event, button_name))
            button.bind("<ButtonRelease>", lambda event, button_name=var: self.JoggingButtonRelease(event, button_name))
            self.buttons.append(button)

        #Activate JogAdvanced Toggle
        self.activate_jog_advanced = tk.BooleanVar(value=False)
        self.jog_advanced_checkbutton = tk.Checkbutton(self.JoggingTab, text="Activate JogAdvanced", variable=self.activate_jog_advanced, command=self.activateJogAdvanced_Toggle, fg="red", activeforeground= "red")
        self.jog_advanced_checkbutton.grid(row=len(self.variables), column=0, sticky = "nw")

        #Frame 2
        self.move_cordsys_label = tk.Label(self.jog2_frame, text = "Base/Tool Move Coordinate System: ")
        self.move_cordsys_label.grid(row=0, column=0)

        self.move_cordsys_combobox_variable = tk.IntVar()
        self.move_cordsys_combobox = ttk.Combobox(self.jog2_frame, textvariable = self.move_cordsys_combobox_variable)
        self.move_cordsys_combobox["values"] = (1,2)
        self.move_cordsys_combobox.current(0)
        self.move_cordsys_combobox.grid(row=1, column=0, pady=10)

        self.move_cordsysInfo_label = tk.Label(self.jog2_frame, text = "1 -> Base Coordinate System\n 2 -> Tool Coordinate System ", fg= "grey")
        self.move_cordsysInfo_label.grid(row=2, column=0, pady = 10, sticky = "nwe")        
        
    #---------------TechFunction Tab---------------
        self.TechFunc_Button = tk.Button(self.TechFunctionTab, text = "TechFunc Advanced")
        self.TechFunc_Button.grid(row = 0, column = 0, pady = 10, padx=10)
        self.TechFunc_Button.bind('<ButtonPress>', self.TechFctAdv_Button_Press)
        self.TechFunc_Button.bind('<ButtonRelease>', self.TechFctAdv_Button_Release)

        self.TechFunc_Label = tk.Label(self.TechFunctionTab, text = "TechFunc Output:", font = ("Segoe UI", 10, "bold"))
        self.TechFunc_Label.grid(row = 0, column = 1, pady = 5, sticky = "w")

        self.TechFuncOutput_Label = tk.Label(self.TechFunctionTab, text = "TECHFUNCTIONADVANCED.RETURNVALUE:\n{}".format(_mxA_KRC_TECHFUNCTIONADVANCED.RETURNVALUE))

        self.TechFuncOutput_Label.grid(row = 1, column = 1)

    #---------------SafeOP Tab---------------
        #-------------Safe OP Tab Frames-------------
        self.SafeOP_frame = tk.Frame(self.SafeOPTab, borderwidth = 1, relief = "flat", width = 40, height=50)
        self.SafeOP_frame.grid(row = 0, column=0, sticky = "nw", ipadx = 10, pady = 5)

        self.SafeOP2_frame = tk.Frame(self.SafeOPTab, borderwidth = 1, relief = "flat", width = 40, height=50)
        self.SafeOP2_frame.grid(row = 1, column=0, sticky = "nw", ipadx = 10, pady = 5)

        #Frame 1
        self.StartBraketest_Button = tk.Button(self.SafeOP_frame, text="Start Brake Test")
        self.StartBraketest_Button.grid(row=0, column=0, padx = 5, pady = 10, ipady = 5)
        self.StartBraketest_Button.bind('<ButtonRelease>', self.StartBraketest_Release)
        self.StartBraketest_Button.bind('<ButtonPress>', self.StartBraketest_Press)

        self.ReqBraketest_Button = tk.Button(self.SafeOP_frame, text="Request Brake Test")
        self.ReqBraketest_Button.grid(row=0, column=1, padx = 5, pady = 10, ipady = 5)
        self.ReqBraketest_Button.bind('<ButtonRelease>', self.ReqBraketest_Release)
        self.ReqBraketest_Button.bind('<ButtonPress>', self.ReqBraketest_Press)


        #Frame 2
        self.BraketestActive_label = tk.Label(self.SafeOP2_frame, text = "Active: ")
        self.BraketestActive_label.grid(row=0, column=0, padx=1, pady = 5, sticky = 'e')

        self.BraketestActiveStatusCanvas = tk.Canvas(self.SafeOP2_frame, width=20, height=20)
        self.BraketestActiveStatusCanvas.grid(row=0,column=1, pady = 5, sticky = 'w')
        self.BrakeTestActiveStatusLed = self.BraketestActiveStatusCanvas.create_oval(5, 5, 15, 15)

        self.BraketestDone_label = tk.Label(self.SafeOP2_frame, text = "Done: ")
        self.BraketestDone_label.grid(row=0, column=2, padx=1, pady = 5, sticky = 'e')

        self.BraketestDoneStatusCanvas = tk.Canvas(self.SafeOP2_frame, width=20, height=20)
        self.BraketestDoneStatusCanvas.grid(row=0,column=3, pady = 5, sticky = 'w')
        self.BrakeTestDoneStatusLed = self.BraketestDoneStatusCanvas.create_oval(5, 5, 15, 15)


    #Data Update loop
    def update(self, loop_counter, test_step_hmi ): 

        self.toolbasepos_label.config(text="Tool: {}      Base: {}".format(_mxA_READACTUALPOSITION._TOOL, _mxA_READACTUALPOSITION._BASE))

        self.currentposition1_label.config(text="Current Axis Position:")
        self.currentposition2_label.config(text="A1: {}\nA2: {}\nA3: {}\nA4: {}\nA5: {}\nA6: {}".format(
            round(_mxA_READACTUALAXISPOSITION._A1, 2),
            round(_mxA_READACTUALAXISPOSITION._A2, 2),
            round(_mxA_READACTUALAXISPOSITION._A3, 2),
            round(_mxA_READACTUALAXISPOSITION._A4, 2),
            round(_mxA_READACTUALAXISPOSITION._A5, 2),
            round(_mxA_READACTUALAXISPOSITION._A6, 2)
        ))

        self.cart1_label.config(text="Cartisian Position:")
        self.cart2_label.config(text="X: {}\nY: {}\nZ: {}\nA: {}\nB: {}\nC: {}".format(
            round(_mxA_READACTUALPOSITION._X, 2),
            round(_mxA_READACTUALPOSITION._Y, 2),
            round(_mxA_READACTUALPOSITION._Z, 2),
            round(_mxA_READACTUALPOSITION._A, 2),
            round(_mxA_READACTUALPOSITION._B, 2),
            round(_mxA_READACTUALPOSITION._C, 2)
        ))
        self.statusturn_label.config(text="Status: {}  Turn: {}".format(
            _mxA_READACTUALPOSITION._STATUS,
            _mxA_READACTUALPOSITION._TURN
        ))
        self.loop_counter_label.config(text="Loop number: {}".format(loop_counter))
        self.test_step_label.config(text="    Test step: {}".format(test_step_hmi))


    #-----------ErrorID-----------
        if _mxA_KRC_ERROR.ERRORID == 0:
            self.errorNr_label.config(text="Error ID: {}".format(_mxA_KRC_ERROR.ERRORID), fg="Black")
        else:
            self.errorNr_label.config(text="Error ID: {}".format(_mxA_KRC_ERROR.ERRORID), fg="red")



    #-----------State of the Robot-----------
        if _mxA_KRC_AUTOMATICEXTERNAL.VALID:
           self.robotstateS_label.config(bg="Light Green")
        else: 
            self.robotstateS_label.config(bg="Red")

        if _mxA_KRC_AUTOMATICEXTERNAL.PRO_ACT:
            self.robotstateR_label.config(bg="Light Green")
        else: 
            self.robotstateR_label.config(bg="Red")

        if _mxA_KRC_AUTOMATICEXTERNAL.RC_RDY1:
            self.robotstateI_label.config(bg="Light Green")
        else: 
            self.robotstateI_label.config(bg="Red")

        if _mxA_KRC_AUTOMATICEXTERNAL.IO_ACTCONF:
            self.robotstateExt_label.config(bg="Light Green")
        else:
            self.robotstateExt_label.config(bg="Red")

    #-----------AUTOSTART-----------         
        if _mxA_KRC_AUTOSTART.DONE or _mxA_KRC_AUTOSTART.ERROR:
           self.messages_scrolledtext.insert(INSERT, "-> AUTOSTART.DONE: {}\n".format(_mxA_KRC_AUTOSTART.DONE))

           _mxA_KRC_AUTOSTART.EXECUTERESET = False

    #-----------SET COORDSYS-----------
        if _mxA_KRC_SETCOORDSYS.DONE or _mxA_KRC_SETCOORDSYS.ERROR:   
           _mxA_KRC_SETCOORDSYS.EXECUTECMD = False
        
    #-----------MOVE STATUS-----------
    #MoveAxisAbsolute Active Status

        if _mxA_KRC_MOVEAXISABSOLUTE.ACTIVE:
           self.AxisActiveStatusCanvas.itemconfig(self.AxisActiveStatusLed, fill="Green")
        else: 
            self.AxisActiveStatusCanvas.itemconfig(self.AxisActiveStatusLed, fill="SystemButtonFace")


        if  _mxA_KRC_MOVEAXISABSOLUTE.DONE:
            self.AxisDoneStatusCanvas.itemconfig(self.AxisDoneStatusLed, fill="Green")
            self.messages_scrolledtext.insert(INSERT, "-> MOVEAXISABSOLUTE.DONE: {}\n".format(_mxA_KRC_MOVEAXISABSOLUTE.DONE))
            _mxA_KRC_MOVEAXISABSOLUTE.EXECUTECMD = False
        
        elif _mxA_KRC_MOVEAXISABSOLUTE.EXECUTECMD == False: 
            self.AxisDoneStatusCanvas.itemconfig(self.AxisDoneStatusLed, fill="SystemButtonFace")
        
    #MoveDirectAbsolute Active Status

        if _mxA_KRC_MOVEDIRECTABSOLUTE.ACTIVE:
            self.DirectActiveStatusCanvas.itemconfig(self.DirectActiveStatusLed, fill="Green")
        else: 
            self.DirectActiveStatusCanvas.itemconfig(self.DirectActiveStatusLed, fill="SystemButtonFace")


        if _mxA_KRC_MOVEDIRECTABSOLUTE.DONE:
           self.DirectDoneStatusCanvas.itemconfig(self.DirectDoneStatusLed, fill="Green")
           self.messages_scrolledtext.insert(INSERT, "-> mxA_KRC_MOVEDIRECTABSOLUTE.DONE: {}\n".format(_mxA_KRC_MOVEDIRECTABSOLUTE.DONE))
           _mxA_KRC_MOVEDIRECTABSOLUTE.EXECUTECMD = False
        
        elif _mxA_KRC_MOVEDIRECTABSOLUTE.EXECUTECMD == False: 
             self.DirectDoneStatusCanvas.itemconfig(self.DirectDoneStatusLed, fill="SystemButtonFace")

        if _mxA_KRC_MOVEDIRECTABSOLUTE.ERROR or  _mxA_KRC_MOVEDIRECTABSOLUTE.ABORTED or _mxA_KRC_ABORT.BUSY:
             _mxA_KRC_MOVEDIRECTABSOLUTE.EXECUTECMD = False
             
             
    #Jogging Move Coordinate System
        if self.move_cordsys_combobox_variable.get() == 2:
           _mxA_KRC_JOGADVANCED.MOVETYPE = 2
        else:
            _mxA_KRC_JOGADVANCED.MOVETYPE = 1

    #Tech Function Advanced      
        element_str = "\n".join(str(round(val,2)) for val in _mxA_KRC_TECHFUNCTIONADVANCED.RETURNVALUE)
        self.TechFuncOutput_Label.config(text = "{}\n".format(element_str))

        if  _mxA_KRC_TECHFUNCTIONADVANCED.DONE:
            self.messages_scrolledtext.insert(INSERT, "-> Tech Function Advanced Done: {}\n".format(_mxA_KRC_TECHFUNCTIONADVANCED.DONE))
            _mxA_KRC_TECHFUNCTIONADVANCED.EXECUTECMD = False
        
        elif _mxA_KRC_TECHFUNCTIONADVANCED.ERROR:
            self.messages_scrolledtext.insert(INSERT, "-> Tech Function Error ID: {}\n".format(_mxA_KRC_TECHFUNCTIONADVANCED.ERRORID))

            _mxA_KRC_TECHFUNCTIONADVANCED.EXECUTECMD = False
        
    #SafeOP Active Status

        if _mxA_KRC_Braketest._ACTIVE:
            self.BraketestActiveStatusCanvas.itemconfig(self.BrakeTestActiveStatusLed, fill="Green")
        else:
            self.BraketestActiveStatusCanvas.itemconfig(self.BrakeTestActiveStatusLed, fill="SystemButtonFace") 
            _mxA_KRC_Braketest.EXECUTECMD == False


        if _mxA_KRC_Braketest.DONE:
           self.BraketestDoneStatusCanvas.itemconfig(self.BrakeTestDoneStatusLed, fill="Green")
           self.messages_scrolledtext.insert(INSERT, "-> Braketest Done: {}\n".format(_mxA_KRC_Braketest.DONE))


        elif  _mxA_KRC_Braketest.EXECUTECMD == False:
              self.BraketestDoneStatusCanvas.itemconfig(self.BrakeTestDoneStatusLed, fill="SystemButtonFace")

        self.root.update_idletasks()
        self.root.update()
    
    def get_slider_value(self):
           return round(self.override_value.get())
    
UserHMI = HMI()


for i_loop_counter in range( loops ):
    time.sleep( loop_Time )

    UserHMI.update(i_loop_counter, test_step )
    override_value = (UserHMI.get_slider_value())
    print("\n\n")
    
#-----------KRC_ReadAxisGroup function call-----------
    _mxA_KRC_READAXISGROUP.KRC4_INPUT = input_buffer
    _mxA_KRC_READAXISGROUP.AXISGROUPIDX = _axisGroupIdx
    print(   "Heartbeats   PCOS " , _mxA_KRC_READAXISGROUP.M_HEARTBEATPCOS , " SINT ", _mxA_KRC_READAXISGROUP.M_HEARTBEATSUBMIT , " Error ID ", _mxA_KRC_READAXISGROUP.ERRORID)


#-----------KRC_Diag function call-----------
    _mxA_KRC_Diag.AXISGROUPIDX = _axisGroupIdx

    print( "KRC_Diag  - QUEUECOUNT: " , _mxA_KRC_Diag.QUEUECOUNT , " Error ID " , _mxA_KRC_Diag.ERRORID, "S-int AVG time " , _mxA_KRC_Diag.SUBMITCYC_AVG )


#-----------KRC_ReadActualPosition axis wise function call-----------
    _mxA_READACTUALAXISPOSITION.AXISGROUPIDX = _axisGroupIdx
    print( "Axis Position ---- A1 " , _mxA_READACTUALAXISPOSITION.A1 , " A2 ", _mxA_READACTUALAXISPOSITION.A2 , " A3 ", _mxA_READACTUALAXISPOSITION.A3 , " A4 ", _mxA_READACTUALAXISPOSITION.A4 , " A5 ", _mxA_READACTUALAXISPOSITION.A5 , " A6 ", _mxA_READACTUALAXISPOSITION.A6 )

#-----------KRC_ReadActualPosition cartesian function call-----------
    _mxA_READACTUALPOSITION.AXISGROUPIDX = _axisGroupIdx
    print("Cartesian  Position ---- X " , _mxA_READACTUALPOSITION.X , " Y ", _mxA_READACTUALPOSITION.Y , " Z ", _mxA_READACTUALPOSITION.Z , " A ", _mxA_READACTUALPOSITION.A , " B ", _mxA_READACTUALPOSITION.B , " C ", _mxA_READACTUALPOSITION.C )
    print("Tool: ", _mxA_READACTUALPOSITION.TOOL , "Base: ", _mxA_READACTUALPOSITION._BASE )
    print(" Status ", _mxA_READACTUALPOSITION.STATUS ,  " Status binary ", bin(_mxA_READACTUALPOSITION.STATUS), "   -----   TURN " ,   _mxA_READACTUALPOSITION._TURN , " TURN  binary " ,  bin( _mxA_READACTUALPOSITION._TURN ) )
    
#-----------KRC_Abort function call-----------
    _mxA_KRC_ABORT.AXISGROUPIDX = _axisGroupIdx
    if _mxA_KRC_ABORT.DONE or _mxA_KRC_ABORT.ACTIVE:
        print( "_mxA_KRC_ABORT"  )
        _mxA_KRC_ABORT.EXECUTECMD = False

#-----------KRC_Error function call-----------
    _mxA_KRC_ERROR.AXISGROUPIDX = _axisGroupIdx
    print( "KRC_Error ErrorID: ", _mxA_KRC_ERROR.ERRORID, " Drives not ready? ", _mxA_KRC_ERROR.DRIVESNOTREADY, "No program active? ", _mxA_KRC_ERROR.NOPROGACTIVE  )


#-----------KRC_SetOverride function call-----------
    _mxA_KRC_SETOVERRIDE.AXISGROUPIDX = _axisGroupIdx
    _mxA_KRC_SETOVERRIDE.OVERRIDE = override_value

#-----------KRC_AutomaticExternal function call-----------
    _mxA_KRC_AUTOMATICEXTERNAL.AXISGROUPIDX = _axisGroupIdx
    _mxA_KRC_AUTOMATICEXTERNAL.MOVE_ENABLE = True
    _mxA_KRC_AUTOMATICEXTERNAL.DRIVES_OFF = True

    # _mxA_KRC_AUTOMATICEXTERNAL.ENABLE_T1 = True
    _mxA_KRC_AUTOMATICEXTERNAL.ENABLE_T2 = True
    _mxA_KRC_AUTOMATICEXTERNAL.ENABLE_AUT = True
    _mxA_KRC_AUTOMATICEXTERNAL.ENABLE_EXT = True

#-----------Set Coordsys-----------
    _mxA_KRC_SETCOORDSYS.AXISGROUPIDX = _axisGroupIdx
    _mxA_KRC_SETCOORDSYS.COORDINATESYSTEM = CoordSys_ToolBase
    _mxA_KRC_SETCOORDSYS.BUFFERMODE = 2
    
#-----------KRC_JOGADVANCED function call-----------
    _mxA_KRC_JOGADVANCED.AXISGROUPIDX = _axisGroupIdx
    _mxA_KRC_JOGADVANCED.VELOCITY = 50.0
    _mxA_KRC_JOGADVANCED.ACCELERATION = 50.0
    #_mxA_KRC_JOGADVANCED.JOGADVANCED = HMI_activate_Jog_Advanced
    _mxA_KRC_JOGADVANCED.COORDINATESYSTEM = CoordSys_ToolBase
    if _mxA_KRC_JOGADVANCED.ACTIVE:
        print("HMI_activate_Jog_Advanced ", _mxA_KRC_JOGADVANCED.JOGADVANCED, " _mxA_KRC_JOGADVANCED Error ID " , _mxA_KRC_JOGADVANCED.ERRORID , " _mxA_KRC_JOGADVANCED.B_X_JA_P ",  _mxA_KRC_JOGADVANCED.B_X_JA_P)

#-----------KRC_ReadSafeOPstatus function call by button-----------
    _mxA_KRC_ReadSafeOPstatus.AXISGROUPIDX = _axisGroupIdx

    if _mxA_KRC_ReadSafeOPstatus.BRAKETEST_REQ_EXT == True :
        print("Braketest requested by python program")

#-----------KRC_TECHFUNCTION ADVANCED function call-----------
    _mxA_KRC_TECHFUNCTIONADVANCED.AXISGROUPIDX = _axisGroupIdx
    _mxA_KRC_TECHFUNCTIONADVANCED.TECHFUNCTIONID = 5
    _mxA_KRC_TECHFUNCTIONADVANCED.PARAMETERCOUNT = 1

# -------- STEP 0 - KRC_Initialize function call  ------------

    _mxA_KRC_INITIALIZE.AXISGROUPIDX = _axisGroupIdx
    if test_step == 0:
        print("KRC_Initalize Error ID: ",  _mxA_KRC_INITIALIZE.ERRORID , "Done? ", _mxA_KRC_INITIALIZE.DONE , "Test_Step", test_step , "KRC_Version:", _mxA_KRC_INITIALIZE.KRC_MAJOR , _mxA_KRC_INITIALIZE.KRC_MINOR , _mxA_KRC_INITIALIZE.KRC_REVISION, "Serial Number: ", _mxA_KRC_INITIALIZE.KRC_SERIAL , "Absolutgenau?" , _mxA_KRC_INITIALIZE.KRC_ABSACCUR)
        if i_loop_counter <= 100:
            print("100 cycles waiting for krc...")
            
    if test_step == 0 and _mxA_KRC_INITIALIZE.DONE :
        test_step = 10
        print("KRC_Initalize Error ID: ",  _mxA_KRC_INITIALIZE.ERRORID , "Done? ", _mxA_KRC_INITIALIZE.DONE , "Test_Step", test_step  )

# -------- STEP 10 - KRC_Autostart function call  ------------

    _mxA_KRC_AUTOSTART.AXISGROUPIDX = _axisGroupIdx
    if test_step == 10  :
        _mxA_KRC_AUTOSTART.EXECUTERESET = True
        print( "\n", "Autostart --------- > Error ID " , _mxA_KRC_AUTOSTART._ERRORID , "DispActive" , _mxA_KRC_AUTOSTART._DISPACTIVE , " Reset Valid??? " , _mxA_KRC_AUTOSTART._RESETVALID ) 
        print("Test_Step: ", test_step  )

    if test_step == 10 and _mxA_KRC_AUTOSTART._DISPACTIVE:
        _mxA_KRC_AUTOSTART.EXECUTERESET = False
        test_step = 14

# -------- KRC_MOVEAXISABSOLUTE   ------------  
    _mxA_KRC_MOVEAXISABSOLUTE.AXISGROUPIDX = _axisGroupIdx
    _mxA_KRC_MOVEAXISABSOLUTE.AXISPOSITION = axis_target_pos
    _mxA_KRC_MOVEAXISABSOLUTE.BUFFERMODE = 2
    _mxA_KRC_MOVEAXISABSOLUTE.VELOCITY = 100 # %
    _mxA_KRC_MOVEAXISABSOLUTE.APPROXIMATE = APO_parameter
    
#---------------- KRC_MOVEDIRECTABSOLUTE ----------------
    _mxA_KRC_MOVEDIRECTABSOLUTE.AXISGROUPIDX = _axisGroupIdx
    _mxA_KRC_MOVEDIRECTABSOLUTE.POSITION = direct_target_pos
    _mxA_KRC_MOVEDIRECTABSOLUTE.BUFFERMODE = 2
    _mxA_KRC_MOVEDIRECTABSOLUTE.VELOCITY = 100 # %
    _mxA_KRC_MOVEDIRECTABSOLUTE.APPROXIMATE = APO_parameter
    _mxA_KRC_MOVEDIRECTABSOLUTE.SPLINEMODE = Movements_in_Spline

# ------  KRC_WriteAxisGroup function call  ------
    print("\n")
    
    _mxA_KRC_WRITEAXISGROUP.AXISGROUPIDX = _axisGroupIdx
    output_to_robot = _mxA_KRC_WRITEAXISGROUP.KRC4_OUTPUT
    update_mxAutomation_interface()
    print(".............. end of the program reached - loop " , i_loop_counter , " - STEP Nr: ", test_step," .........................")
