# VPMVT V2 - Pine Script İndikatörleri

TradingView için hazırlanmış VPMVT V2 (Volume-Price-Momentum-Volatility-Time) indikatör ve strateji kodları.

## 📁 Dosyalar

### 1. **vpmvt_v2.pine** - İndikatör Versiyonu
Temel indikatör versiyonu. Grafik üzerinde VPMVT V2 değerlerini gösterir ve sinyal verir.

**Özellikler:**
- 5 bileşenli kompozit indikatör (Volume, Price, Momentum, Volatility, Time)
- Özelleştirilebilir ağırlıklar ve periyotlar
- Alım/Satım sinyalleri
- Gerçek zamanlı değer tablosu
- Bileşenleri ayrı ayrı gösterme seçeneği
- Alert (uyarı) desteği

### 2. **vpmvt_v2_strategy.pine** - Strateji Versiyonu
Backtest yapılabilir strateji versiyonu. Otomatik alım-satım simülasyonu yapar.

**Özellikler:**
- Tüm indikatör özellikleri
- Stop Loss ve Take Profit desteği
- Otomatik ticaret simülasyonu
- Performans metrikleri
- Risk yönetimi ayarları

## 🚀 Kurulum ve Kullanım

### Adım 1: Pine Script Kodunu Kopyalayın

1. İstediğiniz dosyayı açın (`vpmvt_v2.pine` veya `vpmvt_v2_strategy.pine`)
2. Tüm kodu kopyalayın (Ctrl+A, Ctrl+C)

### Adım 2: TradingView'e Ekleyin

