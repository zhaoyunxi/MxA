using MxA;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Globalization;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Threading;

namespace mxAutomation_wpf
{
    public class MainViewModel : ViewModeBase
    {
        public MainViewModel()
        {
            
        }

        private string _robotIP = "127.0.0.1";
        public string RobotIP
        {
            get { return _robotIP; }
            set
            {
                _robotIP = value;
                OnPropertyChanged();
            }
        }


        private string _errorID = " - ";
        public string ErrorID
        {
            get { return _errorID; }
            set
            {
                _errorID = value;
                OnPropertyChanged();
            }
        }


        private int _programOverride = 50;
        public int ProgramOverride
        {
            get { return _programOverride; }
            set
            {
                _programOverride = value;
                OnPropertyChanged();
            }
        }


        private string _newLogMessage;
        public string NewLogMessage
        {
            get { return _newLogMessage; }
            set
            {
                if (_newLogMessage == null)
                {
                    _newLogMessage = value;
                }
                else
                {
                    _newLogMessage = _newLogMessage + Environment.NewLine + value;
                }
                
                OnPropertyChanged();
            }
        }


        private string _stateStr = "";
        public string StateStr
        {
            get { return _stateStr; }
            set
            {
                _stateStr = value;
                OnPropertyChanged();
            }
        }


        private E6AXIS_EXTEND _e6AXIS_T = new E6AXIS_EXTEND { A1 = 0, A2 = -90, A3 = 90, A4 = 0, A5 = 90, A6 = 0 };
        public E6AXIS_EXTEND E6AXIS_T
        {
            get { return _e6AXIS_T; }
            set
            {
                _e6AXIS_T = value;
                OnPropertyChanged();
            }
        }


        private E6POS_EXTEND _e6POS_PTP_ABS = new E6POS_EXTEND { X = 540, Y = 20, Z = 895, A = 180, B = 0, C = 180, S = 2, T = 35 };
        public E6POS_EXTEND E6POS_PTP_ABS
        {
            get { return _e6POS_PTP_ABS; }
            set
            {
                _e6POS_PTP_ABS = value;
                OnPropertyChanged();
            }
        }


        private E6POS_EXTEND _e6POS_PTP_REL = new E6POS_EXTEND { X = 0, Y = 10, Z = 0, A = 0, B = 0, C = 0 };
        public E6POS_EXTEND E6POS_PTP_REL
        {
            get { return _e6POS_PTP_REL; }
            set
            {
                _e6POS_PTP_REL = value;
                OnPropertyChanged();
            }
        }


        private E6POS_EXTEND _e6POS_LIN_ABS = new E6POS_EXTEND { X = 540, Y = -20, Z = 895, A = 180, B = 0, C = 180 };
        public E6POS_EXTEND E6POS_LIN_ABS
        {
            get { return _e6POS_LIN_ABS; }
            set
            {
                _e6POS_LIN_ABS = value;
                OnPropertyChanged();
            }
        }


        private E6POS_EXTEND _e6POS_LIN_REL = new E6POS_EXTEND { X = 0, Y = -10, Z = 0, A = 0, B = 0, C = 0 };
        public E6POS_EXTEND E6POS_LIN_REL
        {
            get { return _e6POS_LIN_REL; }
            set
            {
                _e6POS_LIN_REL = value;
                OnPropertyChanged();
            }
        }


        private CustomCommand _connectedCmd;
        public CustomCommand ConnectCmd 
        { 
            get
            {
                if(_connectedCmd == null)
                {
                    _connectedCmd = new CustomCommand(ConnectToRobot, CanConnectToRobot);
                }

                return _connectedCmd;
            }
        }
        public void ConnectToRobot(object o)
        {
            if (cycleThread == null || !cycleThread.IsAlive)
            {
                cycleNr = 0;

                if (!IPAddress.TryParse(RobotIP, out robotIP))
                {
                    Log("The ip address is not valid!");
                    return;
                }

                sendEndPoint = new IPEndPoint(robotIP, sendPort);
                if (sendSocket == null)
                {
                    sendSocket = new UdpClient();
                    GLOBAL.KRC_AXISGROUPREFARR[axisGroupIndex].HEARTBEATTO = 2000;
                }
                sendSocket.Connect(sendEndPoint);

                cycleFlag = true;
                cycleThread = new Thread(Cycle);
                cycleThread.IsBackground = true;
                cycleThread.Start();

                //校验机器人当前是否在外部自动EXT模式
                if (!IsInEXTMode())
                {
                    cycleFlag = false;
                    Log("Robot is not in EXT mode!");
                    return;
                }

                //开始外部自动启动流程
                confirmMsg = true;

                //1.驱动器上电
                if (!SetDriveOn())
                {
                    Log("Failed to set drive on!");
                    return;
                }

                //2.电机上电
                if (!SetMotorOn())
                {
                    Log("Failed to set motor on!");
                    return;
                }

                //3.清除其余错误状态
                if (!ResetError())
                {
                    Log("Failed to reset error!");
                    return;
                }

                //4.复位启动
                resetStart = true;

                if (!IsProgramRunning())
                {
                    Log("Failed to start robot!");
                }
                else
                {
                    Log("Start robot successfully!");
                    startRunning = true;
                }
                resetStart = false;
            }
        }
        public bool CanConnectToRobot()
        {
            return !cycleFlag;
        }


