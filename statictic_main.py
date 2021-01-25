import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
import style


con = sqlite3.connect("db_database/main_database.db")
cur = con.cursor()


class StatisticClass(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transactions")
        self.setWindowIcon(QIcon('src/icons/power_module.png'))
        self.setGeometry(300, 200, 1500, 700)
        self.ui()
        self.show()

    def ui(self):
        self.widgets()
        self.layouts()
        self.displayProducts()

    def widgets(self):
        self.statisticTable = QTableWidget()
        self.statisticTable.horizontalHeader().setStyleSheet(style.horizontalHeaderView())
        self.statisticTable.setStyleSheet(style.forQTabWidget())
        self.statisticTable.setColumnCount(7)
        self.statisticTable.setColumnHidden(0, True)
        self.statisticTable.setHorizontalHeaderItem(0, QTableWidgetItem("Transaction ID"))
        self.statisticTable.setHorizontalHeaderItem(1, QTableWidgetItem("Product Name"))
        self.statisticTable.setHorizontalHeaderItem(2, QTableWidgetItem("PO#"))
        self.statisticTable.setHorizontalHeaderItem(3, QTableWidgetItem("Employee"))
        self.statisticTable.setHorizontalHeaderItem(4, QTableWidgetItem("Amount"))
        self.statisticTable.setHorizontalHeaderItem(5, QTableWidgetItem("Date&Time"))
        self.statisticTable.setHorizontalHeaderItem(6, QTableWidgetItem("Action"))
        self.statisticTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.statisticTable.horizontalHeader().setSectionResizeMode(1), QHeaderView.Stretch
        self.statisticTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.statisticTable.setFont(QFont("Times", 10))


    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.childLayout = QVBoxLayout()
        self.childLayout.addWidget(self.statisticTable)
        self.mainLayout.addLayout(self.childLayout)
        self.setLayout(self.mainLayout)

    def displayProducts(self):

        for i in reversed(range(self.statisticTable.rowCount())):
            self.statisticTable.removeRow(i)

        query = cur.execute("SELECT * FROM transaction_history")
        for row_data in query:
            print(row_data[6])
            row_number = self.statisticTable.rowCount()
            self.statisticTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):

                if row_data[6] == 'Picked':
                    self.statisticTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.statisticTable.item(row_number, column_number).setBackground(QColor(255, 204, 204))
                elif row_data[6] == 'Returned':
                    self.statisticTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.statisticTable.item(row_number, column_number).setBackground(QColor(204, 229, 255))
