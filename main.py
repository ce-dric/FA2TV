import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QFileDialog, QLabel, QProgressBar, QWidget, QMessageBox, QScrollArea
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os
from convert import convert_files

class ConverterThread(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str, str)

    def __init__(self, input_folder, output_folder):
        super().__init__()
        self.input_folder = input_folder
        self.output_folder = output_folder

    def run(self):
        convert_files(self.input_folder, self.output_folder, self.progress.emit, self.log.emit)

class ConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('HEIC to JPG & MOV to MP4 Converter')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Select Input and Output Folders")
        layout.addWidget(self.label)

        self.input_folder_label = QLabel("Input Folder: Not selected")
        layout.addWidget(self.input_folder_label)

        self.output_folder_label = QLabel("Output Folder: Not selected")
        layout.addWidget(self.output_folder_label)

        self.input_button = QPushButton("Select Input Folder")
        self.input_button.clicked.connect(self.select_input_folder)
        layout.addWidget(self.input_button)

        self.output_button = QPushButton("Select Output Folder")
        self.output_button.clicked.connect(self.select_output_folder)
        layout.addWidget(self.output_button)

        self.start_button = QPushButton("Start Conversion")
        self.start_button.clicked.connect(self.confirm_conversion)
        layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        self.log_label = QLabel("Logs:")
        layout.addWidget(self.log_label)

        self.logs = QLabel("")
        self.logs.setWordWrap(True)
        self.logs.setAlignment(Qt.AlignTop)
        self.logs.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.logs)
        self.scroll_area.setFixedHeight(150)
        layout.addWidget(self.scroll_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.input_folder = ''
        self.output_folder = ''

    def select_input_folder(self):
        self.input_folder = QFileDialog.getExistingDirectory(self, 'Select Input Folder')
        self.input_folder_label.setText(f"Input Folder: {self.input_folder}")

    def select_output_folder(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, 'Select Output Folder')
        self.output_folder_label.setText(f"Output Folder: {self.output_folder}")

    def confirm_conversion(self):
        if self.input_folder and self.output_folder:
            confirm_msg = QMessageBox.question(
                self,
                'Confirm Folders',
                f"Input Folder: {self.input_folder}\nOutput Folder: {self.output_folder}\n\nDo you want to start the conversion?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if confirm_msg == QMessageBox.Yes:
                self.start_conversion()

    def start_conversion(self):
        if self.input_folder and self.output_folder:
            self.thread = ConverterThread(self.input_folder, self.output_folder)
            self.thread.progress.connect(self.update_progress)
            self.thread.log.connect(self.update_logs)
            self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_logs(self, message, status="success"):
        if status == "success":
            colored_message = f'<span style="color:green;">[success]</span> {message}'
        elif status == "failed":
            colored_message = f'<span style="color:red;">[failed]</span> {message}'
        elif status == "skipped":
            colored_message = f'<span style="color:purple;">[skipped]</span> {message}'
        else:
            colored_message = message

        current_text = self.logs.text()
        self.logs.setText(current_text + "<br>" + colored_message)
        self.logs.adjustSize()

        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())
