import sys
from PySide6.QtWidgets import QApplication

from app import AppManager
from screen.home import Home

app = QApplication(sys.argv)

manager = AppManager()

home = Home()

manager.add_page("home", home)

manager.go_to("home")

manager.stack.resize(1200, 800)
manager.stack.show()

sys.exit(app.exec())