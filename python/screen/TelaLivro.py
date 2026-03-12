from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit
)

from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsBlurEffect

from modules.mysql import MySQL


class TelaLivro(QWidget):

    def __init__(self, app, livro_id):
        super().__init__()

        self.app = app
        self.livro_id = livro_id
        self.mysql = MySQL()

        self.setWindowTitle("Informações do Livro")

        # ==========================
        # BACKGROUND COM BLUR
        # ==========================

        self.background = QLabel(self)
        self.background.setScaledContents(True)

        self.bg_pixmap = QPixmap("fundo.jpg/AlexandriaFundo.jpg")
        self.background.setPixmap(self.bg_pixmap)

        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(40)
        self.background.setGraphicsEffect(blur)

        self.background.lower()

        # ==========================
        # ESTILO GERAL
        # ==========================

        self.setStyleSheet("""
        QWidget{
            color:white;
            font-family:Segoe UI;
        }

        QLabel{
            font-size:14px;
        }

        QTextEdit{
            background-color:rgba(20,20,20,190);
            border:1px solid #3a3a3a;
            border-radius:6px;
            padding:10px;
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

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 30, 40, 30)
        self.layout.setSpacing(20)

        # ==========================
        # ZONA SUPERIOR
        # ==========================

        top_layout = QHBoxLayout()
        top_layout.setSpacing(30)

        # ==========================
        # CAPA
        # ==========================

        self.capa = QLabel()
        self.capa.setFixedSize(220, 320)
        self.capa.setAlignment(Qt.AlignCenter)

        self.capa.setStyleSheet("""
        background-color:rgba(30,30,30,200);
        border:2px solid #3a3a3a;
        border-radius:6px;
        """)

        # ==========================
        # CONTAINER DAS INFORMAÇÕES
        # ==========================

        info_container = QWidget()
        info_container.setStyleSheet("""
        background-color:rgba(20,20,20,190);
        border:1px solid #3a3a3a;
        border-radius:6px;
        padding:15px;
        """)

        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(12)

        self.nome_livro = QLabel("Nome do Livro")
        self.nome_livro.setFont(QFont("Segoe UI", 22, QFont.Bold))

        self.autor_livro = QLabel("Autor")
        self.idade_livro = QLabel("Idade")
        self.tags_livro = QLabel("Tags")

        info_layout.addWidget(self.nome_livro)
        info_layout.addWidget(self.autor_livro)
        info_layout.addWidget(self.idade_livro)
        info_layout.addWidget(self.tags_livro)
        info_layout.addStretch()

        top_layout.addWidget(self.capa)
        top_layout.addWidget(info_container)

        # ==========================
        # SINOPSE
        # ==========================

        self.sinopse = QTextEdit()
        self.sinopse.setReadOnly(True)
        self.sinopse.setPlaceholderText("Sinopse do livro")

        # ==========================
        # BOTÃO
        # ==========================

        self.botao_ler = QPushButton("Ler Livro")
        self.botao_ler.setFixedHeight(45)

        self.botao_ler.clicked.connect(self.abrir_leitura)

        # ==========================
        # MONTAGEM
        # ==========================

        self.layout.addLayout(top_layout)
        self.layout.addWidget(self.sinopse)
        self.layout.addWidget(self.botao_ler)

        # carregar dados do banco
        self.carregar_livro()

    # ==========================
    # AJUSTAR FUNDO
    # ==========================

    def resizeEvent(self, event):
        self.background.resize(self.size())
        super().resizeEvent(event)

    # ==========================
    # CARREGAR LIVRO DO BANCO
    # ==========================

    def carregar_livro(self):

        query = """
        SELECT
            id,
            nome,
            autor,
            idade_recomendada,
            tags,
            sinopse,
            capa
        FROM livros
        WHERE id = %s
        """

        try:

            resultado = self.mysql.select(query, (self.livro_id,))

            if not resultado:
                print("Livro não encontrado no banco.")
                return

            livro = resultado[0]

            nome = livro.get("nome")
            autor = livro.get("autor")
            idade = livro.get("idade_recomendada")
            tags = livro.get("tags")
            sinopse = livro.get("sinopse")
            capa = livro.get("capa")

            # ==========================
            # TEXTO
            # ==========================

            self.nome_livro.setText(nome if nome else "Livro sem nome")

            if autor:
                self.autor_livro.setText(f"Autor: {autor}")
            else:
                self.autor_livro.setText("Autor desconhecido")

            if idade:
                self.idade_livro.setText(f"Idade recomendada: {idade}")
            else:
                self.idade_livro.setText("Idade não definida")

            if tags:
                self.tags_livro.setText(f"Tags: {tags}")
            else:
                self.tags_livro.setText("Tags não definidas")

            if sinopse:
                self.sinopse.setText(sinopse)
            else:
                self.sinopse.setText("Sinopse não disponível.")

            # ==========================
            # CAPA
            # ==========================

            if capa:

                pixmap = QPixmap(capa)

                if not pixmap.isNull():

                    self.capa.setPixmap(
                        pixmap.scaled(
                            220,
                            320,
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation
                        )
                    )

        except Exception as erro:
            print("Erro ao carregar livro:", erro)

    # ==========================
    # ABRIR LEITOR
    # ==========================

    def abrir_leitura(self):

        from screen.LeitorLivro import LeitorLivro

        tela = LeitorLivro(self.app, self.livro_id)

        self.app.add_page("leitor", tela)
        self.app.go_to("leitor")