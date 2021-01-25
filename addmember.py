from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import style
import os
from PIL import Image



con = sqlite3.connect("db_database/main_database.db")
cur = con.cursor()

defaulImg = 'src/img/default_img.png'


class AddMember(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setWindowTitle("Add Member")
        self.setWindowIcon(QIcon('src/icons/new_member.png'))
        self.setGeometry(650, 300, 350, 550)
        self.setFixedSize(self.size())
        self.empl_dc = dict()
        self.main = main
        self.chek_empl()
        self.ui()
        self.show()

    def ui(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Widgets of top layout
        self.addMemberImg = QLabel()
        self.addMemberImg.setPixmap(QPixmap('src/icons/add_engineer.png'))
        self.addMemberImg.setAlignment(Qt.AlignCenter)
        #self.titleText = QLabel("Add Member")
        #self.titleText.setAlignment(Qt.AlignCenter)

        # Widgets of bottom layout
        self.nameEntry = QLineEdit()
        self.nameEntry.setStyleSheet(style.search_btn_style_2())
        #self.nameEntry.setPlaceholderText("Enter name of member ...")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setStyleSheet(style.search_btn_style_2())
        #self.surnameEntry.setPlaceholderText("Enter surname of member ...")
        self.phonenumberEntry = QLineEdit()
        self.phonenumberEntry.setStyleSheet(style.search_btn_style_2())
        #self.phonenumberEntry.setPlaceholderText("Enter phone number of member ...")
        self.uploadBtn = QPushButton("Upload Image")
        self.uploadBtn.setStyleSheet("QPushButton{font-size: 13pt; font: Liberation Mono}")
        self.uploadBtn.clicked.connect(self.upload_img_btn)
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.setStyleSheet("QPushButton{font-size: 13pt; font: Liberation Mono}")
        self.submitBtn.clicked.connect(self.add_member_btn)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.sell_product_top_frame())
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet(style.sell_product_bottom_frame())

        # Add widgets
        #self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.addMemberImg)
        self.topFrame.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Position: "), self.surnameEntry)
        self.bottomLayout.addRow(QLabel("ID: "), self.phonenumberEntry)
        self.bottomLayout.addRow(QLabel(""), self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def upload_img_btn(self):
        global defaulImg
        self.fileName, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.jpg *.png)")
        if ok:
            print(self.fileName)
            defaulImg = os.path.basename(self.fileName)
            img = Image.open(self.fileName)
            img.save("src/img/{0}".format(defaulImg))
            self.addMemberImg.setPixmap(QPixmap('src/icons/{}'.format(defaulImg)))

    def add_member_btn(self):
        global defaulImg
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phonenumberEntry.text()

        if (name and surname and phone != ""):
            print("Done")
            self.chek_empl()
            try:
                existing_members = []
                chech_mem = cur.execute("SELECT member_name FROM members")
                for i in chech_mem:
                    existing_members.append(str(i[0]))
                if str(name) in existing_members:
                    self.nameEntry.setStyleSheet(style.qLineEditRed())
                    QMessageBox.warning(self, "Warning!","Member with {} name already exist. \nPlease choose name!".format(name))


                elif str(name) in str(self.empl_dc.keys()) and str(phone) in str(self.empl_dc.values()):
                    print("User Exist")
                    self.nameEntry.setStyleSheet(style.qLineEditRed())
                    self.phonenumberEntry.setStyleSheet(style.qLineEditRed())
                    QMessageBox.warning(self, "Warning!", "User with Name='{}' and id='{}' Already exists. \nPlease choose unique Id OR Name.".format(name, phone))

                else:
                    print("New User")
                    query = "INSERT INTO 'members' (member_name,member_surname,member_phone,member_photo) VALUES(?,?,?,?)"
                    cur.execute(query, (name, surname, phone, defaulImg))
                    con.commit()
                    self.main.displayMembers()
                    self.nameEntry.setStyleSheet(style.search_btn_style_2())
                    self.phonenumberEntry.setStyleSheet(style.search_btn_style_2())
                    QMessageBox.information(self, "Info", "Member Has Been Added!")
                    self.nameEntry.setText("")
                    self.surnameEntry.setText("")
                    self.phonenumberEntry.setText("")


            except:
                QMessageBox.warning(self, "Warning", "Member has not been added!!!!")
        else:
            QMessageBox.warning(self, "Warning", "Fields can not be empty!!!!")

        self.addMemberImg.setPixmap(QPixmap('src/icons/add_engineer.png'))

    def chek_empl(self):
        self.empl_dc.clear()
        self.sq = cur.execute("SELECT member_name,member_phone FROM members").fetchall()
        for i in self.sq:
            self.empl_dc[i[0]] = i[1]
        print(self.empl_dc)

