# TelaInicial.py

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QScrollArea, QFrame, QGridLayout, QLineEdit, QTextEdit,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
import mysql.connector
import sys

from screen.TelaLivro import TelaLivro
from screen.TelaLogin import TelaLogin


# ===============================
# TELA PARA CRIAR NOVO LIVRO
# ===============================
class TelaNovoLivro(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setWindowTitle("Cadastrar Livro")
        self.resize(400, 450)

        layout = QVBoxLayout(self)

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome do Livro")

        self.input_autor = QLineEdit()
        self.input_autor.setPlaceholderText("Autor")

        self.input_ano = QLineEdit()
        self.input_ano.setPlaceholderText("Ano")

        self.input_genero = QLineEdit()
        self.input_genero.setPlaceholderText("Gênero")

        self.input_sinopse = QTextEdit()
        self.input_sinopse.setPlaceholderText("Sinopse")

        self.botao_salvar = QPushButton("Salvar Livro")
        self.botao_salvar.clicked.connect(self.salvar_livro)

        layout.addWidget(self.input_nome)
        layout.addWidget(self.input_autor)
        layout.addWidget(self.input_ano)
        layout.addWidget(self.input_genero)
        layout.addWidget(self.input_sinopse)
        layout.addWidget(self.botao_salvar)

    def conectar_banco(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="livraria"
        )

    def salvar_livro(self):

        nome = self.input_nome.text()
        autor = self.input_autor.text()
        ano = self.input_ano.text()
        genero = self.input_genero.text()
        sinopse = self.input_sinopse.toPlainText()

        if nome == "":
            QMessageBox.warning(self, "Erro", "O livro precisa ter um nome.")
            return

        try:

            conexao = self.conectar_banco()
            cursor = conexao.cursor()

            query = """
            INSERT INTO livros
            (livros, autor, ano, genero, sinopse)
            VALUES (%s, %s, %s, %s, %s)
            """

            valores = (nome, autor, ano, genero, sinopse)

            cursor.execute(query, valores)
            conexao.commit()

            cursor.close()
            conexao.close()

            QMessageBox.information(self, "Sucesso", "Livro cadastrado!")

            # Atualiza lista na tela inicial
            self.parent.recarregar_livros()

            self.close()

        except Exception as erro:

            QMessageBox.critical(self, "Erro", f"Erro ao salvar livro:\n{erro}")


# ===============================
# TELA INICIAL
# ===============================
class TelaInicial(QWidget):
    def __init__(self, app):
        super().__init__()

        self.app = app

        self.setWindowTitle("Livraria")
        self.resize(900, 600)

        self.layout_principal = QVBoxLayout(self)

        # BOTÃO CRIAR NOVO
        self.botao_criar = QPushButton("Criar Novo Livro")
        self.botao_criar.setFixedHeight(40)
        self.botao_criar.clicked.connect(self.abrir_tela_novo)

        self.layout_principal.addWidget(self.botao_criar)

        # ÁREA SCROLL
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)

        self.scroll_area.setWidget(self.scroll_content)

        self.layout_principal.addWidget(self.scroll_area)

        # CARREGAR LIVROS
        self.carregar_livros()

    def conectar_banco(self):

        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="livraria"
        )

    def criar_evento_card(self, card, id):

        def evento(event):
            self.ir_para_livro(id)

        card.mousePressEvent = evento

    def carregar_livros(self):

        conexao = self.conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("SELECT id, livros, autor, ano, sinopse FROM livros")
        livros = cursor.fetchall()

        cursor.close()
        conexao.close()

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

            titulo = QLabel(livro["livros"])
            titulo.setFont(QFont("Arial", 12, QFont.Bold))

            autor = QLabel(f"Autor: {livro['autor']}")

            ano = QLabel(f"Ano: {livro['ano']}")

            sinopse = QLabel(livro["sinopse"])
            sinopse.setWordWrap(True)

            card_layout.addWidget(titulo)
            card_layout.addWidget(autor)
            card_layout.addWidget(ano)
            card_layout.addWidget(sinopse)

            self.criar_evento_card(card, livro["id"])

            self.grid_layout.addWidget(card, row, col)

            col += 1

            if col >= 3:
                col = 0
                row += 1

    # LIMPA E RECARREGA OS LIVROS
    def recarregar_livros(self):

        while self.grid_layout.count():

            item = self.grid_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        self.carregar_livros()

    # ABRIR TELA NOVO LIVRO
    def abrir_tela_novo(self):

        self.tela_novo = TelaNovoLivro(self)
        self.tela_novo.show()

    def ir_para_livro(self, id):

        self.TelaLivro = TelaLivro(self.app, id)
        self.TelaLivro.show()
        self.close()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    tela = TelaInicial(app)
    tela.show()

    sys.exit(app.exec())