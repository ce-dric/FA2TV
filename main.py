import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QFileDialog, QLabel, QProgressBar, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from convert import convert_files

class ConverterThread(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)

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
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Select Input and Output Folders")
        layout.addWidget(self.label)

        self.input_button = QPushButton("Select Input Folder")
        self.input_button.clicked.connect(self.select_input_folder)
        layout.addWidget(self.input_button)

        self.output_button = QPushButton("Select Output Folder")
        self.output_button.clicked.connect(self.select_output_folder)
        layout.addWidget(self.output_button)

        self.start_button = QPushButton("Start Conversion")
        self.start_button.clicked.connect(self.start_conversion)
        layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        self.log_label = QLabel("Logs:")
        layout.addWidget(self.log_label)

        self.logs = QLabel("")
        layout.addWidget(self.logs)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.input_folder = ''
        self.output_folder = ''

    def select_input_folder(self):
        self.input_folder = QFileDialog.getExistingDirectory(self, 'Select Input Folder')
        self.label.setText(f"Input Folder: {self.input_folder}")

    def select_output_folder(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, 'Select Output Folder')
        self.label.setText(f"Output Folder: {self.output_folder}")

    def start_conversion(self):
        if self.input_folder and self.output_folder:
            self.thread = ConverterThread(self.input_folder, self.output_folder)
            self.thread.progress.connect(self.update_progress)
            self.thread.log.connect(self.update_logs)
            self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_logs(self, message):
        current_text = self.logs.text()
        self.logs.setText(current_text + "\n" + message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())
