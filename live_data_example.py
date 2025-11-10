"""
VPMVT V2 - Gerçek Borsa Verisi ile Kullanım
Binance'den canlı veri çekerek VPMVT V2 hesaplar
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
from datetime import datetime
from backend.indicators.vpmvt_v2 import VPMVT_V2

try:
    import ccxt
    CCXT_AVAILABLE = True
except ImportError:
    CCXT_AVAILABLE = False
    print("⚠️  UYARI: ccxt kütüphanesi yüklü değil.")
    print("   Yüklemek için: pip install ccxt")
    print("   Şimdilik örnek veri ile devam ediliyor...\n")


def fetch_binance_data(symbol='BTC/USDT', timeframe='1h', limit=200):
    """
    Binance'den OHLCV verisi çek

    Args:
        symbol: İşlem çifti (örn: 'BTC/USDT', 'ETH/USDT')
        timeframe: Zaman dilimi ('1m', '5m', '15m', '1h', '4h', '1d')
        limit: Kaç adet mum verisi

    Returns:
        pd.DataFrame: OHLCV verisi
    """
    if not CCXT_AVAILABLE:
        return None

    try:
        # Binance bağlantısı
        exchange = ccxt.binance({
            'enableRateLimit': True,
        })

        print(f"📊 {symbol} için {timeframe} verisi çekiliyor...")

        # OHLCV verisi çek
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

        # DataFrame'e dönüştür
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        # Timestamp'i datetime'a çevir
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        print(f"✓ {len(df)} adet veri çekildi")
        print(f"  Başlangıç: {df['timestamp'].iloc[0]}")
        print(f"  Bitiş:     {df['timestamp'].iloc[-1]}")
        print(f"  Son Fiyat: ${df['close'].iloc[-1]:,.2f}\n")

        return df

    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        return None


def analyze_with_vpmvt(df, symbol='BTC/USDT'):
    """
    VPMVT V2 ile analiz yap

    Args:
        df: OHLCV DataFrame
        symbol: İşlem çifti adı
    """
    print("=" * 80)
    print(f"VPMVT V2 ANALİZİ - {symbol}")
    print("=" * 80)

    # VPMVT V2 indikatörü
    vpmvt = VPMVT_V2(
        volume_period=20,
        price_period=20,
        momentum_period=14,
        volatility_period=14,
        time_period=20,
        # Dengeli ağırlıklar
        volume_weight=0.20,
        price_weight=0.20,
        momentum_weight=0.20,
        volatility_weight=0.20,
        time_weight=0.20
    )

    # Hesapla
    df['VPMVT_V2'] = vpmvt.calculate(df)
    df['signal'] = vpmvt.get_signal(df, buy_threshold=70, sell_threshold=30)
    df['strength'] = vpmvt.get_strength(df)

    # Bileşenleri al
    components = vpmvt.calculate_components(df)

    # Mevcut değerler
    current_price = df['close'].iloc[-1]
    current_vpmvt = df['VPMVT_V2'].iloc[-1]
    current_signal = df['signal'].iloc[-1]
    current_strength = df['strength'].iloc[-1]

    # Güç rengi
    if current_vpmvt >= 70:
        strength_emoji = "🟢 GÜÇLÜ ALIM"
    elif current_vpmvt >= 50:
        strength_emoji = "🟡 ORTA"
    elif current_vpmvt >= 30:
        strength_emoji = "🟠 ZAYIF"
    else:
        strength_emoji = "🔴 GÜÇLÜ SATIM"

    # Rapor
    print("\n📊 MEVCUT DURUM:")
    print("-" * 80)
    print(f"Zaman:           {df['timestamp'].iloc[-1]}")
    print(f"Fiyat:           ${current_price:,.2f}")
    print(f"\nVPMVT V2:        {current_vpmvt:.2f}/100  {strength_emoji}")
    print(f"Güç Seviyesi:    {current_strength}")

    if current_signal == 1:
        print(f"Sinyal:          🟢 ALIM SİNYALİ")
    elif current_signal == -1:
        print(f"Sinyal:          🔴 SATIM SİNYALİ")
    else:
        print(f"Sinyal:          ⚪ NÖTR")

    # Bileşen skorları
    print("\n📈 BİLEŞEN SKORLARI:")
    print("-" * 80)
    print(f"📊 Volume:       {components['volume'].iloc[-1]:>6.2f}/100  {'🟢' if components['volume'].iloc[-1] > 60 else '🔴' if components['volume'].iloc[-1] < 40 else '🟡'}")
    print(f"💹 Price:        {components['price'].iloc[-1]:>6.2f}/100  {'🟢' if components['price'].iloc[-1] > 60 else '🔴' if components['price'].iloc[-1] < 40 else '🟡'}")
    print(f"⚡ Momentum:     {components['momentum'].iloc[-1]:>6.2f}/100  {'🟢' if components['momentum'].iloc[-1] > 60 else '🔴' if components['momentum'].iloc[-1] < 40 else '🟡'}")
    print(f"📉 Volatility:   {components['volatility'].iloc[-1]:>6.2f}/100  {'🟢' if components['volatility'].iloc[-1] > 60 else '🔴' if components['volatility'].iloc[-1] < 40 else '🟡'}")
    print(f"⏰ Time:         {components['time'].iloc[-1]:>6.2f}/100  {'🟢' if components['time'].iloc[-1] > 60 else '🔴' if components['time'].iloc[-1] < 40 else '🟡'}")

    # Son sinyaller
    recent_signals = df[df['signal'] != 0].tail(5)

    if len(recent_signals) > 0:
        print("\n🔔 SON SİNYALLER:")
        print("-" * 80)
        for idx, row in recent_signals.iterrows():
            signal_type = "🟢 ALIM" if row['signal'] == 1 else "🔴 SATIM"
            print(f"{row['timestamp']} | {signal_type:12} | ${row['close']:>10,.2f} | VPMVT: {row['VPMVT_V2']:>6.2f}")

    # İstatistikler
    print("\n📊 İSTATİSTİKLER (Son 200 Mum):")
    print("-" * 80)
    buy_count = (df['signal'] == 1).sum()
    sell_count = (df['signal'] == -1).sum()

    print(f"Toplam Alım Sinyali:  {buy_count}")
    print(f"Toplam Satım Sinyali: {sell_count}")
    print(f"Ortalama VPMVT:       {df['VPMVT_V2'].mean():.2f}")
    print(f"Min VPMVT:            {df['VPMVT_V2'].min():.2f}")
    print(f"Max VPMVT:            {df['VPMVT_V2'].max():.2f}")

    # Trend analizi
    vpmvt_trend = "📈 Yükseliş" if df['VPMVT_V2'].iloc[-1] > df['VPMVT_V2'].iloc[-10] else "📉 Düşüş"
    print(f"VPMVT Trend (10 bar): {vpmvt_trend}")

    print("\n" + "=" * 80)

    return df


def main():
    """Ana fonksiyon"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "VPMVT V2 - CANLI VERİ ANALİZİ" + " " * 29 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    # Kullanıcıdan sembol al
    print("📝 Hangi kripto parayı analiz etmek istersiniz?")
    print("   Örnekler: BTC/USDT, ETH/USDT, SOL/USDT, DOGE/USDT")
    print()

    # Varsayılan değerler
    default_symbol = 'BTC/USDT'
    default_timeframe = '1h'

    if CCXT_AVAILABLE:
        symbol = input(f"Sembol [{default_symbol}]: ").strip() or default_symbol
        timeframe = input(f"Zaman dilimi (1m/5m/15m/1h/4h/1d) [{default_timeframe}]: ").strip() or default_timeframe

        # Veri çek
        df = fetch_binance_data(symbol=symbol, timeframe=timeframe, limit=200)
    else:
        # CCXT yoksa örnek veri
        print("⚠️  ccxt yüklü olmadığı için örnek veri kullanılıyor...\n")
        from datetime import timedelta
        import numpy as np

        dates = pd.date_range(end=datetime.now(), periods=200, freq='1H')
        np.random.seed(42)

        base_price = 50000
        returns = np.random.randn(200) * 0.02
        close = base_price * (1 + returns).cumprod()

        df = pd.DataFrame({
            'timestamp': dates,
            'open': close * 0.99,
            'high': close * 1.01,
            'low': close * 0.98,
            'close': close,
            'volume': np.random.uniform(100, 1000, 200)
        })

        symbol = 'BTC/USDT (Örnek Veri)'

    if df is not None:
        # Analiz yap
        df = analyze_with_vpmvt(df, symbol=symbol)

        # Dosyaya kaydet
        output_file = f'vpmvt_analysis_{symbol.replace("/", "_")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(output_file, index=False)
        print(f"\n💾 Analiz sonuçları '{output_file}' dosyasına kaydedildi.")

        print("\n💡 İPUÇLARI:")
        print("   • VPMVT > 70: Güçlü yükseliş, uzun pozisyon")
        print("   • VPMVT < 30: Güçlü düşüş, kısa pozisyon veya çık")
        print("   • Bileşenleri inceleyin: Hangi faktör dominan?")
        print("   • Farklı zaman dilimlerini karşılaştırın (1h vs 4h)")
        print()

        # TradingView önerisi
        print("📊 Bu sonuçları TradingView'de görmek için:")
        print("   1. pine_script/vpmvt_v2.pine dosyasını açın")
        print("   2. TradingView Pine Editor'e yapıştırın")
        print("   3. Add to Chart tıklayın")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ İptal edildi.")
    except Exception as e:
        print(f"\n❌ Hata oluştu: {str(e)}")
        import traceback
        traceback.print_exc()
