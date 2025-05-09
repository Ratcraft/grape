from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
import sys

from database.db import init_db

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
