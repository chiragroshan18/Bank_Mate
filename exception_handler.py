#exception_handler
import sys
import traceback
import logging
from PyQt5.QtWidgets import QMessageBox, QApplication

def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler for uncaught exceptions"""
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logging.critical(f"Unhandled exception: {error_msg}")
    
    # Ensure QApplication exists before showing message
    app = QApplication.instance()
    if app is not None:
        error_dialog = QMessageBox()
        error_dialog.setWindowTitle("Critical Error")
        error_dialog.setText("An unexpected error occurred")
        error_dialog.setDetailedText(error_msg)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.exec_()
    
    sys.exit(1)

def install_exception_handler():
    """Install the global exception handler"""
    sys.excepthook = handle_exception
