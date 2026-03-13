from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QMessageBox,
    QLineEdit,
    QFrame
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from modules.mysql import MySQL

class TelaEditarLivro(QWidget):

    def __init__(self, parent, id):
        super().__init__()

        self.parent = parent
        self.id = id
        self.mysql = MySQL()

        self.setWindowTitle("Editar Livro")
        self.resize(450, 500)

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

        card = QFrame()
        layout = QVBoxLayout(card)

        layout.setSpacing(12)
        layout.setContentsMargins(25,25,25,25)

        titulo = QLabel("Editar Livro")
        titulo.setFont(QFont("Segoe UI",16,QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)

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

        layout.addWidget(titulo)
        layout.addWidget(self.nome)
        layout.addWidget(self.autor)
        layout.addWidget(self.ano)
        layout.addWidget(self.genero)
        layout.addWidget(self.sinopse)
        layout.addWidget(self.botao_salvar)

        layout_principal.addWidget(card)

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
        self.resize(750,520)

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
        }

        QTextEdit{
            background:white;
            border:1px solid #cfd6dd;
            border-radius:8px;
            padding:10px;
        }

        QPushButton{
            background-color:#a8d8f0;
            border:none;
            border-radius:8px;
            font-size:14px;
            padding:10px;
            color:black;
        }

        QPushButton:hover{
            background-color:#92cde8;
        }

        """)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40,30,40,30)

        top_layout = QHBoxLayout()

        self.capa = QFrame()
        self.capa.setFixedSize(220,320)

        capa_layout = QVBoxLayout(self.capa)

        capa_text = QLabel("Capa do Livro")
        capa_text.setAlignment(Qt.AlignCenter)

        capa_layout.addWidget(capa_text)

        info_container = QFrame()
        info_layout = QVBoxLayout(info_container)

        self.nome_livro = QLabel("Nome do Livro")
        self.nome_livro.setFont(QFont("Segoe UI",22,QFont.Bold))

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

        self.sinopse = QTextEdit()
        self.sinopse.setReadOnly(True)

        botoes_layout = QHBoxLayout()

        self.botao_editar = QPushButton("Editar")
        self.botao_editar.clicked.connect(self.editar_livro)

        self.botao_excluir = QPushButton("Excluir")
        self.botao_excluir.clicked.connect(self.excluir_livro)

        botoes_layout.addWidget(self.botao_editar)
        botoes_layout.addWidget(self.botao_excluir)

        self.botao_voltar = QPushButton("Voltar")
        self.botao_voltar.setFixedHeight(45)
        self.botao_voltar.clicked.connect(self.abrir_leitura)

        self.layout.addLayout(top_layout)
        self.layout.addWidget(self.sinopse)
        self.layout.addLayout(botoes_layout)
        self.layout.addWidget(self.botao_voltar)

        self.carregar_livro()

    def carregar_livro(self):

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
                print("Livro não encontrado")
                return

            livro = resultado[0]

            self.nome_livro.setText(livro.get("livros","Livro"))
            self.autor_livro.setText(f"Autor: {livro.get('autor','Desconhecido')}")
            self.idade_livro.setText(f"Ano: {livro.get('ano','')}")
            self.tags_livro.setText(f"Gênero: {livro.get('genero','')}")
            self.sinopse.setText(livro.get("sinopse",""))

        except Exception as erro:
            print("Erro:",erro)

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
            self.mysql.execute_query(query,(self.id,))
            self.mysql.disconnect()

            QMessageBox.information(self,"Sucesso","Livro excluído.")

            self.abrir_leitura()

        except Exception as erro:
            print("Erro ao excluir:",erro)

    def editar_livro(self):

        self.tela_editar = TelaEditarLivro(self,self.id)
        self.tela_editar.show()

    def abrir_leitura(self):

        from screen.TelaInicial import TelaInicial

        self.leitor = TelaInicial(self.app)
        self.leitor.show()
        self.close()