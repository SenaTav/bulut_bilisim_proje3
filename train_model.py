import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def ornek_veri_olustur():
    np.random.seed(42)

    veri_sayisi = 600

    metrekare = np.random.randint(50, 250, veri_sayisi)
    oda_sayisi = np.random.randint(1, 7, veri_sayisi)
    banyo_sayisi = np.random.randint(1, 4, veri_sayisi)
    bina_yasi = np.random.randint(0, 40, veri_sayisi)
    kat = np.random.randint(0, 20, veri_sayisi)
    merkeze_uzaklik_km = np.round(np.random.uniform(0.5, 35, veri_sayisi), 1)

    otopark = np.random.randint(0, 2, veri_sayisi)
    asansor = np.random.randint(0, 2, veri_sayisi)
    site_ici = np.random.randint(0, 2, veri_sayisi)
    esyali = np.random.randint(0, 2, veri_sayisi)

    fiyat = (
        metrekare * 28000
        + oda_sayisi * 180000
        + banyo_sayisi * 120000
        - bina_yasi * 35000
        + kat * 15000
        - merkeze_uzaklik_km * 45000
        + otopark * 250000
        + asansor * 180000
        + site_ici * 350000
        + esyali * 150000
        + np.random.normal(0, 250000, veri_sayisi)
    )

    fiyat = np.maximum(fiyat, 500000)

    df = pd.DataFrame({
        "metrekare": metrekare,
        "oda_sayisi": oda_sayisi,
        "banyo_sayisi": banyo_sayisi,
        "bina_yasi": bina_yasi,
        "kat": kat,
        "merkeze_uzaklik_km": merkeze_uzaklik_km,
        "otopark": otopark,
        "asansor": asansor,
        "site_ici": site_ici,
        "esyali": esyali,
        "fiyat": fiyat.astype(int)
    })

    df.to_csv("ev_verileri.csv", index=False)
    return df


def main():
    try:
        df = pd.read_csv("ev_verileri.csv")
        print("ev_verileri.csv dosyası bulundu ve yüklendi.")
    except FileNotFoundError:
        print("ev_verileri.csv bulunamadı. Örnek veri seti oluşturuluyor.")
        df = ornek_veri_olustur()

    ozellikler = [
        "metrekare",
        "oda_sayisi",
        "banyo_sayisi",
        "bina_yasi",
        "kat",
        "merkeze_uzaklik_km",
        "otopark",
        "asansor",
        "site_ici",
        "esyali"
    ]

    hedef = "fiyat"

    X = df[ozellikler]
    y = df[hedef]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=150,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    model_bilgileri = {
        "model": model,
        "model_adi": "Random Forest Regressor",
        "veri_seti": "Ev Fiyat Tahmin Veri Seti",
        "ozellikler": ozellikler,
        "hedef_degisken": hedef,
        "egitim_verisi_orani": "80%",
        "test_verisi_orani": "20%",
        "mae": mae,
        "mse": mse,
        "rmse": rmse,
        "r2_score": r2
    }

    joblib.dump(model_bilgileri, "model.pkl")

    print("Model başarıyla eğitildi ve model.pkl dosyasına kaydedildi.")
    print("MAE:", round(mae, 2))
    print("MSE:", round(mse, 2))
    print("RMSE:", round(rmse, 2))
    print("R2 Score:", round(r2, 4))


if __name__ == "__main__":
    main()