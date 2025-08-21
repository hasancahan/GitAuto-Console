# 🚀 GitAuto GUI - Windows Uygulaması

GitAuto'nun modern ve kullanıcı dostu Windows GUI versiyonu. Artık terminal komutları yazmadan, görsel arayüz ile projelerinizi GitHub'a kolayca yayınlayabilirsiniz!

## ✨ **Özellikler**

### 🎨 **Modern Arayüz**
- **Tkinter tabanlı** Windows uygulaması
- **Responsive tasarım** - Pencere boyutu değiştirilebilir
- **Emoji destekli** - Görsel olarak çekici
- **Profesyonel görünüm** - Windows 10/11 uyumlu

### 📋 **Kolay Kullanım**
- **Form tabanlı giriş** - Tüm bilgiler tek ekranda
- **Radio button seçenekleri** - README.md yönetimi
- **Dropdown menüler** - Branch seçimi
- **Anlık geri bildirim** - Her adımda bilgilendirme

### 🔧 **Gelişmiş Özellikler**
- **Gerçek zamanlı log** - İşlemleri canlı takip edin
- **Progress bar** - İşlem durumunu görün
- **Thread güvenliği** - UI donmaz
- **Hata yönetimi** - Detaylı hata mesajları
- **Git durum kontrolü** - Otomatik tespit
- **📂 Klasör Seçimi** - Yayınlamak istediğiniz proje klasörünü seçin
- **📋 Otomatik İçerik Listesi** - Seçilen klasördeki dosyaları görün
- **🤖 Akıllı Öneriler** - Proje adı ve README seçenekleri otomatik önerilir

## 🖥️ **Sistem Gereksinimleri**

