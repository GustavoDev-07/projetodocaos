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
        self.resize(500, 520)

        # ESTILO VISUAL IGUAL AO DA TELA INICIAL
        self.setStyleSheet("""

        QWidget{
            background-color:#e9edf2;
            font-family:Segoe UI;
            color:black;
        }

        QFrame{
            background:#dfe4ea;
            border-radius:14px;
            border:1px solid #cfd6dd;
        }

        QLabel{
            font-size:14px;
            font-weight:bold;
        }

        QLineEdit, QTextEdit{
            background:white;
            border:1px solid #cfd6dd;
            border-radius:8px;
            padding:8px;
            font-size:14px;
        }

        QLineEdit:focus, QTextEdit:focus{
            border:1px solid #a8d8f0;
        }

        QPushButton{
            background-color:#a8d8f0;
            border:none;
            border-radius:8px;
            padding:10px;
            font-size:14px;
            color:black;
        }

        QPushButton:hover{
            background-color:#92cde8;
        }

        """)

        layout_principal = QVBoxLayout(self)
        layout_principal.setAlignment(Qt.AlignCenter)

        # CARD CENTRAL
        card = QFrame()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        card_layout.setContentsMargins(25, 25, 25, 25)

        titulo = QLabel("Cadastrar Novo Livro")
        titulo.setFont(QFont("Segoe UI", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)

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

        card_layout.addWidget(titulo)
        card_layout.addWidget(self.input_nome)
        card_layout.addWidget(self.input_autor)
        card_layout.addWidget(self.input_ano)
        card_layout.addWidget(self.input_genero)
        card_layout.addWidget(self.input_sinopse)
        card_layout.addWidget(self.botao_salvar)

        layout_principal.addWidget(card)

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

            self.parent.recarregar_livros()
            self.close()

        except Exception as erro:

            QMessageBox.critical(self, "Erro", f"Erro ao salvar livro:\n{erro}")


# ===============================
# TELA INICIAL
# ===============================
class TelaInicial(QWidget):

    CARD_WIDTH = 220

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.setWindowTitle("Livraria")
        self.resize(1100, 700)

        # ESTILO GLOBAL
        self.setStyleSheet("""

        QWidget{
            background-color:#e9edf2;
            font-family:Segoe UI;
        }

        QPushButton{
            background-color:#a8d8f0;
            border:none;
            border-radius:8px;
            padding:10px;
            font-size:14px;
            color:black;
        }

        QPushButton:hover{
            background-color:#92cde8;
        }

        QFrame{
            background:#dfe4ea;
            border-radius:14px;
            border:1px solid #cfd6dd;
        }

        QLabel{
            color:black;
        }

        """)

        self.layout_principal = QVBoxLayout(self)

        # BOTÃO CRIAR NOVO
        self.botao_criar = QPushButton("Criar Novo Livro")
        self.botao_criar.setFixedHeight(40)
        self.botao_criar.clicked.connect(self.abrir_tela_novo)

        self.layout_principal.addWidget(self.botao_criar)

        # SCROLL
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(20)

        self.scroll_area.setWidget(self.scroll_content)

        self.layout_principal.addWidget(self.scroll_area)

        self.livros = []

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
        self.livros = cursor.fetchall()

        cursor.close()
        conexao.close()

        self.organizar_cards()

    def organizar_cards(self):

        while self.grid_layout.count():

            item = self.grid_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        largura = self.scroll_area.width()

        colunas = max(1, largura // self.CARD_WIDTH)

        row = 0
        col = 0

        for livro in self.livros:

            card = QFrame()
            card.setCursor(QCursor(Qt.PointingHandCursor))
            card.setFixedWidth(self.CARD_WIDTH)

            card.setStyleSheet("""

            QFrame{
                background:#dfe4ea;
                border-radius:14px;
                border:1px solid #cfd6dd;
            }

            QFrame:hover{
                border:1px solid #a8d8f0;
                background:#eef6fb;
            }

            QLabel{
                color:black;
            }

            """)

            card_layout = QVBoxLayout(card)

            titulo = QLabel(livro["livros"])
            titulo.setFont(QFont("Segoe UI", 11, QFont.Bold))
            titulo.setWordWrap(True)

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

            if col >= colunas:
                col = 0
                row += 1

    def resizeEvent(self, event):

        self.organizar_cards()
        super().resizeEvent(event)

    def recarregar_livros(self):

        self.carregar_livros()

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