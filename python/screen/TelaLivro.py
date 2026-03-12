from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QGraphicsBlurEffect
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from modules.mysql import MySQL


class TelaLivro(QWidget):

    def __init__(self, app, id):
        super().__init__()

        self.app = app
        self.id = id
        self.mysql = MySQL()

        self.setWindowTitle("Informações do Livro")
        self.resize(700, 500)

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

        # CAPA
        self.capa = QLabel()
        self.capa.setFixedSize(220, 320)
        self.capa.setAlignment(Qt.AlignCenter)
        self.capa.setStyleSheet("""
        background-color:rgba(30,30,30,200);
        border:2px solid #3a3a3a;
        border-radius:6px;
        """)

        # CONTAINER DAS INFORMAÇÕES
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
        self.idade_livro = QLabel("Ano")
        self.tags_livro = QLabel("Gênero")

        info_layout.addWidget(self.nome_livro)
        info_layout.addWidget(self.autor_livro)
        info_layout.addWidget(self.idade_livro)
        info_layout.addWidget(self.tags_livro)
        info_layout.addStretch()

        top_layout.addWidget(self.capa)
        top_layout.addWidget(info_container)

        # SINOPSE
        self.sinopse = QTextEdit()
        self.sinopse.setReadOnly(True)
        self.sinopse.setPlaceholderText("Sinopse do livro")

        # BOTÃO
        self.botao_ler = QPushButton("Voltar")
        self.botao_ler.setFixedHeight(45)
        self.botao_ler.clicked.connect(self.abrir_leitura)

        # MONTAGEM
        self.layout.addLayout(top_layout)
        self.layout.addWidget(self.sinopse)
        self.layout.addWidget(self.botao_ler)

        # CARREGAR DADOS DO BANCO
        self.carregar_livro()

    # AJUSTAR FUNDO
    def resizeEvent(self, event):
        self.background.resize(self.size())
        super().resizeEvent(event)

    # CARREGAR LIVRO DO BANCO
    def carregar_livro(self):
        query = """
        SELECT
            livros,
            autor,
            ano,
            genero,
            sinopse
        FROM livros
        WHERE id = %s
        """

        try:
            self.mysql.connect()
            resultado = self.mysql.execute_query(query, (self.id,))
            self.mysql.disconnect()

            if not resultado:
                print("Livro não encontrado no banco.")
                return

            livro = resultado[0]

            # Preenche os campos do container
            self.nome_livro.setText(livro.get("livros", "Livro sem nome"))
            self.autor_livro.setText(f"Autor: {livro.get('autor', 'Desconhecido')}")
            self.idade_livro.setText(f"Ano: {livro.get('ano', 'Não definido')}")
            self.tags_livro.setText(f"Gênero: {livro.get('genero', 'Não definido')}")
            self.sinopse.setText(livro.get("sinopse", "Sinopse não disponível."))

            # Carrega capa se existir
            # capa = livro.get("capa")
            # if capa:
            #     pixmap = QPixmap(capa)
            #     if not pixmap.isNull():
            #         self.capa.setPixmap(
            #             pixmap.scaled(
            #                 220,
            #                 320,
            #                 Qt.KeepAspectRatio,
            #                 Qt.SmoothTransformation
            #             )
            #         )

        except Exception as erro:
            print("Erro ao carregar livro:", erro)
    
    # def carregar_livro(self):

    #     query = """
    #     SELECT
    #         nome,
    #         conteudo
    #     FROM livros
    #     WHERE id = %s
    #     """

    #     try:

    #         resultado = self.mysql.select(query, (self.id))

    #         if not resultado:
    #             print("Livro não encontrado.")
    #             return

    #         livro = resultado[0]

    #         nome = livro.get("nome")
    #         conteudo = livro.get("conteudo")

    #         if nome:
    #             self.nome_livro.setText(f"Lendo: {nome}")

    #         if conteudo:
    #             self.area_leitura.setText(conteudo)
    #         else:
    #             self.area_leitura.setText(
    #                 "Este livro ainda não possui conteúdo cadastrado."
    #             )

    #     except Exception as erro:

    #         print("Erro ao carregar conteúdo do livro:", erro)

    # ABRIR LEITOR
    def abrir_leitura(self):
        from screen.TelaInicial import TelaInicial
        self.leitor = TelaInicial(self.app)
        self.leitor.show()
        self.close()