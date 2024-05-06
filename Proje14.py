import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QInputDialog, QMessageBox

class Proje:
    def __init__(self, adı, başlangıç_tarihi, bitiş_tarihi):
        self.adı = adı
        self.başlangıç_tarihi = başlangıç_tarihi
        self.bitiş_tarihi = bitiş_tarihi
        self.görevler = []

    def görev_oluştur(self, görev_adı, sorumlu_kişi):
        görev = Görev(görev_adı, sorumlu_kişi)
        self.görevler.append(görev)

    def görev_atama(self, görev, çalışan):
        görev.sorumlu_kişi = çalışan

    def ilerleme_kaydet(self, görev, ilerleme):
        görev.ilerleme = ilerleme

    def __str__(self):
        return f"Proje: {self.adı}, Başlangıç Tarihi: {self.başlangıç_tarihi}, Bitiş Tarihi: {self.bitiş_tarihi}"

class Görev:
    def __init__(self, adı, sorumlu_kişi):
        self.adı = adı
        self.sorumlu_kişi = sorumlu_kişi
        self.ilerleme = 0

    def __str__(self):
        return f"Görev: {self.adı}, Sorumlu Kişi: {self.sorumlu_kişi.adı}"

class Çalışan:
    def __init__(self, adı):
        self.adı = adı
        self.görevler = []

    def görev_ekle(self, görev):
        self.görevler.append(görev)

    def __str__(self):
        return f"Çalışan: {self.adı}"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Proje Yönetimi")
        self.layout = QVBoxLayout()

        self.projeler_list = QListWidget()

        self.button_projeleri_goster = QPushButton("Projeleri Göster")
        self.button_projeleri_goster.clicked.connect(self.projeleri_goster)

        self.button_proje_olustur = QPushButton("Proje Oluştur")
        self.button_proje_olustur.clicked.connect(self.proje_olustur)

        self.button_gorev_olustur = QPushButton("Görev Oluştur")
        self.button_gorev_olustur.clicked.connect(self.gorev_olustur)

        self.button_gorev_atama = QPushButton("Görevi Çalışana Ata")
        self.button_gorev_atama.clicked.connect(self.gorev_atama)

        self.button_ilerleme_kaydet = QPushButton("İlerleme Kaydet")
        self.button_ilerleme_kaydet.clicked.connect(self.ilerleme_kaydet)

        self.button_gorevleri_goster = QPushButton("Görevleri Göster")
        self.button_gorevleri_goster.clicked.connect(self.gorevleri_goster)

        self.button_projeleri_goster.setMaximumWidth(200)
        self.button_proje_olustur.setMaximumWidth(200)
        self.button_gorev_olustur.setMaximumWidth(200)
        self.button_gorev_atama.setMaximumWidth(200)
        self.button_ilerleme_kaydet.setMaximumWidth(200)
        self.button_gorevleri_goster.setMaximumWidth(200)

        self.layout.addWidget(self.projeler_list)
        self.layout.addWidget(self.button_projeleri_goster)
        self.layout.addWidget(self.button_proje_olustur)
        self.layout.addWidget(self.button_gorev_olustur)
        self.layout.addWidget(self.button_gorev_atama)
        self.layout.addWidget(self.button_ilerleme_kaydet)
        self.layout.addWidget(self.button_gorevleri_goster)

        self.setLayout(self.layout)

    def projeleri_goster(self):
        self.projeler_list.clear()
        for proje in projeler:
            self.projeler_list.addItem(f"{proje.adı}")

    def proje_olustur(self):
        proje_adi, ok = QInputDialog.getText(self, "Proje Oluştur", "Proje adı:")
        if ok and proje_adi:
            başlangıç_tarihi, ok = QInputDialog.getText(self, "Proje Oluştur", "Başlangıç tarihi:")
            if ok and başlangıç_tarihi:
                bitiş_tarihi, ok = QInputDialog.getText(self, "Proje Oluştur", "Bitiş tarihi:")
                if ok and bitiş_tarihi:
                    proje = Proje(proje_adi, başlangıç_tarihi, bitiş_tarihi)
                    projeler.append(proje)
                    QMessageBox.information(self, "Proje Oluşturma", "Proje başarıyla oluşturuldu.")
                    self.projeleri_goster()

    def gorev_olustur(self):
        selected_item = self.projeler_list.currentItem()
        if selected_item:
            proje_adi = selected_item.text()
            görev_adı, ok = QInputDialog.getText(self, "Görev Oluştur", f"{proje_adi} için görev adı:")
            if ok:
                sorumlu_kişi, ok = QInputDialog.getText(self, "Görev Oluştur", "Sorumlu kişinin adı:")
                if ok:
                    proje = next((p for p in projeler if p.adı == proje_adi), None)
                    if proje:
                        çalışan = next((c for c in çalışanlar if c.adı == sorumlu_kişi), None)
                        if not çalışan:
                            çalışan = Çalışan(sorumlu_kişi)
                            çalışanlar.append(çalışan)
                        proje.görev_oluştur(görev_adı, çalışan)
                        QMessageBox.information(self, "Görev Oluşturma", "Görev başarıyla oluşturuldu.")
                    else:
                        QMessageBox.warning(self, "Uyarı", "Proje bulunamadı.")
            else:
                QMessageBox.warning(self, "Uyarı", "Görev adı girmediniz.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir proje seçin.")

    def gorev_atama(self):
        selected_item = self.projeler_list.currentItem()
        if selected_item:
            proje_adi = selected_item.text()
            görev_adı, ok = QInputDialog.getText(self, "Görev Atama", f"{proje_adi} için görev adı:")
            if ok:
                çalışan_adı, ok = QInputDialog.getText(self, "Görev Atama", "Çalışanın adı:")
                if ok:
                    proje = next((p for p in projeler if p.adı == proje_adi), None)
                    if proje:
                        görev = next((g for g in proje.görevler if g.adı == görev_adı), None)
                        if görev:
                            çalışan = next((c for c in çalışanlar if c.adı == çalışan_adı), None)
                            if not çalışan:
                                çalışan = Çalışan(çalışan_adı)
                                çalışanlar.append(çalışan)
                            proje.görev_atama(görev, çalışan)
                            QMessageBox.information(self, "Görev Atama", "Görev başarıyla atanmıştır.")
                        else:
                            QMessageBox.warning(self, "Uyarı", "Görev bulunamadı.")
                    else:
                        QMessageBox.warning(self, "Uyarı", "Proje bulunamadı.")
            else:
                QMessageBox.warning(self, "Uyarı", "Görev adı girmediniz.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir proje seçin.")

    def ilerleme_kaydet(self):
        selected_item = self.projeler_list.currentItem()
        if selected_item:
            proje_adi = selected_item.text()
            görev_adı, ok = QInputDialog.getText(self, "İlerleme Kaydet", f"{proje_adi} için görev adı:")
            if ok:
                ilerleme, ok = QInputDialog.getInt(self, "İlerleme Kaydet", "İlerleme (hafta):", 0)
                if ok:
                    proje = next((p for p in projeler if p.adı == proje_adi), None)
                    if proje:
                        görev = next((g for g in proje.görevler if g.adı == görev_adı), None)
                        if görev:
                            proje.ilerleme_kaydet(görev, ilerleme)
                            QMessageBox.information(self, "İlerleme Kaydet", "İlerleme kaydedildi.")
                        else:
                            QMessageBox.warning(self, "Uyarı", "Görev bulunamadı.")
                    else:
                        QMessageBox.warning(self, "Uyarı", "Proje bulunamadı.")
            else:
                QMessageBox.warning(self, "Uyarı", "Görev adı girmediniz.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir proje seçin.")

    def gorevleri_goster(self):
        selected_item = self.projeler_list.currentItem()
        if selected_item:
            proje_adi = selected_item.text()
            proje = next((p for p in projeler if p.adı == proje_adi), None)
            if proje:
                görevler = "\n".join([str(g) for g in proje.görevler])
                QMessageBox.information(self, "Görevler", f"{proje_adi} için görevler:\n{görevler}")
            else:
                QMessageBox.warning(self, "Uyarı", "Proje bulunamadı.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir proje seçin.")

projeler = []
çalışanlar = []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
