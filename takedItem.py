from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
import style


con = sqlite3.connect("db_database/main_database.db")
cur = con.cursor()


class TakedItem(QWidget):
    def __init__(self, id_product_name):
        super().__init__()
        self.setWindowTitle("Statistic")
        self.setWindowIcon(QIcon('src/icons/power_module.png'))
        self.setGeometry(650, 300, 1200, 500)
        self.setFixedSize(self.size())
        self.id_product_name = id_product_name
        print(self.id_product_name)

        self.ui()
        self.show()

    def ui(self):

        self.widgets()
        self.layouts()

    def widgets(self):
        self.takedItemsTable = QTableWidget()

        self.takedItemsTable.setColumnCount(4)
        self.takedItemsTable.setColumnHidden(0, True)
        self.takedItemsTable.setHorizontalHeaderItem(0, QTableWidgetItem("Product Id"))
        self.takedItemsTable.setHorizontalHeaderItem(1, QTableWidgetItem("Employee"))
        self.takedItemsTable.setHorizontalHeaderItem(2, QTableWidgetItem("Items picked"))
        self.takedItemsTable.setHorizontalHeaderItem(3, QTableWidgetItem("Date and time"))
        self.takedItemsTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.takedItemsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.takedItemsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.takedItemsTable.horizontalHeader().setStyleSheet(style.horizontalHeaderView())
        self.takedItemsTable.setStyleSheet(style.forQTabWidget())


    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.childLayout = QVBoxLayout()
        self.childLayout.addWidget(self.takedItemsTable)
        self.mainLayout.addLayout(self.childLayout)
        self.setLayout(self.mainLayout)

    def displayProducts(self):
        for i in reversed(range(self.takedItemsTable.rowCount())):
            self.takedItemsTable.removeRow(i)

        query = cur.execute("SELECT product_id, taker_name, items_amount, time_day_picking, picked_product_name FROM take_product WHERE picked_product_name=?", (self.id_product_name,)).fetchall()

        for row_data in query:
            row_number = self.takedItemsTable.rowCount()
            self.takedItemsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.takedItemsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))



