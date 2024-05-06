import sys
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QDialog, QDialogButtonBox, QMessageBox, QInputDialog, QFormLayout
)
from PyQt5.QtCore import QTimer

class Kullanıcı:
    def __init__(self, isim, yaş, cinsiyet):
        self.isim = isim
        self.yaş = yaş
        self.cinsiyet = cinsiyet
        self.sağlık_kayıtları = []
        self.egzersizler = []

    def kayıt_ekle(self, sağlık_kaydı):
        self.sağlık_kayıtları.append(sağlık_kaydı)

    def egzersiz_ekle(self, egzersiz):
        self.egzersizler.append(egzersiz)

    def rapor_oluştur(self):
        rapor = f"Sağlık Raporu için {self.isim}\n"
        for kayıt in self.sağlık_kayıtları:
            rapor += str(kayıt) + "\n"
        rapor += "Egzersiz Rutini:\n"
        for egzersiz in self.egzersizler:
            rapor += str(egzersiz) + "\n"
        return rapor

class SağlıkKaydı:
    def __init__(self, tarih, kilo, boy, sigara_iciliyor_mu):
        self.tarih = tarih
        self.kilo = kilo
        self.boy = boy
        self.sigara_iciliyor_mu = sigara_iciliyor_mu

    def __str__(self):
        return f"Tarih: {self.tarih}, Kilo: {self.kilo} kg, Boy: {self.boy} cm, Sigara: {self.sigara_iciliyor_mu}"

class Egzersiz:
    def __init__(self, isim, süre, tekrar):
        self.isim = isim
        self.süre = süre
        self.tekrar = tekrar

    def __str__(self):
        return f"{self.isim}: {self.süre} dakika, {self.tekrar} tekrar"

class KayitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sağlık Kaydı Ekle")
        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()

        self.input_tarih = QLineEdit()
        self.form_layout.addRow("Tarih (YYYY-MM-DD):", self.input_tarih)

        self.input_kilo = QLineEdit()
        self.form_layout.addRow("Kilo (kg):", self.input_kilo)

        self.input_boy = QLineEdit()
        self.form_layout.addRow("Boy (cm):", self.input_boy)

        self.input_sigara = QLineEdit()
        self.form_layout.addRow("Sigara içiyor mu? [E/H]:", self.input_sigara)

        self.layout.addLayout(self.form_layout)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)

    def get_kayit(self):
        tarih = self.input_tarih.text()
        kilo = self.input_kilo.text()
        boy = self.input_boy.text()
        sigara = self.input_sigara.text()
        return SağlıkKaydı(tarih, kilo, boy, sigara)

class EgzersizDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Egzersiz Rutini Oluştur")
        self.layout = QVBoxLayout()

        self.label_isim = QLabel("Egzersiz İsmi:")
        self.input_isim = QLineEdit()

        self.label_sure = QLabel("Süre (dakika):")
        self.input_sure = QLineEdit()

        self.label_tekrar = QLabel("Tekrar Sayısı:")
        self.input_tekrar = QLineEdit()

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.label_isim)
        self.layout.addWidget(self.input_isim)
        self.layout.addWidget(self.label_sure)
        self.layout.addWidget(self.input_sure)
        self.layout.addWidget(self.label_tekrar)
        self.layout.addWidget(self.input_tekrar)
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_egzersiz(self):
        isim = self.input_isim.text()
        sure = self.input_sure.text()
        tekrar = self.input_tekrar.text()
        return Egzersiz(isim, sure, tekrar)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.kullanici = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hatirlatici_goster)

    def init_ui(self):
        self.setWindowTitle("Kişisel Sağlık Takip Uygulaması")
        self.layout = QVBoxLayout()

        self.label_isim = QLabel("İsim:")
        self.input_isim = QLineEdit()

        self.label_yas = QLabel("Yaş:")
        self.input_yas = QLineEdit()

        self.label_cinsiyet = QLabel("Cinsiyet [E/K]:")
        self.input_cinsiyet = QLineEdit()

        self.button_kullanici_olustur = QPushButton("Kullanıcı Oluştur")
        self.button_kullanici_olustur.clicked.connect(self.kullanici_olustur)

        self.button_egzersiz_olustur = QPushButton("Egzersiz Rutini Oluştur")
        self.button_egzersiz_olustur.clicked.connect(self.egzersiz_olustur)

        self.button_kayit_olustur = QPushButton("Sağlık Kaydı Ekle")
        self.button_kayit_olustur.clicked.connect(self.kayit_olustur)

        self.button_hatirlatici = QPushButton("Hatırlatıcı Ekle")
        self.button_hatirlatici.clicked.connect(self.hatirlatici_ekle)

        self.button_grafik_goster = QPushButton("Sağlık Verileri Grafiği Göster")
        self.button_grafik_goster.clicked.connect(self.grafik_goster)

        self.text_rapor = QTextEdit()

        self.layout.addWidget(self.label_isim)
        self.layout.addWidget(self.input_isim)
        self.layout.addWidget(self.label_yas)
        self.layout.addWidget(self.input_yas)
        self.layout.addWidget(self.label_cinsiyet)
        self.layout.addWidget(self.input_cinsiyet)
        self.layout.addWidget(self.button_kullanici_olustur)
        self.layout.addWidget(self.button_egzersiz_olustur)
        self.layout.addWidget(self.button_kayit_olustur)
        self.layout.addWidget(self.button_hatirlatici)
        self.layout.addWidget(self.button_grafik_goster)
        self.layout.addWidget(self.text_rapor)

        self.setLayout(self.layout)

    def kullanici_olustur(self):
        isim = self.input_isim.text()
        yas = self.input_yas.text()
        cinsiyet = self.input_cinsiyet.text()

        self.kullanici = Kullanıcı(isim, yas, cinsiyet)
        self.text_rapor.setText(self.kullanici.rapor_oluştur())

    def egzersiz_olustur(self):
        if not self.kullanici:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir kullanıcı oluşturun!")
            return

        dialog = EgzersizDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            egzersiz = dialog.get_egzersiz()
            self.kullanici.egzersiz_ekle(egzersiz)
            self.text_rapor.append(f"Egzersiz Oluşturuldu: {egzersiz}")

    def kayit_olustur(self):
        if not self.kullanici:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir kullanıcı oluşturun!")
            return

        dialog = KayitDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            kayit = dialog.get_kayit()
            self.kullanici.kayıt_ekle(kayit)
            self.text_rapor.append(f"Sağlık Kaydı Eklendi: {kayit}")

    def hatirlatici_ekle(self):
        tarih, ok = QInputDialog.getText(self, "Hatırlatıcı Ekle", "Hatırlatıcı zamanını girin (HH:MM):")
        if ok:
            self.timer.stop()
            self.timer.start(1000 * 60)
            self.hatirlatici_zamani = datetime.datetime.strptime(tarih, "%H:%M")
            cevap = QMessageBox.question(self, "Hatırlatıcı Ekle", "Ekranı kapatmak istiyor musunuz?",
                                         QMessageBox.Yes | QMessageBox.No)
            if cevap == QMessageBox.Yes:
                self.close()

    def hatirlatici_goster(self):
        simdiki_zaman = datetime.datetime.now().time()
        if simdiki_zaman.hour == self.hatirlatici_zamani.hour and simdiki_zaman.minute == self.hatirlatici_zamani.minute:
            QMessageBox.information(self, "Hatırlatıcı", "Egzersiz yapma zamanı geldi!")
            self.timer.stop()

    def grafik_goster(self):
        if self.kullanici:
            tarihler = [datetime.datetime.strptime(kayit.tarih, "%Y-%m-%d") for kayit in
                        self.kullanici.sağlık_kayıtları]
            kilolar = [float(kayit.kilo) for kayit in self.kullanici.sağlık_kayıtları]
            boyler = [float(kayit.boy) for kayit in self.kullanici.sağlık_kayıtları]

            fig, ax = plt.subplots()
            ax.plot(tarihler, kilolar, label='Kilo')
            ax.plot(tarihler, boyler, label='Boy')
            ax.set_xlabel('Tarih')
            ax.set_ylabel('Değer')
            ax.legend()
            ax.grid(True)

            canvas = FigureCanvasQTAgg(fig)
            canvas.show()

            grafik_dialog = QDialog(self)
            grafik_dialog.setWindowTitle("Sağlık Verileri Grafiği")
            layout = QVBoxLayout()
            layout.addWidget(canvas)
            grafik_dialog.setLayout(layout)
            grafik_dialog.exec_()

            plt.close(fig)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
