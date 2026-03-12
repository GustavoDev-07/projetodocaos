from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QGraphicsBlurEffect,
    QMessageBox,
    QLineEdit
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from modules.mysql import MySQL


class TelaEditarLivro(QWidget):

    def __init__(self, parent, id):
        super().__init__()

        self.parent = parent
        self.id = id
        self.mysql = MySQL()

        self.setWindowTitle("Editar Livro")
        self.resize(400, 400)

        layout = QVBoxLayout(self)

        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Nome do Livro")

        self.autor = QLineEdit()
        self.autor.setPlaceholderText("Autor")

        self.ano = QLineEdit()
        self.ano.setPlaceholderText("Ano")

        self.genero = QLineEdit()
        self.genero.setPlaceholderText("Gênero")

        self.sinopse = QTextEdit()
        self.sinopse.setPlaceholderText("Sinopse")

        self.botao_salvar = QPushButton("Salvar Alterações")
        self.botao_salvar.clicked.connect(self.salvar)

        layout.addWidget(self.nome)
        layout.addWidget(self.autor)
        layout.addWidget(self.ano)
        layout.addWidget(self.genero)
        layout.addWidget(self.sinopse)
        layout.addWidget(self.botao_salvar)

        self.carregar_dados()

    def carregar_dados(self):

        query = """
        SELECT livros, autor, ano, genero, sinopse
        FROM livros
        WHERE id = %s
        """

        try:

            self.mysql.connect()
            resultado = self.mysql.execute_query(query, (self.id,))
            self.mysql.disconnect()

            if not resultado:
                return

            livro = resultado[0]

            self.nome.setText(livro.get("livros", ""))
            self.autor.setText(livro.get("autor", ""))
            self.ano.setText(str(livro.get("ano", "")))
            self.genero.setText(livro.get("genero", ""))
            self.sinopse.setText(livro.get("sinopse", ""))

        except Exception as erro:
            print("Erro ao carregar dados:", erro)

    def salvar(self):

        query = """
        UPDATE livros
        SET
        livros = %s,
        autor = %s,
        ano = %s,
        genero = %s,
        sinopse = %s
        WHERE id = %s
        """

        valores = (
            self.nome.text(),
            self.autor.text(),
            self.ano.text(),
            self.genero.text(),
            self.sinopse.toPlainText(),
            self.id
        )

        try:

            self.mysql.connect()
            self.mysql.execute_query(query, valores)
            self.mysql.disconnect()

            QMessageBox.information(self, "Sucesso", "Livro atualizado!")

            self.parent.carregar_livro()
            self.close()

        except Exception as erro:
            print("Erro ao atualizar:", erro)


class TelaLivro(QWidget):

    def __init__(self, app, id):
        super().__init__()

        self.app = app
        self.id = id
        self.mysql = MySQL()

        self.setWindowTitle("Informações do Livro")
        self.resize(700, 500)

        # BACKGROUND
        self.background = QLabel(self)
        self.background.setScaledContents(True)
        self.bg_pixmap = QPixmap("fundo.jpg/AlexandriaFundo.jpg")
        self.background.setPixmap(self.bg_pixmap)

        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(40)
        self.background.setGraphicsEffect(blur)
        self.background.lower()

        # ESTILO
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

        # PARTE SUPERIOR
        top_layout = QHBoxLayout()
        top_layout.setSpacing(30)

        self.capa = QLabel()
        self.capa.setFixedSize(220, 320)
        self.capa.setAlignment(Qt.AlignCenter)

        self.capa.setStyleSheet("""
        background-color:rgba(30,30,30,200);
        border:2px solid #3a3a3a;
        border-radius:6px;
        """)

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

        # BOTÕES NOVOS
        botoes_layout = QHBoxLayout()

        self.botao_editar = QPushButton("Editar")
        self.botao_editar.clicked.connect(self.editar_livro)

        self.botao_excluir = QPushButton("Excluir")
        self.botao_excluir.clicked.connect(self.excluir_livro)

        botoes_layout.addWidget(self.botao_editar)
        botoes_layout.addWidget(self.botao_excluir)

        # BOTÃO VOLTAR
        self.botao_ler = QPushButton("Voltar")
        self.botao_ler.setFixedHeight(45)
        self.botao_ler.clicked.connect(self.abrir_leitura)

        # MONTAGEM
        self.layout.addLayout(top_layout)
        self.layout.addWidget(self.sinopse)
        self.layout.addLayout(botoes_layout)
        self.layout.addWidget(self.botao_ler)

        self.carregar_livro()

    def resizeEvent(self, event):
        self.background.resize(self.size())
        super().resizeEvent(event)

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

            self.nome_livro.setText(livro.get("livros", "Livro sem nome"))
            self.autor_livro.setText(f"Autor: {livro.get('autor', 'Desconhecido')}")
            self.idade_livro.setText(f"Ano: {livro.get('ano', 'Não definido')}")
            self.tags_livro.setText(f"Gênero: {livro.get('genero', 'Não definido')}")
            self.sinopse.setText(livro.get("sinopse", "Sinopse não disponível."))

        except Exception as erro:
            print("Erro ao carregar livro:", erro)

    # EXCLUIR LIVRO
    def excluir_livro(self):

        confirmar = QMessageBox.question(
            self,
            "Confirmar",
            "Deseja realmente excluir este livro?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmar == QMessageBox.No:
            return

        query = "DELETE FROM livros WHERE id = %s"

        try:

            self.mysql.connect()
            self.mysql.execute_query(query, (self.id,))
            self.mysql.disconnect()

            QMessageBox.information(self, "Sucesso", "Livro excluído.")

            self.abrir_leitura()

        except Exception as erro:
            print("Erro ao excluir:", erro)

    # EDITAR LIVRO
    def editar_livro(self):

        self.tela_editar = TelaEditarLivro(self, self.id)
        self.tela_editar.show()

    # VOLTAR
    def abrir_leitura(self):
        from screen.TelaInicial import TelaInicial
        self.leitor = TelaInicial(self.app)
        self.leitor.show()
        self.close()