# ☁️ Python Hava Durumu Uygulaması 🌦️

Bu proje, Python ve Tkinter kullanarak geliştirilmiş basit bir masaüstü hava durumu uygulamasıdır. [Visual Crossing Weather API](https://www.visualcrossing.com/) üzerinden güncel hava durumu verilerini çeker ve performansı artırmak ve API çağrılarını optimize etmek için [Redis](https://redis.io/) kullanarak önbelleğe alır.

## ✨ Özellikler

* **Güncel Hava Durumu:** Belirtilen bir şehir için sıcaklık, hissedilen sıcaklık, nem, rüzgar hızı, koşullar, yağış ve UV indeksi gibi anlık verileri gösterir.
* **Akıllı Önbellekleme:** 🚀 Redis ile API yanıtlarını önbelleğe alarak tekrarlanan isteklerde performansı artırır ve API limitlerini korur.
* **Kullanıcı Dostu Arayüz:** 💻 Tkinter ile oluşturulmuş sezgisel grafik arayüzü sayesinde kolayca şehir arayabilir ve sonuçları görüntüleyebilirsiniz.
* **Sağlam Hata Yönetimi:** API veya ağ sorunları gibi durumlarda kullanıcıya bilgilendirici mesajlar sunar.

## ⚙️ Gereksinimler

* [Python 3.x](https://www.python.org/downloads/)
*!!! HERE!!! ---->>> [Visual Crossing Weather API Key](https://www.visualcrossing.com/weather-api-sign-up) (Ücretsiz hesap oluşturabilirsiniz!)<-------!!! HERE !!!
* [Redis Sunucusu](https://redis.io/docs/getting-started/installation/) çalışır durumda olmalı

## 🚀 Kurulum

Projeyi yerel makinenize kurmak ve çalıştırmak için aşağıdaki adımları izleyin:

### 1. Depoyu Klonlayın

Öncelikle GitHub deposunu yerel makinenize indirin:

```bash
git clone [https://github.com/Phpl3arn/python_Weather_app.git](https://github.com/Phpl3arn/python_Weather_app.git)
cd python_Weather_app

python -m venv venv
# Windows için etkinleştirme:
.\venv\Scripts\activate
# macOS/Linux için etkinleştirme:
source venv/bin/activate

Download: pip install requests redis python-dotenv

take for your api key I'm advice you up url----> : 'VISUAL_CROSSING_API_KEY=SİZİN_API_ANAHTARINIZ'