        private CustomCommand _disconnectCmd;
        public CustomCommand DisconnectCmd 
        { 
            get
            {
                if(_disconnectCmd == null)
                {
                    _disconnectCmd = new CustomCommand(DisconnectFromRobot, CanDisconnectFromRobot);
                }
                return _disconnectCmd;
            }
        }
        public void DisconnectFromRobot(object o)
        {
            driveOff = false;

            for (int i = 0; i < 40; i++)
            {
                if (!krcAutoExt.PRO_ACT)
                {
                    break;
                }
                Thread.Sleep(50);
            }

            if (krcAutoExt.PRO_ACT)
            {
                Log("Error occurred when disconnecting from robot!");
            }
            else
            {
                Log("Disconnect from robot successfully!");
            }
            cycleFlag = false;
            startRunning = false;
        }
        public bool CanDisconnectFromRobot()
        {
            return cycleFlag;
        }


        private CustomCommand _pauseCmd;
        public CustomCommand PauseCmd
        { 
            get
            {
                if(_pauseCmd == null)
                {
                    _pauseCmd = new CustomCommand(PauseRobot, CanPauseRobot);
                }
                return _pauseCmd;
            }
        }
        public void PauseRobot(object o)
        {
            driveOff = false;
            Log("Robot is paused!");
        }
        public bool CanPauseRobot()
        {
            return cycleFlag && driveOff && proActiveNew;
        }


        private CustomCommand _resumeCmd;
        public CustomCommand ResumeCmd
        {
            get
            {
                if(_resumeCmd == null)
                {
                    _resumeCmd = new CustomCommand(ResumeRobot, CanResumeRobot);
                }
                return _resumeCmd;
            }
        }
        public void ResumeRobot(object o)
        {
            //校验机器人当前是否在外部自动EXT模式
            if (!IsInEXTMode())
            {
                Log("Robot is not in EXT mode!");
                return;
            }

            //开始恢复启动流程
            confirmMsg = true;

            //1.驱动器上电
            if (!SetDriveOn())
            {
                Log("Failed to set drive on!");
                return;
            }

            //2.清除其余错误状态
            if (!ResetError())
            {
                Log("Failed to reset error!");
                return;
            }

            //3.恢复启动
            extStart = true;

            if(!IsProgramRunning())
            {
                Log("Failed to resume robot!");
            }
            else
            {
                Log("Resume robot successfully!");
            }
            extStart = false;
        }
        public bool CanResumeRobot()
        {
            return cycleFlag && (!driveOff || !proActiveNew);
        }


        private CustomCommand _resetCmd;
        public CustomCommand ResetCmd
        {
            get 
            { 
                if(_resetCmd == null)
                {
                    _resetCmd = new CustomCommand(ResetRobot, CanResetRobot);
                }
                return _resetCmd;
            }
        }
        public void ResetRobot(object o)
        {
            //校验机器人当前是否在外部自动EXT模式
            if (!IsInEXTMode())
            {
                Log("Robot is not in EXT mode!");
                return;
            }

            //开始复位启动流程
            confirmMsg = true;

            //1.驱动器上电
            if (!SetDriveOn())
            {
                Log("Failed to set drive on!");
                return;
            }

            //2.清除其余错误状态
            if (!ResetError())
            {
                Log("Failed to reset error!");
                return;
            }

            //3.复位启动
            resetStart = true;

            if (!IsProgramRunning())
            {
                Log("Failed to reset robot!");
            }
            else
            {
                Log("Reset robot successfully!");
            }
            resetStart = false;
        }
        public bool CanResetRobot()
        {
            return cycleFlag && (!driveOff || !proActiveNew);
        }


        private CustomCommand _interruptCmd;
        public CustomCommand InterruptCmd
        {
            get 
            { 
                if(_interruptCmd == null)
                {
                    _interruptCmd = new CustomCommand(InterruptRobot, CanInterruptRobot);
                }
                return _interruptCmd;
            }
        }
        public void InterruptRobot(object o)
        {
            interruptPause = true;
        }
        public bool CanInterruptRobot()
        {
            return cycleFlag && !interruptPause;
        }


        private CustomCommand _continueCmd;
        public CustomCommand ContinueCmd
        {
            get
            {
                if(_continueCmd == null)
                {
                    _continueCmd = new CustomCommand(ContinueRobot, CanContinueRobot);
                }
                return _continueCmd;
            } 
        }
        public void ContinueRobot(object o)
        {
            interruptPause = false;
            Thread.Sleep(50);
            continueResume = true;
        }
        public bool CanContinueRobot()
        {
            return interruptPause;
        }


        private CustomCommand _ptpAxisAbsCmd;
        public CustomCommand PtpAxisAbsCmd
        {
            get
            {
                if(_ptpAxisAbsCmd == null)
                {
                    _ptpAxisAbsCmd = new CustomCommand(SendPtpAxisAbs, CanSendPtpAxisAbs);
                }
                return _ptpAxisAbsCmd;
            }
        }
        public void SendPtpAxisAbs(object o)
        {
            ptpAxisAbs = true;
        }
        public bool CanSendPtpAxisAbs()
        {
            return cycleFlag && !ptpAxisAbs;
        }


        private CustomCommand _ptpPosAbsCmd;
        public CustomCommand PtpPosAbsCmd
        {
            get
            {
                if(_ptpPosAbsCmd == null)
                {
                    _ptpPosAbsCmd = new CustomCommand(SendPtpPosAbs, CanSendPtpPosAbs);
                }
                return _ptpPosAbsCmd;
            }
        }
        public void SendPtpPosAbs(object o)
        {
            ptpCartAbs = true;
        }
        public bool CanSendPtpPosAbs()
        {
            return cycleFlag && !ptpCartAbs;
        }


        private CustomCommand _ptpPosRelCmd;
        public CustomCommand PtpPosRelCmd
        {
            get
            {
                if(_ptpPosRelCmd == null)
                {
                    _ptpPosRelCmd = new CustomCommand(SendPtpPosRel, CanSendPtpPosRel);
                }
                return _ptpPosRelCmd;
            }
        }
        public void SendPtpPosRel(object o)
        {
            ptpCartRel = true;
        }
        public bool CanSendPtpPosRel()
        {
            return cycleFlag && !ptpCartRel;
        }


