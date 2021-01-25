import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QTime, QDate, QDateTime
import sqlite3
import style


con = sqlite3.connect("db_database/main_database.db")
cur = con.cursor()

defaultImg = "src/icons/add_emp.png"


class ReturnProductItem(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setWindowTitle("Return Product")
        self.setWindowIcon(QIcon("src/icons/return.png"))
        self.setGeometry(650, 300, 850, 350)
        self.setFixedSize(self.size())
        self.main = main
        self.ui()
        self.show()

    def ui(self):
        self.widgets()
        self.layouts()

    def widgets(self):

        self.employeeCombo = QComboBox()
        self.employeeCombo.setStyleSheet("QComboBox{font-size: 13pt; font: Liberation Mono}")
        self.productCombo = QComboBox()
        self.productCombo.setStyleSheet("QComboBox{font-size: 13pt; font: Liberation Mono}")
        self.quantityCombo = QComboBox()
        self.quantityCombo.setStyleSheet("QComboBox{font-size: 13pt; font: Liberation Mono}")
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.setStyleSheet("QPushButton{font-size: 13pt; font: Liberation Mono}")
        self.employeeCombo.currentIndexChanged.connect(self.changedEmployeeCombo)
        self.productCombo.currentIndexChanged.connect(self.changedProductCombo)
        self.submitBtn.clicked.connect(self.return_product)

        self.fetch_data_from = cur.execute("SELECT DISTINCT taker_name,take_by FROM take_product").fetchall()
        items_taken = cur.execute("SELECT product_personal_name FROM take_product WHERE taker_name=?", (self.fetch_data_from[0][0],))

        for member in self.fetch_data_from:
            self.employeeCombo.addItem(member[0], member[1])

        try:

            for i in items_taken:
                self.productCombo.addItem(str(i[1]),i[0])

        except:
            raise Exception

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrameLayout = QFrame()
        self.topFrameLayout.setStyleSheet(style.sell_product_top_frame())
        self.bottomFrameLayout = QFrame()
        self.bottomFrameLayout.setStyleSheet(style.sell_product_bottom_frame())
        # Add widgets
        self.bottomLayout.addRow(QLabel("Employee: "), self.employeeCombo)
        self.bottomLayout.addRow(QLabel("Product: "), self.productCombo)
        self.bottomLayout.addRow(QLabel("Quantity: "), self.quantityCombo)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrameLayout.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.bottomFrameLayout)
        self.setLayout(self.mainLayout)

    def changedEmployeeCombo(self):
        self.quantityCombo.clear()
        self.productCombo.clear()
        employee_id = self.employeeCombo.currentData()
        items_taken = cur.execute("SELECT * FROM take_product WHERE take_by=?", (employee_id,)).fetchall()

        for i in items_taken:
            self.productCombo.addItem(str(i[6]), i[4])

    def changedProductCombo(self):
        self.quantityCombo.clear()
        employee_id = self.employeeCombo.currentData()
        product_id = self.productCombo.currentData()
        query = cur.execute("SELECT items_amount FROM take_product WHERE picked_product_name=? AND take_by=?", (product_id,employee_id)).fetchall()

        for i in query:
            for i in range(1, i[0]+1):
                self.quantityCombo.addItem(str(i))


    def return_product(self):
        emp_name = self.employeeCombo.currentText()
        emp_id = self.employeeCombo.currentData()
        prod_name = self.productCombo.currentText()
        prod_id = self.productCombo.currentData()
        quantity_return = self.quantityCombo.currentText()
        datetime = QDateTime.currentDateTime().toString(3)

        current_quantity_prod = cur.execute("SELECT product_quota FROM products WHERE product_po=?", (prod_id,)).fetchone()
        current_quantity_return = cur.execute("SELECT items_amount FROM take_product WHERE picked_product_name=? AND take_by=?", (prod_id, emp_id)).fetchone()
        new_value_prod = int(current_quantity_prod[0]) + int(quantity_return)
        new_val_return = int(current_quantity_return[0]) - int(quantity_return)
        cur.execute("UPDATE products SET product_quota=?, product_availability=? WHERE product_po=?", (new_value_prod, 'Available', prod_id))
        cur.execute("UPDATE take_product SET items_amount=? WHERE take_by=? AND picked_product_name=?", (new_val_return, emp_id, prod_id))

        if new_val_return == 0:

            cur.execute("DELETE FROM take_product WHERE picked_product_name=? AND take_by=?", (prod_id, emp_id))
            de = cur.execute("SELECT * from take_product WHERE picked_product_name=?", (prod_id,)).fetchall()
            if de:
                print("Still Data")
            else:
                print("No data")
                cur.execute("UPDATE products SET picked_by=? WHERE product_po=?", ('None', prod_id))

        transactionQuery = ("INSERT INTO 'transaction_history' (item_name_transaction, item_po_transaction, employee_name_transaction, amount_transaction, date_of_transaction, action_transaction) VALUES (?,?,?,?,?,?)")
        cur.execute(transactionQuery, (prod_name, prod_id, emp_name, quantity_return, datetime, 'Returned'))
        self.main.update_to_DB.setIcon(QIcon('src/icons/updateToServer.png'))
        self.main.update_to_DB.setText("Update")
        con.commit()
        self.main.productsTable.sortItems(10, Qt.AscendingOrder)
        self.main.displayProducts()
        self.close()