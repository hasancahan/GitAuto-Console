# 📥 GitAuto Kurulum Kılavuzu

Bu kılavuz, GitAuto uygulamasını Windows sisteminize nasıl kuracağınızı adım adım açıklar.

## 🎯 Kurulum Seçenekleri

### **Seçenek 1: Hazır Exe Dosyası (Önerilen) ⭐**
En kolay ve hızlı kurulum yöntemi. Python kurulumu gerektirmez.

### **Seçenek 2: Python ile Çalıştırma**
Geliştiriciler ve Python kullanıcıları için. Kaynak koddan çalıştırma.

## 🚀 Seçenek 1: Hazır Exe Dosyası

### **Adım 1: Dosyayı İndirin**
1. [Releases](https://github.com/yourusername/GitAuto/releases) sayfasına gidin
2. En son sürümü bulun (örn: v1.0.0)
3. `GitAuto.exe` dosyasını indirin

### **Adım 2: Çalıştırın**
1. İndirilen `GitAuto.exe` dosyasını çift tıklayın
2. Windows güvenlik uyarısı çıkarsa "Çalıştır" seçin
3. Uygulama otomatik olarak başlayacaktır

### **Adım 3: İlk Çalıştırma**
- Uygulama ilk açıldığında proje klasörünü seçin
- GitHub kullanıcı adınızı girin
- README seçeneklerini belirleyin

## 🐍 Seçenek 2: Python ile Çalıştırma

### **Gereksinimler**
- **Python 3.8+** kurulu olmalı
- **Git** kurulu olmalı
- **pip** paket yöneticisi

### **Adım 1: Python Kurulumu**
1. [Python.org](https://www.python.org/downloads/) adresine gidin
2. En son Python sürümünü indirin (3.8 veya üzeri)
3. Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin
4. Kurulumu tamamlayın

### **Adım 2: Git Kurulumu**
1. [Git-SCM](https://git-scm.com/downloads) adresine gidin
2. Windows için Git'i indirin
3. Kurulumu tamamlayın (varsayılan ayarlar yeterli)
4. Sistemi yeniden başlatın

### **Adım 3: Proje Dosyalarını İndirin**
```bash
# GitHub'dan projeyi klonlayın
git clone https://github.com/yourusername/GitAuto.git

# Proje klasörüne gidin
cd GitAuto
```

### **Adım 4: Bağımlılıkları Yükleyin**
```bash
# Gereksinimleri yükleyin
pip install -r requirements.txt
```

### **Adım 5: Uygulamayı Çalıştırın**
```bash
# Ana uygulamayı başlatın
python git_auto_gui.py
```

## 🔧 Sistem Gereksinimleri

### **Minimum Gereksinimler**
- **İşletim Sistemi**: Windows 10 (64-bit) veya üzeri
- **RAM**: 4 GB
- **Disk Alanı**: 100 MB boş alan
- **İnternet**: GitHub erişimi için

### **Önerilen Gereksinimler**
- **İşletim Sistemi**: Windows 11 (64-bit)
- **RAM**: 8 GB veya üzeri
- **Disk Alanı**: 500 MB boş alan
- **İnternet**: Hızlı bağlantı (AI README için)

## 📋 Kurulum Sonrası Kontrol

### **Git Kurulum Kontrolü**
```bash
# Git versiyonunu kontrol edin
git --version

# Git konfigürasyonunu kontrol edin
git config --list
```

### **Python Kurulum Kontrolü**
```bash
# Python versiyonunu kontrol edin
python --version

# pip versiyonunu kontrol edin
pip --version
```

### **Uygulama Testi**
1. GitAuto'yu çalıştırın
2. Proje klasörü seçin
3. GitHub kullanıcı adınızı girin
4. README seçeneklerini test edin

## 🚨 Sorun Giderme

### **Exe Dosyası Çalışmıyor**
```
❌ "Windows protected your PC" hatası
```
**Çözüm**:
1. Dosyaya sağ tıklayın
2. "Properties" seçin
3. "Unblock" kutucuğunu işaretleyin
4. "Apply" ve "OK" tıklayın

### **Python Hatası**
```
❌ "python is not recognized" hatası
```
**Çözüm**:
1. Python'u yeniden kurun
2. "Add Python to PATH" seçeneğini işaretleyin
3. Sistemi yeniden başlatın

### **Git Hatası**
```
❌ "git is not recognized" hatası
```
**Çözüm**:
1. Git'i yeniden kurun
2. Sistemi yeniden başlatın
3. PATH değişkenini kontrol edin

### **Bağımlılık Hatası**
```
❌ "ModuleNotFoundError" hatası
```
**Çözüm**:
```bash
# Bağımlılıkları yeniden yükleyin
pip install --upgrade -r requirements.txt

# Virtual environment kullanın
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 🔄 Güncelleme

### **Exe Dosyası Güncelleme**
1. Yeni sürümü [Releases](https://github.com/yourusername/GitAuto/releases) sayfasından indirin
2. Eski dosyayı silin
3. Yeni dosyayı çalıştırın

### **Python Kodu Güncelleme**
```bash
# Proje klasörüne gidin
cd GitAuto

# Değişiklikleri çekin
git pull origin main

# Bağımlılıkları güncelleyin
pip install -r requirements.txt
```

## 📞 Destek

### **Kurulum Sorunları**
- [GitHub Issues](https://github.com/yourusername/GitAuto/issues) sayfasını kullanın
- Hata mesajlarını ve ekran görüntülerini ekleyin
- Sistem bilgilerinizi paylaşın

### **Topluluk Desteği**
- [Discussions](https://github.com/yourusername/GitAuto/discussions) sayfasında sorularınızı sorun
- Diğer kullanıcılarla deneyimlerinizi paylaşın

## ✅ Kurulum Tamamlandı!

Tebrikler! GitAuto başarıyla kuruldu. Şimdi:

1. **İlk projenizi** oluşturun
2. **AI README** özelliğini test edin
3. **Git işlemlerinizi** otomatikleştirin
4. **Deneyimlerinizi** paylaşın

---

**🚀 GitAuto ile Git işlemlerinizi kolaylaştırın!**
