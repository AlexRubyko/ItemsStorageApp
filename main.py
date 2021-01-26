import sys
from PyQt5.QtCore import *
import csv
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDateTime
import sqlite3
from PIL import Image
import tkinter as tk
from PIL import ImageGrab
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
import re
from shutil import copyfile
import xlwt
from xlwt import Workbook

import addproduct, addmember, statictic_main, take_item, takedItem, return_item, style, password, update_new_to_DB

con = sqlite3.connect("db_database/main_database.db")
cur = con.cursor()
productId = 0

defaulImg = 'src/icons/upload_new_img.png'
update_db_img = 'src/icons/update.png'
update_DB_text = 'Updated'


class Main(QMainWindow):
    somedata = 10
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product management system")
        self.setWindowIcon(QIcon("src/icons/main_win_logo.jpg"))
        self.setGeometry(200, 200, 1600, 786)
        
        #self.restoreState()
        with open('database_backup/state.txt', 'r') as f:
            if f.read() == 'state':
                global update_db_img
                global update_DB_text 
                update_DB_text = 'Update'
                update_db_img = 'src/icons/updateToServer.png'
        self.ui()
        self.show()

    def ui(self):
        self.toolBar()
        self.mainMenu()
        self.tabWidget()
        self.widgets()
        self.layouts()
        self.displayProducts()
        self.displayMembers()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb.setStyleSheet("QToolBar {background-color:#90AFC5;}")
        
        # Tool Bar Buttons
        self.addProductBtn = QAction(QIcon('src/icons/new_item.png'), "Add item", self)
        self.addProductBtn.triggered.connect(self.add_product_btn)
        self.addProductBtn.setFont(QFont("Liberation Mono", 12))
        self.tb.addAction(self.addProductBtn)
        self.tb.addSeparator()


        self.addMember = QAction(QIcon('src/icons/new_member.png'), "Add engineer", self)
        self.addMember.triggered.connect(self.add_member)
        self.addMember.setFont(QFont("Liberation Mono",12))
        self.tb.addAction(self.addMember)
        self.tb.addSeparator()

        self.sellProduct = QAction(QIcon('src/icons/take_item.png'), "Take Item", self)
        self.sellProduct.setFont(QFont("Liberation Mono", 12))
        self.sellProduct.triggered.connect(self.sell_product)
        self.tb.addAction(self.sellProduct)
        self.tb.addSeparator()

        self.returnProduct = QAction(QIcon('src/icons/return.png'), "Return Item", self)
        self.returnProduct.setFont(QFont("Liberation Mono", 12))
        self.returnProduct.triggered.connect(self.return_product)
        self.tb.addAction(self.returnProduct)
        self.tb.addSeparator()

        self.refreshTb = QAction(QIcon('src/icons/upgrade_btn.png'), "Refresh", self)
        self.refreshTb.setFont(QFont("Arial", 12))
        self.refreshTb.triggered.connect(self.refresh_all_tables)
        self.tb.addAction(self.refreshTb)
        self.tb.addSeparator()

        self.update_to_DB = QAction(QIcon(update_db_img), update_DB_text, self)
        self.update_to_DB.setFont(QFont("Arial", 12))
        self.update_to_DB.triggered.connect(self.update_DB_database)
        self.tb.addAction(self.update_to_DB)
        self.tb.addSeparator()

    def mainMenu(self):
        self.menubar = self.menuBar()
        file_bar = self.menubar.addMenu("File")
        edit_bar = self.menubar.addMenu("Edit")
        code_bar = self.menubar.addMenu("Code")
        view_bar = self.menubar.addMenu("View")
        help_bar = self.menubar.addMenu("Help")

        # Sub menu items
        save_to_excel = QAction("Save As...", self)
        file_bar.addAction(save_to_excel)
        save_to_excel.triggered.connect(self.save_to_EXCEL_file)

        open_file = QAction("Open", self)
        open_file.setIcon(QIcon("src/icons/ds.png"))
        file_bar.addAction(open_file)

        exit_file = QAction("Exit", self)
        exit_file.setIcon(QIcon("src/icons/cancel.png"))
        exit_file.triggered.connect(self.exit_programm_func)
        file_bar.addAction(exit_file)

        # Code Bar
        check_statistic = QAction("Transaction Table", self)
        check_statistic.triggered.connect(self.check_staticctics)
        code_bar.addAction(check_statistic)

        clear_items_table = QAction("Clear All Tables", self)
        clear_items_table.triggered.connect(self.clear_all_items)
        code_bar.addAction(clear_items_table)

        # Help_bar
        about_prg = QAction("About", self)
        about_prg.triggered.connect(self.about_programm)
        help_bar.addAction(about_prg)

        # View Bar
        full_screen = QAction("Fullscreen Mode", self)
        full_screen.triggered.connect(self.enter_full_screen_mode)
        view_bar.addAction(full_screen)

    def tabWidget(self):
        font = QFont("Arial",12,10,False)
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(style.qTabWidgetStyle())
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.tabChanged)
        self.setCentralWidget(self.tabs)
        self.tabs1 = QWidget()
        self.tabs2 = QWidget()
        self.tabs.addTab(self.tabs1, "Product")
        self.tabs.addTab(self.tabs2, "Engineers")
        self.tabs.setFont(font)
        self.tabs.setStyleSheet("QTabWidget {background-color:#90AFC5;}")

    def widgets(self):
        # [Tab_1] Widgets
        # Main Left Layout Widgets
        self.productsTable = QTableWidget()
        

        self.productsTable.setColumnCount(11)
        self.productsTable.setColumnHidden(0, True)
        self.productsTable.setHorizontalHeaderItem(0, QTableWidgetItem("Product Id"))
        self.productsTable.setHorizontalHeaderItem(1, QTableWidgetItem("Description"))
        self.productsTable.setHorizontalHeaderItem(2, QTableWidgetItem("Manufacturer"))
        self.productsTable.setHorizontalHeaderItem(3, QTableWidgetItem("Model"))
        self.productsTable.setHorizontalHeaderItem(4, QTableWidgetItem("Unit"))
        self.productsTable.setHorizontalHeaderItem(5, QTableWidgetItem("Availability"))
        self.productsTable.setHorizontalHeaderItem(6, QTableWidgetItem("Supplier"))
        self.productsTable.setHorizontalHeaderItem(7, QTableWidgetItem("Date"))
        self.productsTable.setHorizontalHeaderItem(8, QTableWidgetItem("Price"))
        self.productsTable.setHorizontalHeaderItem(9, QTableWidgetItem("PO#"))
        self.productsTable.setHorizontalHeaderItem(10, QTableWidgetItem("Picked"))
        #self.productsTable.setHorizontalHeaderItem(11, QTableWidgetItem("Some"))

        self.productsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.productsTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.productsTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.productsTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.productsTable.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.productsTable.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        

        self.productsTable.doubleClicked.connect(self.selected_product) #TODO double click event
        self.productsTable.cellClicked.connect(self.sell_picked_clicked)
        self.productsTable.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.quitAction = QAction("Add Product", self)
        self.quitAction.triggered.connect(self.add_product_btn)
        self.productsTable.addAction(self.quitAction)

        self.productsTable.horizontalHeader().setStyleSheet(style.horizontalHeaderView())
        self.productsTable.setStyleSheet(style.forQTabWidget())

        # TODO Second Table
        self.productsTable2 = QTableWidget()
        self.productsTable2.setColumnCount(5)
        self.productsTable2.setColumnHidden(0, True)
        self.productsTable2.setHorizontalHeaderItem(0, QTableWidgetItem("id"))
        self.productsTable2.setHorizontalHeaderItem(1, QTableWidgetItem("Employee"))
        self.productsTable2.setHorizontalHeaderItem(2, QTableWidgetItem("Product"))
        self.productsTable2.setHorizontalHeaderItem(3, QTableWidgetItem("PO#"))
        self.productsTable2.setHorizontalHeaderItem(4, QTableWidgetItem("Units"))
        self.productsTable2.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.productsTable2.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.productsTable2.horizontalHeader().setStyleSheet(style.horizontalHeaderView())
        self.productsTable2.setStyleSheet(style.forQTabWidget())
        self.productsTable2.setSortingEnabled(True)
        # Right Top Layout Widgets
        self.searchText = QLabel("Search")
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Enter product name ...")
        self.searchEntry.setStyleSheet('QLineEdit{border-color: #A3C1DA; font-size: 12pt; font: Liberation Mono}')
        self.searchBtn = QPushButton("Search")
        self.searchBtn.setStyleSheet(style.search_btn_style())
        self.searchBtn.clicked.connect(self.search_products_btn)

        # Right Middle Layout Widgets
        self.ftn = QFont("Times", 10)
        self.allProducts = QRadioButton("All products")
        self.allProducts.setFont(QFont("Liberation Mono", 10))
        self.picked_items = QRadioButton("Picked")
        self.picked_items.setFont(QFont("Liberation Mono", 10))
        self.availableProducts = QRadioButton("Available")
        self.availableProducts.setFont(QFont("Liberation Mono", 10))
        self.notAvailableProducts = QRadioButton("Not available")
        self.notAvailableProducts.setFont(QFont("Liberation Mono", 10))
        self.listButton = QPushButton("List")
        self.listButton.setStyleSheet(style.search_btn_style())
        self.listButton.clicked.connect(self.list_products)

        # Right Bottom layout Widgets
        self.searchEntryPickedByEmployee = QLineEdit()
        self.searchEntryPickedByEmployee.setPlaceholderText("Enter employee name ...")
        self.searchEntryPickedByEmployee.setStyleSheet('QLineEdit{border-color: #A3C1DA; font-size: 12pt; font: Liberation Mono}')
        self.searchByEmployee = QPushButton("Search")
        self.searchByEmployee.setStyleSheet(style.search_btn_style())
        self.searchByEmployee.clicked.connect(self.search_products_by_emmployee_btn)

        # [Tab_2] Widgets
        self.membersTableWidgets = QTableWidget()
        self.membersTableWidgets.horizontalHeader().setStyleSheet(style.horizontalHeaderView())
        self.membersTableWidgets.setStyleSheet(style.forQTabWidget())
        self.membersTableWidgets.setColumnCount(4)
        self.membersTableWidgets.setHorizontalHeaderItem(0, QTableWidgetItem("Member Id"))
        self.membersTableWidgets.setHorizontalHeaderItem(1, QTableWidgetItem("Member Name"))
        self.membersTableWidgets.setHorizontalHeaderItem(2, QTableWidgetItem("Member Position"))
        self.membersTableWidgets.setHorizontalHeaderItem(3, QTableWidgetItem("Member ID"))
        self.membersTableWidgets.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.membersTableWidgets.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.membersTableWidgets.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.membersTableWidgets.doubleClicked.connect(self.selected_member)
        self.memberSearchText = QLabel("Search members")
        self.memberSearchEntry = QLineEdit()
        self.memberSearchEntry.setPlaceholderText("Enter name ...")
        self.membersearchBtn = QPushButton("Search")
        self.membersearchBtn.clicked.connect(self.search_members_btn)
        self.membersTableWidgets.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addMemberSmall = QAction("Add Member", self)
        self.addMemberSmall.triggered.connect(self.add_member)
        self.membersTableWidgets.addAction(self.addMemberSmall)

    def layouts(self):
        # Tab_l layouts
        self.main_layout = QHBoxLayout()
        self.main_left_layout = QVBoxLayout()
        self.main_right_layout = QVBoxLayout()
        self.right_childTop = QVBoxLayout()
        self.right_childBottom = QVBoxLayout()

        self.right_top_layout = QHBoxLayout()
        self.right_middle_layout = QHBoxLayout()
        self.right_bottom_layout = QHBoxLayout()

        self.topGroupBox = QGroupBox()
        self.topGroupBox.setStyleSheet(style.groupBoxStylee())
        self.middleGroupBox = QGroupBox()
        self.bottomGroupBox = QGroupBox("By employee")
        self.bottomGroupBox.setFont(QFont("Liberation Mono", 10))

        self.main_left_layout.addWidget(self.productsTable)

        self.right_top_layout.addWidget(self.searchEntry)
        self.right_top_layout.addWidget(self.searchBtn)
        self.topGroupBox.setLayout(self.right_top_layout)

        self.right_middle_layout.addWidget(self.allProducts)
        self.right_middle_layout.addWidget(self.picked_items)
        self.right_middle_layout.addWidget(self.availableProducts)
        self.right_middle_layout.addWidget(self.notAvailableProducts)
        self.right_middle_layout.addWidget(self.listButton)
        self.middleGroupBox.setLayout(self.right_middle_layout)

        self.right_bottom_layout.addWidget(self.searchEntryPickedByEmployee)
        self.right_bottom_layout.addWidget(self.searchByEmployee)
        self.bottomGroupBox.setLayout(self.right_bottom_layout)

        self.right_childTop.addWidget(self.topGroupBox, 20)
        self.right_childTop.addWidget(self.middleGroupBox, 20)
        self.right_childBottom.addWidget(self.bottomGroupBox)
        self.right_childBottom.addWidget(self.productsTable2)
        self.main_right_layout.addLayout(self.right_childTop,20)
        self.main_right_layout.addLayout(self.right_childBottom, 70)

        self.main_layout.addLayout(self.main_left_layout, 70)
        self.main_layout.addLayout(self.main_right_layout, 30)
        self.tabs1.setLayout(self.main_layout)

        # Tab_2 Layouts
        self.memberMainLayout = QHBoxLayout()
        self.memberLeftLayout = QHBoxLayout()
        self.memberLeftLayout.addWidget(self.membersTableWidgets)
        self.memberMainLayout.addLayout(self.memberLeftLayout)
        self.tabs2.setLayout(self.memberMainLayout)

    def closeEvent(self, event):
        
        if self.update_to_DB.text() == 'Update':
            result = QMessageBox.question(self, "Confirm Exit?", "You didn't save changes to DataBase\nPlease save Changes", QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)
            event.ignore()
            if result == QMessageBox.Save:
                self.update_DB_database()
                #event.accept()
            elif result == QMessageBox.No:
                file = open('database_backup/state.txt', 'w')
                file.write('state')
                event.accept()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            #self.close()
            self.productsTable.sortItems(10, Qt.AscendingOrder)
            self.displayProducts()
         
        elif e.key() == Qt.Key_Return:
            self.search_products_btn()


    def exit_programm_func(self):
        mbox = QMessageBox.information(self, "Warning", "Are you sure yo exit?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            sys.exit()

    def about_programm(self):
        print("About software ...") # TODO delete line

    def add_product_btn(self):
        self.newProductWindow = addproduct.AddProduct(self)

    def add_member(self):
        self.newMemberWindow = addmember.AddMember(self)


    def displayProducts(self):
        self.productsTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.productsTable.rowCount())):
            self.productsTable.removeRow(i)
        query = cur.execute("SELECT product_id,description,product_manufacturer,product_name,product_quota,product_availability,supplier,date_adding,product_price,product_po,picked_by FROM products")

        for row_data in query:
            row_number = self.productsTable.rowCount()
            #print("Row ", row_number)
            self.productsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                #print("Column ", column_number)

                if row_data[4] == 0:
                    self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    
                    # Setting Red color for Anavailable items
                    if column_number == 10 and row_data[4] == 0:
                        continue
                    self.productsTable.item(row_number, column_number).setBackground(QColor(255, 204, 204))

                elif str(row_data[10]) == 'Picked': #10
                    
                    self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                    # Setting gray color for picked items
                    if column_number == 10:
                        continue
                    self.productsTable.item(row_number, column_number).setBackground(QColor(180, 190, 204))
                    
                else:                    
                    self.productsTable.setItem(row_number, column_number,QTableWidgetItem(str(data)))
                    
                    

        self.productsTable.setEditTriggers(QAbstractItemView.NoEditTriggers) #TODO Check this line for table
        self.productsTable.resizeColumnsToContents()
        #self.productsTable.setSortingEnabled(True)
        #oldSort = self.productsTable.horizontalHeader().sortIndicatorSection()
        #oldOrder = self.productsTable.horizontalHeader().sortIndicatorOrder()
        #self.productsTable.setSortingEnabled(False)

        #self.productsTable.sortItems(oldSort, oldOrder)
        self.productsTable.setSortingEnabled(True)
        self.productsTable.sortItems(1, Qt.AscendingOrder)

    def displayMembers(self):
        self.membersTableWidgets.setFont(QFont("Times", 12))

        for i in reversed(range(self.membersTableWidgets.rowCount())):
            self.membersTableWidgets.removeRow(i)

        query_members = cur.execute("SELECT * FROM members")
        for row_data in query_members:
            row_number = self.membersTableWidgets.rowCount()
            self.membersTableWidgets.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membersTableWidgets.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.membersTableWidgets.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selected_product(self):
        global productId
        listProduct = []
        for i in range(0, 8):
            listProduct.append(self.productsTable.item(self.productsTable.currentRow(), i).text())

        productId = listProduct[0]
        self.display = DisplayProduct(self)
        self.display.show()

    def selected_member(self):
        global memberId
        listMember = []
        for i in range(0, 4):
            listMember.append(self.membersTableWidgets.item(self.membersTableWidgets.currentRow(), i).text())
        memberId = listMember[0]
        self.displayMember = DisplayMember(self)
        self.displayMember.show()

    def search_products_btn(self):
        value = self.searchEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning!", "Search query is Empty!")
        else:
            self.searchEntry.setText("")
            #query = cur.execute("")
            query = ('SELECT product_id,description,product_manufacturer,product_name,product_quota,product_availability,supplier,date_adding,product_price,product_po,picked_by FROM products WHERE description LIKE ? or product_manufacturer LIKE ? or product_po LIKE ? or product_name LIKE ? or supplier LIKE ?')
            results = cur.execute(query, ('%'+value+'%','%'+value+'%','%'+value+'%','%'+value+'%','%'+value+'%')).fetchall()
            if results == []:
                QMessageBox.information(self, "Warning!", "There is no such a product or manufacturer.")
            else:
                for i in reversed(range(self.productsTable.rowCount())):
                    self.productsTable.removeRow(i)
                for row_data in results:
                    row_number = self.productsTable.rowCount()
                    self.productsTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        if str(row_data[5]) == "UnAvailable":
                            self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                            self.productsTable.item(row_number, column_number).setBackground(QColor(255, 204, 204))
                            self.productsTable.sortItems(10, Qt.AscendingOrder)
                        elif str(row_data[10]) == 'Picked' and str(row_data[5]) == "Available":
                            print("Picked")
                            self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                            self.productsTable.item(row_number, column_number).setBackground(QColor(180, 190, 204))
                            self.productsTable.sortItems(10, Qt.AscendingOrder)
                        else:
                            self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                            self.productsTable.sortItems(10, Qt.AscendingOrder)

    # TODO Working on
    def search_products_by_emmployee_btn(self):
        empl_name = self.searchEntryPickedByEmployee.text()
        if empl_name == "":
            QMessageBox.information(self, "Warning!", "Search query is Empty!")
        else:
            self.searchEntryPickedByEmployee.setText("")
            query_by_empl = ("SELECT product_id, taker_name, product_personal_name,picked_product_name,items_amount,time_day_picking FROM take_product WHERE taker_name LIKE ? or product_personal_name LIKE ? or picked_product_name LIKE ?")
            query = cur.execute(query_by_empl, ('%'+empl_name+'%','%'+empl_name+'%','%'+empl_name+'%')).fetchall()
            if query == []:
                for i in reversed(range(self.productsTable2.rowCount())):
                    self.productsTable2.removeRow(i)
                QMessageBox.information(self, "Warning!", "No item were picked by ' {} '".format(empl_name))


            else:
                for i in reversed(range(self.productsTable2.rowCount())):
                    self.productsTable2.removeRow(i)

                for row_data in query:
                    row_number = self.productsTable2.rowCount()

                    self.productsTable2.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.productsTable2.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def search_members_btn(self):
        value = self.memberSearchEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning!", "Search query is Empty!")
        else:
            self.memberSearchEntry.setText("")

            query = ('SELECT * FROM members WHERE member_name LIKE ? or member_surname LIKE ? or member_phone LIKE ?')
            results = cur.execute(query, ('%'+value+'%','%'+value+'%','%'+value+'%')).fetchall()
            if results == []:
                QMessageBox.information(self, "Warning!", "There is no employee. Search for another one.")
            else:
                for i in reversed(range(self.membersTableWidgets.rowCount())):
                    self.membersTableWidgets.removeRow(i)
                for row_data in results:
                    row_number = self.membersTableWidgets.rowCount()
                    self.membersTableWidgets.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.membersTableWidgets.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def list_products(self):
        if self.allProducts.isChecked() == True:
            self.productsTable.sortItems(10, Qt.AscendingOrder)
            self.displayProducts()
        elif self.picked_items.isChecked() == True:
            self.productsTable.sortItems(10, Qt.AscendingOrder)
            query_selected = ("SELECT product_id,description,product_manufacturer,product_name,product_quota,product_availability,supplier,date_adding,product_price,product_po,picked_by FROM products WHERE picked_by='Picked'")

            products = cur.execute(query_selected).fetchall()

            for i in reversed(range(self.productsTable.rowCount())):
                self.productsTable.removeRow(i)
            for row_data in products:
                row_number = self.productsTable.rowCount()
                self.productsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    if str(row_data[5]) == "UnAvailable":
                        self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                        self.productsTable.item(row_number, column_number).setBackground(QColor(255, 204, 204))
                    elif str(row_data[10]) == 'Picked' and str(row_data[5]) == "Available":
                        print("Picked")
                        self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                        self.productsTable.item(row_number, column_number).setBackground(QColor(180, 190, 204))

        elif self.availableProducts.isChecked() == True:
            self.productsTable.sortItems(10, Qt.AscendingOrder)
            query = ("SELECT product_id,description,product_manufacturer,product_name,product_quota,product_availability,supplier,date_adding,product_price,product_po,picked_by FROM products WHERE product_availability='Available'")
            products = cur.execute(query).fetchall()
            

            for i in reversed(range(self.productsTable.rowCount())):
                self.productsTable.removeRow(i)
            for row_data in products:
                row_number = self.productsTable.rowCount()
                self.productsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    if str(row_data[5]) == "UnAvailable":
                        self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                        self.productsTable.item(row_number, column_number).setBackground(QColor(255, 204, 204))
                    elif str(row_data[10]) == 'Picked' and str(row_data[5]) == "Available":
                        print("Picked")
                        self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                        self.productsTable.item(row_number, column_number).setBackground(QColor(180, 190, 204))

                    else:
                        self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        elif self.notAvailableProducts.isChecked() == True:
            self.productsTable.sortItems(10, Qt.AscendingOrder)
            query = ("SELECT product_id,description,product_manufacturer,product_name,product_quota,product_availability,supplier,date_adding,product_price,product_po,picked_by FROM products WHERE product_availability='UnAvailable'")
            products = cur.execute(query).fetchall()
            

            for i in reversed(range(self.productsTable.rowCount())):
                self.productsTable.removeRow(i)
            for row_data in products:
                row_number = self.productsTable.rowCount()
                self.productsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.productsTable.item(row_number, column_number).setBackground(QColor(255, 204, 204))

    def sell_product(self):
        #try:
        self.takeOneItem = take_item.TakeProductItem(self)
        #except:
            #QMessageBox.warning(self, "Warning!", "No items left! Contact manager.")

    def return_product(self):
        try:
            self.returnOneItem = return_item.ReturnProductItem(self)
        except:
            QMessageBox.warning(self, "Warning!", "No Item was taken!")

    def tabChanged(self):
        self.displayProducts()
        self.displayMembers()

    def refresh_all_tables(self):
        self.close()
        self.main = Main()

    def sell_picked_clicked(self, row, column):
        some = self.productsTable.item(row, 9)
        self.id = some.text()
        
        if column == 10:
            query = ("SELECT * FROM products WHERE product_po=?")
            product = cur.execute(query, (self.id,)) # single item tuple=(1,)

            for i in product:
                if i[10] == 'Picked':
                    self.newMemberWindow = takedItem.TakedItem(self.id)
                    self.newMemberWindow.displayProducts()
                else:
                    QMessageBox.information(self, "Warning", "No items were picked by {}")


    def enter_full_screen_mode(self):
        self.showFullScreen()

    def save_to_EXCEL_file(self):
        wb = Workbook()
        path, _ = QFileDialog.getSaveFileName(self, "Save File", QDir.homePath() + "/exports.xls", "XLS Files(*.xls *.txt)")
        if path:
            sheet1 = wb.add_sheet('exports')
            
            
            #sheet1.write(3,0, "Some") # 3-> row, o-> column
            for column in range(self.productsTable.columnCount()):
                header = self.productsTable.horizontalHeaderItem(column)
                sheet1.write(0,column, header.text())

            for column in range(self.productsTable.columnCount()):
                for row in range(self.productsTable.rowCount()):
                    item = self.productsTable.item(row, column)
                    sheet1.write(row+1, column, item.text())

        wb.save(path)

    def check_staticctics(self):
        sum = 0
        self.statisctic_window = statictic_main.StatisticClass()
        print("Done") # TODO delete line
        sq = cur.execute("SELECT product_quota FROM products").fetchall()
        for i in sq:
            sum+= i[0]
        print("Sum: ", sum) # TODO delete line

    def clear_all_items(self):
        self.password_window = password.PasswordInitializer()
        if self.password_window.exec_() == QDialog.Accepted:

            mbox = QMessageBox.warning(self, "Warning", "Delete All items?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if mbox == QMessageBox.Yes:

                try:
                    cur.execute("DELETE FROM products")
                    cur.execute("DELETE FROM members")
                    cur.execute("DELETE FROM take_product")
                    cur.execute("DELETE FROM transaction_history")
                    cur.execute("DELETE FROM transactions")
                    con.commit()

                    folder = 'src/img'
                    for the_file in os.listdir(folder):
                        file_path = os.path.join(folder, the_file)
                        try:
                            if os.path.isfile(file_path):
                                if file_path == r"src/img\default_img.png":
                                    pass
                                elif file_path == r"src/img\upload_new_img.png":
                                    pass
                                else:
                                    print("Deleting, ", file_path)
                                    os.unlink(file_path)
                        except Exception as e:
                            QMessageBox.information(self, "Information!", "{}".format(e))

                    QMessageBox.information(self, "Information!", "Every table was cleaned successfully!")
                    self.refresh_all_tables()
                except:
                    QMessageBox.warning(self, "Information!", "Something Wrong! Please refresh Window")

    def update_DB_database(self):
        self.updating = update_new_to_DB.ConnectingUpdating(self)


class DisplayMember(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setWindowTitle("Member Details")
        self.setWindowIcon(QIcon("src/icons/add_emp.png"))
        self.setGeometry(550, 250, 350, 600)
        self.setFixedSize(700, 300)
        self.main = main
        self.ui()
        self.show()

    def ui(self):
        self.memberDetails()
        self.memberWidgets()
        self.layouts()

    def memberDetails(self):
        global memberId
        query = ("SELECT * FROM members WHERE member_id=?")
        member = cur.execute(query, (memberId,)).fetchone()
        print(member[1])
        self.memberName = member[1]
        self.memberSurname = member[2]
        self.memberPhone = member[3]
        self.memberPhoto = member[4]


    def memberWidgets(self):
        # Widgets of top layout
        self.memberImg = QLabel()
        self.memberImg.setPixmap(QPixmap('src/img/{}'.format(self.memberPhoto)))
        self.memberImg.setStyleSheet(style.membersPicsStyle())
        self.memberImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Semiland Engineer")
        self.titleText.setAlignment(Qt.AlignCenter)

        # Widgets of bottom layout
        self.nameEntry = QLineEdit()
        self.nameEntry.setStyleSheet(style.search_btn_style_2())
        self.nameEntry.setText(self.memberName)
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setStyleSheet(style.search_btn_style_2())
        self.surnameEntry.setText(self.memberSurname)
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setStyleSheet(style.search_btn_style_2())
        self.phoneEntry.setText(self.memberPhone)
        self.updateBtn = QPushButton("Update")
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.setStyleSheet(style.simple_btn_style())
        self.deleteBtn.clicked.connect(self.delete_member)
        self.updateBtn.clicked.connect(self.update_member)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.topLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.member_top_frame())
        self.leftFrame = QFrame()
        self.leftFrame.setLayout(self.rightLayout)
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet(style.member_bottom_frame())
        # Add widgets
        #self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.memberImg)
        self.topFrame.setLayout(self.topLayout)


        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Position: "), self.surnameEntry)
        self.bottomLayout.addRow(QLabel("ID: "), self.phoneEntry)
        #self.bottomLayout.addRow(QLabel(""), self.updateBtn)
        self.bottomLayout.addRow(QLabel(""), self.deleteBtn)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.mainLayout.addWidget(self.leftFrame)

        self.setLayout(self.mainLayout)

    def delete_member(self):
        global memberId
        mbox = QMessageBox.information(self, "Warning!", "Are you sure to delete this member?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if mbox == QMessageBox.Yes:
            try:
                query = "DELETE FROM members WHERE member_id=?"
                cur.execute(query, (memberId,))
                con.commit()
                self.main.displayMembers()
                QMessageBox.information(self, "Information!", "User has been deleted successfuly!")
                self.close()
            except:
                QMessageBox.information(self, "Information!", "User has not been deleted")

    def update_member(self):
        global memberId
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()

        if (name and surname and phone != ""):
            try:
                query = 'UPDATE members set member_name=?, member_surname=?, member_phone=? WHERE member_id=?'
                cur.execute(query, (name, surname,phone,memberId))
                con.commit()
                QMessageBox.information(self, "Info", "Product has been updated!")
            except:
                QMessageBox.information(self, "Info", "Product has not been updated!!!!")
        else:
            QMessageBox.information(self, "Info", "Please fill all the fields!!!!")



class DisplayProduct(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setWindowTitle("Details")
        self.setWindowIcon(QIcon("src/icons/add_emp.png"))
        self.setGeometry(50, 50, 650, 600)
        self.setFixedSize(self.size())
        self.mainWindow = None
        copyfile('src/icons/default_img.png', 'src/img/default_img.png')
        copyfile('src/icons/upload_new_img.png', 'src/img/upload_new_img.png')
        self.snippingTool = SnippingWidget(self)
        self.main = main
        self.ui()
        self.show()

    def ui(self):
        self.productDetails()
        self.widgets()
        self.layouts()

    def productDetails(self):
        global productId
        query = ("SELECT * FROM products WHERE product_id=?")
        product = cur.execute(query, (productId,)).fetchone()  # single item tuple=(1,)
        print(product)
        self.description = product[1]
        self.productManufacturer = product[2]
        self.productName = product[3]
        self.productQuota = product[4]
        self.productStatus = product[5]
        self.supplier = product[6]
        self.productPrice = product[8]
        self.productPo = product[9]
        self.productImg = product[11]


    def widgets(self):
        # Top layout widget
        self.product_Img = QLabel()
        self.img = QPixmap(self.productImg)
        self.product_Img.setPixmap(self.img)
        self.product_Img.mousePressEvent = self.snipping_tool
        self.product_Img.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Update Product")
        self.titleText.setAlignment(Qt.AlignCenter)

        # Bottom layout widget
        self.descriptionEntry = QLineEdit()
        self.descriptionEntry.setText(self.description)
        self.descriptionEntry.setStyleSheet(style.search_btn_style_2())

        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.productName)
        self.nameEntry.setStyleSheet(style.search_btn_style_2())
        self.manufacturerEntry = QLineEdit()
        self.manufacturerEntry.setStyleSheet(style.search_btn_style_2())
        self.manufacturerEntry.setText(self.productManufacturer)
        self.PoNumberEntry = QLineEdit()
        self.PoNumberEntry.setStyleSheet(style.search_btn_style_2())
        self.PoNumberEntry.setText(str(self.productPo))
        self.priceEntry = QLineEdit()
        self.priceEntry.setStyleSheet(style.search_btn_style_2())
        self.priceEntry.setText(str(self.productPrice))
        self.supplierEntry = QLineEdit()
        self.supplierEntry.setText(self.supplier)
        self.supplierEntry.setStyleSheet(style.search_btn_style_2())
        self.quotaEntry = QLineEdit()
        self.quotaEntry.setStyleSheet(style.search_btn_style_2())
        self.quotaEntry.setText(str(self.productQuota))
        self.availableCombo = QComboBox()
        self.availableCombo.setStyleSheet(style.search_btn_style_3())
        self.availableCombo.addItems(["Available", "UnAvailable"])
        self.availableCombo.setStyleSheet("QComboBox{font-size: 13pt; font: Liberation Mono}")
        #self.uploadBtn = QPushButton("Upload")
        #self.uploadBtn.setStyleSheet("QPushButton{font-size: 13pt; font: Liberation Mono}")
        #self.uploadBtn.clicked.connect(self.uploadImg)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.setStyleSheet("QPushButton{font-size: 13pt; font: Liberation Mono}")
        self.deleteBtn.clicked.connect(self.delete_product)
        self.updateBtn = QPushButton("Update")
        self.updateBtn.setStyleSheet("QPushButton{font-size: 13pt; font: Liberation Mono}")
        self.updateBtn.clicked.connect(self.update_product)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.product_top_frame())
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet(style.product_bottom_frame())

        # Add widgets
        #self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.product_Img)
        self.topFrame.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel("Description: "), self.descriptionEntry)
        self.bottomLayout.addRow(QLabel("Manufacturer: "), self.manufacturerEntry)
        self.bottomLayout.addRow(QLabel("Model: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("PO #: "), self.PoNumberEntry)
        self.bottomLayout.addRow(QLabel("Price: "), self.priceEntry)
        self.bottomLayout.addRow(QLabel("Supplier: "), self.supplierEntry)
        self.bottomLayout.addRow(QLabel("Units: "), self.quotaEntry)
        self.bottomLayout.addRow(QLabel("Status: "), self.availableCombo)
        #self.bottomLayout.addRow(QLabel("Image: "), self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""), self.deleteBtn)
        self.bottomLayout.addRow(QLabel(""), self.updateBtn)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def uploadImg(self):
        size = (256, 256)
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload Image", '', "Image Files (*.jpg *.png)")
        if ok:
            self.productImg = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("src/img/{0}".format(self.productImg))
            self.product_Img.setPixmap(QPixmap('src/icons/{}'.format(self.productImg)))

    def update_product(self):
        global productId
        global defaulImg
        img_name = os.path.basename(defaulImg)
        defaulImgSrc = 'src/img/{}'.format(img_name)
        name = self.nameEntry.text()
        manufacturer = self.manufacturerEntry.text()
        description = self.descriptionEntry.text()
        supplier = self.supplierEntry.text()
        productId_po = self.PoNumberEntry.text()
        print("productId_po--> ",productId_po)
        try:
            price = self.priceEntry.text()
            #price = float(price) #TODO Price integer now
            quota = int(self.quotaEntry.text())
            status = self.availableCombo.currentText()
            print("Def IMG IS: .", defaulImgSrc)
            if (name and manufacturer and price and quota != ""):
                img_to_delete = cur.execute("SELECT product_img FROM products WHERE product_id=?", (productId,)).fetchone()

                if len(os.listdir('src/current_pictures/')) == 0:
                    print("Empty Directory")
                    defaulImgSrc = img_to_delete[0]
                    print("defaulImgSrc->> ", defaulImgSrc)
                else:
                    print("There is some items")
                    os.unlink(img_to_delete[0])
                
                query = 'UPDATE products set description=?, supplier=?, product_name=?, product_manufacturer=?, product_price=?, product_quota=?, product_img=?, product_availability=? WHERE product_id=?'
                cur.execute(query, (description, supplier, name, manufacturer, price, quota, defaulImgSrc, status, productId))
                cur.execute("UPDATE products set product_po=? WHERE product_id=?", (productId_po, productId))
                con.commit()
                print("Commited!")
                self.main.productsTable.sortItems(10, Qt.AscendingOrder)
                self.main.displayProducts()
                QMessageBox.information(self, "Info", "Product has been updated!")
                # TODO delete line

                #except:
                    #QMessageBox.information(self, "Info", "Product has not been updated!!!!")
            else:
                QMessageBox.information(self, "Info", "Please fill all the fields!!!!")
        except:
            QMessageBox.information(self, "Information", "Please enter integer Value for price")

        copyfile("db_database/main_database.db", "database_backup/main_database.db")
        copyfile(defaulImg, 'src/img/{}'.format(img_name))
        copyfile('src/icons/default_img.png', 'src/img/default_img.png')
        self.main.update_to_DB.setIcon(QIcon('src/icons/updateToServer.png'))
        self.main.update_to_DB.setText("Update")
        self.main.productsTable.sortItems(1, Qt.AscendingOrder)
        self.main.productsTable.sortItems(10, Qt.AscendingOrder)
        self.main.displayProducts()
        folder = 'src/current_pictures'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                QMessageBox.warning(self, "Warning!", "{}".format(e))

###############################################

    def snipping_tool(self, event):
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

    def delete_product(self):
        global productId

        mbox = QMessageBox.question(self, "Warning!", "Are you sure to delete this product?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if (mbox == QMessageBox.Yes):

            try:
                img_to_delete = cur.execute("SELECT product_img FROM products WHERE product_id=?",(productId,)).fetchone()
                print(img_to_delete[0])
                if img_to_delete[0] == "src/img/upload_new_img.png":
                    pass
                else:
                    os.unlink(img_to_delete[0])
                cur.execute("DELETE FROM products WHERE product_id=?", (productId,))
                con.commit()
                self.main.productsTable.sortItems(10, Qt.AscendingOrder)
                self.main.displayProducts()

                QMessageBox.information(self, "Information!", "Product has been deleted!")
                self.main.update_to_DB.setIcon(QIcon('src/icons/updateToServer.png'))
                self.main.update_to_DB.setText("Update")
                self.close()

            except:
                QMessageBox.information(self, "Information!", "Product has not been deleted!")
        else:
            QMessageBox.information(self, "Information!", "Product has not been deleted!")


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
            self.add_prod.product_Img.setPixmap(QPixmap(real_img_name_current))
        except:
            pass
        defaulImg = real_img_name_current
        print("Real Image: ", defaulImg)
        self.close()

def main():
    app = QApplication(sys.argv)
    style = """
        QWidget{
            ;
        }
    """
    app.setStyleSheet(style)
    window = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
