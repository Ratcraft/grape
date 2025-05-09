from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic
from controllers.wine_controller import add_new_wine, get_all_wines

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main_window.ui", self)

        self.addButton.clicked.connect(self.add_wine)
        self.load_wine_table()

    def add_wine(self):
        name = self.nameInput.text()
        year = self.yearInput.text()
        wine_type = self.typeInput.text()
        quantity = self.quantityInput.text()

        add_new_wine(name, year, wine_type, quantity)

        self.nameInput.clear()
        self.yearInput.clear()
        self.typeInput.clear()
        self.quantityInput.clear()

        self.load_wine_table()

    def load_wine_table(self):
        wines = get_all_wines()
        self.wineTable.setRowCount(0)
        for row_num, wine in enumerate(wines):
            self.wineTable.insertRow(row_num)
            for col_num, value in enumerate(wine):
                self.wineTable.setItem(row_num, col_num, QTableWidgetItem(str(value)))
