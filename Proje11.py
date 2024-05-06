import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5 import QtCore
# Enstrüman sınıfı
class Enstrüman:
    def __init__(self, adı, stok_miktarı, fiyat):
        self.adı = adı
        self.stok_miktarı = stok_miktarı
        self.fiyat = fiyat
        self.satış_listesi = []

    def enstrüman_ekle(self, miktar):
        self.stok_miktarı += miktar

    def satış_yap(self, miktar):
        if self.stok_miktarı >= miktar:
            self.stok_miktarı -= miktar
            return True
        else:
            return False

    def destek_oluştur(self, talep_detayı):
        destek_talebi = Destek(talep_detayı)
        return destek_talebi

# Müşteri sınıfı
class Müşteri:
    def __init__(self, adı, soyadı, email, adres):
        self.adı = adı
        self.soyadı = soyadı
        self.email = email
        self.adres = adres
        self.sipariş_geçmişi = []

    def sipariş_ver(self, enstrüman, miktar, adres):
        if enstrüman.satış_yap(miktar):
            satış = Satış(enstrüman, miktar, adres)
            self.sipariş_geçmişi.append(satış)
            return True
        else:
            return False

# Satış sınıfı
class Satış:
    def __init__(self, enstrüman, miktar, adres):
        self.enstrüman = enstrüman
        self.miktar = miktar
        self.adres = adres
        self.sipariş_numarası = len(enstrüman.satış_listesi) + 1
        enstrüman.satış_listesi.append(self)

# Destek sınıfı
class Destek:
    destek_listesi = []

    def __init__(self, talep_detayı):
        self.talep_detayı = talep_detayı
        self.destek_talebi_numarası = len(Destek.destek_listesi) + 1
        Destek.destek_listesi.append(self)

# PyQt5 kullanarak arayüz oluştur
class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Enstrüman Mağazası')
        self.setGeometry(100, 100, 300, 300)

        layout = QVBoxLayout()

        self.label = QLabel('Menü:', self)
        layout.addWidget(self.label)

        self.button1 = QPushButton('Enstrümanları Görüntüle', self)
        layout.addWidget(self.button1)

        self.button2 = QPushButton('Sipariş Ver', self)
        layout.addWidget(self.button2)

        self.button3 = QPushButton('Destek Talebi Oluştur', self)
        layout.addWidget(self.button3)

        self.button4 = QPushButton('Çıkış', self)
        layout.addWidget(self.button4)

        self.setLayout(layout)

        self.button1.clicked.connect(self.goster_enstrumanlar)
        self.button2.clicked.connect(self.siparis_ver_dialog_ac)
        self.button3.clicked.connect(self.destek_talebi_dialog_ac)
        self.button4.clicked.connect(self.close)

    def goster_enstrumanlar(self):
        self.label.setText("Enstrümanlar:\nGitar - Stok: 1000 - Fiyat: 2500TL\nPiyano - Stok: 2000 - Fiyat: 10000\nDavul - Stok: 2500 - Fiyat:1500")

    def siparis_ver_dialog_ac(self):
        self.siparis_ver_dialog = SiparisVerDialog()
        self.siparis_ver_dialog.siparis_ver_signal.connect(self.siparis_ver)
        self.siparis_ver_dialog.show()

    def destek_talebi_dialog_ac(self):
        self.destek_talebi_dialog = DestekTalebiDialog()
        self.destek_talebi_dialog.destek_talebi_signal.connect(self.goster_destek_talebi)
        self.destek_talebi_dialog.show()

    def siparis_ver(self, müşteri_adi, enstruman_adi, miktar, adres):
        # Sipariş verme işlemleri buraya gelecek
        self.label.setText(f"Sipariş Verildi:\nMüşteri Adı: {müşteri_adi}\nEnstrüman Adı: {enstruman_adi}\nMiktar: {miktar}\nAdres: {adres}")

    def goster_destek_talebi(self, talep_detayı):
        self.destek_talebi_pencere = DestekTalebiPencere(talep_detayı)
        self.destek_talebi_pencere.show()

# Sipariş verme dialog penceresi
class SiparisVerDialog(QWidget):
    siparis_ver_signal = QtCore.pyqtSignal(str, str, int, str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sipariş Ver')
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.musteri_adı = QLineEdit(self)
        self.musteri_adı.setPlaceholderText('Müşteri adı')
        layout.addWidget(self.musteri_adı)

        self.enstruman_adı = QLineEdit(self)
        self.enstruman_adı.setPlaceholderText('Enstrüman adı')
        layout.addWidget(self.enstruman_adı)

        self.miktar = QLineEdit(self)
        self.miktar.setPlaceholderText('Miktar')
        layout.addWidget(self.miktar)

        self.adres = QLineEdit(self)
        self.adres.setPlaceholderText('Adres')
        layout.addWidget(self.adres)

        self.siparis_ver_button = QPushButton('Sipariş Ver', self)
        layout.addWidget(self.siparis_ver_button)

        self.setLayout(layout)

        self.siparis_ver_button.clicked.connect(self.siparis_ver)

    def siparis_ver(self):
        müsteri_adi = self.musteri_adı.text()
        enstruman_adi = self.enstruman_adı.text()
        miktar = int(self.miktar.text())
        adres = self.adres.text()
        self.siparis_ver_signal.emit(müsteri_adi, enstruman_adi, miktar, adres)
        self.close()

# Destek talebi oluşturma dialog penceresi
class DestekTalebiDialog(QWidget):
    destek_talebi_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Destek Talebi Oluştur')
        self.setGeometry(200, 200, 300, 100)

        layout = QVBoxLayout()

        self.talep_detayı = QLineEdit(self)
        self.talep_detayı.setPlaceholderText('Destek talebi detayları')
        layout.addWidget(self.talep_detayı)

        self.destek_talebi_button = QPushButton('Destek Talebi Oluştur', self)
        layout.addWidget(self.destek_talebi_button)

        self.setLayout(layout)

        self.destek_talebi_button.clicked.connect(self.destek_talebi_olustur)

    def destek_talebi_olustur(self):
        talep_detayı = self.talep_detayı.text()
        self.destek_talebi_signal.emit(talep_detayı)
        self.close()

# Destek talebi penceresi
class DestekTalebiPencere(QWidget):
    def __init__(self, talep_detayı):
        super().__init__()
        self.initUI(talep_detayı)

    def initUI(self, talep_detayı):
        self.setWindowTitle('Destek Talebi Detayı')
        self.setGeometry(300, 300, 300, 100)

        layout = QVBoxLayout()

        self.label = QLabel(talep_detayı, self)
        layout.addWidget(self.label)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec_())

