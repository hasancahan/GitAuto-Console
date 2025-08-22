# 🚀 GitAuto - Adım Adım Git Repository Yönetimi

**GitAuto**, Windows için geliştirilmiş, modern ve kullanıcı dostu bir Git repository yönetim uygulamasıdır. Adım adım ilerleyen arayüzü ile Git işlemlerini kolaylaştırır.

## ✨ Özellikler

### 🎯 **Ana Özellikler**
- **Adım Adım İlerleme**: 6 adımlık rehberli süreç
- **Modern Arayüz**: Tkinter tabanlı güzel ve kullanıcı dostu GUI
- **Otomatik Repository Kurulumu**: GitHub repository'leri otomatik oluşturma
- **AI README Oluşturucu**: Gemini AI ile profesyonel README.md oluşturma
- **Akıllı Dosya Filtreleme**: Büyük dosyaları otomatik tespit ve filtreleme

### 🔧 **Teknik Özellikler**
- **Çoklu Branch Desteği**: Branch oluşturma, listeleme ve yönetimi
- **Repository Temizleme**: Gereksiz dosyaları kaldırma ve optimize etme
- **Gerçek Zamanlı Durum Kontrolü**: Git ve repository durumu sürekli izleme
- **Hata Yönetimi**: Kapsamlı hata yakalama ve kullanıcı bilgilendirme
- **Thread Güvenliği**: Arka plan işlemleri için thread desteği

### 📁 **Desteklenen Proje Türleri**
- **Web Uygulamaları**: React, Vue, Angular, Flask, Django
- **Masaüstü Uygulamaları**: Python GUI, Electron, JavaFX
- **API Projeleri**: REST, GraphQL, Microservices
- **Veri Bilimi**: Pandas, NumPy, TensorFlow, PyTorch
- **Oyun Geliştirme**: Pygame, Unity, Unreal Engine
- **CLI Uygulamaları**: Command Line Tools
- **Kütüphaneler**: Python packages, Node.js modules

## 🚀 Hızlı Başlangıç

### 📥 **Kurulum**

