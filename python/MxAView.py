# MxAView.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QGroupBox, QPushButton, QLabel, QLineEdit, 
    QTextEdit, QSlider, QTabWidget, QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from MxAViewModel import MxAViewModel, robot_data_queue, E6AXIS, E6POS

class AxisInputWidget(QWidget):
    """Axis input widget that binds to E6AXIS data class"""
    def __init__(self, label_prefix="Axis", parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create input fields for all 6 axes
        self.inputs = {}
        axis_names = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
        
        for axis_name in axis_names:
            row = QHBoxLayout()
            label = QLabel(f"{axis_name}:")
            label.setFixedWidth(35)
            input_field = QLineEdit("0.0")
            input_field.setFixedWidth(80)
            input_field.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.inputs[axis_name] = input_field
            
            row.addWidget(label)
            row.addWidget(input_field)
            self.layout.addLayout(row)
    
    def to_e6axis(self) -> E6AXIS:
        """Convert input values to E6AXIS data class"""
        try:
            return E6AXIS(
                A1=float(self.inputs['A1'].text()),
                A2=float(self.inputs['A2'].text()),
                A3=float(self.inputs['A3'].text()),
                A4=float(self.inputs['A4'].text()),
                A5=float(self.inputs['A5'].text()),
                A6=float(self.inputs['A6'].text())
            )
        except ValueError:
            return E6AXIS()
    
    def from_e6axis(self, axis_data: E6AXIS):
        """Update input fields from E6AXIS data class"""
        self.inputs['A1'].setText(f"{axis_data.A1:.2f}")
        self.inputs['A2'].setText(f"{axis_data.A2:.2f}")
        self.inputs['A3'].setText(f"{axis_data.A3:.2f}")
        self.inputs['A4'].setText(f"{axis_data.A4:.2f}")
        self.inputs['A5'].setText(f"{axis_data.A5:.2f}")
        self.inputs['A6'].setText(f"{axis_data.A6:.2f}")

class CartesianInputWidget(QWidget):
    """Cartesian input widget that binds to E6POS data class"""
    def __init__(self, label_prefix="", parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create input fields for cartesian coordinates
        self.inputs = {}
        coord_names = ['X', 'Y', 'Z', 'A', 'B', 'C']
        
        for coord_name in coord_names:
            row = QHBoxLayout()
            label = QLabel(f"{coord_name}:")
            label.setFixedWidth(25)
            input_field = QLineEdit("0.0")
            input_field.setFixedWidth(80)
            input_field.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.inputs[coord_name] = input_field
            
            row.addWidget(label)
            row.addWidget(input_field)
            self.layout.addLayout(row)
    
    def to_e6pos(self) -> E6POS:
        """Convert input values to E6POS data class"""
        try:
            return E6POS(
                X=float(self.inputs['X'].text()),
                Y=float(self.inputs['Y'].text()),
                Z=float(self.inputs['Z'].text()),
                A=float(self.inputs['A'].text()),
                B=float(self.inputs['B'].text()),
                C=float(self.inputs['C'].text())
            )
        except ValueError:
            return E6POS()
    
    def from_e6pos(self, pos_data: E6POS):
        """Update input fields from E6POS data class"""
        self.inputs['X'].setText(f"{pos_data.X:.2f}")
        self.inputs['Y'].setText(f"{pos_data.Y:.2f}")
        self.inputs['Z'].setText(f"{pos_data.Z:.2f}")
        self.inputs['A'].setText(f"{pos_data.A:.2f}")
        self.inputs['B'].setText(f"{pos_data.B:.2f}")
        self.inputs['C'].setText(f"{pos_data.C:.2f}")

class MxAView(QMainWindow):
    """PyQt6 style interface view with E6AXIS/E6POS data binding"""
    def __init__(self, view_model: MxAViewModel):
        super().__init__()
        self.vm = view_model
        # 存储当前JOG模式标签，用于按键映射
        self.current_jog_labels = [
            ("A1+", "A1-"),
            ("A2+", "A2-"),
            ("A3+", "A3-"),
            ("A4+", "A4-"),
            ("A5+", "A5-"),
            ("A6+", "A6-")
        ]
        self.init_ui()
        self.setup_connections()
        
        # Timer for display updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(100)  # Update every 100ms

    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("MxAutomation V6.0 Example Program")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set style sheet
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
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Top connection control area
        top_layout = self.create_top_control_panel()
        main_layout.addLayout(top_layout)
        
        # Central content area
        center_layout = self.create_center_content()
        main_layout.addLayout(center_layout)
        
        # Bottom log area
        log_layout = self.create_log_panel()
        main_layout.addLayout(log_layout)

    def create_top_control_panel(self):
        """Create top control panel"""
        layout = QHBoxLayout()
        
        # Robot IP input
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("Robot IP:"))
        self.ip_input = QLineEdit(self.vm.robot_ip)
        self.ip_input.setMaximumWidth(150)
        ip_layout.addWidget(self.ip_input)
        layout.addLayout(ip_layout)
        
        # Connect/Disconnect buttons
        self.connect_btn = QPushButton("Connect")
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.setEnabled(False)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.connect_btn)
        btn_layout.addWidget(self.disconnect_btn)
        layout.addLayout(btn_layout)
        
        # Override control
        override_layout = QHBoxLayout()
        override_layout.addWidget(QLabel("Override:"))
        self.override_slider = QSlider(Qt.Orientation.Horizontal)
        self.override_slider.setRange(0, 100)
        self.override_slider.setValue(self.vm.program_override)
        self.override_label = QLabel(f"{self.vm.program_override}%")
        self.override_label.setMinimumWidth(40)
        
        override_layout.addWidget(self.override_slider)
        override_layout.addWidget(self.override_label)
        layout.addLayout(override_layout)
        
        # Add stretchable space
        layout.addStretch()
        
        return layout

    def create_center_content(self):
        """Create central content area"""
        layout = QHBoxLayout()
        
        # Left panel - Controls and movement commands
        left_panel = self.create_left_panel()
        left_container = QWidget()
        left_container.setLayout(left_panel)
        left_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        layout.addWidget(left_container)
        
        # Right panel - Status information
        right_panel = self.create_right_panel()
        right_container = QWidget()
        right_container.setLayout(right_panel)
        right_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(right_container)
        
        return layout

    def create_left_panel(self):
        """Create left panel with E6AXIS/E6POS binding"""
        layout = QVBoxLayout()
        
        # Control button group
        control_group = QGroupBox("Control")
        control_layout = QHBoxLayout(control_group)
        
        self.pause_btn = QPushButton("Pause")
        self.resume_btn = QPushButton("Resume")
        self.reset_btn = QPushButton("Reset")
        self.interrupt_btn = QPushButton("Interrupt")
        self.continue_btn = QPushButton("Continue")
        self.confirm_error_btn = QPushButton("Confirm Error")
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.resume_btn)
        control_layout.addWidget(self.reset_btn)
        control_layout.addWidget(self.interrupt_btn)
        control_layout.addWidget(self.continue_btn)
        control_layout.addWidget(self.confirm_error_btn)
        
        layout.addWidget(control_group)
        
        # Movement command button group with E6AXIS/E6POS binding
        move_group = QGroupBox("Movement Commands")
        move_layout = QVBoxLayout(move_group)
        
        # Create tab widget for movement inputs
        self.move_tab = QTabWidget()

        # Tab 1: PTP Axis
        ptp_axis_widget = QWidget()
        ptp_axis_layout = QHBoxLayout(ptp_axis_widget)
        
        ptp_axis_abs_group = QGroupBox("Absolute")
        ptp_axis_abs_layout = QVBoxLayout(ptp_axis_abs_group)
        self.ptp_axis_abs_input = AxisInputWidget()
        self.send_ptp_axis_abs_btn = QPushButton("Send PTP Axis Abs")
        ptp_axis_abs_layout.addWidget(self.ptp_axis_abs_input)
        ptp_axis_abs_layout.addWidget(self.send_ptp_axis_abs_btn)
        ptp_axis_rel_group = QGroupBox("Relative")
        ptp_axis_rel_layout = QVBoxLayout(ptp_axis_rel_group)
        self.ptp_axis_rel_input = AxisInputWidget()
        self.send_ptp_axis_rel_btn = QPushButton("Send PTP Axis Rel")
        ptp_axis_rel_layout.addWidget(self.ptp_axis_rel_input)
        ptp_axis_rel_layout.addWidget(self.send_ptp_axis_rel_btn)
        ptp_axis_layout.addWidget(ptp_axis_abs_group)
        ptp_axis_layout.addWidget(ptp_axis_rel_group)
        self.move_tab.addTab(ptp_axis_widget, "PTP Axis")
        
        # Tab 2: PTP Position
        ptp_pos_widget = QWidget()
        ptp_pos_layout = QHBoxLayout(ptp_pos_widget)

        ptp_pos_abs_group = QGroupBox("Absolute")
        ptp_pos_abs_layout = QVBoxLayout(ptp_pos_abs_group)
        self.ptp_pos_abs_input = CartesianInputWidget()
        self.send_ptp_pos_abs_btn = QPushButton("Send PTP Pos Abs")
        ptp_pos_abs_layout.addWidget(self.ptp_pos_abs_input)
        ptp_pos_abs_layout.addWidget(self.send_ptp_pos_abs_btn)

        ptp_pos_rel_group = QGroupBox("Relative")
        ptp_pos_rel_layout = QVBoxLayout(ptp_pos_rel_group)
        self.ptp_pos_rel_input = CartesianInputWidget()
        self.send_ptp_pos_rel_btn = QPushButton("Send PTP Pos Rel")
        ptp_pos_rel_layout.addWidget(self.ptp_pos_rel_input)
        ptp_pos_rel_layout.addWidget(self.send_ptp_pos_rel_btn)
        ptp_pos_layout.addWidget(ptp_pos_abs_group)
        ptp_pos_layout.addWidget(ptp_pos_rel_group)
        self.move_tab.addTab(ptp_pos_widget, "PTP Position")
        
        # Tab 3: LIN Position
        lin_pos_widget = QWidget()
        lin_pos_layout = QHBoxLayout(lin_pos_widget)

        lin_pos_abs_group = QGroupBox("Absolute")
        lin_pos_abs_layout = QVBoxLayout(lin_pos_abs_group)
        self.lin_pos_abs_input = CartesianInputWidget()
        self.send_lin_pos_abs_btn = QPushButton("Send LIN Pos Abs")
        lin_pos_abs_layout.addWidget(self.lin_pos_abs_input)
        lin_pos_abs_layout.addWidget(self.send_lin_pos_abs_btn)

        lin_pos_rel_group = QGroupBox("Relative")
        lin_pos_rel_layout = QVBoxLayout(lin_pos_rel_group)
        self.lin_pos_rel_input = CartesianInputWidget()
        self.send_lin_pos_rel_btn = QPushButton("Send LIN Pos Rel")
        lin_pos_rel_layout.addWidget(self.lin_pos_rel_input)
        lin_pos_rel_layout.addWidget(self.send_lin_pos_rel_btn)
        
        lin_pos_layout.addWidget(lin_pos_abs_group)
        lin_pos_layout.addWidget(lin_pos_rel_group)
        self.move_tab.addTab(lin_pos_widget, "LIN Position")
        move_layout.addWidget(self.move_tab)
        
        layout.addWidget(move_group)
        
        # Jog control button group
        jog_group = QGroupBox("Jog Control")
        jog_layout = QGridLayout(jog_group)
        
        self.jog_buttons = {}
        self.jog_buttons_list = []  # 存储按钮引用用于更新文本
        
        for i, (pos_label, neg_label) in enumerate(self.current_jog_labels):
            pos_btn = QPushButton(pos_label)
            neg_btn = QPushButton(neg_label)
            
            pos_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            neg_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            
            # 存储按钮引用，使用索引而不是标签名
            self.jog_buttons[f"pos_{i}"] = pos_btn
            self.jog_buttons[f"neg_{i}"] = neg_btn
            # 同时也存储到列表中方便更新
            self.jog_buttons_list.append((pos_btn, neg_btn))
            
            # 绑定 key down 和 key up 事件
            pos_btn.pressed.connect(lambda idx=i, sign=1: self.jog_button_pressed(idx, sign))
            pos_btn.released.connect(lambda idx=i, sign=1: self.jog_button_released(idx, sign))
            neg_btn.pressed.connect(lambda idx=i, sign=-1: self.jog_button_pressed(idx, sign))
            neg_btn.released.connect(lambda idx=i, sign=-1: self.jog_button_released(idx, sign))
            
            jog_layout.addWidget(pos_btn, i, 0)
            jog_layout.addWidget(neg_btn, i, 1)
        
        # Add jog mode toggle button
        self.jog_mode_toggle_btn = QPushButton("Switch to Cartesian Mode")
        self.jog_mode_toggle_btn.setStyleSheet("padding: 8px; font-weight: bold;")
        jog_layout.addWidget(self.jog_mode_toggle_btn, len(self.current_jog_labels), 0, 1, 2)
        self.jog_mode_toggle_btn.clicked.connect(self.toggle_jog_mode)
        
        layout.addWidget(jog_group)
        
        # Add stretchable space
        layout.addStretch()
        
        return layout

    def create_right_panel(self):
        """Create right panel"""
        layout = QVBoxLayout()
        
        # Status information group
        status_group = QGroupBox("Status Information")
        status_layout = QGridLayout(status_group)
        
        # Error ID
        status_layout.addWidget(QLabel("Error ID:"), 0, 0)
        self.error_id_label = QLabel(str(self.vm.error_id))
        self.error_id_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
        status_layout.addWidget(self.error_id_label, 0, 1)
        
        # Running status
        status_layout.addWidget(QLabel("Running Status:"), 1, 0)
        self.running_status_label = QLabel("Stopped")
        self.running_status_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
        status_layout.addWidget(self.running_status_label, 1, 1)
        
        # Loop count
        status_layout.addWidget(QLabel("Loop Count:"), 2, 0)
        self.loop_count_label = QLabel("0")
        status_layout.addWidget(self.loop_count_label, 2, 1)
        
        # Test step
        status_layout.addWidget(QLabel("Test Step:"), 3, 0)
        self.test_step_label = QLabel("0")
        status_layout.addWidget(self.test_step_label, 3, 1)
        
        layout.addWidget(status_group)
        
        # Status indicator lights group
        indicator_group = QGroupBox("System Status")
        indicator_layout = QGridLayout(indicator_group)
        
        # Create status indicator frames (lights)
        self.error_status_light = QFrame()
        self.error_status_light.setFixedSize(20, 20)
        self.error_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        indicator_layout.addWidget(QLabel("Error:"), 0, 0)
        indicator_layout.addWidget(self.error_status_light, 0, 1)
        
        self.comm_status_light = QFrame()
        self.comm_status_light.setFixedSize(20, 20)
        self.comm_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        indicator_layout.addWidget(QLabel("Comm:"), 0, 2)
        indicator_layout.addWidget(self.comm_status_light, 0, 3)
        
        self.drive_status_light = QFrame()
        self.drive_status_light.setFixedSize(20, 20)
        self.drive_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        indicator_layout.addWidget(QLabel("Drives:"), 1, 0)
        indicator_layout.addWidget(self.drive_status_light, 1, 1)
        
        self.program_status_light = QFrame()
        self.program_status_light.setFixedSize(20, 20)
        self.program_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        indicator_layout.addWidget(QLabel("Pro Act:"), 1, 2)
        indicator_layout.addWidget(self.program_status_light, 1, 3)
        
        self.ext_status_light = QFrame()
        self.ext_status_light.setFixedSize(20, 20)
        self.ext_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        indicator_layout.addWidget(QLabel("Ext Mode:"), 2, 0)
        indicator_layout.addWidget(self.ext_status_light, 2, 1)
        
        self.movement_status_light = QFrame()
        self.movement_status_light.setFixedSize(20, 20)
        self.movement_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        indicator_layout.addWidget(QLabel("Movement:"), 2, 2)
        indicator_layout.addWidget(self.movement_status_light, 2, 3)
        
        layout.addWidget(indicator_group)
        
        # Real-time data display
        real_time_group = QGroupBox("Real-Time Data")
        real_time_layout = QVBoxLayout(real_time_group)
        
        # Axis position display (E6AXIS binding)
        axis_group = QGroupBox("Axis Position")
        axis_layout = QGridLayout(axis_group)
        
        self.axis_labels = []
        self.axis_values = []
        
        axes = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
        for i, axis in enumerate(axes):
            label = QLabel(f"{axis}:")
            value_label = QLabel("--")
            value_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px; font-family: monospace;")
            self.axis_labels.append(label)
            self.axis_values.append(value_label)
            
            row = i // 3
            col = (i % 3) * 2
            axis_layout.addWidget(label, row, col)
            axis_layout.addWidget(value_label, row, col + 1)
        
        real_time_layout.addWidget(axis_group)
        
        # Cartesian position display (E6POS binding)
        cart_group = QGroupBox("Cartesian Position")
        cart_layout = QGridLayout(cart_group)
        
        self.cart_labels = []
        self.cart_values = []
        
        coords = ['X', 'Y', 'Z', 'A', 'B', 'C']
        for i, coord in enumerate(coords):
            label = QLabel(f"{coord}:")
            value_label = QLabel("--")
            value_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px; font-family: monospace;")
            self.cart_labels.append(label)
            self.cart_values.append(value_label)
            
            row = i // 3
            col = (i % 3) * 2
            cart_layout.addWidget(label, row, col)
            cart_layout.addWidget(value_label, row, col + 1)
        
        real_time_layout.addWidget(cart_group)
        
        layout.addWidget(real_time_group)
        
        # Add stretchable space
        layout.addStretch()
        
        return layout

    def create_log_panel(self):
        """Create log panel"""
        layout = QVBoxLayout()
        
        log_group = QGroupBox("Log")
        log_layout = QHBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        return layout

    def setup_connections(self):
        """Setup signal connections"""
        # Connect button events
        self.connect_btn.clicked.connect(self.connect_cmd)
        self.disconnect_btn.clicked.connect(self.disconnect_cmd)
        self.pause_btn.clicked.connect(self.pause_cmd)
        self.resume_btn.clicked.connect(self.resume_cmd)
        self.reset_btn.clicked.connect(self.reset_cmd)
        self.interrupt_btn.clicked.connect(self.interrupt_cmd)
        self.continue_btn.clicked.connect(self.continue_cmd)
        self.confirm_error_btn.clicked.connect(self.confirm_error_cmd)
        
        # Override slider event
        self.override_slider.valueChanged.connect(self.override_changed)
        
        # Connect movement send buttons with E6AXIS/E6POS binding
        self.send_ptp_axis_abs_btn.clicked.connect(self.send_ptp_axis_abs_cmd)
        self.send_ptp_axis_rel_btn.clicked.connect(self.send_ptp_axis_rel_cmd)
        self.send_ptp_pos_abs_btn.clicked.connect(self.send_ptp_pos_abs_cmd)
        self.send_ptp_pos_rel_btn.clicked.connect(self.send_ptp_pos_rel_cmd)
        self.send_lin_pos_abs_btn.clicked.connect(self.send_lin_pos_abs_cmd)
        self.send_lin_pos_rel_btn.clicked.connect(self.send_lin_pos_rel_cmd)
        
        # Connect ViewModel signals
        self.vm.log_updated.connect(self.append_log)

    def connect_cmd(self):
        """Handle connect button click"""
        success = self.vm.connect_to_robot()
        if success:
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
        self.update_display()

    def disconnect_cmd(self):
        """Handle disconnect button click"""
        self.vm.disconnect_from_robot()
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.update_display()

    def pause_cmd(self):
        """Handle pause button click"""
        self.vm.pause_robot()
        self.update_display()

    def resume_cmd(self):
        """Handle resume button click"""
        self.vm.resume_robot()
        self.update_display()

    def reset_cmd(self):
        """Handle reset button click"""
        self.vm.reset_robot()
        self.update_display()

    def interrupt_cmd(self):
        """Handle interrupt button click"""
        self.vm.interrupt_robot()
        self.update_display()

    def continue_cmd(self):
        """Handle continue button click"""
        self.vm.continue_robot()
        self.update_display()
        
    def confirm_error_cmd(self):
        """Handle confirm error button click"""
        self.vm.confirm_error()
        self.update_display()

    def override_changed(self, value):
        """Handle override change"""
        self.vm.program_override = int(value)
        self.override_label.setText(f"{value}%")
        
    def send_ptp_axis_abs_cmd(self):
        """Send PTP axis absolute command with E6AXIS binding"""
        axis_data = self.ptp_axis_abs_input.to_e6axis()
        self.vm.send_ptp_axis_abs(axis_data)
        
    def send_ptp_axis_rel_cmd(self):
        """Send PTP axis relative command with E6AXIS binding"""
        axis_data = self.ptp_axis_rel_input.to_e6axis()
        self.vm.send_ptp_axis_rel(axis_data)
        
    def send_ptp_pos_abs_cmd(self):
        """Send PTP position absolute command with E6POS binding"""
        pos_data = self.ptp_pos_abs_input.to_e6pos()
        self.vm.send_ptp_pos_abs(pos_data)
        
    def send_ptp_pos_rel_cmd(self):
        """Send PTP position relative command with E6POS binding"""
        pos_data = self.ptp_pos_rel_input.to_e6pos()
        self.vm.send_ptp_pos_rel(pos_data)
        
    def send_lin_pos_abs_cmd(self):
        """Send LIN position absolute command with E6POS binding"""
        pos_data = self.lin_pos_abs_input.to_e6pos()
        self.vm.send_lin_pos_abs(pos_data)
        
    def send_lin_pos_rel_cmd(self):
        """Send LIN position relative command with E6POS binding"""
        pos_data = self.lin_pos_rel_input.to_e6pos()
        self.vm.send_lin_pos_rel(pos_data)

    def append_log(self, message):
        """Add log message"""
        self.log_text.append(message)
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_display(self):
        """Update display content with E6AXIS/E6POS data"""
        # Update error ID
        self.error_id_label.setText(str(self.vm.error_id))
        
        # Update running status
        if self.vm.start_running:
            self.running_status_label.setText("Running")
            self.running_status_label.setStyleSheet("font-weight: bold; color: #27ae60;")
        else:
            self.running_status_label.setText("Stopped")
            self.running_status_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
        
        # Update status indicator lights based on robot state
        if not self.vm.start_running:
            self.comm_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        elif not self.vm._mxA_KRC_READAXISGROUP.ERROR:
            self.comm_status_light.setStyleSheet("background-color: #27ae60; border-radius: 10px;")
        else:
            self.comm_status_light.setStyleSheet("background-color: red; border-radius: 10px;")
        
        if not self.vm.start_running:
            self.drive_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        elif self.vm._mxA_KRC_AUTOMATICEXTERNAL.RC_RDY1 and self.vm._mxA_KRC_AUTOMATICEXTERNAL.PERI_RDY:
            self.drive_status_light.setStyleSheet("background-color: #27ae60; border-radius: 10px;")
        else:
            self.drive_status_light.setStyleSheet("background-color: red; border-radius: 10px;")
        
        if not self.vm.start_running:
            self.error_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        elif self.vm.error_id is not None and self.vm.error_id != 0:
            self.error_status_light.setStyleSheet("background-color: red; border-radius: 10px;")
        elif self.vm._mxA_KRC_ERROR.ERROR:
            self.error_status_light.setStyleSheet("background-color: orange; border-radius: 10px;")
        else:
            self.error_status_light.setStyleSheet("background-color: #27ae60; border-radius: 10px;")
        
        if not self.vm.start_running:
            self.movement_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        elif (self.vm._mxA_KRC_MOVEAXISABSOLUTE.ACTIVE or 
            self.vm._mxA_KRC_MOVEDIRECTABSOLUTE.ACTIVE or 
            self.vm._mxA_KRC_MOVELINEARABSOLUTE.ACTIVE):
            self.movement_status_light.setStyleSheet("background-color: #27ae60; border-radius: 10px;")
        else:
            self.movement_status_light.setStyleSheet("background-color: red; border-radius: 10px;")
        
        if not self.vm.start_running:
            self.ext_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        elif self.vm._mxA_KRC_AUTOMATICEXTERNAL.EXT:
            self.ext_status_light.setStyleSheet("background-color: #27ae60; border-radius: 10px;")
        else:
            self.ext_status_light.setStyleSheet("background-color: red; border-radius: 10px;")
        
        if not self.vm.start_running:
            self.program_status_light.setStyleSheet("background-color: gray; border-radius: 10px;")
        elif self.vm._mxA_KRC_AUTOMATICEXTERNAL.PRO_ACT:
            self.program_status_light.setStyleSheet("background-color: #27ae60; border-radius: 10px;")
        else:
            self.program_status_light.setStyleSheet("background-color: red; border-radius: 10px;")
        
        # Update loop count
        self.loop_count_label.setText(str(self.vm.cycle_nr))
        
        # Update test step
        self.test_step_label.setText(str(self.vm.test_step))
        
        # Update axis position displays from E6AXIS data
        actual_axis = self.vm._mxA_READACTUALAXISPOSITION
        axis_keys = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
        for i, key in enumerate(axis_keys):
            value = getattr(actual_axis, f'_{key}', 0.0)
            self.axis_values[i].setText(f"{value:.2f}°")
        
        # Update cartesian position displays from E6POS data
        actual_pos = self.vm._mxA_READACTUALPOSITION
        cart_keys = ['X', 'Y', 'Z', 'A', 'B', 'C']
        for i, key in enumerate(cart_keys):
            value = getattr(actual_pos, f'_{key}', 0.0)
            unit = "mm" if key in ['X', 'Y', 'Z'] else "°"
            self.cart_values[i].setText(f"{value:.2f}{unit}")

    def toggle_jog_mode(self):
        """Toggle between axis and cartesian jog modes"""
        if self.jog_mode_toggle_btn.text() == "Switch to Cartesian Mode":
            self.current_jog_labels = [
                ("X+", "X-"), ("Y+", "Y-"), ("Z+", "Z-"), 
                ("A+", "A-"), ("B+", "B-"), ("C+", "C-")
            ]
            self.jog_mode_toggle_btn.setText("Switch to Axis Mode")
            self.vm.jog_type = 1  # Cartesian mode
        else:
            self.current_jog_labels = [
                ("A1+", "A1-"), ("A2+", "A2-"), ("A3+", "A3-"), 
                ("A4+", "A4-"), ("A5+", "A5-"), ("A6+", "A6-")
            ]
            self.jog_mode_toggle_btn.setText("Switch to Cartesian Mode")
            self.vm.jog_type = 0  # Axis mode
        
        # 更新按钮文本（使用索引循环）
        for i, (pos_label, neg_label) in enumerate(self.current_jog_labels):
            self.jog_buttons[f"pos_{i}"].setText(pos_label)
            self.jog_buttons[f"neg_{i}"].setText(neg_label)

    def jog_button_pressed(self, index: int, sign: int):
        """Handle jog button pressed (key down)"""
        pos_label, neg_label = self.current_jog_labels[index]
        actual_label = pos_label if sign == 1 else neg_label
        
        # 更新 ViewModel jog state
        jog_mapping = {
            # Axis mode
            "A1+": "x_a1_plus", "A1-": "x_a1_minus",
            "A2+": "y_a2_plus", "A2-": "y_a2_minus",
            "A3+": "z_a3_plus", "A3-": "z_a3_minus",
            "A4+": "a_a4_plus", "A4-": "a_a4_minus",
            "A5+": "b_a5_plus", "A5-": "b_a5_minus",
            "A6+": "c_a6_plus", "A6-": "c_a6_minus",
            # Cartesian mode
            "X+": "x_a1_plus", "X-": "x_a1_minus",
            "Y+": "y_a2_plus", "Y-": "y_a2_minus",
            "Z+": "z_a3_plus", "Z-": "z_a3_minus",
            "A+": "a_a4_plus", "A-": "a_a4_minus",
            "B+": "b_a5_plus", "B-": "b_a5_minus",
            "C+": "c_a6_plus", "C-": "c_a6_minus",
        }
        
        if actual_label in jog_mapping:
            setattr(self.vm, jog_mapping[actual_label], True)
            print(f"JOG {actual_label} pressed")  # Debug

    def jog_button_released(self, index: int, sign: int):
        """Handle jog button released (key up)"""
        pos_label, neg_label = self.current_jog_labels[index]
        actual_label = pos_label if sign == 1 else neg_label
        
        # 更新 ViewModel jog state
        jog_mapping = {
            # Axis mode
            "A1+": "x_a1_plus", "A1-": "x_a1_minus",
            "A2+": "y_a2_plus", "A2-": "y_a2_minus",
            "A3+": "z_a3_plus", "A3-": "z_a3_minus",
            "A4+": "a_a4_plus", "A4-": "a_a4_minus",
            "A5+": "b_a5_plus", "A5-": "b_a5_minus",
            "A6+": "c_a6_plus", "A6-": "c_a6_minus",
            # Cartesian mode
            "X+": "x_a1_plus", "X-": "x_a1_minus",
            "Y+": "y_a2_plus", "Y-": "y_a2_minus",
            "Z+": "z_a3_plus", "Z-": "z_a3_minus",
            "A+": "a_a4_plus", "A-": "a_a4_minus",
            "B+": "b_a5_plus", "B-": "b_a5_minus",
            "C+": "c_a6_plus", "C-": "c_a6_minus",
        }
        
        if actual_label in jog_mapping:
            setattr(self.vm, jog_mapping[actual_label], False)
            print(getattr(self.vm, jog_mapping[actual_label]))
            print(f"JOG {actual_label} released")  # Debug


if __name__ == "__main__":
    # Create ViewModel and View
    vm = MxAViewModel()
    app = QApplication(sys.argv)
    window = MxAView(vm)
    
    # Show window
    window.show()
    
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("Stopping application...")
        if vm.main_thread and vm.main_thread.is_alive():
            vm.stop_event.set()
            vm.main_thread.join(timeout=2)
        print("Application stopped.")