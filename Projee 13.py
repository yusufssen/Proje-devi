import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QInputDialog, QMessageBox, QLabel

class Etkinlik:
    def __init__(self, adı, tarih, mekan, bilet_miktarı):
        self.adı = adı
        self.tarih = tarih
        self.mekan = mekan
        self.bilet_miktarı = bilet_miktarı

class Kullanıcı:
    def __init__(self, adı, soyadı, email):
        self.adı = adı
        self.soyadı = soyadı
        self.email = email

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Etkinlik Yönetimi")
        self.layout = QVBoxLayout()

        self.etkinlik_list = QListWidget()

        self.button_goster = QPushButton("Etkinlikleri Göster")
        self.button_goster.clicked.connect(self.goster_etkinlikler)

        self.button_satin_al = QPushButton("Bilet Satın Al")
        self.button_satin_al.clicked.connect(self.bilet_satin_al)

        self.bilgi_label = QLabel("")
        self.layout.addWidget(self.etkinlik_list)
        self.layout.addWidget(self.button_goster)
        self.layout.addWidget(self.button_satin_al)
        self.layout.addWidget(self.bilgi_label)

        self.setLayout(self.layout)

    def goster_etkinlikler(self):
        self.etkinlik_list.clear()
        for etkinlik in etkinlikler:
            self.etkinlik_list.addItem(f"{etkinlik.adı} - {etkinlik.tarih} - {etkinlik.mekan} - Kalan bilet: {etkinlik.bilet_miktarı}")

    def bilet_satin_al(self):
        selected_item = self.etkinlik_list.currentItem()
        if selected_item:
            etkinlik_adı = selected_item.text().split(" - ")[0]
            miktar, ok = QInputDialog.getInt(self, "Bilet Satın Al", f"{etkinlik_adı} için kaç bilet almak istiyorsunuz?")
            if ok:
                for etkinlik in etkinlikler:
                    if etkinlik.adı == etkinlik_adı:
                        etkinlik.bilet_miktarı -= miktar
                        self.goster_etkinlikler()
                        isim, ok = QInputDialog.getText(self, "Bilgi", "Adınızı Giriniz:")
                        telefon, ok = QInputDialog.getText(self, "Bilgi", "Telefon Numaranızı Giriniz:")
                        email, ok = QInputDialog.getText(self, "Bilgi", "E-mail Adresinizi Giriniz:")
                        self.bilgi_label.setText(f"Bilet Alıcı Bilgileri:\nAdı: {isim}\nTelefon: {telefon}\nE-mail: {email}")
                        QMessageBox.information(self, "Bilet Satın Alma", f"{miktar} adet bilet satın alındı.")
                        return  # Bilet satın alındıktan sonra işlemi sonlandır
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir etkinlik seçin.")

etkinlikler = [
    Etkinlik("Konser", "2023-02-15", "İstanbul", 100),
    Etkinlik("Tiyatro", "2023-03-20", "Ankara", 50),
    Etkinlik("Festival", "2023-04-01", "İzmir", 200)
]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

