# Ev Fiyati Tahmin Sistemi

Bu proje, Bulut Bilisim dersi icin gelistirilmis makine ogrenmesi tabanli bir ev fiyati tahmin uygulamasidir. Kullanici tarafindan girilen ev ozellikleri Random Forest Regressor modeliyle degerlendirilir ve tahmini satis fiyati hesaplanir. Tahmin bilgileri MongoDB Atlas veritabanina kaydedilir.

---

## Sistem Mimarisi

```text
Kullanici
↓
Web Arayuzu / HTTP Istegi
↓
AWS Lambda
↓
Egitilmis Random Forest Modeli
↓
MongoDB Atlas
```

Model yerel ortamda `train_model.py` ile egitilir ve `model.pkl` dosyasina kaydedilir. AWS Lambda, gelen ev ozelliklerini bu modele gondererek tahmin yapar. Tahmin sonucu kullaniciya dondurulur ve MongoDB Atlas'a kaydedilir.

---

## Kullanilan Teknolojiler

* **Programlama Dili:** Python
* **Makine Ogrenmesi:** Scikit-learn, Random Forest Regressor
* **Veri Isleme:** Pandas, NumPy
* **Model Kaydetme:** Joblib
* **Yerel Web Uygulamasi:** Flask
* **Serverless Bulut Servisi:** AWS Lambda
* **Veritabani:** MongoDB Atlas
* **Kod Deposu:** GitHub

---

## Kullanilan Ev Ozellikleri

Model tahmin yaparken su bilgileri kullanir:

* Metrekare
* Oda sayisi
* Banyo sayisi
* Bina yasi
* Bulundugu kat
* Sehir merkezine uzaklik
* Otopark bilgisi
* Asansor bilgisi
* Site icinde olma bilgisi
* Esyali olma bilgisi

---

## Model Egitimi

Proje icin ev ozellikleri ve fiyat bilgisinden olusan ornek bir veri seti olusturulmustur. Veri setinin yuzde 80'i egitim, yuzde 20'si test verisi olarak kullanilir.

Modeli egitmek icin:

```powershell
python train_model.py
```

Bu islem sonunda `model.pkl` dosyasi olusur. Model basarisi MAE, MSE, RMSE ve R2 Score degerleriyle degerlendirilir.

---

## Yerel Kurulum ve Calistirma

Proje baska bir bilgisayara aktarildiginda eski `.venv` klasoru kullanilmamalidir. Her bilgisayarda yeni bir sanal ortam olusturulmalidir.

Windows PowerShell uzerinde proje klasorunde su komutlari sirayla calistirin:

```powershell
py -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python train_model.py
python app.py
```

Uygulama su adresten acilir:

```text
http://127.0.0.1:5000/
```

`model.pkl` dosyasi zaten varsa `python train_model.py` komutunun tekrar calistirilmasi zorunlu degildir.

MongoDB baglantisi icin proje klasorunde `.env` dosyasi bulunmalidir:

```env
MONGO_URI=MongoDB_Atlas_baglanti_adresi
```

---

## AWS Lambda

Final bulut dagitimi AWS Lambda ile serverless olarak yapilandirilir. Lambda fonksiyonu `lambda_function.py` dosyasindaki `lambda_handler` fonksiyonunu calistirir.

Lambda'nin temel gorevleri sunlardir:

* Kullanici tarafindan gonderilen ev ozelliklerini almak
* `model.pkl` dosyasindaki egitilmis modeli yuklemek
* Tahmini ev fiyatini hesaplamak
* Tahmin kaydini MongoDB Atlas'a eklemek
* Sonucu HTTP cevabi olarak dondurmek

MongoDB baglanti adresi Lambda icinde kodun icine yazilmaz. AWS Lambda ayarlarinda `MONGO_URI` adli Environment Variable olarak tanimlanir.

Lambda Function URL veya API Gateway kullanilarak fonksiyona internet uzerinden HTTPS istegi gonderilebilir.

---

## Proje Dosyalari

```text
app.py                 Yerel Flask uygulamasi
lambda_function.py     AWS Lambda tahmin fonksiyonu
train_model.py         Model egitim islemleri
model.pkl              Egitilmis makine ogrenmesi modeli
ev_verileri.csv        Ev fiyati veri seti
requirements.txt       Gerekli Python kutuphaneleri
.env                   MongoDB baglanti bilgisi
```

---

## Guvenlik

Asagidaki dosya ve klasorler GitHub'a yuklenmemelidir:

```text
.env
.venv/
__pycache__/
*.pyc
```

MongoDB kullanici adi, sifresi ve baglanti adresi kaynak kodun icinde acik olarak tutulmamalidir.

---

## Sonuc

Bu proje ile ev ozelliklerinden fiyat tahmini yapan bir Random Forest modeli gelistirilmis, model Flask ile yerel ortamda test edilmis, tahmin kayitlari MongoDB Atlas'ta saklanmis ve uygulama AWS Lambda serverless mimarisine uygun hale getirilmistir.
