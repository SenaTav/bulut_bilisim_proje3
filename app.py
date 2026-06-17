from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os
import joblib

app = Flask(__name__)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = None
collection = None

if MONGO_URI:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=20000)
    db = client["BulutBilisimProje3"]
    collection = db["EvFiyatTahminLoglari"]


try:
    model_bilgileri = joblib.load("model.pkl")
    model = model_bilgileri["model"]
    model_ozellikleri = model_bilgileri["ozellikler"]
except FileNotFoundError:
    raise FileNotFoundError(
        "model.pkl bulunamadı. Önce python train_model.py çalıştırın."
    )


def tahmin_yap(ozellikler):
    tahmin_sonucu = model.predict([ozellikler])[0]
    return float(tahmin_sonucu)


def mongo_kaydet(ozellikler, tahmini_fiyat):
    if collection is None:
        raise Exception("MongoDB bağlantısı bulunamadı.")

    log_kaydi = {
        "girilen_ozellikler": {
            "metrekare": ozellikler[0],
            "oda_sayisi": ozellikler[1],
            "banyo_sayisi": ozellikler[2],
            "bina_yasi": ozellikler[3],
            "kat": ozellikler[4],
            "merkeze_uzaklik_km": ozellikler[5],
            "otopark": ozellikler[6],
            "asansor": ozellikler[7],
            "site_ici": ozellikler[8],
            "esyali": ozellikler[9]
        },
        "tahmini_fiyat_tl": tahmini_fiyat,
        "model": model_bilgileri["model_adi"],
        "veri_seti": model_bilgileri["veri_seti"],
        "tarih": datetime.now()
    }

    collection.insert_one(log_kaydi)


