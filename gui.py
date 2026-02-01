import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFileDialog, QTextEdit, QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal as Signal
from PyQt6.QtGui import QFont, QIcon
from backend import TranslationBackend

# Hardcoded API Key


class WorkerThread(QThread):
    progress_update = Signal(int)
    log_update = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(self, backend, input_path, output_path):
        super().__init__()
        self.backend = backend
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        self.log_update.emit(f"Starting processing for: {self.input_path}")
        success, message = self.backend.process_docx(
            self.input_path, 
            self.output_path, 
            self.progress_callback
        )
        self.finished_signal.emit(success, message)

    def progress_callback(self, value):
        self.progress_update.emit(value)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Urdu Translation Helper")
        self.resize(600, 400)
        self.setup_ui()
        # Initialize backend with hardcoded API key
        self.backend = TranslationBackend(API_KEY)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("📚 Urdu Docx Translator")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #6366f1;
            margin-bottom: 20px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Updated for PyQt6 enum
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Transform your documents with AI-powered Urdu translations")
        subtitle.setStyleSheet("color: #64748b; font-size: 12px; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # File Selection Section
        file_layout = QHBoxLayout()
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("No file selected - Click Browse to select a .docx file")
        self.file_path_input.setReadOnly(True)
        self.file_path_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: #f8fafc;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #6366f1;
            }
        """)
        
        browse_btn = QPushButton("📁 Browse")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                padding: 12px 24px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #4f46e5;
            }
        """)
        browse_btn.clicked.connect(self.browse_file)
        
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)

        # Process Button
        self.process_btn = QPushButton("🚀 Start Translation")
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981; 
                color: white; 
                padding: 15px; 
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:disabled {
                background-color: #94a3b8;
            }
        """)
        self.process_btn.clicked.connect(self.start_processing)
        layout.addWidget(self.process_btn)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 8px;
                background-color: #e2e8f0;
                height: 20px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #6366f1;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Log Area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("Status logs will appear here...")
        self.log_area.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px;
                background-color: #f8fafc;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.log_area)

        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
        """)

    def log(self, message):
        self.log_area.append(message)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Docx File", "", "Word Documents (*.docx)")
        if file_name:
            self.file_path_input.setText(file_name)

    def start_processing(self):
        input_path = self.file_path_input.text().strip()

        if not input_path:
            QMessageBox.warning(self, "Error", "Please select a .docx file.")
            return

        if not self.backend.client:
            QMessageBox.critical(self, "Error", "Failed to connect to Gemini API. Please check your internet connection.")
            return

        # Output path - append _translated
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_translated{ext}"

        self.process_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_area.clear()

        self.worker = WorkerThread(self.backend, input_path, output_path)
        self.worker.progress_update.connect(self.progress_bar.setValue)
        self.worker.log_update.connect(self.log)
        self.worker.finished_signal.connect(self.on_process_finished)
        self.worker.start()

    def on_process_finished(self, success, message):
        self.process_btn.setEnabled(True)
        if success:
            self.log(f"✓ SUCCESS: {message}")
            QMessageBox.information(self, "Success", f"File saved to:\n{self.worker.output_path}")
        else:
            self.log(f"✗ ERROR: {message}")
            QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
