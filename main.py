from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import os

# Plyer paylaşım (yoksa sorun çıkarmasın diye try)
try:
    from plyer import share as plyer_share
except Exception:
    plyer_share = None


def kayit_dosyasi_yolu():
    # APK içinde güvenli kayıt yeri
    return os.path.join(App.get_running_app().user_data_dir, "tum_kayitlar.txt")


def popup_goster(baslik, mesaj):
    p = Popup(
        title=baslik,
        content=Label(text=mesaj),
        size_hint=(0.88, 0.38),
        auto_dismiss=True,
    )
    p.open()


class MainUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=8, **kwargs)

        self.add_widget(Label(text="Mini Kayıt Uygulaması", size_hint_y=None, height=40))

        self.isim = TextInput(hint_text="Ad", multiline=False)
        self.soy = TextInput(hint_text="Soyad", multiline=False)
        self.yas = TextInput(hint_text="Yaş", multiline=False, input_filter="int")
        self.kilo = TextInput(hint_text="Kilo", multiline=False)
        self.il = TextInput(hint_text="İl", multiline=False)
        self.ilce = TextInput(hint_text="İlçe", multiline=False)
        self.hayal = TextInput(hint_text="Hayaliniz", multiline=False)

        for w in [self.isim, self.soy, self.yas, self.kilo, self.il, self.ilce, self.hayal]:
            self.add_widget(w)

        # 1. Buton satırı
        row1 = BoxLayout(size_hint_y=None, height=55, spacing=8)
        btn_kaydet = Button(text="Kaydet")
        btn_goster = Button(text="Kayıtları Göster")
        btn_temizle = Button(text="Temizle")

        btn_kaydet.bind(on_press=self.kaydet)
        btn_goster.bind(on_press=self.kayitlari_goster)
        btn_temizle.bind(on_press=self.temizle)

        row1.add_widget(btn_kaydet)
        row1.add_widget(btn_goster)
        row1.add_widget(btn_temizle)
        self.add_widget(row1)

        # 2. Buton satırı (Paylaş)
        row2 = BoxLayout(size_hint_y=None, height=55, spacing=8)
        btn_paylas = Button(text="Dosyayı Paylaş")
        btn_paylas.bind(on_press=self.dosyayi_paylas)
        row2.add_widget(btn_paylas)
        self.add_widget(row2)

        # Çıktı alanı
        self.out_label = Label(text="Hazır ✅", size_hint_y=None, halign="left", valign="top")
        self.out_label.bind(width=lambda *_: setattr(self.out_label, "text_size", (self.out_label.width, None)))
        self.out_label.bind(texture_size=lambda *_: setattr(self.out_label, "height", self.out_label.texture_size[1] + 20))

        scroll = ScrollView()
        scroll.add_widget(self.out_label)
        self.add_widget(scroll)

    def kaydet(self, *_):
        isim = self.isim.text.strip()
        soy = self.soy.text.strip()
        yas = self.yas.text.strip()
        kilo = self.kilo.text.strip()
        il = self.il.text.strip()
        ilce = self.ilce.text.strip()
        hayal = self.hayal.text.strip()

        if not isim or not soy:
            popup_goster("Hata", "Ad ve Soyad boş olamaz.")
            return

        icerik = (
            f"Ad: {isim}\n"
            f"Soyad: {soy}\n"
            f"Yaş: {yas}\n"
            f"Kilo: {kilo}\n"
            f"İl: {il}\n"
            f"İlçe: {ilce}\n"
            f"Hayal: {hayal}\n"
            "-------------------------\n"
        )

        path = kayit_dosyasi_yolu()
        with open(path, "a", encoding="utf-8") as f:
            f.write(icerik)

        self.out_label.text = f"✅ Kaydedildi!\n\nDosya yolu:\n{path}"
        popup_goster("Başarılı", "Kayıt eklendi ✅")

    def kayitlari_goster(self, *_):
        path = kayit_dosyasi_yolu()
        try:
            with open(path, "r", encoding="utf-8") as f:
                icerik = f.read().strip()
            self.out_label.text = "📄 TÜM KAYITLAR:\n\n" + (icerik if icerik else "📭 Dosya var ama boş.")
        except FileNotFoundError:
            self.out_label.text = "📭 Henüz kayıt yok. Önce 'Kaydet' yap."
            popup_goster("Bilgi", "Henüz kayıt yok.")

    def dosyayi_paylas(self, *_):
        path = kayit_dosyasi_yolu()

        if not os.path.exists(path):
            popup_goster("Bilgi", "Paylaşılacak dosya yok.\nÖnce bir kayıt kaydet.")
            return

        # Plyer yoksa: yol göster
        if plyer_share is None:
            popup_goster(
                "Paylaşım Yok",
                "Plyer bulunamadı.\nPip'ten 'plyer' kur.\n\nDosya yolu:\n" + path
            )
            return

        try:
            # Plyer share: Android paylaşım menüsünü açar
            plyer_share.share(
                title="Kayıt Dosyası",
                text="Kayıtlar dosyası ektedir.",
                file_path=path
            )
            self.out_label.text = "📤 Paylaşım menüsü açıldı.\nDosyayı WhatsApp/Telegram ile gönderebilirsin."
        except Exception as e:
            popup_goster("Hata", "Paylaşım sırasında sorun oldu.\n\nDosya yolu:\n" + path)
            self.out_label.text = f"❌ Paylaşım hatası: {e}\n\nDosya yolu:\n{path}"

    def temizle(self, *_):
        self.isim.text = ""
        self.soy.text = ""
        self.yas.text = ""
        self.kilo.text = ""
        self.il.text = ""
        self.ilce.text = ""
        self.hayal.text = ""
        self.out_label.text = "🧹 Temizlendi."


class MiniUygulama(App):
    def build(self):
        self.title = "Mini Kayıt"
        return MainUI()


if __name__ == "__main__":
    MiniUygulama().run()