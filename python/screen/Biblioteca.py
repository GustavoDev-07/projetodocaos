import sys
import sqlite3
import requests
from urllib.parse import quote

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


# -------------------------
# FUNÇÃO GLOBAL DE CAPA
# -------------------------

def get_book_cover(title, size="M"):
    try:
        query = quote(title)
        url = f"https://openlibrary.org/search.json?title={query}"

        r = requests.get(url, timeout=5).json()

        if r["docs"]:
            doc = r["docs"][0]

            if "cover_i" in doc:
                cover_id = doc["cover_i"]
                cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"

                data = requests.get(cover_url, timeout=5).content
                pix = QPixmap()
                pix.loadFromData(data)

                if not pix.isNull():
                    return pix
    except:
        pass

    return None


# -------------------------
# BANCO DE DADOS
# -------------------------

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("biblioteca.db")
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS favoritos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        autor TEXT
        )
        """)

    def add(self, titulo, autor):
        self.conn.execute(
            "INSERT INTO favoritos(titulo,autor) VALUES(?,?)",
            (titulo, autor)
        )
        self.conn.commit()

    def ranking(self):
        cur = self.conn.cursor()
        cur.execute("""
        SELECT titulo, autor, COUNT(*) as total
        FROM favoritos
        GROUP BY titulo, autor
        ORDER BY total DESC
        LIMIT 5
        """)
        return cur.fetchall()


db = Database()


# -------------------------
# CARD DE LIVRO
# -------------------------

class LivroCard(QFrame):

    def __init__(self, titulo, autor):
        super().__init__()

        self.titulo = titulo
        self.autor = autor

        self.setFixedSize(200, 300)

        layout = QVBoxLayout(self)

        self.capa = QLabel()
        self.capa.setFixedHeight(170)
        self.capa.setScaledContents(True)

        self.load_cover()

        titulo_label = QLabel(titulo)
        titulo_label.setWordWrap(True)
        titulo_label.setStyleSheet("font-weight:bold")

        autor_label = QLabel(autor)
        autor_label.setStyleSheet("color:gray")

        btn_ler = QPushButton("Ler")
        btn_fav = QPushButton("⭐")

        btn_ler.setMinimumHeight(32)
        btn_ler.setCursor(Qt.PointingHandCursor)

        btn_fav.setFixedSize(36, 32)
        btn_fav.setCursor(Qt.PointingHandCursor)

        btn_row = QHBoxLayout()
        btn_row.addWidget(btn_ler, stretch=1)
        btn_row.addWidget(btn_fav)

        btn_ler.clicked.connect(self.ler)
        btn_fav.clicked.connect(self.favorito)

        layout.addWidget(self.capa)
        layout.addWidget(titulo_label)
        layout.addWidget(autor_label)
        layout.addLayout(btn_row)

    def load_cover(self):
        pix = get_book_cover(self.titulo, "M")

        if pix:
            self.capa.setPixmap(pix)
        else:
            self.capa.setStyleSheet("background:#ddd;border-radius:6px;")

    def favorito(self):
        db.add(self.titulo, self.autor)
        QMessageBox.information(self, "Favorito", "Livro salvo!")

    def ler(self):
        self.reader = Reader(self.titulo)
        self.reader.show()


# -------------------------
# CARROSSEL
# -------------------------

class Carrossel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        container = QWidget()
        row = QHBoxLayout(container)

        livros = [
            ("Dom Casmurro", "Machado de Assis"),
            ("Memórias Póstumas de Brás Cubas", "Machado de Assis"),
            ("O Alienista", "Machado de Assis"),
            ("Iracema", "José de Alencar"),
            ("Senhora", "José de Alencar"),
            ("O Pequeno Príncipe", "Antoine de Saint-Exupéry"),
            ("Orgulho e Preconceito", "Jane Austen"),
            ("Cem Anos de Solidão", "Gabriel García Márquez"),
            ("Grande Sertão: Veredas", "Guimarães Rosa"),
            ("O Processo", "Franz Kafka"),
            ("A Revolução dos Bichos", "George Orwell"),
            ("Crime e Castigo", "Fiódor Dostoiévski"),
            ("Fahrenheit 451", "Ray Bradbury"),
            ("A Metamorfose", "Franz Kafka"),
            ("Ensaio sobre a Cegueira", "José Saramago"),
        ]

        for t, a in livros:
            row.addWidget(LivroCard(t, a))

        row.addStretch()

        self.scroll.setWidget(container)

        layout.addWidget(self.scroll)


# -------------------------
# LEITOR
# -------------------------

class Reader(QWidget):

    def __init__(self, titulo):
        super().__init__()

        self.setWindowTitle(titulo)

        layout = QVBoxLayout(self)

        self.text = QLabel("Página 1\n\nConteúdo do livro...")
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setWordWrap(True)

        btn = QPushButton("Próxima Página")
        btn.clicked.connect(self.next_page)

        layout.addWidget(self.text)
        layout.addWidget(btn)

        self.page = 1

    def next_page(self):
        self.page += 1
        self.text.setText(f"Página {self.page}\n\nTexto do livro...")


# -------------------------
# RANKING
# -------------------------

class Ranking(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("🏆 Livros mais favoritados")
        title.setStyleSheet("font-size:18px;font-weight:bold")
        layout.addWidget(title)

        self.lista = QListWidget()
        layout.addWidget(self.lista)

        self.populate()

    def populate(self):
        self.lista.clear()

        for titulo, autor, total in db.ranking():

            item = QListWidgetItem()

            widget = QWidget()
            row = QHBoxLayout(widget)

            cover = QLabel()
            cover.setFixedSize(48, 64)
            cover.setScaledContents(True)

            pix = get_book_cover(titulo, "S")
            if pix:
                cover.setPixmap(pix)
            else:
                cover.setStyleSheet("background:#ddd")

            text = QLabel(f"{titulo}\n{autor}\n⭐ {total}")

            row.addWidget(cover)
            row.addWidget(text)

            item.setSizeHint(widget.sizeHint())

            self.lista.addItem(item)
            self.lista.setItemWidget(item, widget)


# -------------------------
# JANELA PRINCIPAL
# -------------------------

class Biblioteca(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Biblioteca Digital")

        tabs = QTabWidget()

        home = QWidget()
        v = QVBoxLayout(home)

        v.addWidget(QLabel("🔥 Populares"))
        v.addWidget(Carrossel())

        tabs.addTab(home, "Home")
        tabs.addTab(Ranking(), "Ranking")

        self.setCentralWidget(tabs)

        self.resize(1100, 700)


# -------------------------
# APP
# -------------------------

app = QApplication(sys.argv)

window = Biblioteca()
window.show()

sys.exit(app.exec())