from PySide6.QtWidgets import QPushButton


class NavButton(QPushButton):
# texto = texto que aparece no botao, destino = pagina a ser aberta app_maneger = objeto responsavel pela troca de pagina
    def __init__(self, texto, destino, app_manager):
        super().__init__(texto)

        self.destino = destino
        self.app = app_manager

        self.clicked.connect(self.navegar)

    def navegar(self):
        """
        Método chamado ao clicar no botão
        """
        self.app.go_to(self.destino)