import requests

url = 'http://18.212.121.16:5000/tahmin'
veri = {
    "ozellikler": [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
}

cevap = requests.post(url, json=veri)
print(cevap.json())
