from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from modules.mysql import MySQL


class TelaLogin(QWidget):

    def __init__(self, app):

        super().__init__()

        self.app = app
        self.mysql = MySQL()

        layout = QVBoxLayout(self)

        titulo = QLabel("Login")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.senha = QLineEdit()
        self.senha.setPlaceholderText("Senha")

        botao = QPushButton("Entrar")

        botao.clicked.connect(self.login)

        layout.addWidget(titulo)
        layout.addWidget(self.email)
        layout.addWidget(self.senha)
        layout.addWidget(botao)

    def login(self):

        email = self.email.text()
        senha = self.senha.text()

        query = """
        SELECT id FROM usuarios
        WHERE email=%s AND senha=%s
        """

        resultado = self.mysql.select(query, (email, senha))

        if not resultado:

            QMessageBox.warning(self, "Erro", "Login inválido")
            return

        from screen.TelaLivro import TelaLivro

        tela = TelaLivro(self.app, 1)

        self.app.add_page("livro", tela)
        self.app.go_to("livro")