- **Windows 7/8/10/11** (64-bit önerilen)
- **Python 3.6+** (Tkinter dahil)
- **Git** (https://git-scm.com/downloads)
- **GitHub hesabı**

## 💻 **Kurulum**

### **1. Python Kurulumu**
```bash
# Python'un kurulu olduğundan emin olun
python --version

# Tkinter kontrolü (genellikle dahil gelir)
python -c "import tkinter; print('Tkinter kurulu')"
```

### **2. Git Kurulumu**
- [Git for Windows](https://git-scm.com/download/win) indirin
- Kurulum sırasında "Git from the command line and also from 3rd-party software" seçin
- Kurulum sonrası bilgisayarı yeniden başlatın

### **3. GitAuto GUI Çalıştırma**
```bash
# Uygulamayı çalıştırın
python git_auto_gui.py
```

## 🎯 **Kullanım Kılavuzu**

### **📱 Ana Ekran Bölümleri**

#### **1. 📁 Proje Bilgileri**
- **Proje Klasörü**: Yayınlamak istediğiniz proje klasörünü seçin
- **📂 Klasör Seç**: Klasör seçim dialog'u açar
- **Proje Adı**: GitHub repository adınız (otomatik önerilir)
- **GitHub Kullanıcı**: GitHub hesap adınız
- **Commit Mesajı**: İlk commit için mesaj

#### **2. 📖 README.md Yönetimi**
- **📝 Mevcut README.md'yi koru** (önerilen)
- **🔄 GitAuto ile yeni README.md oluştur**

#### **3. 🌿 Branch Yönetimi**
- **Hedef Branch**: Dropdown'dan seçin (main, master, develop, feature)
- **Yeni Branch**: Özel branch adı girin
- **🌱 Branch Oluştur**: Yeni branch oluşturun
- **📋 Branch'leri Listele**: Mevcut branch'leri görün

#### **4. 🔍 Git Durumu**
- **Git Kurulum**: Git'in kurulu olup olmadığı
- **Repository**: Git repository durumu

#### **5. 📋 İşlem Logları**
- **Gerçek zamanlı log**: Tüm işlemleri takip edin
- **Scroll edilebilir**: Uzun logları kolayca görün

### **🚀 Adım Adım Kullanım**

1. **Uygulamayı açın** → `python git_auto_gui.py`
2. **📂 Proje klasörünü seçin** → "📂 Klasör Seç" butonuna tıklayın
3. **Proje bilgilerini doldurun** (otomatik öneriler)
4. **README.md seçeneğini belirleyin** (otomatik önerilir)
5. **Branch seçin veya oluşturun**
6. **🚀 Repository'yi Yayınla butonuna tıklayın**
7. **Onay verin**
8. **İşlemi takip edin** (log panelinde)
9. **Başarı mesajını görün**

## 🔧 **Teknik Detaylar**

### **Thread Güvenliği**
- **Ana thread**: UI güncellemeleri
- **Worker thread**: Git işlemleri
- **Queue sistemi**: Thread'ler arası iletişim

### **Git Komutları**
```bash
# Otomatik çalıştırılan komutlar
git init                    # Repository başlat
git add .                   # Tüm dosyaları ekle
git commit -m "mesaj"       # Commit yap
git branch -M branch        # Branch ayarla
git remote add origin URL   # Remote ekle
git push -u origin branch   # Yayınla
```

### **Hata Yönetimi**
- **Git kurulum kontrolü**
- **Repository durum kontrolü**
- **Branch adı validasyonu**
- **Network hata yakalama**

## 🎨 **Arayüz Özellikleri**

### **Renkler ve Stiller**
- **Modern tema**: Clam style
- **Accent buton**: Mavi vurgu (#0078d4)
- **Durum renkleri**: Yeşil (✅), Kırmızı (❌), Mavi (ℹ️)

### **Layout Sistemi**
- **Grid layout**: Responsive tasarım
- **Sticky widgets**: Pencere boyutuna uyum
- **Padding ve margin**: Profesyonel görünüm

### **Responsive Tasarım**
- **Pencere boyutu**: 800x700 (varsayılan)
- **Genişletilebilir**: Tüm yönlerde
- **Widget uyumu**: Boyut değişikliklerinde

## 📂 **Klasör Seçimi ve Akıllı Öneriler**

GitAuto GUI artık gelişmiş klasör yönetimi özelliklerine sahip:

### **📂 Klasör Seçimi:**
- **📂 Klasör Seç butonu** - Windows klasör seçim dialog'u açar
- **Otomatik yol güncelleme** - Seçilen klasör yolu otomatik güncellenir
- **Çalışma dizini değişimi** - Tüm Git işlemleri seçilen klasörde yapılır

### **📋 Otomatik İçerik Listesi:**
- **Dosya ve klasör listesi** - Seçilen klasördeki tüm öğeler görüntülenir
- **Akıllı filtreleme** - Git ve sistem dosyaları gizlenir
- **Kategorize edilmiş görünüm** - Klasörler ve dosyalar ayrı ayrı listelenir

### **🤖 Akıllı Öneriler:**
- **Proje adı önerisi** - Klasör adı otomatik proje adı olarak önerilir
- **README.md tespiti** - Mevcut README.md varsa otomatik "koru" seçilir
- **README.md yoksa** - Otomatik "oluştur" seçilir

### **🔄 Dinamik Güncelleme:**
- **Git durum kontrolü** - Klasör değiştiğinde otomatik güncellenir
- **Repository tespiti** - .git klasörü varlığı kontrol edilir
- **Branch durumu** - Mevcut branch'ler kontrol edilir

### **💡 Kullanım Avantajları:**
- ✅ **Kolay erişim** - Herhangi bir proje klasörünü seçebilirsiniz
- ✅ **Otomatik tespit** - README.md ve Git durumu otomatik belirlenir
- ✅ **Görsel geri bildirim** - Klasör içeriği log panelinde görüntülenir
- ✅ **Hata önleme** - Yanlış klasör seçimi önlenir
- ✅ **Zaman tasarrufu** - Manuel giriş gereksinimi azalır

## 🐛 **Hata Çözümleri**

### **"Git kurulu değil" Hatası**
```
❌ Git kurulu değil
```
**Çözüm**: Git'i yükleyin ve bilgisayarı yeniden başlatın

### **"Repository bulunamadı" Hatası**
```
❌ Push hatası: remote: Repository not found
```
**Çözüm**: GitHub'da repository'yi oluşturun

### **"Permission denied" Hatası**
```
❌ Push hatası: Authentication failed
```
**Çözüm**: GitHub hesabınıza giriş yapın

### **"Branch oluşturulamadı" Hatası**
```
❌ Branch oluşturulamadı
```
**Çözüm**: Geçersiz karakterleri kaldırın

## 📱 **Ekran Görüntüleri**

### **Ana Ekran**
```
┌─────────────────────────────────────────────────────────┐
│ 🚀 GitAuto - Otomatik Git Repository Yayınlama        │
├─────────────────────────────────────────────────────────┤
│ 📁 Proje Bilgileri                                    │
│ ├─ Proje Klasörü: [________________] [📂 Klasör Seç] │
│ ├─ Proje Adı: [________________]                       │
│ ├─ GitHub Kullanıcı: [______________]                  │
│ └─ Commit Mesajı: [________________]                   │
├─────────────────────────────────────────────────────────┤
│ 📖 README.md Yönetimi                                 │
│ ├─ ○ 📝 Mevcut README.md'yi koru                      │
│ └─ ○ 🔄 GitAuto ile yeni README.md oluştur            │
├─────────────────────────────────────────────────────────┤
│ 🌿 Branch Yönetimi                                    │
│ ├─ Hedef Branch: [main ▼]                             │
│ ├─ Yeni Branch: [________] [🌱 Branch Oluştur]        │
│ └─ [📋 Branch'leri Listele]                           │
├─────────────────────────────────────────────────────────┤
│ 🔍 Git Durumu                                         │
│ ├─ ✅ Git kurulu ve hazır                             │
│ └─ ℹ️ Git repository henüz başlatılmamış              │
├─────────────────────────────────────────────────────────┤
│                    [🚀 Repository'yi Yayınla]          │
├─────────────────────────────────────────────────────────┤
│ 📋 İşlem Logları                                      │
│ └─ [Scroll edilebilir log alanı]                      │
├─────────────────────────────────────────────────────────┤
│ [████████████████████████████████████████████████████] │
└─────────────────────────────────────────────────────────┘
```

## 🚀 **Geliştirme**

### **Kod Yapısı**
```python
class GitAutoGUI:
    def __init__(self, root):
        # Ana pencere ayarları
        
    def create_widgets(self):
        # UI widget'ları oluştur
        
    def check_git_status(self):
        # Git durumunu kontrol et
        
    def publish_repository(self):
        # Repository yayınla
```

### **Genişletme Özellikleri**
- **Yeni tema desteği**
- **Çoklu dil desteği**
- **Plugin sistemi**
- **Batch işlemler**

## 📞 **Destek**

### **Yaygın Sorunlar**
1. **Git kurulumu**: https://git-scm.com/downloads
2. **Python Tkinter**: `python -m tkinter`
3. **GitHub repository**: GitHub.com'da oluşturun

### **Hata Raporlama**
- Log panelindeki hata mesajlarını kopyalayın
- Python ve Git versiyonlarını belirtin
- Windows sürümünü belirtin

## 📄 **Lisans**

Bu proje açık kaynak kodludur ve özgürce kullanılabilir.

---

**🎉 GitAuto GUI ile projelerinizi kolayca GitHub'a yayınlayın!**
