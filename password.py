from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import style


class PasswordInitializer(QDialog):
    def __init__(self, parent=None):
        super(PasswordInitializer, self).__init__(parent)
        self.setWindowTitle("Please Authorize!")
        self.setWindowIcon(QIcon('src/icons/power_module.png'))
        self.setGeometry(650, 300, 450, 450)
        self.setFixedSize(self.size())

        self.ui()
        self.show()

    def ui(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.textName = QLineEdit(self)
        self.textName.setText("Login")
        self.textPass = QLineEdit(self)
        self.textPass.setText("Password")
        self.btnLogin = QPushButton("Login", self)
        self.btnLogin.clicked.connect(self.handlePassword)
        self.addProductImg = QLabel()
        self.addProductImg.setPixmap(QPixmap('src/icons/main_win_logo.jpg'))
        self.addProductImg.setAlignment(Qt.AlignCenter)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.sell_product_top_frame())
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet(style.sell_product_bottom_frame())

        # Add widgets
        self.topLayout.addWidget(self.addProductImg)
        # self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        # Widgets of Form layout
        self.bottomLayout.addRow(QLabel("Login: "), self.textName)
        self.bottomLayout.addRow(QLabel("Password: "), self.textPass)
        self.bottomLayout.addRow(QLabel(""), self.btnLogin)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def handlePassword(self):
        if (self.textName.text() == 'Login' and self.textPass.text() == 'Password'):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error!', 'Bad user or password!')