        private CustomCommand _linPosAbsCmd;
        public CustomCommand LinPosAbsCmd
        {
            get
            {
                if(_linPosAbsCmd == null)
                {
                    _linPosAbsCmd = new CustomCommand(SendLinPosAbs, CanSendLinPosAbs);
                }
                return _linPosAbsCmd;
            }
        }
        public void SendLinPosAbs(object o)
        {
            linAbs = true;
        }
        public bool CanSendLinPosAbs()
        {
            return cycleFlag && !linAbs;
        }


        private CustomCommand _linPosRelCmd;
        public CustomCommand LinPosRelCmd
        { 
            get
            {
                if(_linPosRelCmd == null)
                {
                    _linPosRelCmd = new CustomCommand(SendLinPosRel, CanSendLinPosRel);
                }
                return _linPosRelCmd;
            }
        }
        public void SendLinPosRel(object o)
        {
            linRel = true;
        }
        public bool CanSendLinPosRel()
        {
            return cycleFlag && !linRel;
        }


        private CustomCommand _ptpArrayCmd;
        public CustomCommand PtpArrayCmd
        {
            get
            {
                if(_ptpArrayCmd == null)
                {
                    _ptpArrayCmd = new CustomCommand(SendPtpArray, CanSendPtpArray);
                }
                return _ptpArrayCmd;
            }
        }
        public void SendPtpArray(object o)
        {
            E6AXIS axisPos0;
            E6AXIS axisPos1 = new E6AXIS();
            E6AXIS axisPos2 = new E6AXIS();
            E6AXIS axisPos3 = new E6AXIS();

            axisPos0 = E6AXIS_T.ToE6Axis();
            axisPos1.CopyFrom(axisPos0);
            axisPos2.CopyFrom(axisPos0);
            axisPos3.CopyFrom(axisPos0);

            axisPos0.A1 -= 15;
            axisPos1.A1 -= 45;
            axisPos2.A1 -= 90;
            axisPos3.A1 -= 5;

            List<E6AXIS> axisPosList = new List<E6AXIS>();
            
            for(int i = 0; i < 10; i++)
            {
                axisPosList.Add(axisPos0);
                axisPosList.Add(axisPos1);
                axisPosList.Add(axisPos2);
                axisPosList.Add(axisPos3);
            }

            AddPtpMotionToList(axisPosList);
            ptpArray = true;
        }
        public bool CanSendPtpArray()
        {
            return cycleFlag && !ptpArray;
        }


        private CustomCommand _linArrayCmd;
        public CustomCommand LinArrayCmd
        {
            get
            {
                if(_linArrayCmd == null)
                {
                    _linArrayCmd = new CustomCommand(SendLinArray, CanSendLinArray);
                }
                return _linArrayCmd;
            }
        }
        public void SendLinArray(object o)
        {
            E6POS cartPos0;
            E6POS cartPos1 = new E6POS();
            E6POS cartPos2 = new E6POS();
            E6POS cartPos3 = new E6POS();

            cartPos0 = E6POS_LIN_ABS.ToE6Pos();
            cartPos0.STATUS = krcReadCartPos.STATUS;
            cartPos0.TURN = krcReadCartPos.TURN;
            cartPos1.CopyFrom(cartPos0);
            cartPos2.CopyFrom(cartPos0);
            cartPos3.CopyFrom(cartPos0);
            cartPos0.Z -= 50;
            cartPos1.Z -= 100;
            cartPos2.Z -= 150;
            cartPos3.Z -= 200;

            List<E6POS> cartPosList = new List<E6POS>();

            for(int i = 0; i < 10; i++)
            {
                cartPosList.Add(cartPos0);
                cartPosList.Add(cartPos1);
                cartPosList.Add(cartPos2);
                cartPosList.Add(cartPos3);
            }

            AddLinMotionToList(cartPosList);
            linArray = true;
        }
        public bool CanSendLinArray()
        {
            return cycleFlag && !linArray;
        }


        private CustomCommand _motionArrayCmd;
        public CustomCommand MotionArrayCmd
        {
            get
            {
                if(_motionArrayCmd == null)
                {
                    _motionArrayCmd = new CustomCommand(SendMotionArray, CanSendMotionArray);
                }
                return _motionArrayCmd;
            }
        }
        public void SendMotionArray(object o)
        {
            E6AXIS axisPos0;
            E6AXIS axisPos1 = new E6AXIS();

            axisPos0 = E6AXIS_T.ToE6Axis();
            axisPos1.CopyFrom(axisPos0);

            axisPos0.A1 -= 90;

            E6POS cartPos0;
            E6POS cartPos1 = new E6POS();
            E6POS cartPos2;
            E6POS cartPos3 = new E6POS();

            cartPos0 = new E6POS { X = 0, Y = 540, Z = 695, A = -90, B = 0, C = 180};
            cartPos0.STATUS = krcReadCartPos.STATUS;
            cartPos0.TURN = krcReadCartPos.TURN;
            cartPos1.CopyFrom(cartPos0);
            cartPos1.Z += 200;

            cartPos2 = new E6POS { X = 540, Y = 0, Z = 695, A = -180, B = 0, C = 180 };
            cartPos2.STATUS = krcReadCartPos.STATUS;
            cartPos2.TURN = krcReadCartPos.TURN;
            cartPos3.CopyFrom(cartPos2);
            cartPos3.Z += 200;

            Dictionary<string, object> targets = new Dictionary<string, object>();
            for(int i = 0; i < 10; i++)
            {
                targets.Add("AXIS_PTP_" + i, axisPos0);
                targets.Add("LIN_" + i, cartPos0);
                targets.Add("LIN_" + i + 1, cartPos1);
                targets.Add("AXIS_PTP_" + i + 1, axisPos1);
                targets.Add("LIN_" + i + 2, cartPos2);
                targets.Add("LIN_" + i + 3, cartPos3);
            }

            AddAnyMotionToList(targets);
            motionArray = true;
        }
        public bool CanSendMotionArray()
        {
            return cycleFlag && !motionArray;
        }


