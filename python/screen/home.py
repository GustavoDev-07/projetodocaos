import mysql.connector

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QGridLayout,
    QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from modules.mysql import MySQL


class Home(QWidget):

    def __init__(self):
        super().__init__()

        layout_principal = QVBoxLayout(self)

        titulo = QLabel("Biblioteca")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size:26px; font-weight:bold; margin:20px;")

        layout_principal.addWidget(titulo)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.grid = QGridLayout(container)

        scroll.setWidget(container)

        layout_principal.addWidget(scroll)

        self.carregar_livros()

    def conectar_banco(self):

        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="livraria"
        )

        return conexao

    def carregar_livros(self):

        conexao = self.conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
        SELECT livros, autor, genero, sinopse
        FROM livros
        LIMIT 30
        """)

        dados = cursor.fetchall()

        linha = 0
        coluna = 0

        for livro in dados:

            card = self.criar_card(livro)

            self.grid.addWidget(card, linha, coluna)

            coluna += 1

            if coluna == 5:
                coluna = 0
                linha += 1

            if linha == 6:
                break

    def criar_card(self, livro):

        frame = QFrame()
        frame.setStyleSheet("""
        QFrame{
            border:1px solid #ccc;
            border-radius:6px;
            padding:8px;
        }
        """)

        layout = QVBoxLayout(frame)

        titulo = QLabel(livro["livros"])
        titulo.setStyleSheet("font-weight:bold; font-size:14px")

        autor = QLabel(f'Autor: {livro["autor"]}')
        genero = QLabel(f'Genero: {livro["genero"]}')

        sinopse = livro["sinopse"][:120] + "..."
        sinopse_label = QLabel(sinopse)
        sinopse_label.setWordWrap(True)

        layout.addWidget(titulo)
        layout.addWidget(autor)
        layout.addWidget(genero)
        layout.addWidget(sinopse_label)

        return frame