#### **Seçenek 1: Hazır Exe Dosyası (Önerilen)**
1. [Releases](https://github.com/yourusername/GitAuto/releases) sayfasından `GitAuto.exe` dosyasını indirin
2. İndirilen dosyayı çift tıklayarak çalıştırın
3. Python kurulumu gerekmez!

#### **Seçenek 2: Python ile Çalıştırma**
```bash
# Gereksinimleri yükleyin
pip install -r requirements.txt

# Uygulamayı çalıştırın
python git_auto_gui.py
```

### 📋 **Gereksinimler**
- **Windows 10/11** (64-bit)
- **Git** ([https://git-scm.com/downloads](https://git-scm.com/downloads))
- **GitHub Hesabı** (repository oluşturmak için)

## 📖 Kullanım Kılavuzu

### **Adım 1: Proje Bilgileri** 📁
- Proje klasörünü seçin
- Proje adını girin
- GitHub kullanıcı adınızı girin
- İlk commit mesajını belirleyin

### **Adım 2: README.md Yönetimi** 📝
- **Mevcut README.md'yi koru**: Var olan README dosyasını korur
- **AI ile yeni README.md oluştur**: Gemini AI ile profesyonel README oluşturur
- **README olmadan devam et**: README dosyasını kaldırır

### **Adım 3: AI README Oluşturucu** 🤖
- Gemini API Key'inizi girin
- AI otomatik olarak proje kodlarını analiz eder
- Profesyonel ve kapsamlı README.md oluşturur

### **Adım 4: Git Durumu** 🔍
- Git kurulum durumunu kontrol eder
- Repository varlığını doğrular
- Sistem durumunu raporlar

### **Adım 5: Branch Yönetimi** 🌿
- Mevcut branch'leri listeler
- Yeni branch oluşturur
- Branch'ler arası geçiş yapar
- Repository temizleme işlemleri

### **Adım 6: Repository Yayınlama** 🚀
- Tüm proje dosyalarını GitHub'a yayınlar
- Büyük dosyaları otomatik filtreler
- Final commit ve push işlemlerini gerçekleştirir

## 🔑 AI README Oluşturucu

### **Gemini API Key Alma**
1. [Google AI Studio](https://aistudio.google.com/) adresine gidin
2. Google hesabınızla giriş yapın
3. "Get API key" butonuna tıklayın
4. API key'inizi kopyalayın

### **AI Analiz Özellikleri**
- **Kod Analizi**: Import'lar, fonksiyonlar, class'lar
- **Teknoloji Tespiti**: Kullanılan framework'ler ve kütüphaneler
- **Proje Amacı**: Otomatik proje kategorilendirme
- **Dosya Yapısı**: Klasör organizasyonu ve dosya hiyerarşisi

## ⚙️ Konfigürasyon

### **Git Ayarları**
```bash
# Kullanıcı adı
git config user.name "Your Name"

# E-posta
git config user.email "your.email@example.com"
```

### **Repository Ayarları**
- **Branch**: main, master, develop
- **Remote**: GitHub origin otomatik bağlama
- **Commit**: Özelleştirilebilir commit mesajları

## 🛠️ Geliştirici Bilgileri

### **Teknoloji Stack**
- **Backend**: Python 3.8+
- **GUI**: Tkinter (Modern CSS-style styling)
- **Git İşlemleri**: subprocess, threading
- **AI Entegrasyonu**: Google Gemini API
- **Dosya İşlemleri**: os, pathlib, shutil

### **Proje Yapısı**
```
GitAuto/
├── git_auto_gui.py      # Ana uygulama
├── requirements.txt      # Python bağımlılıkları
├── GitAuto.exe          # Windows executable
├── build/               # PyInstaller build dosyaları
└── dist/                # Dağıtım dosyaları
```

### **Kod Özellikleri**
- **Modüler Yapı**: Her adım ayrı fonksiyonlarda
- **Hata Yönetimi**: Try-catch blokları ile güvenli işlemler
- **Thread Güvenliği**: UI bloklamayan arka plan işlemleri
- **Log Sistemi**: Detaylı işlem takibi
- **Modern UI**: CSS-style styling ve responsive tasarım

## 🚨 Sorun Giderme

### **Yaygın Sorunlar**

#### **Git Kurulu Değil**
```
❌ Git kurulu değil
```
**Çözüm**: [Git'i indirin](https://git-scm.com/downloads) ve sistemi yeniden başlatın

#### **Repository Bağlanamıyor**
```
❌ Repository bağlama hatası
```
**Çözüm**: 
1. GitHub'da repository'nin var olduğundan emin olun
2. Kullanıcı adı ve proje adını kontrol edin
3. İnternet bağlantınızı kontrol edin

#### **Büyük Dosya Hatası**
```
🚨 Büyük dosya tespit edildi
```
**Çözüm**: 
1. .gitignore dosyası otomatik güncellenir
2. Büyük dosyalar otomatik filtrelenir
3. Repository temizleme işlemi yapın

#### **AI README Hatası**
```
❌ Gemini API hatası
```
**Çözüm**:
1. API key'inizin doğru olduğundan emin olun
2. İnternet bağlantınızı kontrol edin
3. API key'inizin aktif olduğunu doğrulayın

### **Log Mesajları**
- **✅**: Başarılı işlem
- **❌**: Hata
- **⚠️**: Uyarı
- **ℹ️**: Bilgi
- **🔍**: İşlem devam ediyor

## 📝 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📞 Destek

### **Sorun Bildirimi**
- [GitHub Issues](https://github.com/yourusername/GitAuto/issues) sayfasını kullanın
- Hata detaylarını ve ekran görüntülerini ekleyin

### **Özellik İsteği**
- [Feature Request](https://github.com/yourusername/GitAuto/issues/new?template=feature_request.md) template'ini kullanın
- Özelliğin faydalarını açıklayın

### **Topluluk**
- [Discussions](https://github.com/yourusername/GitAuto/discussions) sayfasında sorularınızı sorun
- Diğer kullanıcılarla deneyimlerinizi paylaşın

## 🔄 Güncellemeler

### **v1.0.0** (2024-12-19)
- ✅ İlk sürüm
- ✅ Temel Git işlemleri
- ✅ AI README oluşturucu
- ✅ Modern GUI tasarımı
- ✅ Windows exe desteği

### **Gelecek Özellikler**
- 🔄 Çoklu dil desteği
- 🔄 Dark/Light tema
- 🔄 GitHub Actions entegrasyonu
- 🔄 Proje şablonları
- 🔄 Otomatik güncelleme sistemi

## 🙏 Teşekkürler

- **Google Gemini AI** - README oluşturma için
- **Python Community** - Harika araçlar için
- **GitHub** - Versiyon kontrol sistemi için
- **Tkinter** - GUI framework için

---

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!**

**🚀 GitAuto ile Git işlemlerinizi kolaylaştırın!**