        private CustomCommand _jogTypeSwitchCmd;
        public CustomCommand JogTypeSwtichCmd
        {
            get
            {
                if(_jogTypeSwitchCmd == null)
                {
                    _jogTypeSwitchCmd = new CustomCommand(SwitchJogType, null);
                }
                return _jogTypeSwitchCmd;
            }
        }
        public void SwitchJogType(object o)
        {
            Button btn = (Button)o;
            if (btn.Content.Equals("Axis"))
            {
                jogType = 0;
                btn.Content = "Cartesian";
                JogButton1 = "A1+";
                JogButton2 = "A1-";
                JogButton3 = "A2+";
                JogButton4 = "A2-";
                JogButton5 = "A3+";
                JogButton6 = "A3-";
                JogButton7 = "A4+";
                JogButton8 = "A4-";
                JogButton9 = "A5+";
                JogButton10 = "A5-";
                JogButton11 = "A6+";
                JogButton12 = "A6-";
            }
            else
            {
                jogType = 1;
                btn.Content = "Axis";
                JogButton1 = "X+";
                JogButton2 = "X-";
                JogButton3 = "Y+";
                JogButton4 = "Y-";
                JogButton5 = "Z+";
                JogButton6 = "Z-";
                JogButton7 = "A+";
                JogButton8 = "A-";
                JogButton9 = "B+";
                JogButton10 = "B-";
                JogButton11 = "C+";
                JogButton12 = "C-";
            }
        }

        private string _jogButton1 = "A1+";
        public string JogButton1
        {
            get { return _jogButton1; }
            set
            {
                _jogButton1 = value;
                OnPropertyChanged();
            }
        }

        private string _jogButton2 = "A1-";
        public string JogButton2
        {
            get { return _jogButton2; }
            set
            {
                _jogButton2 = value;
                OnPropertyChanged();
            }
        }

        private string _jogButton3 = "A2+";
        public string JogButton3
        {
            get { return _jogButton3; }
            set
            {
                _jogButton3 = value;
                OnPropertyChanged();
            }
        }

        private string _jogButton4 = "A2-";
        public string JogButton4
        {
            get { return _jogButton4; }
            set
            {
                _jogButton4 = value;
                OnPropertyChanged();
            }
        }

        private string _jogButton5 = "A3+";
        public string JogButton5
        {
            get { return _jogButton5; }
            set
            {
                _jogButton5 = value;
                OnPropertyChanged();
            }
        }

        private string _jogButton6 = "A3-";
        public string JogButton6
        {
            get { return _jogButton6; }
            set
            {
                _jogButton6 = value;
                OnPropertyChanged();
            }
        }

        private string _jogButton7 = "A4+";
        public string JogButton7
        {
            get { return _jogButton7; }
            set
            {
                _jogButton7 = value;
                OnPropertyChanged();
            }
        }

        private string _jogButton8 = "A4-";
        public string JogButton8
        {
            get { return _jogButton8; }
            set
            {
                _jogButton8 = value;
                OnPropertyChanged();
            }
        }

        private string _jogButton9 = "A5+";
        public string JogButton9
        {
            get { return _jogButton9; }
            set
            {
                _jogButton9 = value;
                OnPropertyChanged();
            }
        }

        private string _jogButton10 = "A5-";
        public string JogButton10
        {
            get { return _jogButton10; }
            set
            {
                _jogButton10 = value;
                OnPropertyChanged();
            }
        }

        private string _jogButton11 = "A6+";
        public string JogButton11
        {
            get { return _jogButton11; }
            set
            {
                _jogButton11 = value;
                OnPropertyChanged();
            }
        }

        private string _jogButton12 = "A6-";
        public string JogButton12
        {
            get { return _jogButton12; }
            set
            {
                _jogButton12 = value;
                OnPropertyChanged();
            }
        }


        private IPAddress robotIP;
        private UdpClient sendSocket;
        private UdpClient recvSocket;
        private IPEndPoint sendEndPoint;
        private IPEndPoint recvEndPoint;
        private Thread cycleThread;
        private bool cycleFlag;
        private long cycleNr = 0;
        private const int sendPort = 1337;
        private const int recvPort = 2001;
        private const short axisGroupIndex = 1;
        private int recvTimeout = 0;

        private byte[] krc4Input = new byte[256];
        private byte[] krc4Output = new byte[256];

        private bool startRunning = false;
        private bool proActiveOld = false;
        private bool proActiveNew = false;
        private bool extStart = false;
        private bool resetStart = false;
        private bool confirmMsg = true;
        private bool moveEnable = true;
        private bool driveOff = true;
        private bool interruptPause = false;
        private bool continueResume = false;
        private bool ptpAxisAbs = false;
        private bool ptpCartAbs = false;
        private bool ptpCartRel = false;
        private bool linAbs = false;
        private bool linRel = false;
        private bool ptpArray = false;
        private bool linArray = false;
        private bool motionArray = false;
        private short jogType = 0;
        public bool X_A1_Plus = false;
        public bool Y_A2_Plus = false;
        public bool Z_A3_Plus = false;
        public bool A_A4_Plus = false;
        public bool B_A5_Plus = false;
        public bool C_A6_Plus = false;
        public bool X_A1_Minus = false;
        public bool Y_A2_Minus = false;
        public bool Z_A3_Minus = false;
        public bool A_A4_Minus = false;
        public bool B_A5_Minus = false;
        public bool C_A6_Minus = false;


