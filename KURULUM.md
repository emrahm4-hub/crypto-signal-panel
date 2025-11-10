# VPMVT V2 - Kurulum Kılavuzu

Bu kılavuz, VPMVT V2 indikatör sistemini kendi bilgisayarınıza kurmanız için adım adım talimatlar içerir.

## 📋 Gereksinimler

### Yazılım Gereksinimleri
- **Python 3.8** veya üzeri
- **pip** (Python paket yöneticisi)
- **git** (versiyon kontrol sistemi)

### İsteğe Bağlı
- **TradingView hesabı** (Pine Script için)
- **Binance/Bybit hesabı** (canlı veri için)

## 🚀 Hızlı Kurulum (Windows)

### 1. Repository'yi İndirin

Komut satırını (CMD veya PowerShell) açın ve şu komutları çalıştırın:

```bash
# Repository'yi klonlayın
git clone https://github.com/emrahm4-hub/crypto-signal-panel.git

# Klasöre girin
cd crypto-signal-panel

# En son geliştirme branch'ını çekin
git checkout claude/vpmvt-v2-indicators-011CUyuWeKc7PYucHzAjF725
```

### 2. Python Sanal Ortamı Oluşturun (Önerilen)

```bash
# Sanal ortam oluştur
python -m venv venv

# Aktive et
venv\Scripts\activate
```

### 3. Bağımlılıkları Yükleyin

```bash
# Temel bağımlılıklar
pip install pandas numpy

# Canlı veri için (isteğe bağlı)
pip install ccxt

# Grafik çizim için (isteğe bağlı)
pip install plotly matplotlib

# Tüm bağımlılıklar (tam kurulum)
pip install -r requirements.txt
```

### 4. Hızlı Test

```bash
# Örnek veri ile test
python quick_start.py

# Detaylı örnekler
python examples/vpmvt_v2_example.py

# Canlı veri ile test (ccxt gerektirir)
python live_data_example.py
```

## 🚀 Hızlı Kurulum (Linux/Mac)

### 1. Repository'yi İndirin

Terminal açın ve şu komutları çalıştırın:

```bash
# Repository'yi klonlayın
git clone https://github.com/emrahm4-hub/crypto-signal-panel.git

# Klasöre girin
cd crypto-signal-panel

# En son geliştirme branch'ını çekin
git checkout claude/vpmvt-v2-indicators-011CUyuWeKc7PYucHzAjF725
```

### 2. Python Sanal Ortamı Oluşturun (Önerilen)

```bash
# Sanal ortam oluştur
python3 -m venv venv

# Aktive et
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

```bash
# Temel bağımlılıklar
pip install pandas numpy

# Canlı veri için (isteğe bağlı)
pip install ccxt

# Grafik çizim için (isteğe bağlı)
pip install plotly matplotlib

# Tüm bağımlılıklar (tam kurulum)
pip install -r requirements.txt
```

### 4. Hızlı Test

```bash
# Örnek veri ile test
python quick_start.py

# Detaylı örnekler
python examples/vpmvt_v2_example.py

# Canlı veri ile test (ccxt gerektirir)
python live_data_example.py
```

## 📊 TradingView Kurulumu (Pine Script)

### Adım 1: Pine Script Kodunu Açın

```bash
# İndikatör versiyonu
notepad pine_script\vpmvt_v2.pine

# Strateji versiyonu (backtest için)
notepad pine_script\vpmvt_v2_strategy.pine
```

### Adım 2: TradingView'e Yükleyin

1. **TradingView'i açın**: [https://www.tradingview.com/](https://www.tradingview.com/)
2. Bir grafik açın
3. Alt menüden **Pine Editor** sekmesini tıklayın
4. Yeni bir script oluşturun
5. Pine Script kodunu kopyalayıp yapıştırın (Ctrl+A, Ctrl+V)
6. **Save** (Kaydet) tıklayın
7. **Add to Chart** (Grafiğe Ekle) tıklayın

### Adım 3: Ayarları Yapılandırın

- Grafik üzerinde **VPMVT V2** indikatör adına tıklayın
- **Settings** (Ayarlar) → **Inputs** (Girdiler)
- Ağırlıkları ve periyotları özelleştirin
- **OK** tıklayın

## 🧪 Test ve Kullanım

### Temel Python Kullanımı

```python
from backend.indicators.vpmvt_v2 import VPMVT_V2
import pandas as pd

# Verilerinizi yükleyin (örnek)
df = pd.read_csv('your_data.csv')

# VPMVT V2 indikatörü oluştur
vpmvt = VPMVT_V2()

# Hesapla
df['VPMVT_V2'] = vpmvt.calculate(df)

# Sinyal üret
df['signal'] = vpmvt.get_signal(df)

