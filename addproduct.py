import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDateTime
import sqlite3
from PIL import Image, ImageQt
import style
from shutil import copyfile
import tkinter as tk
from PIL import ImageGrab
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
import re


con = sqlite3.connect("db_database/main_database.db")
cur = con.cursor()

defaulImg = 'src/icons/upload_new_img.png'
real_img_name = ''


class AddProduct(QWidget):
    background = True

    def __init__(self, main):
        super().__init__()
        self.setWindowTitle("New Product")
        self.setWindowIcon(QIcon('src/icons/new_item.png'))
        self.setGeometry(650, 300, 650, 550)
        self.setFixedSize(self.size())
        self.main = main
        self.snippingTool = SnippingWidget(self)
        self.ui()
        self.show()

    def ui(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Top Layout
        self.addProductImg = QLabel()
        self.addProductImg.setPixmap(QPixmap('src/icons/upload_new_img.png'))
        #self.addProductImg.mouseDoubleClickEvent = self.some_stuff
        #self.titleText = QLabel("Add Product")
        self.addProductImg.setAlignment(Qt.AlignCenter)
        self.addProductImg.mousePressEvent = self.snipping_tool
        # Bottom Layout
        self.descriptionEntry = QLineEdit()
        self.descriptionEntry.setStyleSheet(style.search_btn_style_2())
        self.manufacturerEntry = QLineEdit()
        self.supplier = QLineEdit()
        self.supplier.setStyleSheet(style.search_btn_style_2())
        self.manufacturerEntry.setStyleSheet(style.search_btn_style_2())
        self.nameEntry = QLineEdit()
        self.nameEntry.setStyleSheet(style.search_btn_style_2())
        #self.nameEntry.setPlaceholderText("Enter name of product ...")
        self.manufactuterEntry = QLineEdit()
        self.manufactuterEntry.setStyleSheet(style.search_btn_style_2())
        #self.manufactuterEntry.setPlaceholderText("Enter name of manufacturer ...")
        self.PoNumber = QLineEdit()
        self.PoNumber.setStyleSheet(style.search_btn_style_2())

        self.priceEntry = QLineEdit()
        self.priceEntry.setStyleSheet(style.search_btn_style_2())
        #self.priceEntry.setPlaceholderText("Enter price of product ...")
        self.quotaEntry = QLineEdit()
        self.quotaEntry.setStyleSheet(style.search_btn_style_2())

        self.timeAndDateEdit = QDateEdit()
        self.timeAndDateEdit.setDateTime(QDateTime.currentDateTime())
        self.timeAndDateEdit.setCalendarPopup(True)
        self.timeAndDateEdit.setStyleSheet("QDateEdit{font-size: 13pt; font: Liberation Mono}")
        #self.timeAndDateEdit.setStyleSheet(style.time_edit())
        #self.quotaEntry.setPlaceholderText("Enter quota of product ...")
        self.uploadBtn = QPushButton("Upload")
        self.uploadBtn.setStyleSheet("QPushButton{font-size: 13pt; font: Liberation Mono}")
        self.uploadBtn.clicked.connect(self.upload_img_btn)
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.setStyleSheet("QPushButton{font-size: 13pt; font: Liberation Mono}")
        self.submitBtn.clicked.connect(self.add_product)

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
        #self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        # Widgets of Form layout
        self.bottomLayout.addRow(QLabel("Product Name: "), self.descriptionEntry)
        self.bottomLayout.addRow(QLabel("Manufacturer: "), self.manufacturerEntry)
        self.bottomLayout.addRow(QLabel("Model: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("PO #: "), self.PoNumber)
        self.bottomLayout.addRow(QLabel("Price: "), self.priceEntry)
        self.bottomLayout.addRow(QLabel("Supplier: "), self.supplier)
        self.bottomLayout.addRow(QLabel("Units: "), self.quotaEntry)
        self.bottomLayout.addRow(QLabel(""), self.timeAndDateEdit)
        self.bottomLayout.addRow(QLabel(""), self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def some_stuff(self):
        pass

    def upload_img_btn(self):
        global defaulImg
        poNumber = str(self.PoNumber.text())
        self.fileName, self.ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.jpg *.png)")
        if self.ok:
            defaulImg = os.path.basename(self.fileName)
            img = Image.open(self.fileName)
            self.unique_img_name = poNumber + defaulImg
            img.save("src/img/{}".format(self.unique_img_name))
            self.addProductImg.setPixmap(QPixmap('src/icons/{}'.format(defaulImg)))
            defaulImg = self.unique_img_name

    def add_product(self):
        global defaulImg
        print("The DEFAULT: \n",defaulImg)
        img_name = os.path.basename(defaulImg)
        defaulImgSrc = 'src/img/{}'.format(img_name)

        try:
            description = self.descriptionEntry.text()
            name = self.nameEntry.text()
            manufacturer = self.manufacturerEntry.text()
            supplier = self.supplier.text()
            #poNumber = int(self.PoNumber.text()) #TODO change
            #price = int(self.priceEntry.text()) #TODO change
            price = str(self.priceEntry.text()) #TODO change
            poNumber = str(self.PoNumber.text()) #TODO change
            qouta = self.quotaEntry.text()
            dayOfAdding = self.timeAndDateEdit.text()

            # Checking if fields are empty or not
            if (name and manufacturer and price and qouta and poNumber != ""):
                try:
                    #price = int(price) #TODO Price integer now
                    existing_products = []
                    query = "INSERT INTO 'products' (description,product_manufacturer,product_name,supplier,product_price,product_quota,product_img,product_po,date_adding) VALUES(?,?,?,?,?,?,?,?,?)"
                    check = cur.execute("SELECT product_po FROM products").fetchall()
                    for i in check:
                        existing_products.append(str(i[0]))
                    if str(poNumber) in existing_products:
                        self.PoNumber.setStyleSheet(style.qLineEditRed())
                        QMessageBox.warning(self, "Warning!", "Product with {} id already exist. Please choose unique Id".format(poNumber))
                    else:
                        self.PoNumber.setStyleSheet(style.search_btn_style_2())
                        cur.execute(query, (description,manufacturer,name, supplier, price, qouta, defaulImgSrc, poNumber, dayOfAdding))
                        con.commit()
                        self.main.productsTable.sortItems(10, Qt.AscendingOrder)
                        self.main.displayProducts()
                        QMessageBox.information(self, "Info", "Product has been added")
                        self.main.update_to_DB.setIcon(QIcon('src/icons/updateToServer.png'))
                        self.main.update_to_DB.setText("Update")
                        self.nameEntry.setText("")
                        self.manufactuterEntry.setText("")
                        self.priceEntry.setText("")
                        self.PoNumber.setText("")
                        self.quotaEntry.setText("")
                        self.descriptionEntry.setText("")
                        self.manufacturerEntry.setText("")
                        self.supplier.setText("")
                        self.addProductImg.setPixmap(QPixmap('src/icons/upload_new_img.png'))

                except:
                    QMessageBox.warning(self, "Info", "Check All Fields Properly!!!")
            else:
                QMessageBox.warning(self, 'Info', "Please fill all the fields. Fields can not been empty!!!")
        except:
            QMessageBox.warning(self, 'Info', "Please enter a whole number")

        print(defaulImg)
        #defaulImg = 'src/icons/upload_new_img.png'
        if defaulImg == 'src/icons/upload_new_img.png':
            copyfile(defaulImg, 'src/img/{}'.format(img_name))
            copyfile('src/icons/default_img.png', 'src/img/default_img.png')
            print("Copying: ", img_name)
        else:
            print("Else")
            try:
                img_name = os.path.basename(defaulImg)
                copyfile("db_database/semiland_database.db","database_backup/semiland_database.db")
                copyfile(defaulImg,'src/img/{}'.format(img_name))

                folder = 'src/current_pictures'
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        QMessageBox.warning(self, "Warning!", "{}".format(e))

            except Exception as e:
                copyfile('src/icons/upload_new_img.png', 'src/img/upload_new_img.png')

        defaulImg = 'src/icons/upload_new_img.png'


    def snipping_tool(self, event):
        global real_img_name

        folder = 'src/current_pictures'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                QMessageBox.information(self, "Information!", "{}".format(e))

        self.snippingTool.start()
        self.show()


class SnippingWidget(QtWidgets.QWidget):
    num_snip = 0
    is_snipping = False
    background = True
    img_name = ''

    def __init__(self, add_prod):
        super(SnippingWidget, self).__init__()
        self.parent = None
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.add_prod = add_prod
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.real_img_name = ''

    def start(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        SnippingWidget.background = False
        SnippingWidget.is_snipping = True
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def paintEvent(self, event):
        if SnippingWidget.is_snipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            opacity = 0.3
        else:
            # reset points, so the rectangle won't show up again.
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0

        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        rect = QtCore.QRectF(self.begin, self.end)
        qp.drawRect(rect)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            print('Quit')
            self.close()
        event.accept()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        global img_name, real_img_name, defaulImg
        SnippingWidget.num_snip += 1
        SnippingWidget.is_snipping = False
        QtWidgets.QApplication.restoreOverrideCursor()
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        QtWidgets.QApplication.processEvents()
        data_img = QDateTime.currentDateTime().toString(1)
        img_name = re.sub(r'[^\w\s]','',data_img)
        img_name = img_name+'.png'
        img_name = os.path.basename(img_name)
        real_img_name = "src/img/{}".format(img_name)
        real_img_name_current = "src/current_pictures/{}".format(img_name)
        #img.save(real_img_name)
        try:
            img.save(real_img_name_current)
            self.add_prod.addProductImg.setPixmap(QPixmap(real_img_name_current))
        except:
            pass
        defaulImg = real_img_name_current
        print("Real Image: ", defaulImg)
        self.close()