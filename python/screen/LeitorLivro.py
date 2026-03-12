from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from modules.mysql import MySQL


class LeitorLivro(QWidget):

    def __init__(self, app, id):
        super().__init__()

        self.app = app
        self.id = id
        self.mysql = MySQL()

        self.setWindowTitle("Leitor de Livro")

        # ==========================
        # ESTILO
        # ==========================

        self.setStyleSheet("""
        QWidget{
            background-color:#121212;
            color:white;
            font-family:Segoe UI;
        }

        QPushButton{
            background-color:#00a8c6;
            border:none;
            border-radius:6px;
            font-size:14px;
            font-weight:bold;
            padding:8px 14px;
        }

        QPushButton:hover{
            background-color:#00c3e3;
        }

        QTextEdit{
            background-color:#1e1e1e;
            border:1px solid #3a3a3a;
            border-radius:6px;
            padding:20px;
            font-size:16px;
        }
        """)

        # ==========================
        # LAYOUT PRINCIPAL
        # ==========================

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)

        # ==========================
        # BARRA SUPERIOR
        # ==========================

        top_bar = QHBoxLayout()
        top_bar.setSpacing(15)

        # botão voltar
        self.botao_voltar = QPushButton("← Voltar")
        self.botao_voltar.setFixedHeight(35)
        self.botao_voltar.clicked.connect(self.voltar_livro)

        # nome do livro
        self.nome_livro = QLabel("Carregando livro...")
        self.nome_livro.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.nome_livro.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        top_bar.addWidget(self.botao_voltar)
        top_bar.addWidget(self.nome_livro)
        top_bar.addStretch()

        # ==========================
        # ÁREA DE LEITURA
        # ==========================

        self.area_leitura = QTextEdit()
        self.area_leitura.setReadOnly(True)
        self.area_leitura.setPlaceholderText("Conteúdo do livro aparecerá aqui...")

        # ==========================
        # MONTAGEM
        # ==========================

        layout.addLayout(top_bar)
        layout.addWidget(self.area_leitura)

        # carregar conteúdo
        self.carregar_livro()

    # ==========================
    # VOLTAR PARA TELA DO LIVRO
    # ==========================

    def voltar_livro(self):
        from screen.TelaLivro import TelaLivro  # importa a tela de volta
        self.tela_livro = TelaLivro(self.app, self.id)  # cria a tela passando o mesmo livro
        self.tela_livro.show()  # mostra a tela
        self.close()  # fecha a tela de leitura

    # ==========================
    # CARREGAR LIVRO
    # ==========================

    def carregar_livro(self):

        query = """
        SELECT
            nome,
            conteudo
        FROM livros
        WHERE id = %s
        """

        try:

            resultado = self.mysql.select(query, (self.id))

            if not resultado:
                print("Livro não encontrado.")
                return

            livro = resultado[0]

            nome = livro.get("nome")
            conteudo = livro.get("conteudo")

            if nome:
                self.nome_livro.setText(f"Lendo: {nome}")

            if conteudo:
                self.area_leitura.setText(conteudo)
            else:
                self.area_leitura.setText(
                    "Este livro ainda não possui conteúdo cadastrado."
                )

        except Exception as erro:

            print("Erro ao carregar conteúdo do livro:", erro)