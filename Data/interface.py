import sys
from PyQt5.QtCore import QSize, QProcess
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QPushButton, 
    QWidget,
    QVBoxLayout,
    QMessageBox
)
from db_utils import get_logged_words
import tempfile
import webbrowser

FLASK_SCRIPT_NAME = "app.py"
PYTHON_EXECUTABLE = sys.executable

# learnt from https://www.pythonguis.com/pyqt5-tutorial/

# it generates an HTML report for the logged words
def generate_html_report(words_list):
    
    css = """
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f4f7f6; color: #333; }
        h1 { color: #2C3E50; border-bottom: 3px solid #3498DB; padding-bottom: 10px; }
        .word-card { background-color: #ffffff; margin-bottom: 15px; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #3498DB; }
        .word-title { font-size: 1.5em; font-weight: bold; color: #E74C3C; margin-bottom: 5px; }
        .word-definition { margin-top: 8px; padding-left: 10px; border-left: 3px solid #E74C3C; }
    </style>
    """

    content = ""
    for item in words_list:
        word = item.get('word', 'N/A')
        definition = item.get('definition', 'No definition found')
        
        content += f"""
        <div class="word-card">
            <div class="word-title">{word}</div>
            <div class="word-definition"><strong>Definiție:</strong> {definition}</div>
        </div>
        """
        
    html = f"""
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <title>Raport Cuvinte Subtitrări</title>
        {css}
    </head>
    <body>
        <h1>📚 Raport Cuvinte Învățate</h1>
        <p>Aceasta este lista cuvintelor unice pe care le-ai căutat în timpul sesiunii de vizionare.</p>
        {content}
        <hr>
    </body>
    </html>
    """
    return html

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Subtitles Translator")
        self.setFixedSize(QSize(400, 150))

        self.flask_process = QProcess(self)
        self.flask_process.finished.connect(self.handle_flask_finished)
        
        container = QWidget()

        layout = QVBoxLayout()
        
        self.button = QPushButton("Start/Stop Server")
        self.button.clicked.connect(self.on_button_clicked)
        self.button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px;")
        
        layout.addStretch(1) 
        layout.addWidget(self.button)
        layout.addStretch(1)

        container.setLayout(layout)

        self.setCentralWidget(container)

        app.aboutToQuit.connect(self.kill_flask_process)

    def open_html_report_in_browser(self, html_content):
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp_file:
                tmp_file.write(html_content)
                temp_filepath = tmp_file.name
            
            webbrowser.open_new_tab(f'file:///{temp_filepath}')
            
        except Exception as e:
            QMessageBox.critical(self, "Browser error", f"Couldn't open {e}")


    def on_button_clicked(self):
        
        if self.flask_process.state() == QProcess.NotRunning:
            self.start_flask_process()
        else:
            html_report = self.get_unknown_words_report()

            self.kill_flask_process()
            
            if html_report:
                self.open_html_report_in_browser(html_report)

    def get_unknown_words_report(self):

        words_list = get_logged_words()
        if not words_list:
                QMessageBox.information(self, "Raport", "Zero words logged.")
                return None
                
        return generate_html_report(words_list)

    def start_flask_process(self):
        
        self.button.setEnabled(False)
        self.button.setText("Starting Server...")
        self.button.setStyleSheet("background-color: orange; color: black; font-size: 18px;")

        command = PYTHON_EXECUTABLE
        arguments = [FLASK_SCRIPT_NAME]
        
        self.flask_process.start(command, arguments)
        
        if self.flask_process.waitForStarted(700):

            # time.sleep(1) 
            
            self.button.setText("Server Running - Click to STOP")
            self.button.setStyleSheet("background-color: red; color: white; font-size: 18px;")
            self.button.setEnabled(True)
            return True
        else:
            QMessageBox.critical(self, "Error Server", f"Couldn't open: {self.flask_process.errorString()}")
            self.button.setText("Start/Stop Server")
            self.button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px;")
            self.button.setEnabled(True)
            return False

    def kill_flask_process(self):
        if self.flask_process.state() == QProcess.Running:
            self.button.setEnabled(False)
            self.button.setText("Stopping Server...")
            self.button.setStyleSheet("background-color: grey; color: white; font-size: 18px;")
            
            print(f"Shutdown...")
            self.flask_process.terminate()
            self.flask_process.waitForFinished(3000) 
            if self.flask_process.state() == QProcess.Running:
                 self.flask_process.kill()
        
    def handle_flask_finished(self):
        if self.flask_process.exitStatus() == QProcess.NormalExit:
            print("Flask server opened normally.")
        else:
            print("Flask server opened with errors.")

        self.button.setText("Start/Stop Server")
        self.button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px;")
        self.button.setEnabled(True)

#it doesn't need sys args
app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())