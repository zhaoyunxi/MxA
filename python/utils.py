from enum import Enum
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QGroupBox, QPushButton, QLabel, QLineEdit, 
    QTextEdit, QSlider, QTabWidget, QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QColor
import time 

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

class LogManager(QObject):
    """Enhanced log manager with color-coded messages by level"""
    log_signal = pyqtSignal(str)  # Will emit HTML-formatted string
    
    def __init__(self):
        super().__init__()
        self.logs = []
        
        # Define colors for each log level
        self.level_colors = {
            LogLevel.INFO: "#0066CC",      # Blue
            LogLevel.WARNING: "#FFA500",   # Orange
            LogLevel.ERROR: "#FF0000",     # Red
            LogLevel.DEBUG: "#808080"      # Gray
        }
        
    def _format_log_message(self, level, message):
        """Format log message with timestamp and HTML styling"""
        timestamp = time.strftime("%H:%M:%S")
        color = self.level_colors[level]
        formatted_message = (
            f'<span style="color: black;">[{timestamp}]</span> '
            f'<span style="color: {color}; font-weight: bold;">{level.value}:</span> '
            f'<span style="color: black;">{message}</span>'
        )
        return formatted_message
        
    def log_info(self, message):
        """Log an info message"""
        formatted_message = self._format_log_message(LogLevel.INFO, message)
        self.logs.append(formatted_message)
        self.log_signal.emit(formatted_message)
        
    def log_error(self, message):
        """Log an error message"""
        formatted_message = self._format_log_message(LogLevel.ERROR, message)
        self.logs.append(formatted_message)
        self.log_signal.emit(formatted_message)
        
    def log_warning(self, message):
        """Log a warning message"""
        formatted_message = self._format_log_message(LogLevel.WARNING, message)
        self.logs.append(formatted_message)
        self.log_signal.emit(formatted_message)
        
    def log_debug(self, message):
        """Log a debug message"""
        formatted_message = self._format_log_message(LogLevel.DEBUG, message)
        self.logs.append(formatted_message)
        self.log_signal.emit(formatted_message)
        
    def clear_logs(self):
        """Clear all logs"""
        self.logs.clear()