from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from modules.mysql import MySQL


class TelaCadastro(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.mysql = MySQL()

        self.setWindowTitle("Cadastro")
        self.setStyleSheet("""
        QWidget{
            background-color:#121212;
            color:white;
            font-family:Segoe UI;
        }

        QLabel{
            font-size:16px;
        }

        QLineEdit{
            background-color:#1e1e1e;
            border:1px solid #3a3a3a;
            border-radius:6px;
            padding:8px;
            font-size:14px;
        }

        QPushButton{
            background-color:#00a8c6;
            border:none;
            border-radius:6px;
            font-size:15px;
            font-weight:bold;
            padding:10px;
        }

        QPushButton:hover{
            background-color:#00c3e3;
        }

        QPushButton:pressed{
            background-color:#008ca3;
        }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        titulo = QLabel("Criar Conta")
        titulo.setFont(QFont("Segoe UI", 22, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)

        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Nome")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.senha = QLineEdit()
        self.senha.setPlaceholderText("Senha")
        self.senha.setEchoMode(QLineEdit.Password)

        botao = QPushButton("Cadastrar")
        botao.clicked.connect(self.cadastrar)

        layout.addWidget(titulo)
        layout.addWidget(self.nome)
        layout.addWidget(self.email)
        layout.addWidget(self.senha)
        layout.addWidget(botao)
