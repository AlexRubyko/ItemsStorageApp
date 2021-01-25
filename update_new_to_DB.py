import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import style
from WaitingSpinnerWidget import QtWaitingSpinner
import socket, pickle


class ConnectingUpdating(QWidget):
    def __init__(self, main_table):
        super().__init__()
        self.setWindowTitle("Client Connection")
        self.setWindowIcon(QIcon("src/icons/return.png"))
        self.setGeometry(650, 300, 250, 250)
        self.setFixedSize(self.size())
        self.spinner = QtWaitingSpinner()
        self.main_table = main_table
        self.ui()
        self.show()

    def ui(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.ipAddressInputField = QLineEdit()
        self.ipAddressInputField.setText("192.168.1.11")

        self.ipAddressInputField.setStyleSheet('QLineEdit{border-color: #A3C1DA; font-size: 15pt; font: Liberation Mono}')
        self.portInputField = QLineEdit()
        self.portInputField.setText("9999")
        self.portInputField.setStyleSheet('QLineEdit{border-color: #A3C1DA; font-size: 15pt; font: Liberation Mono}')
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.setStyleSheet('QPushButton{background-color:#9bc9ff;border-style:solid;border-width:2px;border-radius:10px;border-color:beige;font:14px;padding:6px;min-width:6em;font-family:Liberation Mono;}')
        
        self.submitBtn.clicked.connect(self.submit)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrameLayout = QFrame()
        self.topFrameLayout.setStyleSheet(style.sell_product_top_frame())
        self.bottomFrameLayout = QFrame()
        self.bottomFrameLayout.setStyleSheet(style.sell_product_bottom_frame())
        # Add widgets
        self.bottomLayout.addRow(QLabel("IP: "), self.ipAddressInputField)
        self.bottomLayout.addRow(QLabel("Port: "), self.portInputField)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrameLayout.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.bottomFrameLayout)
        self.mainLayout.addWidget(self.spinner)
        self.setLayout(self.mainLayout)

    def submit(self):
        if self.portInputField.text() == "" or self.ipAddressInputField.text() == "":
            QMessageBox.warning(self, "Warning!", "Fields can not be empty!")
        else:
            self.spinner.start()
            runnable = RequestRunnable(self)

            QThreadPool.globalInstance().start(runnable)

    @pyqtSlot(str)
    def setData(self, data):
        # print(data)
        self.spinner.stop()
        self.adjustSize()
        QMessageBox.information(self, "Success!", "Updated succesfully!")
        self.main_table.update_to_DB.setIcon(QIcon('src/icons/update.png'))
        self.main_table.update_to_DB.setText("Updated")
        with open('database_backup/state.txt', 'w') as f:
            f.write('some')
        self.close()
    
    @pyqtSlot(str)
    def setData_two(self, data):
        # print(data)
        self.spinner.stop()
        self.adjustSize()
        QMessageBox.warning(self, "Warning!", "Server isnt working!")
        self.close()
    

class RequestRunnable(QRunnable):
    def __init__(self, dialog):
        QRunnable.__init__(self)
        self.w = dialog
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.w.ipAddressInputField.text()
        self.port = int(self.w.portInputField.text())

    def run(self):
        try:
            self.s.connect((self.host, self.port))
            filename = 'db_database/main_database.db'
            f = open(filename, 'rb')
            l = f.read(1024)
        
            while l:
                self.s.send(l)
                l = f.read(1024)
            f.close()

            QMetaObject.invokeMethod(self.w, "setData",
                                 Qt.QueuedConnection,
                                 Q_ARG(str, "finish"))
        except socket.error:
            print("Error: ")
            self.s.close()
            QMetaObject.invokeMethod(self.w, "setData_two",
                                 Qt.QueuedConnection,
                                 Q_ARG(str, "Error"))
            
        finally:
            self.s.close()
        self.s.close()

    def loadingDataList(self):
        self.SemilandData = []

        while True:

            self.data = self.s.recv(4096)
            if not self.data: break
            self.SemilandData.append(self.data)
        self.data_attr = pickle.loads(b"".join(self.SemilandData))