@app.route("/", methods=["GET"])
def home():
    html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Ev Fiyatı Tahmin Sistemi</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                margin: 0;
                padding: 0;
            }

            .container {
                width: 620px;
                margin: 35px auto;
                background-color: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
            }

            h1 {
                text-align: center;
                color: #333;
            }

            p {
                color: #555;
                line-height: 1.5;
            }

            label {
                display: block;
                margin-top: 12px;
                font-weight: bold;
            }

            input, select {
                width: 100%;
                padding: 9px;
                margin-top: 5px;
                border: 1px solid #ccc;
                border-radius: 6px;
                box-sizing: border-box;
            }

            button {
                width: 100%;
                margin-top: 20px;
                padding: 12px;
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                cursor: pointer;
            }

            button:hover {
                background-color: #1d4ed8;
            }

            .info {
                background-color: #eef2ff;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 20px;
            }

            .links {
                margin-top: 25px;
                text-align: center;
            }

            .links a {
                margin: 0 10px;
                color: #2563eb;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>Ev Fiyatı Tahmin Sistemi</h1>

            <div class="info">
                <p>
                    Bu uygulama, evin fiziksel özelliklerini kullanarak tahmini satış fiyatı hesaplar.
                
                </p>
            </div>

            <form action="/arayuz-tahmin" method="POST">
                <label>Metrekare</label>
                <input type="number" step="any" name="metrekare" required>

                <label>Oda Sayısı</label>
                <input type="number" step="1" name="oda_sayisi" required>

                <label>Banyo Sayısı</label>
                <input type="number" step="1" name="banyo_sayisi"  required>

                <label>Bina Yaşı</label>
                <input type="number" step="1" name="bina_yasi"  required>

                <label>Bulunduğu Kat</label>
                <input type="number" step="1" name="kat"  required>

                <label>Şehir Merkezine Uzaklık (km)</label>
                <input type="number" step="any" name="merkeze_uzaklik_km" required>

                <label>Otopark Var mı?</label>
                <select name="otopark">
                    <option value="1">Evet</option>
                    <option value="0">Hayır</option>
                </select>

                <label>Asansör Var mı?</label>
                <select name="asansor">
                    <option value="1">Evet</option>
                    <option value="0">Hayır</option>
                </select>

                <label>Site İçinde mi?</label>
                <select name="site_ici">
                    <option value="1">Evet</option>
                    <option value="0">Hayır</option>
                </select>

                <label>Eşyalı mı?</label>
                <select name="esyali">
                    <option value="0">Hayır</option>
                    <option value="1">Evet</option>
                </select>

                <button type="submit">Tahmin Et</button>
            </form>

            <div class="links">
                <a href="/model-bilgisi" target="_blank">Model Bilgisi</a>
                <a href="/tahmin-loglari" target="_blank">Tahmin Logları</a>
            </div>
        </div>
    </body>
    </html>
    """

    return render_template_string(html)


@app.route("/arayuz-tahmin", methods=["POST"])
def arayuz_tahmin():
    try:
        ozellikler = [
            float(request.form["metrekare"]),
            int(request.form["oda_sayisi"]),
            int(request.form["banyo_sayisi"]),
            int(request.form["bina_yasi"]),
            int(request.form["kat"]),
            float(request.form["merkeze_uzaklik_km"]),
            int(request.form["otopark"]),
            int(request.form["asansor"]),
            int(request.form["site_ici"]),
            int(request.form["esyali"])
        ]

        tahmini_fiyat = tahmin_yap(ozellikler)

        try:
            mongo_kaydet(ozellikler, tahmini_fiyat)
            veritabani_durumu = "Tahmin MongoDB veritabanına kaydedildi."
        except Exception:
            veritabani_durumu = "Tahmin yapıldı fakat MongoDB kaydı yapılamadı."

        html = """
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <title>Tahmin Sonucu</title>

            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f6f8;
                    margin: 0;
                    padding: 0;
                }

                .container {
                    width: 600px;
                    margin: 60px auto;
                    background-color: white;
                    padding: 25px;
                    border-radius: 12px;
                    box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }

                h1 {
                    color: #333;
                }

                .result {
                    margin-top: 20px;
                    padding: 20px;
                    background-color: #e8f5e9;
                    border-left: 5px solid #22c55e;
                    border-radius: 6px;
                    text-align: left;
                }

                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 16px;
                    background-color: #2563eb;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                }

                a:hover {
                    background-color: #1d4ed8;
                }
            </style>
        </head>

        <body>
            <div class="container">
                <h1>Tahmin Sonucu</h1>

                <div class="result">
                    <p><strong>Mesaj:</strong> Tahmin başarıyla yapıldı.</p>
                    <p><strong>Tahmini Ev Fiyatı:</strong> {{ tahmini_fiyat }} TL</p>
                    <p><strong>Kullanılan Model:</strong> {{ model_adi }}</p>
                    <p><strong>Veritabanı Durumu:</strong> {{ veritabani_durumu }}</p>
                </div>

                <a href="/">Yeni Tahmin Yap</a>
            </div>
        </body>
        </html>
        """

        return render_template_string(
            html,
            tahmini_fiyat=f"{round(tahmini_fiyat):,}".replace(",", "."),
            model_adi=model_bilgileri["model_adi"],
            veritabani_durumu=veritabani_durumu
        )

    except Exception as e:
        return jsonify({
            "hata": "Arayüz üzerinden tahmin yapılırken hata oluştu.",
            "detay": str(e)
        }), 500


@app.route("/tahmin", methods=["POST"])
def tahmin():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"hata": "JSON veri gönderilmedi."}), 400

        ozellikler = data.get("ozellikler")

        if ozellikler is None:
            return jsonify({"hata": "'ozellikler' alanı eksik."}), 400

        if not isinstance(ozellikler, list):
            return jsonify({"hata": "'ozellikler' alanı liste formatında olmalıdır."}), 400

        if len(ozellikler) != 10:
            return jsonify({
                "hata": "Ev fiyatı tahmini için 10 adet özellik girilmelidir.",
                "gerekli_ozellik_sayisi": 10,
                "girilen_ozellik_sayisi": len(ozellikler)
            }), 400

        try:
            ozellikler = [float(deger) for deger in ozellikler]
        except ValueError:
            return jsonify({"hata": "Tüm özellik değerleri sayısal olmalıdır."}), 400

        tahmini_fiyat = tahmin_yap(ozellikler)

        try:
            mongo_kaydet(ozellikler, tahmini_fiyat)
            veritabani_durumu = "MongoDB kaydı başarılı."
        except Exception:
            veritabani_durumu = "MongoDB kaydı yapılamadı."

        return jsonify({
            "mesaj": "Tahmin başarıyla yapıldı.",
            "girilen_ozellikler": ozellikler,
            "tahmini_fiyat_tl": round(tahmini_fiyat, 2),
            "veritabani_durumu": veritabani_durumu
        })

    except Exception as e:
        return jsonify({
            "hata": "Tahmin işlemi sırasında bir hata oluştu.",
            "detay": str(e)
        }), 500


@app.route("/model-bilgisi", methods=["GET"])
def model_bilgisi():
    return jsonify({
        "model": model_bilgileri["model_adi"],
        "veri_seti": model_bilgileri["veri_seti"],
        "kullanilan_ozellikler": model_bilgileri["ozellikler"],
        "hedef_degisken": model_bilgileri["hedef_degisken"],
        "egitim_verisi_orani": model_bilgileri["egitim_verisi_orani"],
        "test_verisi_orani": model_bilgileri["test_verisi_orani"],
        "mae": round(model_bilgileri["mae"], 2),
        "mse": round(model_bilgileri["mse"], 2),
        "rmse": round(model_bilgileri["rmse"], 2),
        "r2_score": round(model_bilgileri["r2_score"], 4),
        "aciklama": "Model, evin fiziksel özellikleri kullanılarak tahmini fiyat hesaplamak için eğitilmiştir."
    })


@app.route("/tahmin-loglari", methods=["GET"])
def tahmin_loglari():
    try:
        if collection is None:
            return jsonify({
                "hata": "MongoDB bağlantısı bulunamadı."
            }), 500

        loglar = []

        for log in collection.find().sort("tarih", -1).limit(10):
            log["_id"] = str(log["_id"])

            if "tarih" in log:
                log["tarih"] = log["tarih"].strftime("%Y-%m-%d %H:%M:%S")

            loglar.append(log)

        return jsonify({
            "toplam_gosterilen_log": len(loglar),
            "loglar": loglar
        })

    except Exception as e:
        return jsonify({
            "hata": "Loglar alınırken bir hata oluştu.",
            "detay": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
