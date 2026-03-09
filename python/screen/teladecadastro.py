import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt


class TelaLeitura(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Leitor de Livro")
        self.resize(1100, 700)

        self.tamanho_fonte = 14
        self.pagina_atual = 0

        # exemplo de páginas
        self.paginas = [
            "Capítulo 1\n\nEra uma pequena aldeia chamada Macondo...",
            "Capítulo 1\n\nJosé Arcadio Buendía decidiu explorar o mundo...",
            "Capítulo 2\n\nOs anos passaram e a aldeia cresceu..."
        ]

        main_layout = QHBoxLayout(self)

        # -------------------------
        # PAINEL ESQUERDO
        # -------------------------

        esquerda = QVBoxLayout()

        self.capa = QLabel()
        self.capa.setFixedSize(250, 350)
        self.capa.setAlignment(Qt.AlignCenter)

        self.carregar_capa("Cem Anos de Solidão")

        self.titulo = QLabel("Cem Anos de Solidão")
        self.titulo.setStyleSheet("font-size:16px;font-weight:bold")

        self.autor = QLabel("Gabriel García Márquez")
        self.autor.setStyleSheet("color:gray")

        # estrelas
        self.estrelas = []
        estrelas_layout = QHBoxLayout()

        for i in range(5):
            estrela = QPushButton("☆")
            estrela.setFixedWidth(35)
            estrela.clicked.connect(lambda _, x=i: self.avaliar(x + 1))
            estrelas_layout.addWidget(estrela)
            self.estrelas.append(estrela)

        self.nota = QLabel("Sua nota: 0/5")

        # botão ler
        self.btn_ler = QPushButton("📖 Ler")
        self.btn_ler.clicked.connect(self.abrir_livro)

        esquerda.addWidget(self.capa)
        esquerda.addWidget(self.titulo)
        esquerda.addWidget(self.autor)
        esquerda.addLayout(estrelas_layout)
        esquerda.addWidget(self.nota)
        esquerda.addWidget(self.btn_ler)
        esquerda.addStretch()

        # -------------------------
        # PAINEL DIREITO
        # -------------------------

        direita = QVBoxLayout()

        # barra superior
        top_bar = QHBoxLayout()

        self.btn_voltar_tela = QPushButton("⬅ Voltar")
        self.btn_voltar_tela.clicked.connect(self.voltar_visualizacao)

        self.btn_voltar = QPushButton("⬅ Página anterior")
        self.btn_avancar = QPushButton("Próxima página ➡")

        self.btn_voltar.clicked.connect(self.pagina_anterior)
        self.btn_avancar.clicked.connect(self.proxima_pagina)

        self.btn_menos = QPushButton("A-")
        self.btn_mais = QPushButton("A+")

        self.btn_menos.clicked.connect(self.diminuir_fonte)
        self.btn_mais.clicked.connect(self.aumentar_fonte)

        top_bar.addWidget(self.btn_voltar_tela)
        top_bar.addWidget(self.btn_voltar)
        top_bar.addWidget(self.btn_avancar)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_menos)
        top_bar.addWidget(self.btn_mais)

        # texto do livro
        self.texto = QTextEdit()
        self.texto.setReadOnly(True)
        self.texto.hide()

        direita.addLayout(top_bar)
        direita.addWidget(self.texto)

        main_layout.addLayout(esquerda, 1)
        main_layout.addLayout(direita, 3)

    # -------------------------
    # carregar capa
    # -------------------------

    def carregar_capa(self, titulo):

        try:
            url = f"https://covers.openlibrary.org/b/title/{titulo}-L.jpg"

            r = requests.get(url, timeout=5)

            pix = QPixmap()
            pix.loadFromData(r.content)

            if not pix.isNull():
                self.capa.setPixmap(
                    pix.scaled(250, 350, Qt.KeepAspectRatio)
                )
            else:
                self.capa.setText("Sem capa")

        except:
            self.capa.setText("Sem capa")

    # -------------------------
    # avaliar estrelas
    # -------------------------

    def avaliar(self, valor):

        for i, estrela in enumerate(self.estrelas):

            if i < valor:
                estrela.setText("⭐")
            else:
                estrela.setText("☆")

        self.nota.setText(f"Sua nota: {valor}/5")

    # -------------------------
    # abrir livro
    # -------------------------

    def abrir_livro(self):

        self.texto.show()

        self.texto.setFont(QFont("Times", self.tamanho_fonte))

        self.pagina_atual = 0
        self.mostrar_pagina()

    # -------------------------
    # mostrar página
    # -------------------------

    def mostrar_pagina(self):
        self.texto.setText(self.paginas[self.pagina_atual])

    # -------------------------

    def proxima_pagina(self):

        if self.pagina_atual < len(self.paginas) - 1:
            self.pagina_atual += 1
            self.mostrar_pagina()

    # -------------------------

    def pagina_anterior(self):

        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.mostrar_pagina()

    # -------------------------
    # voltar visualização
    # -------------------------

    def voltar_visualizacao(self):

        self.texto.hide()

    # -------------------------
    # tamanho fonte
    # -------------------------

    def aumentar_fonte(self):

        self.tamanho_fonte += 2
        self.texto.setFont(QFont("Times", self.tamanho_fonte))

    # -------------------------

    def diminuir_fonte(self):

        if self.tamanho_fonte > 8:
            self.tamanho_fonte -= 2
            self.texto.setFont(QFont("Times", self.tamanho_fonte))


# -------------------------

if __name__ == "__main__":

    app = QApplication(sys.argv)

    janela = TelaLeitura()
    janela.show()

    sys.exit(app.exec())