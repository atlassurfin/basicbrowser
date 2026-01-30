import sys
from PyQt6.QtCore import QUrl, QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLineEdit, 
                            QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMenu)
from PyQt6.QtWebEngineWidgets import QWebEngineView


#Classe principale del browser
class BBrowser(QMainWindow):
    def __init__(self):
        super().__init__()


        #Finestra principale
        self.setWindowTitle("My First Browser I Guess -_-'' ")
        #qui metterò l'icona del browser, magari creerò il logo con un servizio gratuito o prendo spunto da altri loghi
        self.resize(1024, 768)



        self.setStyleSheet("""
            QMainWindow{
                background-color: #d9d9d9;
            }
            QPushButton{
                background-color: #cccccc;
                color: #333;
                border-radius: 5px;
                padding: 5px;
                min-width: 40px;
            }
            QPushButton:hover{
                background-color: #b3b3b3;
            }
            QLineEdit{
                border: 2px solid #cccccc
                border-radius: 10px;
                padding: 5px;
                background-color: #1e1e1e;
                color: #a9b7c6;             
            }
            #BookmarkBtn {
                background-color: #e0e0e0;
                color: #333;
                min-width: 80px;
                font-size: 11px;
            }
        """)

        #Web Engine
        self.browser = QWebEngineView()
        self.home_url = "https://www.google.com"
        self.browser.setUrl(QUrl(self.home_url))

        #Creazione pulsanti e collegamento a funzioni
        self.btn_back = QPushButton()
        self.btn_back.setIcon(QIcon("assets/back.png"))
        self.btn_back.setIconSize(QSize(24, 24))
        self.btn_back.clicked.connect(self.browser.back)

        self.btn_forward = QPushButton()
        self.btn_forward.setIcon(QIcon("assets/forward.png"))
        self.btn_forward.setIconSize(QSize(24, 24))
        self.btn_forward.clicked.connect(self.browser.forward)

        self.btn_reload = QPushButton()
        self.btn_reload.setIcon(QIcon("assets/reload.png"))
        self.btn_reload.setIconSize(QSize(24, 24))
        self.btn_reload.clicked.connect(self.browser.reload)

        self.btn_home = QPushButton()
        self.btn_home.setIcon(QIcon("assets/home.png"))
        self.btn_home.setIconSize(QSize(24, 24))
        self.btn_home.clicked.connect(self.go_home)


        #Barra URL
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.browse_to_site)

        #Pulsante per aggiungere preferiti
        self.btn_addbkm = QPushButton()
        self.btn_addbkm.setIcon(QIcon("assets/add.png"))
        self.btn_addbkm.setIconSize(QSize(24, 24))
        self.btn_addbkm.clicked.connect(self.add_to_bmarks)

        #Pulsante menù
        self.btn_menu = QPushButton()
        self.btn_menu.setIcon(QIcon("assets/menu.png"))
        self.btn_menu.setIconSize(QSize(24, 24))

        #Menù a tendina
        main_menu = QMenu(self)
        main_menu.addAction("Impostazioni")
        main_menu.addAction("Cronologia")
        main_menu.addSeparator()
        main_menu.addAction("Esci", self.close)

        self.btn_menu.setMenu(main_menu)


        #Pulsante menù preferiti
        self.btn_bmark = QPushButton()
        self.btn_bmark.setIcon(QIcon("assets/star_menu.png"))
        self.btn_bmark.setIconSize(QSize(24,24))


        #Layout Orizzontale per comandi
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.btn_back)
        nav_layout.addWidget(self.btn_forward)
        nav_layout.addWidget(self.btn_reload)
        nav_layout.addWidget(self.btn_home)
        nav_layout.addWidget(self.btn_bmark)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.btn_addbkm)
        nav_layout.addWidget(self.btn_menu)

        #Barra Preferiti
        self.bookmark_layout = QHBoxLayout()
        self.bookmark_layout.setContentsMargins(10, 0, 10, 0)
        self.bookmark_layout.addStretch()

        #Creo un po' di segnalibri
        btn_git = QPushButton("GitHub")
        btn_git.setObjectName("BookmarkBtn")
        btn_git.setIcon(QIcon("assets/star.png"))
        btn_git.clicked.connect(lambda: self.browser.setUrl(QUrl("https://github.com")))

        btn_yt = QPushButton("YouTube")
        btn_yt.setObjectName("BookmarkBtn")
        btn_yt.setIcon(QIcon("assets/star.png"))
        btn_yt.clicked.connect(lambda: self.browser.setUrl(QUrl("https://www.youtube.com")))

        self.bookmark_layout.addWidget(btn_git)
        self.bookmark_layout.addWidget(btn_yt)
        self.bookmark_layout.addStretch()



        #Layout Verticale (principale)
        main_layout = QVBoxLayout()
        main_layout.addLayout(nav_layout) #metto barra comandi sopra
        main_layout.addLayout(self.bookmark_layout) #aggiungo barra preferiti
        main_layout.addWidget(self.browser) #metto browser sotto

        #Contenitore per layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


        #Sincronizzazione
        self.browser.urlChanged.connect(self.update_url_bar)

    #Funzione per caricare sito inserito da user

    def add_to_bmarks(self):
        url = self.browser.url().toString()
        title = self.browser.page().title()

        if len(title) > 15: title = title[:12] + "..."

        new_bmk = QPushButton(title)
        new_bmk.setObjectName("BookmarkBtn")
        new_bmk.setIcon(QIcon("assets/star.png"))
        new_bmk.clicked.connect(lambda: self.browser.setUrl(QUrl(url)))
        new_bmk.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        new_bmk.customContextMenuRequested.connect(lambda pos: self.show_bookmark_menu(pos, new_bmk))

        self.bookmark_layout.insertWidget(0, new_bmk)

    def show_bookmark_menu(self, pos, button):
        menu = QMenu()
        remove_action = menu.addAction("Rimuovi preferito")

        action = menu.exec(button.mapToGlobal(pos))
        if action == remove_action:
            button.deleteLater()

    def browse_to_site(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    def go_home(self):
        self.browser.setUrl(QUrl(self.home_url))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BBrowser()
    window.show()
    sys.exit(app.exec())
        
