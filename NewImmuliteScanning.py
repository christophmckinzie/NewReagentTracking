import sys
import os
import csv
import pandas as pd

from PyQt5.QtGui import (QIcon, QRegExpValidator, QIcon)
from PyQt5.QtCore import Qt, QRegExp, QSortFilterProxyModel, QAbstractTableModel
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QVBoxLayout, QLineEdit, QAction, QMainWindow,
                             QWidget, QLabel, QTableView, QPushButton, QFormLayout, QMessageBox, QHeaderView, QFileDialog, QDialog)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        layout.setContentsMargins(10,10,10,10)

        # Text telling user what window is used for
        directions = QLabel("Select the items that you would like to order.\nClick 'Create Order' to export the order as a CSV file.")
        directions.setStyleSheet('font-size: 12pt;')
        directions.setAlignment(Qt.AlignLeft)
        layout.addWidget(directions, 0, 0, 1, 6)    

        item_list = list()
        self.order_list = list()

        with open('itemswithcatalognumber.csv') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                item_list.append(row[0])

        # skip first row because the "directions" are in that row
        positions = [(r, c) for r in range(1, 23) for c in range(16)]

        for position, value in zip(positions, item_list):
            button = QPushButton(value)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setCheckable(True)
            button.setStyleSheet("QPushButton { background-color: lightblue }"
                                 "QPushButton { font-size: 12pt }"
                                 "QPushButton:clicked { background-color: blue }")
            button.clicked.connect(lambda r=position, c=value: self.add_to_order_list(r,c))                             
            layout.addWidget(button, *position)

        order_button = QPushButton("Create Order", self)
        order_button.setStyleSheet("QPushButton { background-color: lightgreen }"
                                   "QPushButton { font-size: 13pt }"
                                   "QPushButton:clicked { background-color: green }")
        order_button.clicked.connect(self.export_order_list)
        layout.addWidget(order_button, 20, 0, 1, 2)

        self.setLayout(layout)
        self.show()
      
    def export_order_list(self):
        catalog_numbers = pd.read_csv("itemswithcatalognumber.csv", header=None, names=['item', 'catalog_number', 'order_count'])
        catalog_numbers.catalog_number.astype('int')
        catalog_numbers.order_count.astype('int')
        items_to_order = catalog_numbers[catalog_numbers['item'].isin(self.order_list)][['catalog_number', 'order_count']]

        # save file
        file_name = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if len(file_name[0]) > 0:
            file = open(file_name[0], 'w')
            file.write(items_to_order.to_csv(index=False, header=False, line_terminator='\n'))
            file.close()

    def add_to_order_list(self, row, col):
        # checks button clicked status and adds to list if its pressed
        if row == True:
            self.order_list.append(col)
        # or removes it if you click it again.
        else:
            self.order_list.remove(col)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.show()

    sys.exit(app.exec_())
