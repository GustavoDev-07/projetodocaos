from PySide6.QtWidgets import QStackedWidget


class AppManager:

    def __init__(self):
        self.stack = QStackedWidget()
        self.pages = {}

    def add_page(self, nome, pagina):
        """
        Registra uma nova página no sistema
        """
        self.pages[nome] = pagina
        self.stack.addWidget(pagina)

    def go_to(self, nome):
        """
        Troca para a página desejada
        """
        if nome in self.pages:
            self.stack.setCurrentWidget(self.pages[nome])
        else:
            print(f"Página '{nome}' não encontrada.")