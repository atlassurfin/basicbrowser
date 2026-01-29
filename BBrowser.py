import sys
from PyQt6.QtCore import QUrl, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLineEdit, 
                            QVBoxLayout, QHBoxLayout, QWidget, QPushButton)
from PyQt6.QtWebEngineWidgets import QWebEngineView


#Classe principale del browser
class BBrowser(QMainWindow):
    def __init__(self):
        super().__init__()


        #Finestra principale
        self.setWindowTitle("My First Browser I Guess -_-'' ")
        self.resize(1024, 768)



        self.setStyleSheet("""
            QMainWindow{
                background-color: #2b2b2b;
            }
            QPushButton{
                background-color: #3c3f41;
                color: white;
                border-radius: 5px;
                padding: 5px;
                min-width: 40px;
            }
            QPushButton:hover{
                background-color: #4e5254;
            }
            QLineEdit{
                border: 2px solid #3c3f41
                border-radius: 10px;
                padding: 5px;
                background-color: #1e1e1e;
                color: #a9b7c6;
                selection-background-color: #214283               
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

        #Layout Orizzontale per comandi
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.btn_back)
        nav_layout.addWidget(self.btn_forward)
        nav_layout.addWidget(self.btn_reload)
        nav_layout.addWidget(self.btn_home)
        nav_layout.addWidget(self.url_bar)



        #Layout Verticale (principale)
        main_layout = QVBoxLayout()
        main_layout.addLayout(nav_layout) #metto barra comandi sopra
        main_layout.addWidget(self.browser) #metto browser sotto

        #Contenitore per layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


        #Sincronizzazione
        self.browser.urlChanged.connect(self.update_url_bar)

    #Funzione per caricare sito inserito da user
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
        