        private KRC_READAXISGROUP krcReadAxisGroup = new KRC_READAXISGROUP();
        private KRC_WRITEAXISGROUP krcWriteAxisGroup = new KRC_WRITEAXISGROUP();
        private KRC_INITIALIZE krcInitilize = new KRC_INITIALIZE();
        private KRC_READACTUALAXISPOSITION krcReadAxisPos = new KRC_READACTUALAXISPOSITION();
        private KRC_READACTUALPOSITION krcReadCartPos = new KRC_READACTUALPOSITION();
        private KRC_DIAG krcDiag = new KRC_DIAG();
        private KRC_ERROR krcError = new KRC_ERROR();
        private KRC_AUTOMATICEXTERNAL krcAutoExt = new KRC_AUTOMATICEXTERNAL();
        private KRC_SETOVERRIDE krcSetOverride = new KRC_SETOVERRIDE();
        private KRC_INTERRUPT krcInterrupt = new KRC_INTERRUPT();
        private KRC_CONTINUE krcContinue = new KRC_CONTINUE();
        private KRC_JOG krcJog = new KRC_JOG();
        private COORDSYS jogCoordSys = new COORDSYS();
        private KRC_MOVEAXISABSOLUTE krcPtpAxisAbs = new KRC_MOVEAXISABSOLUTE();
        private KRC_MOVEDIRECTABSOLUTE krcPtpCartAbs = new KRC_MOVEDIRECTABSOLUTE();
        private KRC_MOVEDIRECTRELATIVE krcPtpCartRel = new KRC_MOVEDIRECTRELATIVE();
        private KRC_MOVELINEARABSOLUTE krcLinAbs = new KRC_MOVELINEARABSOLUTE();
        private KRC_MOVELINEARRELATIVE krcLinRel = new KRC_MOVELINEARRELATIVE();
        private List<KRC_MOVEAXISABSOLUTE> ptpMotionList = new List<KRC_MOVEAXISABSOLUTE>();
        private List<KRC_MOVELINEARABSOLUTE> linMotionList = new List<KRC_MOVELINEARABSOLUTE>();
        private List<MotionFunctionBlock> fbMotionList = new List<MotionFunctionBlock>();

