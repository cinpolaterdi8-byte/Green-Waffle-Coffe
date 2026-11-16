
import os
import hmac
import hashlib
import requests

from flask import Flask, request

app = Flask(__name__)

# Render Environment Variables
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "")
APP_SECRET = os.environ.get("APP_SECRET", "")
API_VERSION = os.environ.get("API_VERSION", "v27.0")

URL = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"


def whatsapp_gonder(payload):
    if not ACCESS_TOKEN or not PHONE_NUMBER_ID:
        print("WhatsApp ayarları eksik.")
        return False

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            URL,
            json=payload,
            headers=headers,
            timeout=20
        )
        print("WhatsApp API:", response.status_code)
        return response.ok

    except requests.RequestException as hata:
        print("Bağlantı hatası:", hata)
        return False


def metin_gonder(to_phone, mesaj):
    return whatsapp_gonder({
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": mesaj}
    })


def susleme_ve_sos_secimi_gonder(to_phone):
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Süsleme ve Sos Seçimi"
            },
            "body": {
                "text": "Waffle'ınız için süsleme ve sos seçin."
            },
            "footer": {"text": "Greenwall Reçetesi"},
            "action": {
                "button": "Süsleme/Sos Seç",
                "sections": [
                    {
                        "title": "Çikolatalar",
                        "rows": [
                            {"id": "sus_bonibon_renkli", "title": "Bonibon"},
                            {"id": "sus_bonibon_minik", "title": "Minik Bonibon"},
                            {"id": "sus_renkli_tas", "title": "Çakıl Taşı Çikolata"},
                            {"id": "sus_pul_pembe", "title": "Pembe Pul Çikolata"},
                            {"id": "sus_damla_cikolata", "title": "Damla Çikolata"}
                        ]
                    },
                    {
                        "title": "Kıtırlar",
                        "rows": [
                            {"id": "sus_biskuvi_oreo", "title": "Oreo Parçaları"},
                            {"id": "sus_krokan_karamel", "title": "Karamel Kıtırı"}
                        ]
                    },
                    {
                        "title": "Özel Soslar",
                        "rows": [
                            {"id": "sos_fistik", "title": "Fıstık Sosu"},
                            {"id": "sos_cilek", "title": "Çilek Sosu"}
                        ]
                    },
                    {
                        "title": "Diğer Seçenekler",
                        "rows": [
                            {"id": "sus_digerleri", "title": "Diğer Süslemeler"}
                        ]
                    }
                ]
            }
        }
    }
    return whatsapp_gonder(payload)


def diger_suslemeleri_gonder(to_phone):
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Diğer Süslemeler"
            },
            "body": {
                "text": "Diğer süsleme seçeneklerini seçin."
            },
            "action": {
                "button": "Diğerlerini Seç",
                "sections": [
                    {
                        "title": "Ekstra Süslemeler",
                        "rows": [
                            {"id": "sus_pasta_susu", "title": "Renkli Pasta Süsü"},
                            {"id": "sus_pirinc_patlagi", "title": "Pirinç Patlağı"},
                            {"id": "sus_hindistan_cevizi", "title": "Hindistan Cevizi"},
                            {"id": "sus_findik_ceviz", "title": "Fındık / Ceviz"},
                            {"id": "back_to_fruit", "title": "Geri Dön"}
                        ]
                    }
                ]
            }
        }
    }
    return whatsapp_gonder(payload)


def gelen_mesaji_isle(message):
    kullanici = message.get("from")
    if not kullanici:
        return

    if message.get("type") == "text":
        susleme_ve_sos_secimi_gonder(kullanici)
        return

    if message.get("type") == "interactive":
        interactive = message.get("interactive", {})

        if interactive.get("type") == "list_reply":
            secim = interactive.get("list_reply", {})
            secim_id = secim.get("id", "")
            secim_adi = secim.get("title", "")

            if secim_id == "sus_digerleri":
                diger_suslemeleri_gonder(kullanici)
            elif secim_id == "back_to_fruit":
                susleme_ve_sos_secimi_gonder(kullanici)
            else:
                metin_gonder(
                    kullanici,
                    f"Seçiminiz alındı: {secim_adi} 🌿"
                )


def imza_gecerli_mi():
    if not APP_SECRET:
        return False

    gelen_imza = request.headers.get(
        "X-Hub-Signature-256", ""
    )

    if not gelen_imza.startswith("sha256="):
        return False

    beklenen = hmac.new(
        APP_SECRET.encode(),
        request.get_data(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        gelen_imza,
        "sha256=" + beklenen
    )


@app.route("/", methods=["GET"])
def ana_sayfa():
    return "Greenwall Coffee WhatsApp Sunucusu Aktif ☕", 200


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200


@app.route("/webhook", methods=["GET"])
def webhook_dogrula():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if (
        mode == "subscribe"
        and VERIFY_TOKEN
        and token == VERIFY_TOKEN
        and challenge
    ):
        return challenge, 200

    return "Webhook doğrulaması başarısız.", 403


@app.route("/webhook", methods=["POST"])
def webhook_mesaj():
    if not imza_gecerli_mi():
        return "Geçersiz imza.", 403

    data = request.get_json(silent=True) or {}

    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})

                for message in value.get("messages", []):
                    gelen_mesaji_isle(message)

    except Exception as hata:
        print("Webhook hatası:", hata)
        return "İşlem hatası.", 500

    return "EVENT_RECEIVED", 200