# Sonuçları göster
print(df[['close', 'VPMVT_V2', 'signal']].tail())
```

### Canlı Borsa Verisi ile Kullanım

```bash
# Binance'den BTC/USDT 1 saatlik veri çek ve analiz et
python live_data_example.py
```

Program size sembol ve zaman dilimi soracak:
- **Sembol**: BTC/USDT, ETH/USDT, SOL/USDT vb.
- **Zaman dilimi**: 1m, 5m, 15m, 1h, 4h, 1d

### Hızlı Test Scripti

```bash
# En basit kullanım - hemen sonuç gösterir
python quick_start.py
```

## 📁 Proje Yapısı

```
crypto-signal-panel/
├── backend/indicators/
│   ├── base_indicator.py      # Temel indikatör sınıfı
│   └── vpmvt_v2.py            # VPMVT V2 implementasyonu
│
├── pine_script/
│   ├── vpmvt_v2.pine          # TradingView indikatörü
│   ├── vpmvt_v2_strategy.pine # TradingView stratejisi
│   └── README.md              # Pine Script kullanım kılavuzu
│
├── examples/
│   └── vpmvt_v2_example.py    # Detaylı Python örnekleri
│
├── quick_start.py             # ⭐ Hızlı başlangıç
├── live_data_example.py       # ⭐ Canlı veri örneği
├── requirements.txt           # Python bağımlılıkları
└── README.md                  # Ana dokümantasyon
```

## 🛠️ Sorun Giderme

### "ModuleNotFoundError: No module named 'pandas'"

```bash
# Pandas'ı yükleyin
pip install pandas numpy
```

### "ModuleNotFoundError: No module named 'ccxt'"

```bash
# CCXT'yi yükleyin (canlı veri için gerekli)
pip install ccxt
```

### "SyntaxError" veya Python versiyonu hatası

```bash
# Python versiyonunuzu kontrol edin (3.8+ olmalı)
python --version

# Eğer düşükse Python 3.8+ indirin:
# https://www.python.org/downloads/
```

### Git bulunamadı

```bash
# Git'i indirin ve kurun:
# https://git-scm.com/downloads

# Kurulumu doğrulayın:
git --version
```

### İndirme yavaş veya hata veriyor

```bash
# Alternatif: ZIP olarak indirin
# https://github.com/emrahm4-hub/crypto-signal-panel/archive/refs/heads/claude/vpmvt-v2-indicators-011CUyuWeKc7PYucHzAjF725.zip

# ZIP'i açın ve klasöre girin
cd crypto-signal-panel-main
```

## 📚 Ek Kaynaklar

### Dokümantasyon
- **Ana README**: [README.md](README.md)
- **Pine Script Kılavuzu**: [pine_script/README.md](pine_script/README.md)

### Örnekler
- **Temel Kullanım**: `quick_start.py`
- **Canlı Veri**: `live_data_example.py`
- **Detaylı Örnekler**: `examples/vpmvt_v2_example.py`

### Kodlar
- **Python İndikatör**: `backend/indicators/vpmvt_v2.py`
- **TradingView İndikatör**: `pine_script/vpmvt_v2.pine`
- **TradingView Strateji**: `pine_script/vpmvt_v2_strategy.pine`

## ⚡ Hızlı Komutlar Özeti

```bash
# Kurulum
git clone https://github.com/emrahm4-hub/crypto-signal-panel.git
cd crypto-signal-panel
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
pip install pandas numpy ccxt

# Test
python quick_start.py          # Hızlı test
python live_data_example.py    # Canlı veri
python examples/vpmvt_v2_example.py  # Detaylı örnekler
```

## 🎯 Sonraki Adımlar

1. ✅ Kurulumu tamamlayın
2. ✅ `quick_start.py` ile test edin
3. ✅ `live_data_example.py` ile canlı veri deneyin
4. ✅ TradingView'e Pine Script'i yükleyin
5. ✅ Kendi stratejinizi geliştirin

## 💡 İpuçları

- **Başlangıç için**: `quick_start.py` en kolay yol
- **Gerçek ticaret için**: TradingView Pine Script kullanın
- **Özelleştirme için**: Python kodunu düzenleyin
- **Backtest için**: `vpmvt_v2_strategy.pine` kullanın

## 📞 Destek

- **GitHub Issues**: [Sorun bildirin](https://github.com/emrahm4-hub/crypto-signal-panel/issues)
- **Dokümantasyon**: [README.md](README.md)
- **Pine Script Yardım**: [pine_script/README.md](pine_script/README.md)

## ⚠️ Önemli Uyarılar

1. Bu yazılım **eğitim amaçlıdır**
2. Gerçek para ile işlem yapmadan önce **kağıt üzerinde test edin**
3. **Risk yönetimi** kullanın (stop loss, pozisyon büyüklüğü)
4. Kaybetmeyi göze alamayacağınız para ile işlem **yapmayın**

---

**İyi şanslar! 🚀📊**
