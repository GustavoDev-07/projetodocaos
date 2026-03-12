# app.py

import sys
from PySide6.QtWidgets import QApplication
from screen.TelaInicial import TelaInicial  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela_inicial = TelaInicial(app)  
    tela_inicial.show()          
    sys.exit(app.exec())          