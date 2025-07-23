import requests
import redis
import json
import os
from datetime import datetime, timedelta

# --- Yapılandırma ---
# Sağladığınız API URL'si
# Not: API anahtarınızı (key=8KCGAB2XWHNKCXG4KD2VYABKU) doğrudan URL'ye eklediniz.
# Genellikle API anahtarlarını daha güvenli bir şekilde (örneğin ortam değişkeniyle) yönetmek daha iyidir.
# Bu örnekte, sizin verdiğiniz URL'yi olduğu gibi kullanıyoruz.
TARGET_API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/america?unitGroup=us&key=8KCGAB2XWHNKCXG4KD2VYABKU&contentType=json"
LOCATION_NAME = "America" # Bu URL'nin temsil ettiği konum için açıklayıcı bir isim

# Redis bağlantı bilgileri
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Önbellek ömrü (saniye cinsinden). Örneğin, 15 dakika = 900 saniye
CACHE_EXPIRATION_SECONDS = 900 

# Redis bağlantısını başlat
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    r.ping() # Bağlantıyı test et
    print("Redis'e başarıyla bağlanıldı!")
except redis.exceptions.ConnectionError as e:
    print(f"Redis'e bağlanılamadı: {e}")
    r = None # Bağlantı kurulamadıysa Redis'i None olarak ayarla

def get_weather_data_from_url():
    """
    Belirtilen TARGET_API_URL'den hava durumu verilerini alır.
    Önce Redis önbelleğini kontrol eder, yoksa API'den alır ve önbelleğe kaydeder.
    """
    cache_key = f"weather_data_for_{LOCATION_NAME.lower().replace(' ', '_')}"

    # 1. Redis önbelleğini kontrol et
    if r:
        cached_data = r.get(cache_key)
        if cached_data:
            print(f"Hava durumu verileri Redis önbelleğinden alındı: {LOCATION_NAME}")
            return json.loads(cached_data)

    print(f"Hava durumu verileri API'den alınıyor: {LOCATION_NAME} (URL: {TARGET_API_URL})")

    # 2. Redis'te yoksa API'den al
    try:
        response = requests.get(TARGET_API_URL)
        response.raise_for_status()  # HTTP hataları için istisna fırlat
        weather_data = response.json()

        # 3. Verileri Redis'e kaydet (eğer Redis bağlıysa)
        if r:
            r.setex(cache_key, CACHE_EXPIRATION_SECONDS, json.dumps(weather_data))
            print(f"Hava durumu verileri Redis'e kaydedildi: {LOCATION_NAME}")

        return weather_data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP hatası oluştu: {http_err} - Yanıt: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Bağlantı hatası oluştu: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Zaman aşımı hatası oluştu: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Bir hata oluştu: {req_err}")
    except json.JSONDecodeError:
        print(f"API yanıtı geçerli bir JSON değil: {response.text}")
    return None

def display_weather_info(data, location_name: str):
    """
    Alınan hava durumu verilerini düzgün bir şekilde görüntüler.
    Bu kısım, API'den dönen JSON yapısına göre ayarlanmalıdır.
    'america' için genel bir yapı bekliyoruz.
    """
    if not data or 'currentConditions' not in data:
        print(f"{location_name} için hava durumu bilgisi bulunamadı veya eksik.")
        return

    current = data['currentConditions']
    
    print(f"\n--- {location_name} Hava Durumu ---")
    print(f"Sıcaklık: {current.get('temp')}°F (unitGroup=us olduğu için Fahrenheit)")
    print(f"Hissedilen: {current.get('feelslike')}°F")
    print(f"Koşullar: {current.get('conditions')}")
    print(f"Nem: %{current.get('humidity')}")
    print(f"Rüzgar Hızı: {current.get('windspeed')} mph")
    print(f"Yağış: {current.get('precip')} inç")
    print(f"UV İndeksi: {current.get('uvindex')}")
    print("--------------------------")

# --- Uygulama Örneği ---
if __name__ == "__main__":
    print(f"'{LOCATION_NAME}' konumu için hava durumu verileri alınıyor...")
    weather_data = get_weather_data_from_url()
    
    if weather_data:
        display_weather_info(weather_data, LOCATION_NAME)
    else:
        print(f"'{LOCATION_NAME}' için hava durumu alınamadı.")

    # Redis önbelleğinin çalıştığını görmek için aynı URL'yi tekrar sorgula
    print(f"\n--- '{LOCATION_NAME}' için tekrar sorgulama (önbellek testi) ---")
    weather_data_cached = get_weather_data_from_url()
    
    if weather_data_cached:
        display_weather_info(weather_data_cached, LOCATION_NAME)
    else:
        print(f"'{LOCATION_NAME}' için hava durumu alınamadı (ikinci deneme).")