        private void Cycle()
        {
            try
            {
                if(recvSocket == null)
                {
                    recvEndPoint = new IPEndPoint(IPAddress.Any, recvPort);
                    recvSocket = new UdpClient(recvEndPoint);
                    recvSocket.Client.ReceiveTimeout = 100;
                }

                while (cycleFlag)
                {
                    ReadAxisGroup();

                    krcInitilize.AXISGROUPIDX = axisGroupIndex;
                    krcInitilize.OnCycle();

                    if (krcInitilize.ERROR)
                    {
                        Log("Error by KRC_INITIALIZE: " + krcInitilize.ERRORID);
                        return;
                    }

                    krcReadAxisPos.AXISGROUPIDX = axisGroupIndex;
                    krcReadAxisPos.OnCycle();

                    krcReadCartPos.AXISGROUPIDX = axisGroupIndex;
                    krcReadCartPos.OnCycle();

                    krcDiag.AXISGROUPIDX = axisGroupIndex;
                    krcDiag.OnCycle();

                    StateStr = GetStateMsg();

                    krcError.AXISGROUPIDX = axisGroupIndex;
                    krcError.MESSAGERESET = confirmMsg;
                    krcError.OnCycle();

                    ErrorID = krcError.ERRORID.ToString();

                    krcAutoExt.AXISGROUPIDX = axisGroupIndex;
                    krcAutoExt.EXT_START = extStart;
                    krcAutoExt.RESET = resetStart;
                    krcAutoExt.MOVE_ENABLE = moveEnable;
                    krcAutoExt.DRIVES_OFF = driveOff;
                    krcAutoExt.DRIVES_ON = false;
                    krcAutoExt.ENABLE_T1 = true;
                    krcAutoExt.ENABLE_T2 = true;
                    krcAutoExt.ENABLE_AUT = true;
                    krcAutoExt.ENABLE_EXT = true;
                    
                    krcAutoExt.OnCycle();

                    if (krcAutoExt.PRO_ACT)
                    {
                        confirmMsg = false;
                        proActiveNew = true;
                    }
                    else
                    {
                        proActiveNew = false;
                    }

                    if (proActiveOld != proActiveNew && startRunning)
                    {
                        proActiveOld = proActiveNew;
                        RefreshButtonStatus();
                    }

                    krcSetOverride.AXISGROUPIDX = axisGroupIndex;
                    krcSetOverride.OVERRIDE = (short)ProgramOverride;
                    krcSetOverride.OnCycle();

                    krcInterrupt.AXISGROUPIDX = axisGroupIndex;
                    krcInterrupt.EXECUTE = interruptPause;
                    krcInterrupt.FAST = true;
                    krcInterrupt.OnCycle();

                    krcContinue.AXISGROUPIDX = axisGroupIndex;
                    krcContinue.ENABLE = continueResume;
                    krcContinue.OnCycle();

                    if (continueResume && !krcInterrupt.BRAKEACTIVE)
                    {
                        continueResume = false;
                    }

                    krcPtpAxisAbs.AXISGROUPIDX = axisGroupIndex;
                    krcPtpAxisAbs.EXECUTECMD = ptpAxisAbs;
                    krcPtpAxisAbs.AXISPOSITION = E6AXIS_T.ToE6Axis();
                    krcPtpAxisAbs.VELOCITY = 50;
                    krcPtpAxisAbs.ACCELERATION = 50;
                    krcPtpAxisAbs.BUFFERMODE = 2;
                    krcPtpAxisAbs.OnCycle();

                    if (krcPtpAxisAbs.DONE || krcPtpAxisAbs.ERROR || krcPtpAxisAbs.ABORTED)
                    {
                        ptpAxisAbs = false;
                        RefreshButtonStatus();
                    }

                    krcPtpCartAbs.AXISGROUPIDX = axisGroupIndex;
                    krcPtpCartAbs.EXECUTECMD = ptpCartAbs;
                    krcPtpCartAbs.POSITION = E6POS_PTP_ABS.ToE6Pos();
                    krcPtpCartAbs.VELOCITY = 50;
                    krcPtpCartAbs.ACCELERATION = 50;
                    krcPtpCartAbs.BUFFERMODE = 2;
                    krcPtpCartAbs.OnCycle();

                    if (krcPtpCartAbs.DONE || krcPtpCartAbs.ERROR || krcPtpCartAbs.ABORTED)
                    {
                        ptpCartAbs = false;
                        RefreshButtonStatus();
                    }

                    krcPtpCartRel.AXISGROUPIDX = axisGroupIndex;
                    krcPtpCartRel.EXECUTECMD = ptpCartRel;
                    krcPtpCartRel.POSITION = E6POS_PTP_REL.ToE6Pos();
                    krcPtpCartRel.VELOCITY = 50;
                    krcPtpCartRel.ACCELERATION = 50;
                    krcPtpCartRel.BUFFERMODE = 2;
                    krcPtpCartRel.OnCycle();

                    if (krcPtpCartRel.DONE || krcPtpCartRel.ERROR || krcPtpCartRel.ABORTED)
                    {
                        ptpCartRel = false;
                        RefreshButtonStatus();
                    }

                    krcLinAbs.AXISGROUPIDX = axisGroupIndex;
                    krcLinAbs.EXECUTECMD = linAbs;
                    krcLinAbs.POSITION = E6POS_LIN_ABS.ToE6Pos();
                    krcLinAbs.VELOCITY = 50;
                    krcLinAbs.ACCELERATION = 50;
                    krcLinAbs.BUFFERMODE = 2;
                    krcLinAbs.OnCycle();

                    if (krcLinAbs.DONE || krcLinAbs.ERROR || krcLinAbs.ABORTED)
                    {
                        linAbs = false;
                        RefreshButtonStatus();
                    }

                    krcLinRel.AXISGROUPIDX = axisGroupIndex;
                    krcLinRel.EXECUTECMD = linRel;
                    krcLinRel.POSITION = E6POS_LIN_REL.ToE6Pos();
                    krcLinRel.VELOCITY = 50;
                    krcLinRel.ACCELERATION = 50;
                    krcLinRel.BUFFERMODE = 2;
                    krcLinRel.OnCycle();

                    if (krcLinRel.DONE || krcLinRel.ERROR || krcLinRel.ABORTED)
                    {
                        linRel = false;
                        RefreshButtonStatus();
                    }

                    krcJog.AXISGROUPIDX = axisGroupIndex;
                    krcJog.MOVETYPE = jogType;
                    krcJog.VELOCITY = 50;
                    krcJog.ACCELERATION = 50;
                    krcJog.COORDINATESYSTEM = jogCoordSys;
                    krcJog.INCREMENT = 0;
                    krcJog.A1_X_P = X_A1_Plus;
                    krcJog.A1_X_M = X_A1_Minus;
                    krcJog.A2_Y_P = Y_A2_Plus;
                    krcJog.A2_Y_M = Y_A2_Minus;
                    krcJog.A3_Z_P = Z_A3_Plus;
                    krcJog.A3_Z_M = Z_A3_Minus;
                    krcJog.A4_A_P = A_A4_Plus;
                    krcJog.A4_A_M = A_A4_Minus;
                    krcJog.A5_B_P = B_A5_Plus;
                    krcJog.A5_B_M = B_A5_Minus;
                    krcJog.A6_C_P = C_A6_Plus;
                    krcJog.A6_C_M = C_A6_Minus;
                    krcJog.OnCycle();

                    lock(ptpMotionList)
                    {
                        for (int i = 0; i < ptpMotionList.Count; i++)
                        {
                            if (i == 0)
                            {
                                ptpMotionList[i].EXECUTECMD = ptpArray;
                            }
                            else
                            {
                                ptpMotionList[i].EXECUTECMD = ptpMotionList[i - 1].BUSY || ptpMotionList[i - 1].ACTIVE || ptpMotionList[i - 1].DONE;
                            }

                            if (i != ptpMotionList.Count - 1)
                            {
                                ptpMotionList[i].APPROXIMATE.PTP_MODE = 1;
                                ptpMotionList[i].APPROXIMATE.CPTP = 10;
                            }

                            ptpMotionList[i].OnCycle();

                            if(ptpMotionList[i].ABORTED || ptpMotionList[i].ERROR)
                            {
                                ptpArray = false;
                            }
                        }

                        if (ptpMotionList.Count > 0 && ptpMotionList[ptpMotionList.Count - 1].DONE)
                        {
                            ptpArray = false;
                            RefreshButtonStatus();
                        }
                    }

                    lock(linMotionList)
                    {
                        for(int i = 0; i < linMotionList.Count; i++)
                        {
                            if(i == 0)
                            {
                                linMotionList[i].EXECUTECMD = linArray;
                            }
                            else
                            {
                                linMotionList[i].EXECUTECMD = linMotionList[i - 1].BUSY || linMotionList[i - 1].ACTIVE || linMotionList[i - 1].DONE;
                            }

                            if(i != linMotionList.Count - 1)
                            {
                                linMotionList[i].APPROXIMATE.CP_MODE = 1;
                                linMotionList[i].APPROXIMATE.CDIS = 100;
                            }
                            linMotionList[i].OnCycle();

                            if(linMotionList[i].ABORTED || linMotionList[i].ERROR)
                            {
                                linArray = false;
                            }
                        }

                        if (linMotionList.Count > 0 && linMotionList[linMotionList.Count - 1].DONE)
                        {
                            linArray = false;
                            RefreshButtonStatus();
                        }
                    }

                    lock(fbMotionList)
                    {
                        for(int i = 0; i < fbMotionList.Count; i++)
                        {
                            if(i == 0)
                            {
                                fbMotionList[i].SetExecuteCmd(motionArray);
                            }
                            else
                            {
                                fbMotionList[i].SetExecuteCmd(fbMotionList[i - 1].GetBusyStatus() || fbMotionList[i - 1].GetActiveStatus() || fbMotionList[i - 1].GetDoneStatus());
                            }

                            fbMotionList[i].OnCycle();

                            if(fbMotionList[i].GetAbortedStatus() || fbMotionList[i].GetErrorStatus())
                            {
                                motionArray = false;
                            }
                        }

                        if(fbMotionList.Count > 0 && fbMotionList[fbMotionList.Count - 1].GetDoneStatus())
                        {
                            motionArray = false;
                            RefreshButtonStatus();
                        }
                    }
                    
                    WriteAxisGroup();

                    Thread.Sleep(5);
                }
            }
            catch (Exception e)
            {
                cycleFlag = false;
                recvSocket.Close();
                Log("Cycle Exception: " + e.Message);
            }

        }

