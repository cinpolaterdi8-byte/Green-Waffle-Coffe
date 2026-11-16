
import requests
import getpass

# =====================================================
# GREENWALL COFFEE - WHATSAPP CLOUD API
# =====================================================

PHONE_NUMBER_ID = "1486486614542741"
MESSAGING_ACCOUNT_ID = "1096987766483543"

ALICI_TELEFON = "905302925075"

API_VERSION = "v27.0"

URL = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"

# Token ekranda görünmeden girilir
ACCESS_TOKEN = getpass.getpass("EAGDTNN5stDkBTFQIIK4UEb9MXJUYmYCq6uxTX8Fjtjjqktyj9lyCTpto4utZAL9VEgPsPCLR2QbZBfFn5joopAZAktbrWPj7RVlyCOs8Ba6h554soZATufpa3kr3TUh35TB5vkmzPaZCeUMPHZCt8xVSdhA4Nn0v0H6dAKZC7XPOKZAmqU7eOAXpOZANiMZCgLcB84VyfLuX7jbuVkZBnOIQrpoZClzBinqzPHGe98HoeZBy0DEGy9pAmtoUq4oJYaoTOBReFRcmZBu6vs5Ht95nQrGNwkJFzw ")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}


# =====================================================
# ORTAK MESAJ GÖNDERME FONKSİYONU
# =====================================================

def whatsapp_gonder(payload):

    try:
        response = requests.post(
            URL,
            json=payload,
            headers=HEADERS,
            timeout=30
        )

        print("\n========== GREENWALL API ==========")
        print("HTTP Durumu:", response.status_code)

        try:
            sonuc = response.json()
        except ValueError:
            sonuc = {"cevap": response.text}

        print("API Cevabı:", sonuc)

        if response.ok:
            print("MESAJ BAŞARIYLA GÖNDERİLDİ")
        else:
            print("MESAJ GÖNDERİLEMEDİ")

        return response

    except requests.exceptions.RequestException as hata:
        print("Bağlantı hatası:", hata)
        return None


# =====================================================
# 3. ADIM - SÜSLEME VE SOS SEÇİMİ
# SAYFA 1
# =====================================================

def susleme_ve_sos_secimi_gonder(to_phone=ALICI_TELEFON):

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_phone,
        "type": "interactive",

        "interactive": {
            "type": "list",

            "header": {
                "type": "text",
                "text": "Süsleme ve Sos Seçimi"
            },

            "body": {
                "text": "Waffle'ınızın üzerini renklendirecek süslemeleri ve sosları seçin."
            },

            "footer": {
                "text": "Greenwall Reçetesi"
            },

            "action": {
                "button": "Süsleme/Sos Seç",

                "sections": [

                    {
                        "title": "Çikolatalar",
                        "rows": [
                            {
                                "id": "sus_bonibon_renkli",
                                "title": "Bonibon",
                                "description": "Renkli drajeler"
                            },
                            {
                                "id": "sus_bonibon_minik",
                                "title": "Minik Bonibon",
                                "description": "Mikro renkli drajeler"
                            },
                            {
                                "id": "sus_renkli_tas",
                                "title": "Çakıl Taşı Çikolata",
                                "description": "Renkli çikolata taşları"
                            },
                            {
                                "id": "sus_pul_pembe",
                                "title": "Pembe Pul Çikolata",
                                "description": "Ruby pembe çikolata"
                            },
                            {
                                "id": "sus_damla_cikolata",
                                "title": "Damla Çikolata",
                                "description": "Bitter damla çikolata"
                            }
                        ]
                    },

                    {
                        "title": "Kıtırlar",
                        "rows": [
                            {
                                "id": "sus_biskuvi_oreo",
                                "title": "Oreo Parçaları",
                                "description": "Koyu bisküvi kıtırı"
                            },
                            {
                                "id": "sus_krokan_karamel",
                                "title": "Karamel Kıtırı",
                                "description": "Altın sarısı çıtırlar"
                            }
                        ]
                    },

                    {
                        "title": "Özel Soslar",
                        "rows": [
                            {
                                "id": "sos_fistik",
                                "title": "Fıstık Sosu",
                                "description": "Yoğun fıstık lezzeti"
                            },
                            {
                                "id": "sos_cilek",
                                "title": "Çilek Sosu",
                                "description": "Mayhoş çilek sosu"
                            }
                        ]
                    },

                    {
                        "title": "Diğer Seçenekler",
                        "rows": [
                            {
                                "id": "sus_digerleri",
                                "title": "Diğer Süslemeler",
                                "description": "Diğer kıtırları görüntüle"
                            }
                        ]
                    }

                ]
            }
        }
    }

    return whatsapp_gonder(payload)


# =====================================================
# EK SÜSLEMELER - SAYFA 2
# =====================================================

def diger_suslemeleri_gonder(to_phone=ALICI_TELEFON):

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_phone,
        "type": "interactive",

        "interactive": {
            "type": "list",

            "header": {
                "type": "text",
                "text": "Diğer Süslemeler"
            },

            "body": {
                "text": "Waffle'ınız için diğer kıtır ve kuruyemiş seçeneklerini seçin."
            },

            "footer": {
                "text": "Greenwall Reçetesi"
            },

            "action": {
                "button": "Diğerlerini Seç",

                "sections": [
                    {
                        "title": "Ekstra Süslemeler",
                        "rows": [
                            {
                                "id": "sus_pasta_susu",
                                "title": "Renkli Pasta Süsü",
                                "description": "Renkli minik şekerlemeler"
                            },
                            {
                                "id": "sus_pirinc_patlagi",
                                "title": "Pirinç Patlağı",
                                "description": "Çıtır pirinçler"
                            },
                            {
                                "id": "sus_hindistan_cevizi",
                                "title": "Hindistan Cevizi",
                                "description": "İnce öğütülmüş"
                            },
                            {
                                "id": "sus_findik_ceviz",
                                "title": "Fındık / Ceviz",
                                "description": "Kırık kuruyemiş parçaları"
                            },
                            {
                                "id": "back_to_fruit",
                                "title": "Geri Dön",
                                "description": "Meyve seçimine geri dön"
                            }
                        ]
                    }
                ]
            }
        }
    }

    return whatsapp_gonder(payload)


# =====================================================
# TEST - İLK SAYFAYI GÖNDER
# =====================================================

susleme_ve_sos_secimi_gonder()
