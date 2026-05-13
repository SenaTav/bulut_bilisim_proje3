from flask import Flask, request, jsonify
from pymongo import MongoClient
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

MONGO_URI = "mongodb+srv://senatavv:sena6432@cluster0.5urrqbx.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["BulutBilisimProje3"]
collection = db["TahminLoglari"]

data = fetch_california_housing()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

@app.route('/', methods=['GET'])
def ana_sayfa():
    return "Ev Fiyat Tahmin API'si Basariyla Calisiyor! Tahmin almak icin /tahmin adresine POST istegi gonderin."

@app.route('/tahmin', methods=['POST'])
def tahmin_yap():
    try:
        istek_verisi = request.json
        evin_ozellikleri = istek_verisi['ozellikler']
        
        tahmin_edilen_fiyat = model.predict([evin_ozellikleri])[0]
        
        log_kaydi = {
            "girilen_ozellikler": evin_ozellikleri,
            "tahmin_edilen_fiyat": tahmin_edilen_fiyat
        }
        collection.insert_one(log_kaydi)
        
        return jsonify({
            "mesaj": "Tahmin basarili",
            "tahmin_fiyati": tahmin_edilen_fiyat
        })

    except Exception as e:
        return jsonify({"hata": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)