        private void ReadAxisGroup()
        {
            byte[] buffer = null;

            try
            {
                if (recvSocket.Available > 0)
                {
                    while(recvSocket.Available > 0)
                    {
                        buffer = recvSocket.Receive(ref recvEndPoint);
                        recvTimeout = 0;
                    }
                }
                else
                {
                    cycleNr = 0;
                    recvTimeout++;
                    if (recvTimeout > 500)
                    {
                        Log("Don't receive data from robot!");
                        recvTimeout = 0;
                        cycleFlag = false;
                        RefreshButtonStatus();
                    }
                }
            }
            catch (SocketException e)
            {
                recvSocket.Close();
                Log("Socket exception in readAxisGroup with the message: " + e.Message);
            }

            if (buffer != null && buffer.Length >= 246)
            {
                krc4Input = buffer;
            }

            krcReadAxisGroup.AXISGROUPIDX = axisGroupIndex;
            krcReadAxisGroup.KRC4_INPUT = krc4Input;
            krcReadAxisGroup.OnCycle();

            if (krcReadAxisGroup.ERROR)
            {
                Log("Error by Read Axis Group function block: " + krcReadAxisGroup.ERRORID);
                return;
            }
        }

        private void WriteAxisGroup()
        {
            krcWriteAxisGroup.AXISGROUPIDX = axisGroupIndex;
            krcWriteAxisGroup.KRC4_OUTPUT = krc4Output;
            krcWriteAxisGroup.OnCycle();
            sendSocket.Send(krc4Output, krc4Output.Length);
        }

