"""
VPMVT V2 - Hızlı Başlangıç Kodu
Kendi verilerinizle test edin
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from backend.indicators.vpmvt_v2 import VPMVT_V2


# Örnek veri üretimi (gerçek verilerinizle değiştirin)
def create_sample_data():
    """Örnek OHLCV verisi oluştur"""
    dates = pd.date_range(end=datetime.now(), periods=200, freq='1H')

    np.random.seed(42)
    base_price = 50000

    # Rastgele fiyat hareketi
    returns = np.random.randn(200) * 0.02
    close = base_price * (1 + returns).cumprod()

    # OHLCV verisi
    high = close * (1 + np.random.uniform(0, 0.01, 200))
    low = close * (1 - np.random.uniform(0, 0.01, 200))
    open_price = low + (high - low) * np.random.uniform(0.3, 0.7, 200)
    volume = np.random.uniform(100, 1000, 200)

    df = pd.DataFrame({
        'timestamp': dates,
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })

    return df


def main():
    """Ana fonksiyon"""
    print("=" * 80)
    print("VPMVT V2 İndikatör - Hızlı Başlangıç")
    print("=" * 80)

    # 1. Veri yükle
    print("\n1. Veri yükleniyor...")
    df = create_sample_data()
    print(f"   ✓ {len(df)} adet veri yüklendi")

    # 2. İndikatörü başlat
    print("\n2. VPMVT V2 indikatörü başlatılıyor...")
    vpmvt = VPMVT_V2(
        volume_period=20,
        price_period=20,
        momentum_period=14,
        volatility_period=14,
        time_period=20
    )
    print("   ✓ İndikatör hazır")

    # 3. Hesapla
    print("\n3. VPMVT V2 hesaplanıyor...")
    df['VPMVT_V2'] = vpmvt.calculate(df)
    df['signal'] = vpmvt.get_signal(df, buy_threshold=70, sell_threshold=30)
    df['strength'] = vpmvt.get_strength(df)
    print("   ✓ Hesaplama tamamlandı")

    # 4. Sonuçları göster
    print("\n4. Sonuçlar:")
    print("=" * 80)

    # Son 10 değer
    print("\nSon 10 Değer:")
    print(df[['close', 'VPMVT_V2', 'signal', 'strength']].tail(10).to_string())

    # Mevcut durum
    current_vpmvt = df['VPMVT_V2'].iloc[-1]
    current_signal = df['signal'].iloc[-1]
    current_strength = df['strength'].iloc[-1]

    print("\n" + "=" * 80)
    print("MEVCUT DURUM:")
    print("=" * 80)
    print(f"Fiyat:           ${df['close'].iloc[-1]:,.2f}")
    print(f"VPMVT V2:        {current_vpmvt:.2f}/100")
    print(f"Güç:             {current_strength}")

    signal_text = "ALIM 🟢" if current_signal == 1 else "SATIM 🔴" if current_signal == -1 else "NÖTR ⚪"
    print(f"Sinyal:          {signal_text}")

    # Bileşenler
    print("\n" + "=" * 80)
    print("BİLEŞEN SKORLARI:")
    print("=" * 80)

    components = vpmvt.calculate_components(df)
    print(f"Volume:          {components['volume'].iloc[-1]:.2f}/100")
    print(f"Price:           {components['price'].iloc[-1]:.2f}/100")
    print(f"Momentum:        {components['momentum'].iloc[-1]:.2f}/100")
    print(f"Volatility:      {components['volatility'].iloc[-1]:.2f}/100")
    print(f"Time:            {components['time'].iloc[-1]:.2f}/100")

    # Sinyal sayısı
    buy_signals = (df['signal'] == 1).sum()
    sell_signals = (df['signal'] == -1).sum()

    print("\n" + "=" * 80)
    print("SİNYAL İSTATİSTİKLERİ:")
    print("=" * 80)
    print(f"Toplam Alım Sinyali:  {buy_signals}")
    print(f"Toplam Satım Sinyali: {sell_signals}")
    print(f"Ortalama VPMVT V2:    {df['VPMVT_V2'].mean():.2f}")
    print(f"Min VPMVT V2:         {df['VPMVT_V2'].min():.2f}")
    print(f"Max VPMVT V2:         {df['VPMVT_V2'].max():.2f}")

    print("\n" + "=" * 80)
    print("✓ Tamamlandı!")
    print("=" * 80)

    # CSV'ye kaydet
    output_file = 'vpmvt_v2_results.csv'
    df.to_csv(output_file, index=False)
    print(f"\nSonuçlar '{output_file}' dosyasına kaydedildi.")

    print("\n💡 İpucu: Gerçek verilerinizi kullanmak için bu dosyayı düzenleyin.")
    print("   Binance, Bybit veya diğer borsalardan veri çekebilirsiniz.\n")


if __name__ == "__main__":
    main()
