import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QMessageBox, QLabel

class Kitap:
    def _init_(self, isim, yazar, yayınevi):
        self.isim = isim
        self.yazar = yazar
        self.yayınevi = yayınevi
        self.okuyucular = []
        self.yorumlar = []

    def kitap_ekle(self):
        print(f"Kitap '{self.isim}' eklendi.")

    def kitap_oku(self, kullanıcı):
        if kullanıcı not in self.okuyucular:
            self.okuyucular.append(kullanıcı)
            print(f"Kitap '{self.isim}' okunuyor.")
        else:
            print("Kitap zaten okunmuş.")

    def yorum_yap(self, yorum_metni, kullanıcı):
        self.yorumlar.append(Yorum(yorum_metni, kullanıcı))
        print(f"Kitap '{self.isim}' hakkında yorumunuz alındı: {yorum_metni}")

class Kullanıcı:
    def _init_(self, isim, şifre):
        self.isim = isim
        self.şifre = şifre
        self.okuma_listesi = []

    def kitap_okuma(self, kitap):
        kitap.kitap_oku(self)

    def yorum_yapma(self, kitap, yorum_metni):
        kitap.yorum_yap(yorum_metni, self)

class Yorum:
    def _init_(self, metin, kullanıcı):
        self.metin = metin
        self.kullanıcı = kullanıcı

# Veri yapıları
kitaplar = []
kullanıcılar = []
yorumlar = []

# Arayüz sınıfı
class MainWindow(QWidget):
    def _init_(self):
        super()._init_()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Kitap Okuma Uygulaması")
        self.layout = QVBoxLayout()

        self.kitaplar_list = QListWidget()

        self.button_kitaplari_goruntule = QPushButton("Kitapları Görüntüle")
        self.button_kitaplari_goruntule.clicked.connect(self.kitaplari_goruntule)

        self.input_kitap_oku = QLineEdit()
        self.button_kitap_oku = QPushButton("Kitap Oku")
        self.button_kitap_oku.clicked.connect(self.kitap_oku)

        self.input_yorum = QLineEdit()
        self.button_yorum_yap = QPushButton("Yorum Yap")
        self.button_yorum_yap.clicked.connect(self.yorum_yap)

        self.yorum_label = QLabel()  # QLabel for displaying the comment

        self.button_okuma_listesini_goruntule = QPushButton("Okuma Listesini Görüntüle")
        self.button_okuma_listesini_goruntule.clicked.connect(self.okuma_listesini_goruntule)

        self.layout.addWidget(self.kitaplar_list)
        self.layout.addWidget(self.button_kitaplari_goruntule)
        self.layout.addWidget(self.input_kitap_oku)
        self.layout.addWidget(self.button_kitap_oku)
        self.layout.addWidget(self.input_yorum)
        self.layout.addWidget(self.button_yorum_yap)
        self.layout.addWidget(self.yorum_label)
        self.layout.addWidget(self.button_okuma_listesini_goruntule)

        self.setLayout(self.layout)

    def kitaplari_goruntule(self):
        self.kitaplar_list.clear()
        for kitap in kitaplar:
            self.kitaplar_list.addItem(f"{kitap.isim} - {kitap.yazar} - {kitap.yayınevi}")

    def kitap_oku(self):
        selected_item = self.kitaplar_list.currentItem()
        if selected_item:
            kitap_isim = selected_item.text().split(" - ")[0]
            kullanıcı = kullanıcılar[0]
            for kitap in kitaplar:
                if kitap.isim == kitap_isim:
                    kitap.kitap_oku(kullanıcı)
                    QMessageBox.information(self, "Kitap Okuma", f"{kitap_isim} okunuyor.")
                    kullanıcı.okuma_listesi.append(kitap)
                    return
            QMessageBox.warning(self, "Uyarı", "Kitap bulunamadı.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kitap seçin.")

    def yorum_yap(self):
        selected_item = self.kitaplar_list.currentItem()
        if selected_item:
            kitap_isim = selected_item.text().split(" - ")[0]
            yorum_metni = self.input_yorum.text()
            kullanıcı = kullanıcılar[0]
            for kitap in kitaplar:
                if kitap.isim == kitap_isim:
                    kitap.yorum_yap(yorum_metni, kullanıcı)
                    self.yorum_label.setText(f"{kitap_isim} hakkında yorumunuz alındı: {yorum_metni}")  # Set QLabel text
                    QMessageBox.information(self, "Yorum Yapma", f"{kitap_isim} hakkında yorumunuz alındı: {yorum_metni}")
                    return
            QMessageBox.warning(self, "Uyarı", "Kitap bulunamadı.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kitap seçin.")

    def okuma_listesini_goruntule(self):
        kullanıcı = kullanıcılar[0]
        okuma_listesi = "\n".join([kitap.isim for kitap in kullanıcı.okuma_listesi])
        QMessageBox.information(self, "Okuma Listesi", f"{kullanıcı.isim}'nin okuma listesi:\n{okuma_listesi}")

# Örnek kitap ve kullanıcı ekleme
kitaplar.append(Kitap("1984", "George Orwell", "Penguin Books"))
kitaplar.append(Kitap("Tutunamayanlar", "Oğuz Atay", "İletişim Yayınları"))
kitaplar.append(Kitap("Sefiller","Victor Hugo","Can Yayınevi"))
kullanıcılar.append(Kullanıcı("Berkan Koç", "010810"))

if __name__ == "_main_":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())