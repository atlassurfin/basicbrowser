import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView


#Classe principale del browser
class BBrowser(QMainWindow):
    def __init__(self):
        super().__init__()


        #Finestra principale
        self.setWindowTitle("My First Browser I Guess -_-'' ")
        self.resize(1024, 768)


        #Web Engine
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        #Barra URL
        self.url_bar = QLineEdit()
        #Connetto invio al cambia pagina
        self.url_bar.returnPressed.connect(self.browse_to_site)

        #Layout
        layout = QVBoxLayout()
        layout.addWidget(self.url_bar)
        layout.addWidget(self.browser)

        #Contenitore per layout
        container = QWidget()
        container.setLayout(layout)
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
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BBrowser()
    window.show()
    sys.exit(app.exec())
        
