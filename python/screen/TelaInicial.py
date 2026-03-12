# TelaInicial.py

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QScrollArea, QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
import mysql.connector
import sys

# Import correto das telas dentro da pasta screen
from screen.TelaLivro import TelaLivro
from screen.TelaLogin import TelaLogin


class TelaInicial(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Livraria")
        self.resize(900, 600)

        self.layout_principal = QVBoxLayout(self)



        # Área de scroll para os cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout_principal.addWidget(self.scroll_area)

        # Carregar livros do banco
        self.carregar_livros()

    def conectar_banco(self):
        return mysql.connector.connect(
            host="localhost",      # ajuste conforme seu banco
            user="root",           # ajuste conforme seu banco
            password="",           # ajuste conforme seu banco
            database="livraria"
        )

    def criar_evento_card(self, card, id):
        """Cria o evento de clique do card garantindo que o ID correto seja passado"""
        def evento(event):
            self.ir_para_livro(id)
        card.mousePressEvent = evento

    def carregar_livros(self):
        conexao = self.conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        # Seleciona os dados necessários para os cards
        cursor.execute("SELECT id, livros, autor, ano, sinopse FROM livros")
        livros = cursor.fetchall()
        cursor.close()
        conexao.close()

        # Criar cards no grid
        row = 0
        col = 0
        for livro in livros:
            card = QFrame()
            card.setFrameShape(QFrame.Box)
            card.setLineWidth(1)
            card.setStyleSheet("QFrame:hover {background-color: #f0f0f0;}")
            card.setCursor(QCursor(Qt.PointingHandCursor))
            card.setFixedSize(250, 180)
            card_layout = QVBoxLayout(card)

            # Título do livro
            titulo = QLabel(livro["livros"])
            titulo.setFont(QFont("Arial", 12, QFont.Bold))
            card_layout.addWidget(titulo)

            # Autor
            autor = QLabel(f"Autor: {livro['autor']}")
            card_layout.addWidget(autor)

            # Ano
            ano = QLabel(f"Ano: {livro['ano']}")
            card_layout.addWidget(ano)

            # Sinopse
            sinopse = QLabel(livro["sinopse"])
            sinopse.setWordWrap(True)
            card_layout.addWidget(sinopse)

            # --- Passa o ID correto usando função auxiliar ---
            self.criar_evento_card(card, livro["id"])

            self.grid_layout.addWidget(card, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

    def ir_para_livro(self, id):
        """Abre a TelaLivro passando o ID do livro clicado"""
        self.TelaLivro = TelaLivro(self.app, id)
        self.TelaLivro.show()
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = TelaInicial(app)
    tela.show()
    sys.exit(app.exec())