1. [TradingView](https://www.tradingview.com/) sitesine gidin
2. Grafiği açın
3. Alt menüden **Pine Editor** seçeneğini tıklayın
4. Yeni bir script oluşturun
5. Kopyaladığınız kodu yapıştırın
6. **"Add to Chart"** veya **"Grafiğe Ekle"** butonuna tıklayın

### Adım 3: Ayarları Yapılandırın

Grafik üzerindeki indikatör adına tıklayarak ayarlar menüsünü açın:

#### **Periyot Ayarları (Periods)**
- **Volume Period**: Volume hesaplamaları için periyot (varsayılan: 20)
- **Price Period**: Fiyat hesaplamaları için periyot (varsayılan: 20)
- **Momentum Period**: Momentum hesaplamaları için periyot (varsayılan: 14)
- **Volatility Period**: Volatilite hesaplamaları için periyot (varsayılan: 14)
- **Time Period**: Zaman ağırlıklı hesaplamalar için periyot (varsayılan: 20)

#### **Ağırlık Ayarları (Weights)**
Her bileşenin önemini 0-100 arası değerle ayarlayın:
- **Volume Weight**: Volume bileşeni ağırlığı (varsayılan: 20)
- **Price Weight**: Fiyat bileşeni ağırlığı (varsayılan: 20)
- **Momentum Weight**: Momentum bileşeni ağırlığı (varsayılan: 20)
- **Volatility Weight**: Volatilite bileşeni ağırlığı (varsayılan: 20)
- **Time Weight**: Zaman bileşeni ağırlığı (varsayılan: 20)

> **Not:** Ağırlıklar otomatik olarak normalize edilir (toplam %100 olur)

#### **Sinyal Ayarları (Signals)**
- **Buy Threshold**: Alım sinyali eşiği (varsayılan: 70)
- **Sell Threshold**: Satım sinyali eşiği (varsayılan: 30)
- **Show Buy/Sell Signals**: Alım/satım okları göster (varsayılan: açık)
- **Show Individual Components**: Bileşenleri ayrı ayrı göster (varsayılan: kapalı)

#### **Risk Yönetimi (Sadece Strategy)**
- **Use Stop Loss**: Stop loss kullan
- **Stop Loss %**: Stop loss yüzdesi (varsayılan: 5%)
- **Use Take Profit**: Take profit kullan
- **Take Profit %**: Take profit yüzdesi (varsayılan: 10%)

## 📊 İndikatörü Okuma

### VPMVT V2 Değerleri (0-100)

| Aralık | Güç | Yorum |
|--------|-----|-------|
| 80-100 | **Çok Güçlü** 🟢 | Güçlü yükseliş trendi |
| 60-79 | **Güçlü** 🟢 | Yükseliş eğilimi |
| 40-59 | **Orta** 🟡 | Nötr/belirsiz |
| 20-39 | **Zayıf** 🔴 | Düşüş eğilimi |
| 0-19 | **Çok Zayıf** 🔴 | Güçlü düşüş trendi |

### Sinyaller

- **🔺 Yeşil Üçgen (Alım Sinyali)**: VPMVT V2, alım eşiğini yukarı kestiğinde
- **🔻 Kırmızı Üçgen (Satım Sinyali)**: VPMVT V2, satım eşiğini aşağı kestiğinde

### Bilgi Tablosu

Sağ üst köşede gerçek zamanlı bilgi tablosu:
- **VPMVT V2**: Mevcut değer
- **Strength**: Güç seviyesi (Very Strong, Strong, Moderate, Weak, Very Weak)
- **Volume**: Volume bileşeni skoru
- **Price**: Fiyat bileşeni skoru
- **Momentum**: Momentum bileşeni skoru
- **Volatility**: Volatilite bileşeni skoru
- **Time**: Zaman bileşeni skoru
- **Signal**: Mevcut sinyal (BUY ▲, SELL ▼, NEUTRAL)

## 🎯 Kullanım Stratejileri

### 1. Trend Takibi
```
VPMVT V2 > 70 → Uzun pozisyon aç
VPMVT V2 < 30 → Pozisyonu kapat
```

### 2. Ortalamaya Dönüş
```
VPMVT V2 < 20 → Aşırı satım, yukarı dönüş bekle
VPMVT V2 > 80 → Aşırı alım, aşağı düzeltme bekle
```

### 3. Çoklu Zaman Dilimi
```
1H grafikte VPMVT V2 > 70 (trend)
15M grafikte VPMVT V2 > 70'i kesti (giriş)
```

### 4. Divergence (Uyumsuzluk)
```
Fiyat yeni zirve yaparken VPMVT V2 düşükse → Zayıflama sinyali
Fiyat yeni dip yaparken VPMVT V2 yükseliyorsa → Güçlenme sinyali
```

## 🔧 Özelleştirme Örnekleri

### Gün İçi Alım-Satım (Day Trading)
Momentum ve volume ağırlıklı:
```
Volume Weight: 30
Price Weight: 15
Momentum Weight: 40
Volatility Weight: 10
Time Weight: 5

Buy Threshold: 65
Sell Threshold: 35
```

### Swing Trading
Dengeli yaklaşım:
```
Volume Weight: 20
Price Weight: 20
Momentum Weight: 20
Volatility Weight: 20
Time Weight: 20

Buy Threshold: 70
Sell Threshold: 30
```

### Risk Odaklı
Volatilite ve güvenlik öncelikli:
```
Volume Weight: 25
Price Weight: 15
Momentum Weight: 15
Volatility Weight: 35
Time Weight: 10

Buy Threshold: 75
Sell Threshold: 25
```

### Scalping (Çok Kısa Vadeli)
Hızlı hareket odaklı:
```
Volume Weight: 35
Price Weight: 10
Momentum Weight: 35
Volatility Weight: 5
Time Weight: 15

Buy Threshold: 60
Sell Threshold: 40

Periyotlar: 10-14 arası
```

## 🔔 Alert (Uyarı) Kurulumu

İndikatör versiyonunda 3 tip alert bulunur:

1. **VPMVT V2 Buy Signal**: Alım sinyali geldiğinde
2. **VPMVT V2 Sell Signal**: Satım sinyali geldiğinde
3. **VPMVT V2 Neutral Cross**: 50 seviyesini kestiğinde

### Alert Kurma:
1. Grafik üzerinde sağ tık → **Add Alert**
2. Condition: **VPMVT V2** seçin
3. İstediğiniz alert tipini seçin
4. Bildirim ayarlarını yapın (App, Email, Webhook)
5. **Create** tıklayın

## 📈 Backtest (Strategy Versiyonu)

Strategy versiyonunda otomatik performans analizi:

### Backtest Metrikleri
- **Net Profit**: Toplam kar/zarar
- **Total Trades**: Toplam işlem sayısı
- **Win Rate**: Kazanan işlem oranı
- **Profit Factor**: Kar faktörü
- **Max Drawdown**: Maksimum düşüş
- **Sharpe Ratio**: Risk-ayarlı getiri

### Backtest İpuçları
1. En az 6-12 aylık veri kullanın
2. Farklı market koşullarını test edin (yükseliş, düşüş, yatay)
3. Komisyon ve slippage ekleyin (Settings → Properties)
4. Farklı zaman dilimlerinde test edin
5. Optimizasyon yaparken overfitting'den kaçının

## ⚠️ Önemli Notlar

1. **Risk Yönetimi**: Her zaman stop loss kullanın
2. **Pozisyon Büyüklüğü**: Sermayenizin %1-2'sinden fazla riske atmayın
3. **Konfirmasyon**: Başka indikatörlerle teyit edin
4. **Piyasa Koşulları**: Trendsiz piyasalarda dikkatli olun
5. **Backtest ≠ Gerçek**: Geçmiş performans gelecek garantisi değildir

## 🎓 Bileşen Detayları

### 1. Volume Bileşeni
- **MFI (Money Flow Index)**: Paranın akış yönü
- **VROC (Volume ROC)**: Volume değişim hızı
- **OBV Momentum**: On-Balance Volume trendi

### 2. Price Bileşeni
- **SMA/EMA Pozisyonu**: Fiyatın hareketli ortalamalara göre konumu
- **ROC (Rate of Change)**: Fiyat değişim hızı
- **Trend Gücü**: ADX benzeri trend gücü ölçümü

### 3. Momentum Bileşeni
- **RSI**: Göreceli güç endeksi (aşırı alım/satım)
- **Stochastic**: Fiyatın trading range içindeki pozisyonu
- **Momentum Oscillator**: Fiyat momentumu

### 4. Volatility Bileşeni
- **ATR**: Ortalama gerçek aralık
- **Standard Deviation**: Standart sapma
- **Bollinger Width**: Bollinger bantları genişliği

### 5. Time Bileşeni
- **VWAP**: Volume ağırlıklı ortalama fiyat
- **Time-Weighted Momentum**: Zaman ağırlıklı momentum
- **EMA Mesafesi**: Kısa ve uzun EMA arası mesafe

## 🤝 Destek

Sorularınız için:
- GitHub Issues: [crypto-signal-panel/issues](https://github.com/emrahm4-hub/crypto-signal-panel/issues)
- TradingView: Yorum bölümü

## 📝 Lisans

MIT License - Eğitim ve araştırma amaçlıdır.

## ⚖️ Sorumluluk Reddi

Bu indikatör sadece eğitim amaçlıdır. Kripto para ticareti yüksek risk içerir. Yatırım kararlarınızı kendi araştırmanıza dayandırın ve kaybetmeyi göze alamayacağınız parayla işlem yapmayın.

---

**İyi Ticaret Dileklerimizle! 🚀📊**
