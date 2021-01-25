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


class TakeProductItem(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setWindowTitle("Sell Product")
        self.setWindowIcon(QIcon("src/icons/add_emp.png"))
        self.setGeometry(650, 300, 850, 650)
        self.setFixedSize(self.size())
        self.main = main
        self.ui()
        self.show()

    def ui(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Top layout widgets
        self.sellProductImg = QLabel()
        self.img = QPixmap('src/icons/take_item.PNG')
        self.sellProductImg.setPixmap(self.img)
        self.sellProductImg.setAlignment(Qt.AlignCenter)

        # Bottom layout widgets
        self.productCombo = QComboBox()
        self.productCombo.setStyleSheet("QComboBox{font-size: 13pt; font: Liberation Mono}")
        self.productCombo.currentIndexChanged.connect(self.changeComboValue)
        self.productManufacturerCombo = QComboBox()
        self.productManufacturerCombo.setStyleSheet("QComboBox{font-size: 13pt; font: Liberation Mono}")
        self.productManufacturerCombo.currentIndexChanged.connect(self.changeManufacturerCombo)
        self.productModelCombo = QComboBox()
        self.productModelCombo.setStyleSheet("QComboBox{font-size: 13pt; font: Liberation Mono}")
        self.productModelCombo.currentIndexChanged.connect(self.changeModelCombo)
        #self.productManufacturerCombo.currentIndexChanged.connect(self.changeComboValue)
        self.memberCombo = QComboBox()
        self.memberCombo.setStyleSheet("QComboBox{font-size: 13pt; font: Liberation Mono}")
        self.quantityCombo = QComboBox()
        self.quantityCombo.setStyleSheet("QComboBox{font-size: 13pt; font: Liberation Mono}")
        self.unique_id = QLineEdit()
        self.unique_id.setStyleSheet("QLineEdit{font-size: 13pt; font: Liberation Mono}")
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.setStyleSheet("QPushButton{font-size: 13pt; font: Liberation Mono}")
        self.submitBtn.clicked.connect(self.sell_product)

        # TODO The old version Uncomment in a case of ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        # TODO products
        query1 = ("SELECT * FROM products WHERE product_availability=?")
        products = cur.execute(query1, ('Available',)).fetchall()

        # TODO members
        query2 = ("SELECT member_id, member_name FROM members")
        members = cur.execute(query2).fetchall()
        for member in members:
            self.memberCombo.addItem(member[1], member[0])

        try:
            quantity = products[0][4]

        except:
            pass

        for product in products:
            self.productCombo.addItem(product[1], product[0])
            print("What is that? ", product[1], product[0])

        

        try:
            self.quantityCombo.clear()
            for i in range(1, quantity+1):
                self.quantityCombo.addItem(str(i))
        except:
            raise Exception

        """

        # TODO members
        query2 = ("SELECT member_id, member_name FROM members")
        members = cur.execute(query2).fetchall()
        for member in members:
            self.memberCombo.addItem(member[1], member[0])

        # TODO products
        query1 = ("SELECT DISTINCT description FROM products WHERE product_availability=?")
        prod_description = cur.execute(query1, ('Available',)).fetchall()
        
        self.sorting_combos(self.productCombo)

        for i in prod_description:
            self.productCombo.addItem(i[0])

        current_product = self.productCombo.currentText()
        current_manufacturer = self.productManufacturerCombo.currentText()
        current_model = self.productModelCombo.currentText()
        query = ("SELECT DISTINCT product_manufacturer FROM products WHERE description=? AND product_availability=?")
        product_manufacturer = cur.execute(query, (current_product, 'Available')).fetchall()
        self.productManufacturerCombo.clear()
        for product_manufacturer2 in product_manufacturer:
            self.productManufacturerCombo.addItem(str(product_manufacturer2[0]))

    def sorting_combos(self, name_combo):
        proxy = QSortFilterProxyModel(name_combo) 
        proxy.setSourceModel(name_combo.model())
        name_combo.model().setParent(proxy)
        name_combo.setModel(proxy)
        name_combo.model().sort(0)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrameLayout = QFrame()
        self.topFrameLayout.setStyleSheet(style.sell_product_top_frame())
        self.bottomFrameLayout = QFrame()
        self.bottomFrameLayout.setStyleSheet(style.sell_product_bottom_frame())
        # Add widgets
        self.topLayout.addWidget(self.sellProductImg)
        self.topFrameLayout.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel("Product: "), self.productCombo)
        self.bottomLayout.addRow(QLabel("Manufacturer: "), self.productManufacturerCombo)
        self.bottomLayout.addRow(QLabel("Model: "), self.productModelCombo)
        self.bottomLayout.addRow(QLabel("Quantity: "), self.quantityCombo)
        self.bottomLayout.addRow(QLabel("Member: "), self.memberCombo)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrameLayout.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrameLayout)
        self.mainLayout.addWidget(self.bottomFrameLayout)
        self.setLayout(self.mainLayout)

    def changeComboValue(self):
        
        self.productManufacturerCombo.clear()
        self.quantityCombo.clear()
        self.productModelCombo.clear()
        current_product = self.productCombo.currentText()
        query = ("SELECT DISTINCT product_manufacturer FROM products WHERE description=? AND product_availability=?")
        product_manufacturer = cur.execute(query, (current_product, 'Available')).fetchall()

        for product_manufacturer2 in product_manufacturer:
            self.productManufacturerCombo.addItem(str(product_manufacturer2[0]))


    def changeManufacturerCombo(self):        
        self.productModelCombo.clear()
        prod_manuf = self.productManufacturerCombo.currentText()
        prod_name = self.productCombo.currentText()
        query = cur.execute("SELECT product_name, product_id FROM products WHERE description=? AND product_manufacturer=? AND product_availability=?", (prod_name, prod_manuf, 'Available')).fetchall()
        for i in query:
            self.productModelCombo.addItem(str(i[0]),str(i[1]))

    def changeModelCombo(self):
        self.quantityCombo.clear()
        product_id = self.productModelCombo.currentData()
        query = ("SELECT product_quota, product_po FROM products WHERE product_id=?")
        quota = cur.execute(query, (product_id,)).fetchone()
        print(quota)
        try:
            self.qtx = quota[1]
            dfg = cur.execute("SELECT product_img FROM products WHERE product_po=?", (self.qtx,)).fetchone()
            self.sellProductImg.setPixmap(QPixmap(dfg[0]))
            self.unique_id.setText(str(quota[1]))
            for i in range(1, quota[0]+1):
                self.quantityCombo.addItem(str(i))
        except:
            print("Sss")

    def memberComboValue(self):
        print("memberComboValue")

    def sell_product(self):
        description = self.productCombo.currentText()
        product_manuf = self.productManufacturerCombo.currentText()
        productId = self.productModelCombo.currentData()
        product_model = self.productModelCombo.currentText()
        memberName = self.memberCombo.currentText()
        memberId = self.memberCombo.currentData()
        item = self.productModelCombo.currentText()
        datetime = QDateTime.currentDateTime().toString(3)
        quantity = int(self.quantityCombo.currentText())
        uniqueId_item = self.unique_id.text()

        prod_personal_name = description+"/"+product_manuf+"/"+product_model

        if memberName:
            try:
                cur.execute("UPDATE products SET picked_by=? WHERE description=? AND product_manufacturer=? AND product_name=?", ("Picked", description, product_manuf, product_model))
                self.empl_info_data = cur.execute(
                    "SELECT picked_product_name,take_by,product_id FROM take_product WHERE picked_product_name=? AND take_by=?",
                    (uniqueId_item, memberId)).fetchone()
                
                if not self.empl_info_data:
                    cur.execute(
                        "INSERT INTO 'take_product' (picked_product_name,take_by,product_id,items_amount,taker_name,time_day_picking,product_personal_name) VALUES(?,?,?,?,?,?,?)",
                        (uniqueId_item,memberId,productId, quantity, memberName, datetime, prod_personal_name))
                elif str(self.empl_info_data[0] == str(uniqueId_item)):
                    if str(self.empl_info_data[1]) == str(memberId):
                        some_value = cur.execute("SELECT items_amount FROM take_product WHERE picked_product_name=? AND take_by=?", (uniqueId_item, memberId)).fetchone()
                        new_value = int(some_value[0]) + quantity
                        cur.execute("DELETE FROM take_product WHERE picked_product_name=? AND take_by=?", (uniqueId_item, memberId))
                        cur.execute(
                            "INSERT INTO 'take_product' (picked_product_name,take_by,product_id,items_amount,taker_name,time_day_picking,product_personal_name) VALUES(?,?,?,?,?,?,?)",
                            (uniqueId_item,memberId,productId,new_value,memberName,datetime,prod_personal_name))
                    else:
                        pass
                else:
                    pass
                transactionQuery = (
                    "INSERT INTO 'transaction_history' (item_name_transaction, item_po_transaction, employee_name_transaction, amount_transaction, date_of_transaction, action_transaction) VALUES (?,?,?,?,?,?)")
                cur.execute(transactionQuery, (prod_personal_name, uniqueId_item, memberName, quantity, datetime, 'Picked'))

                self.qouta = cur.execute("SELECT product_quota FROM products WHERE product_id=?",
                                         (productId,)).fetchone()

                cur.execute("UPDATE members SET took_items=?, relation_to_items='Took' WHERE member_name=?",
                            (quantity, memberName))

                con.commit()

                if (quantity == self.qouta[0]):
                    updateQoutaQuery = ("UPDATE products set product_quota=?,product_availability=? WHERE product_id=?")
                    cur.execute(updateQoutaQuery, (0, 'UnAvailable', productId))
                    con.commit()

                else:
                    newQouta = (self.qouta[0] - quantity)
                    updateQoutaQuery = ("UPDATE products set product_quota=? WHERE product_id=?")
                    cur.execute(updateQoutaQuery, (newQouta, productId))
                    con.commit()
                self.main.productsTable.sortItems(10, Qt.AscendingOrder)
                self.main.displayProducts()

                QMessageBox.information(self, "Info", "Success")


            except:
                QMessageBox.warning(self, "Info!", "Something Went wrong!!!")
                QMessageBox.warning(self, "Info!", "Contact Sanya!")
            self.close()
        else:
            QMessageBox.warning(self, "Info", "No member!")
        self.main.update_to_DB.setIcon(QIcon('src/icons/updateToServer.png'))
        self.main.update_to_DB.setText("Update")
        self.close()


    """
    def sell_product2(self):
        productName = self.productCombo.currentText()
        productId = self.productCombo.currentData()
        memberName = self.memberCombo.currentText()
        memberId = self.memberCombo.currentData()
        uniqueId_item = self.unique_id.text()
        datetime = QDateTime.currentDateTime().toString(3)

        try:
            quantity = int(self.quantityCombo.currentText())
        except:
            pass

        if memberName:
            try:
                cur.execute("UPDATE products SET picked_by=? WHERE product_po=?", ("Picked", uniqueId_item))
                self.empl_info_data = cur.execute(
                    "SELECT picked_product_name,take_by,product_id FROM take_product where picked_product_name=? AND take_by=?",
                    (uniqueId_item, memberId)).fetchone()

                if not self.empl_info_data:
                    cur.execute(
                        "INSERT INTO 'take_product' (picked_product_name, take_by, product_id,items_amount,taker_name,time_day_picking,product_personal_name) VALUES (?,?,?,?,?,?,?)",
                        (uniqueId_item, memberId, productId, quantity, memberName, datetime, productName))

                elif str(self.empl_info_data[0]) == str(uniqueId_item):
                    if str(self.empl_info_data[1]) == str(memberId):
                        some_value = cur.execute(
                            "SELECT items_amount FROM take_product WHERE picked_product_name=? AND take_by=?",
                            (uniqueId_item, memberId)).fetchone()
                        new_value = int(some_value[0]) + quantity
                        cur.execute("DELETE FROM take_product WHERE picked_product_name=? AND take_by=?",
                                    (uniqueId_item, memberId))
                        cur.execute(
                            "INSERT INTO 'take_product' (picked_product_name, take_by, product_id,items_amount,taker_name,time_day_picking,product_personal_name) VALUES (?,?,?,?,?,?,?)",
                            (uniqueId_item, memberId, productId, new_value, memberName, datetime, productName))

                    else:
                        pass
                else:
                    pass

                transactionQuery = (
                    "INSERT INTO 'transaction_history' (item_name_transaction, item_po_transaction, employee_name_transaction, amount_transaction, date_of_transaction, action_transaction) VALUES (?,?,?,?,?,?)")
                cur.execute(transactionQuery, (productName, uniqueId_item, memberName, quantity, datetime, 'Picked'))

                self.qouta = cur.execute("SELECT product_quota FROM products WHERE product_id=?",
                                         (productId,)).fetchone()

                cur.execute("UPDATE members SET took_items=?, relation_to_items='Took' WHERE member_name=?",
                            (quantity, memberName))

                con.commit()

                if (quantity == self.qouta[0]):

                    updateQoutaQuery = ("UPDATE products set product_quota=?,product_availability=? WHERE product_id=?")
                    cur.execute(updateQoutaQuery, (0, 'UnAvailable', productId))
                    con.commit()

                else:
                    newQouta = (self.qouta[0] - quantity)
                    updateQoutaQuery = ("UPDATE products set product_quota=? WHERE product_id=?")
                    cur.execute(updateQoutaQuery, (newQouta, productId))
                    con.commit()

                self.main.displayProducts()

                QMessageBox.information(self, "Info", "Success")


            except:
                QMessageBox.information(self, "Info", "Something went wrong!!!!")
                QMessageBox.information(self, "Info", "Contact Sanya!")
            self.close()
        else:
            QMessageBox.warning(self, "Info", "No member!")
            self.close()
    """