        private string GetStateMsg()
        {
            string stateStr = "";
            stateStr = stateStr + "Online : " +
                    GLOBAL.KRC_AXISGROUPREFARR[axisGroupIndex].ONLINE.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Initialized : " +
                    GLOBAL.KRC_AXISGROUPREFARR[axisGroupIndex].INITIALIZED.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "PLC Version : " +
                    GLOBAL.KRC_AXISGROUPREFARR[axisGroupIndex].PLC_MAJOR.ToString(CultureInfo.InvariantCulture);
            stateStr = stateStr + "." +
                    GLOBAL.KRC_AXISGROUPREFARR[axisGroupIndex].PLC_MINOR.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Last OrderID : " +
                    GLOBAL.KRC_AXISGROUPREFARR[axisGroupIndex].LASTORDERID.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Read Done : " +
                    GLOBAL.KRC_AXISGROUPREFARR[axisGroupIndex].READDONE.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Error : " +
                    krcDiag.ERROR.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Int_Error ID : " +
                    krcDiag.ERRORID.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Int_FBerror ID : " +
                    krcDiag.ERRORID_PLC.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "KRC_PLC error ID : " +
                    krcDiag.ERRORID_PCOS.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "KRC_ROB error ID : " +
                    krcDiag.ERRORID_RI.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "KRC_SUB error ID : " +
                    krcDiag.ERRORID_SI.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            //stateStr = stateStr + "Recv.  Timeout[ms] : " +
            //        GLOBAL.KRC_AXISGROUPREFARR[axisGroupIndex].HEARTBEATTO.ToString(CultureInfo.InvariantCulture) +
            //        Environment.NewLine;
            stateStr = stateStr + "Read AxisGroupInit : " +
                    GLOBAL.KRC_AXISGROUPREFARR[axisGroupIndex].READAXISGROUPINIT.ToString(CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Axis Position A1 : " +
                    krcReadAxisPos.A1.ToString("0.00", CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Axis Position A2 : " +
                    krcReadAxisPos.A2.ToString("0.00", CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Axis Position A3 : " +
                    krcReadAxisPos.A3.ToString("0.00", CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Axis Position A4 : " +
                    krcReadAxisPos.A4.ToString("0.00", CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Axis Position A5 : " +
                    krcReadAxisPos.A5.ToString("0.00", CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Axis Position A6 : " +
                    krcReadAxisPos.A6.ToString("0.00", CultureInfo.InvariantCulture) +
                    Environment.NewLine;
            stateStr = stateStr + "Current Tool : " + krcReadCartPos.TOOL.ToString("0", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Current Base : " + krcReadCartPos.BASE.ToString("0", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Current IPOMode : " + krcReadCartPos.IPOMODE.ToString("0", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos X : " + krcReadCartPos.POSITION.X.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos Y : " + krcReadCartPos.POSITION.Y.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos Z : " + krcReadCartPos.POSITION.Z.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos A : " + krcReadCartPos.POSITION.A.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos B : " + krcReadCartPos.POSITION.B.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos C : " + krcReadCartPos.POSITION.C.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos E1 : " + krcReadCartPos.POSITION.E1.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos E2 : " + krcReadCartPos.POSITION.E2.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos E3 : " + krcReadCartPos.POSITION.E3.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos E4 : " + krcReadCartPos.POSITION.E4.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos E5 : " + krcReadCartPos.POSITION.E5.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos E6 : " + krcReadCartPos.POSITION.E6.ToString("0.00", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos S : " + krcReadCartPos.POSITION.STATUS.ToString("0", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Cartesian Pos T : " + krcReadCartPos.POSITION.TURN.ToString("0", CultureInfo.InvariantCulture) + Environment.NewLine;
            stateStr = stateStr + "Life Counter (" + cycleNr++ + ")";

            return stateStr;
        }

        private bool IsInEXTMode()
        {
            for (int i = 0; i < 40; i++)
            {
                if (krcAutoExt.EXT && cycleNr > 0)
                {
                    break;
                }
                Thread.Sleep(50);
            }

            return krcAutoExt.EXT;
        }

        private bool SetDriveOn()
        {
            for (int i = 0; i < 40; i++)
            {
                driveOff = true;
                if (krcAutoExt.PERI_RDY)
                {
                    break;
                }
                Thread.Sleep(50);
            }

            return krcAutoExt.PERI_RDY;
        }

        private bool SetMotorOn()
        {
            for (int i = 0; i < 40; i++)
            {
                moveEnable = true;
                if (krcAutoExt.RC_RDY1)
                {
                    break;
                }
                Thread.Sleep(50);
            }
            return krcAutoExt.RC_RDY1;
        }

        private bool ResetError()
        {
            for (int i = 0; i < 40; i++)
            {
                confirmMsg = true;
                if (!krcError.ERROR)
                {
                    break;
                }
                Thread.Sleep(50);
            }
            return !krcError.ERROR;
        }

        private bool IsProgramRunning()
        {
            for (int i = 0; i < 40; i++)
            {
                if (krcAutoExt.PRO_ACT)
                {
                    break;
                }
                Thread.Sleep(50);
            }

            return krcAutoExt.PRO_ACT;
        }

        private void Log(string msg)
        {
            NewLogMessage = msg;
        }

        private void AddPtpMotionToList(List<E6AXIS> axisPosList)
        {
            KRC_MOVEAXISABSOLUTE ptpAxisMotion;

            lock (ptpMotionList)
            {
                ptpMotionList.Clear();

                for (int i = 0; i < axisPosList.Count; i++)
                {
                    ptpAxisMotion = new KRC_MOVEAXISABSOLUTE();
                    ptpAxisMotion.AXISGROUPIDX = axisGroupIndex;
                    ptpAxisMotion.AXISPOSITION = axisPosList[i];
                    ptpAxisMotion.VELOCITY = 50;
                    ptpAxisMotion.ACCELERATION = 50;
                    ptpAxisMotion.BUFFERMODE = 2;
                    ptpAxisMotion.SPLINEMODE = false;

                    ptpMotionList.Add(ptpAxisMotion);
                }
            }
        }

        

        private void AddLinMotionToList(List<E6POS> cartPosList)
        {
            KRC_MOVELINEARABSOLUTE linPosMotion;

            lock(linMotionList)
            {
                linMotionList.Clear();

                for(int i = 0; i < cartPosList.Count; i++)
                {
                    linPosMotion = new KRC_MOVELINEARABSOLUTE();
                    linPosMotion.AXISGROUPIDX = axisGroupIndex;
                    linPosMotion.POSITION = cartPosList[i];
                    linPosMotion.VELOCITY = 50;
                    linPosMotion.ACCELERATION = 50;
                    linPosMotion.BUFFERMODE = 2;
                    linPosMotion.SPLINEMODE = false;

                    linMotionList.Add(linPosMotion);
                }
            }
        }

        private void AddAnyMotionToList(Dictionary<string, object> targets)
        {
            lock (fbMotionList)
            {
                fbMotionList.Clear();

                foreach (string key in targets.Keys)
                {
                    if(key.Contains("AXIS_PTP"))
                    {
                        PTP_Axis_FunctionBlock motion = new PTP_Axis_FunctionBlock();
                        motion.AXISGROUPIDX = axisGroupIndex;
                        motion.AXISPOSITION = (E6AXIS)targets[key];
                        motion.VELOCITY = 50;
                        motion.ACCELERATION = 50;
                        motion.APPROXIMATE.PTP_MODE = 1;
                        motion.APPROXIMATE.CPTP = 20;
                        motion.BUFFERMODE = 2;
                        motion.SPLINEMODE = false;
                        fbMotionList.Add(motion);
                    }

                    if(key.Contains("LIN"))
                    {
                        LIN_FunctionBlock motion = new LIN_FunctionBlock();
                        motion.AXISGROUPIDX = axisGroupIndex;
                        motion.POSITION = (E6POS)targets[key];
                        motion.VELOCITY = 50;
                        motion.ACCELERATION = 50;
                        motion.APPROXIMATE.CP_MODE = 1;
                        motion.APPROXIMATE.CDIS = 200;
                        motion.BUFFERMODE = 2;
                        motion.SPLINEMODE = false;
                        fbMotionList.Add(motion);
                    }
                }
            }
        }

        private void RefreshButtonStatus()
        {
            Application.Current.Dispatcher.Invoke(() => { CommandManager.InvalidateRequerySuggested(); });
        }

    }
}
