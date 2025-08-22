#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitAuto GUI - Windows Uygulaması
Modern ve kullanıcı dostu arayüz ile Git repository yönetimi
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import os
import subprocess
import sys
from pathlib import Path
import threading
import queue

class GitAutoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 GitAuto - Otomatik Git Repository Yayınlama")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        # Modern stil tanımlamaları
        self.setup_styles()
        
        # Ana değişkenler
        self.project_name = tk.StringVar()
        self.github_username = tk.StringVar()
        self.commit_message = tk.StringVar(value="first commit")
        self.selected_branch = tk.StringVar(value="main")
        self.current_directory = os.getcwd()
        
        # Git durumu
        self.git_installed = False
        self.git_repo_exists = False
        
        # Log mesajları için queue
        self.log_queue = queue.Queue()
        
        # Arayüz oluştur
        self.create_widgets()
        
        # Git durumunu kontrol et
        self.check_git_status()
        
        # Log güncellemelerini başlat
        self.update_log()
        
        # Mevcut klasörün içeriğini göster
        self.list_folder_contents()
        
        # Branch listesini güncelle
        self.refresh_branches()

    def setup_styles(self):
        """Modern CSS-style buton ve widget stilleri tanımla"""
        style = ttk.Style()
        
        # Primary buton stili (mavi)
        style.configure("Primary.TButton",
                       background="#2563eb",
                       foreground="white",
                       borderwidth=0,
                       focuscolor="none",
                       font=("Segoe UI", 10, "bold"))
        
        style.map("Primary.TButton",
                 background=[("active", "#1d4ed8"), ("pressed", "#1e40af")],
                 foreground=[("active", "white"), ("pressed", "white")])
        
        # Accent buton stili (yeşil)
        style.configure("Accent.TButton",
                       background="#059669",
                       foreground="white",
                       borderwidth=0,
                       focuscolor="none",
                       font=("Segoe UI", 10, "bold"))
        
        style.map("Accent.TButton",
                 background=[("active", "#047857"), ("pressed", "#065f46")],
                 foreground=[("active", "white"), ("pressed", "white")])
        
        # Secondary buton stili (gri)
        style.configure("Secondary.TButton",
                       background="#64748b",
                       foreground="white",
                       borderwidth=0,
                       focuscolor="none",
                       font=("Segoe UI", 10))
        
        style.map("Secondary.TButton",
                 background=[("active", "#475569"), ("pressed", "#334155")],
                 foreground=[("active", "white"), ("pressed", "white")])
        
        # Progress bar stili
        style.configure("Accent.Horizontal.TProgressbar",
                       background="#2563eb",
                       troughcolor="#e2e8f0",
                       borderwidth=0,
                       lightcolor="#3b82f6",
                       darkcolor="#1d4ed8")
        
        # LabelFrame stili
        style.configure("TLabelframe",
                       background="#ffffff",
                       borderwidth=1,
                       relief="solid")
        
        style.configure("TLabelframe.Label",
                       font=("Segoe UI", 11, "bold"),
                       foreground="#1e293b",
                       background="#ffffff")
        
        # Entry stili
        style.configure("TEntry",
                       fieldbackground="#f8fafc",
                       borderwidth=1,
                       relief="solid",
                       focuscolor="#2563eb")
        
        # Combobox stili
        style.configure("TCombobox",
                       fieldbackground="#f8fafc",
                       borderwidth=1,
                       relief="solid",
                       focuscolor="#2563eb")
        
        # Frame stili
        style.configure("TFrame",
                       background="#ffffff")
        
        # Radiobutton stili
        style.configure("TRadiobutton",
                       background="#ffffff",
                       font=("Segoe UI", 10),
                       foreground="#1e293b")
        
        style.map("TRadiobutton",
                 background=[("active", "#f1f5f9"), ("selected", "#dbeafe")],
                 foreground=[("active", "#1e293b"), ("selected", "#1e40af")])
        
        # Scrollbar stili
        style.configure("Vertical.TScrollbar",
                       background="#e2e8f0",
                       troughcolor="#f1f5f9",
                       borderwidth=0,
                       arrowcolor="#64748b",
                       width=12)
        
        style.map("Vertical.TScrollbar",
                 background=[("active", "#cbd5e1"), ("pressed", "#94a3b8")],
                 arrowcolor=[("active", "#475569"), ("pressed", "#334155")])

    def create_widgets(self):
        """Modern ve derli toplu widget'ları oluştur"""
        # Ana scrollable canvas oluştur
        canvas = tk.Canvas(self.root, bg="#ffffff", highlightthickness=0, width=860, height=760)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
        
        # Scrollable frame
        main_frame = ttk.Frame(canvas, padding="20", width=860)
        
        # Canvas scroll konfigürasyonu
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Grid ağırlıkları
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Canvas ve scrollbar yerleştir
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Canvas içinde frame'i yerleştir
        canvas.create_window((0, 0), window=main_frame, anchor="nw", width=860)
        
        # Scroll fonksiyonu
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def on_mousewheel(event):
            try:
                # Windows için delta değeri
                if hasattr(event, 'delta'):
                    delta = int(-1 * (event.delta / 120))
                    canvas.yview_scroll(delta, "units")
                # Linux/Mac için delta değeri
                elif hasattr(event, 'num'):
                    if event.num == 4:
                        canvas.yview_scroll(-1, "units")
                    elif event.num == 5:
                        canvas.yview_scroll(1, "units")
                # Touchpad için
                elif hasattr(event, 'delta'):
                    canvas.yview_scroll(int(-1 * event.delta), "units")
            except Exception as e:
                # Hata durumunda varsayılan scroll
                try:
                    canvas.yview_scroll(-1, "units")
                except:
                    pass
        
        # Windows için mouse wheel binding
        canvas.bind("<Configure>", configure_scroll)
        canvas.bind("<MouseWheel>", on_mousewheel)
        
        # Linux/Mac için mouse wheel binding
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        # Touchpad için binding
        canvas.bind("<B1-Motion>", lambda e: canvas.yview_scroll(int(e.delta), "units"))
        
        # Alternatif mouse wheel binding'ler
        canvas.bind("<MouseWheel>", on_mousewheel, add="+")
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"), add="+")
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"), add="+")
        
        # Scrollbar'a da mouse wheel binding ekle
        scrollbar.bind("<MouseWheel>", on_mousewheel)
        scrollbar.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        scrollbar.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        # Scrollbar'a alternatif binding'ler
        scrollbar.bind("<MouseWheel>", on_mousewheel, add="+")
        scrollbar.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"), add="+")
        scrollbar.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"), add="+")
        
        # Keyboard scroll desteği
        canvas.bind("<Up>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Down>", lambda e: canvas.yview_scroll(1, "units"))
        canvas.bind("<Page_Up>", lambda e: canvas.yview_scroll(-10, "units"))
        canvas.bind("<Page_Down>", lambda e: canvas.yview_scroll(10, "units"))
        canvas.bind("<Home>", lambda e: canvas.yview_moveto(0))
        canvas.bind("<End>", lambda e: canvas.yview_moveto(1))
        
        # Frame genişliğini canvas'a göre ayarla
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Canvas boyutunu frame'e göre ayarla
        def on_canvas_configure(event):
            try:
                # Canvas içindeki tüm item'ları bul
                items = canvas.find_all()
                if items:
                    # İlk item'ı (main_frame) bul ve genişliğini ayarla
                    canvas.itemconfig(items[0], width=event.width)
            except:
                pass
        
        main_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Main frame'e de mouse wheel binding ekle
        main_frame.bind("<MouseWheel>", on_mousewheel)
        main_frame.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        main_frame.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        # Modern başlık - gradient efekti için frame
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 30), sticky=(tk.W, tk.E))
        title_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(title_frame, 
                               text="🚀 GitAuto", 
                               font=("Segoe UI", 24, "bold"),
                               foreground="#2563eb")
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="Otomatik Git Repository Yayınlama", 
                                  font=("Segoe UI", 12),
                                  foreground="#64748b")
        subtitle_label.grid(row=1, column=0)
        
        # Proje bilgileri frame - modern card tasarımı
        project_frame = ttk.LabelFrame(main_frame, text="📁 Proje Bilgileri", padding="20")
        project_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        project_frame.columnconfigure(1, weight=1)
        
        # Proje klasörü seçimi - modern input tasarımı
        folder_label = ttk.Label(project_frame, text="Proje Klasörü:", font=("Segoe UI", 10, "bold"))
        folder_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        
        self.project_path_var = tk.StringVar(value=self.current_directory)
        project_path_entry = ttk.Entry(project_frame, textvariable=self.project_path_var, 
                                     font=("Segoe UI", 10), width=45)
        project_path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 15), pady=(0, 8))
        
        browse_btn = ttk.Button(project_frame, text="📂 Klasör Seç", 
                               command=self.browse_folder, style="Accent.TButton")
        browse_btn.grid(row=0, column=2, padx=(15, 0), pady=(0, 8))
        
        # Proje adı
        name_label = ttk.Label(project_frame, text="Proje Adı:", font=("Segoe UI", 10, "bold"))
        name_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        project_entry = ttk.Entry(project_frame, textvariable=self.project_name, 
                                font=("Segoe UI", 10), width=45)
        project_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 15), pady=(0, 8))
        
        # GitHub kullanıcı adı
        user_label = ttk.Label(project_frame, text="GitHub Kullanıcı:", font=("Segoe UI", 10, "bold"))
        user_label.grid(row=2, column=0, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        username_entry = ttk.Entry(project_frame, textvariable=self.github_username, 
                                 font=("Segoe UI", 10), width=45)
        username_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 15), pady=(0, 8))
        
        # Commit mesajı
        commit_label = ttk.Label(project_frame, text="Commit Mesajı:", font=("Segoe UI", 10, "bold"))
        commit_label.grid(row=3, column=0, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        commit_entry = ttk.Entry(project_frame, textvariable=self.commit_message, 
                               font=("Segoe UI", 10), width=45)
        commit_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(0, 15), pady=(0, 8))
        
        # README.md yönetimi frame - modern card tasarımı
        readme_frame = ttk.LabelFrame(main_frame, text="📖 README.md Yönetimi", padding="20")
        readme_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        readme_frame.columnconfigure(1, weight=1)
        
        # README seçenekleri - modern radio button tasarımı
        self.readme_var = tk.StringVar(value="keep")
        readme_keep = ttk.Radiobutton(readme_frame, text="📝 Mevcut README.md'yi koru (önerilen)", 
                                     variable=self.readme_var, value="keep")
        readme_keep.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 8))
        
        readme_create = ttk.Radiobutton(readme_frame, text="🔄 GitAuto ile yeni README.md oluştur", 
                                       variable=self.readme_var, value="create")
        readme_create.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 8))
        
        # Branch yönetimi frame - modern card tasarımı
        branch_frame = ttk.LabelFrame(main_frame, text="🌿 Branch Yönetimi", padding="20")
        branch_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        branch_frame.columnconfigure(1, weight=1)
        
        # Branch seçimi - modern input tasarımı
        branch_label = ttk.Label(branch_frame, text="Hedef Branch:", font=("Segoe UI", 10, "bold"))
        branch_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        
        self.branch_combo = ttk.Combobox(branch_frame, textvariable=self.selected_branch, 
                                        values=["main", "master", "develop"], width=25, 
                                        state="readonly", font=("Segoe UI", 10))
        self.branch_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        
        # Branch yenile butonu - modern icon buton
        refresh_btn = ttk.Button(branch_frame, text="🔄", command=self.refresh_branches, 
                                width=4, style="Accent.TButton")
        refresh_btn.grid(row=0, column=2, padx=(15, 0), pady=(0, 8))
        
        # Yeni branch oluştur - modern input tasarımı
        new_branch_label = ttk.Label(branch_frame, text="Yeni Branch:", font=("Segoe UI", 10, "bold"))
        new_branch_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        
        self.new_branch_var = tk.StringVar()
        new_branch_entry = ttk.Entry(branch_frame, textvariable=self.new_branch_var, 
                                   width=25, font=("Segoe UI", 10))
        new_branch_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        
        create_branch_btn = ttk.Button(branch_frame, text="🌱 Branch Oluştur", 
                                     command=self.create_new_branch, style="Accent.TButton")
        create_branch_btn.grid(row=1, column=2, padx=(15, 0), pady=(0, 8))
        
        # Buton satırı - modern buton tasarımı
        button_frame = ttk.Frame(branch_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(15, 0))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        list_branches_btn = ttk.Button(button_frame, text="📋 Branch'leri Listele", 
                                     command=self.list_branches, style="Secondary.TButton")
        list_branches_btn.grid(row=0, column=0, padx=(0, 10))
        
        clean_btn = ttk.Button(button_frame, text="🧹 Repository Temizle", 
                             command=self.clean_repository, style="Secondary.TButton")
        clean_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Git durumu frame - modern card tasarımı
        status_frame = ttk.LabelFrame(main_frame, text="🔍 Git Durumu", padding="20")
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        status_frame.columnconfigure(1, weight=1)
        
        # Git durum etiketleri - modern status tasarımı
        self.git_status_label = ttk.Label(status_frame, text="Git durumu kontrol ediliyor...", 
                                        font=("Segoe UI", 10))
        self.git_status_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 8))
        
        self.repo_status_label = ttk.Label(status_frame, text="Repository durumu kontrol ediliyor...", 
                                         font=("Segoe UI", 10))
        self.repo_status_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 8))
        
        # Ana butonlar frame - modern buton tasarımı
        button_main_frame = ttk.Frame(main_frame)
        button_main_frame.grid(row=5, column=0, columnspan=3, pady=(20, 0))
        button_main_frame.columnconfigure(0, weight=1)
        button_main_frame.columnconfigure(1, weight=1)
        
        # Repository bağlama butonu - modern primary buton
        self.connect_button = ttk.Button(button_main_frame, text="🔗 Repository Bağla", 
                                       command=self.connect_repository, style="Primary.TButton")
        self.connect_button.grid(row=0, column=0, padx=(0, 10))
        
        # Ana işlem butonu - modern primary buton
        self.main_button = ttk.Button(button_main_frame, text="🚀 Repository'yi Yayınla", 
                                     command=self.start_publication, style="Primary.TButton")
        self.main_button.grid(row=0, column=1, padx=(10, 0))
        
        # Log frame - modern card tasarımı
        log_frame = ttk.LabelFrame(main_frame, text="📋 İşlem Logları", padding="20")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Log text widget - modern text tasarımı
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=80, 
                                                font=("Consolas", 9), 
                                                bg="#f8fafc", fg="#1e293b",
                                                insertbackground="#2563eb")
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.E, tk.S))
        
        # Progress bar - modern progress tasarımı
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate', 
                                       style="Accent.Horizontal.TProgressbar")
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status bar - modern status tasarımı
        self.status_bar = ttk.Label(progress_frame, text="Hazır", 
                                   font=("Segoe UI", 9), foreground="#64748b")
        self.status_bar.grid(row=1, column=0, sticky=tk.W)

    def check_git_status(self):
        """Git durumunu kontrol et"""
        try:
            # Git kurulum kontrolü
            result = subprocess.run("git --version", shell=True, capture_output=True, text=True)
            self.git_installed = result.returncode == 0
            
            if self.git_installed:
                self.git_status_label.config(text="✅ Git kurulu ve hazır", foreground="green")
            else:
                self.git_status_label.config(text="❌ Git kurulu değil", foreground="red")
            
            # Repository kontrolü
            self.git_repo_exists = os.path.exists(".git")
            if self.git_repo_exists:
                self.repo_status_label.config(text="✅ Git repository mevcut", foreground="green")
            else:
                self.repo_status_label.config(text="ℹ️  Git repository henüz başlatılmamış", foreground="blue")
                
        except Exception as e:
            self.log_message(f"❌ Git durum kontrolü hatası: {e}")

    def log_message(self, message):
        """Log mesajı ekle"""
        self.log_queue.put(message)

    def update_log(self):
        """Log mesajlarını güncelle"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, f"{message}\n")
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        
        # Her 100ms'de bir kontrol et
        self.root.after(100, self.update_log)

    def browse_folder(self):
        """Kullanıcının klasör seçmesini sağlar"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.project_path_var.set(folder_selected)
            self.current_directory = folder_selected
            
            # Proje adını otomatik öner
            folder_name = os.path.basename(folder_selected)
            if not self.project_name.get().strip():
                self.project_name.set(folder_name)
            
            self.log_message(f"📁 Proje klasörü seçildi: {folder_selected}")
            
            # Git durumunu yeni klasör için güncelle
            self.check_git_status()
            
            # Klasördeki dosyaları listele
            self.list_folder_contents()

    def validate_inputs(self):
        """Kullanıcı girişlerini doğrula"""
        project_name = self.project_name.get().strip()
        github_username = self.github_username.get().strip()
        
        if not project_name:
            messagebox.showerror("Hata", "Proje adı boş olamaz!")
            return False
        
        if not github_username:
            messagebox.showerror("Hata", "GitHub kullanıcı adı boş olamaz!")
            return False
        
        # Geçersiz karakterleri kontrol et
        invalid_chars = [' ', '/', '\\', ':', '*', '?', '"', '<', '>', '|', '@', '{', '}']
        if any(char in project_name for char in invalid_chars):
            messagebox.showerror("Hata", f"Proje adında geçersiz karakterler var!\nGeçersiz: {' '.join(invalid_chars)}")
            return False
        
        if any(char in github_username for char in invalid_chars):
            messagebox.showerror("Hata", f"GitHub kullanıcı adında geçersiz karakterler var!\nGeçersiz: {' '.join(invalid_chars)}")
            return False
        
        if not os.path.exists(self.current_directory):
            messagebox.showerror("Hata", "Proje klasörü bulunamadı!\nLütfen geçerli bir klasör seçin.")
            return False
        
        return True

    def connect_repository(self):
        """Repository bağlama - boş repo oluştur ve first commit at"""
        if not self.validate_inputs():
            return
            
        # Onay dialog'u göster
        result = messagebox.askyesno(
            "Repository Bağla",
            f"🔗 GitHub'da '{self.project_name.get()}' repository'si oluşturulacak ve bağlanacak.\n\n"
            f"📁 Klasör: {self.current_directory}\n"
            f"👤 Kullanıcı: {self.github_username.get()}\n"
            f"📝 İlk commit: {self.commit_message.get()}\n\n"
            "Devam etmek istiyor musunuz?"
        )
        
        if result:
            self.log_message("🔗 Repository bağlama işlemi başlıyor...")
            self.connect_button.config(state='disabled')
            self.main_button.config(state='disabled')
            self.progress.start()
            
            # Repository bağlama işlemini thread'de çalıştır
            threading.Thread(target=self.connect_repository_worker, daemon=True).start()
    
    def connect_repository_worker(self):
        """Repository bağlama işlemi - arka planda çalışır"""
        try:
            original_dir = os.getcwd()
            os.chdir(self.current_directory)
            
            # 1. Git init
            self.log_message("🔧 Git repository başlatılıyor...")
            result = subprocess.run("git init", shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise Exception(f"Git init hatası: {result.stderr}")
            self.log_message("✅ Git repository başlatıldı")
            
            # 2. README.md oluştur (eğer yoksa)
            if self.readme_var.get() == "create":
                readme_path = os.path.join(self.current_directory, "README.md")
                if not os.path.exists(readme_path):
                    self.log_message("📝 README.md oluşturuluyor...")
                    readme_content = f"# {self.project_name.get()}\n\nBu proje GitAuto ile otomatik olarak oluşturuldu.\n"
                    with open(readme_path, "w", encoding="utf-8") as f:
                        f.write(readme_content)
                    self.log_message("✅ README.md oluşturuldu")
            
            # 3. Git add (büyük projeler için daha uzun timeout)
            self.log_message("📁 Dosyalar ekleniyor...")
            result = subprocess.run("git add .", shell=True, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                raise Exception(f"Git add hatası: {result.stderr}")
            self.log_message("✅ Dosyalar eklendi")
            
            # 4. Git commit (konfigürasyon kontrolü ile)
            commit_msg = self.commit_message.get().strip() or "first commit"
            self.log_message(f"💾 İlk commit yapılıyor: {commit_msg}")
            
            # Git konfigürasyonunu kontrol et ve ayarla
            self.log_message("⚙️ Git konfigürasyonu kontrol ediliyor...")
            
            # User name kontrol et
            user_result = subprocess.run("git config user.name", shell=True, capture_output=True, text=True, timeout=5)
            if user_result.returncode != 0 or not user_result.stdout.strip():
                self.log_message("👤 Git user.name ayarlanıyor...")
                subprocess.run(f'git config user.name "{self.github_username.get()}"', shell=True, capture_output=True, text=True, timeout=5)
            
            # User email kontrol et
            email_result = subprocess.run("git config user.email", shell=True, capture_output=True, text=True, timeout=5)
            if email_result.returncode != 0 or not email_result.stdout.strip():
                self.log_message("📧 Git user.email ayarlanıyor...")
                subprocess.run(f'git config user.email "{self.github_username.get()}@users.noreply.github.com"', shell=True, capture_output=True, text=True, timeout=5)
            
            # Commit yap
            result = subprocess.run(f'git commit -m "{commit_msg}"', shell=True, capture_output=True, text=True, timeout=15)
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else "Bilinmeyen commit hatası"
                self.log_message(f"⚠️ Commit hatası: {error_msg}")
                
                # Alternatif commit yöntemi dene
                self.log_message("🔄 Alternatif commit yöntemi deneniyor...")
                result = subprocess.run(f'git commit -m "{commit_msg}" --allow-empty', shell=True, capture_output=True, text=True, timeout=15)
                if result.returncode != 0:
                    raise Exception(f"Git commit hatası: {result.stderr}")
            
            self.log_message("✅ İlk commit tamamlandı")
            
            # 5. Branch ayarla
            target_branch = self.selected_branch.get() or "main"
            self.log_message(f"🌿 Branch '{target_branch}' ayarlanıyor...")
            result = subprocess.run(f"git branch -M {target_branch}", shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                self.log_message(f"⚠️ Branch ayarlama uyarısı: {result.stderr}")
            else:
                self.log_message(f"✅ Branch '{target_branch}' ayarlandı")
            
            # 6. Remote ekle
            repo_url = f"https://github.com/{self.github_username.get()}/{self.project_name.get()}.git"
            self.log_message(f"🔗 Remote repository bağlanıyor: {repo_url}")
            result = subprocess.run(f'git remote add origin "{repo_url}"', shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode != 0 and "already exists" not in result.stderr:
                raise Exception(f"Remote add hatası: {result.stderr}")
            self.log_message("✅ Remote repository bağlandı")
            
            # 7. Push
            self.log_message(f"🚀 GitHub'a yayınlanıyor...")
            result = subprocess.run(f"git push -u origin {target_branch}", shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                raise Exception(f"Push hatası: {result.stderr}")
            self.log_message("✅ Repository GitHub'a yayınlandı!")
            
            os.chdir(original_dir)
            
            # Başarı mesajı
            self.root.after(0, lambda: messagebox.showinfo(
                "Başarılı! 🎉",
                f"🔗 Repository başarıyla bağlandı!\n\n"
                f"📍 URL: https://github.com/{self.github_username.get()}/{self.project_name.get()}\n"
                f"🌿 Branch: {target_branch}\n\n"
                "Artık branch işlemleri yapabilir ve yayınlama yapabilirsiniz!"
            ))
            
            # Branch listesini güncelle
            self.root.after(100, self.refresh_branches)
            
        except Exception as e:
            os.chdir(original_dir)
            error_msg = str(e)  # Hata mesajını string olarak sakla
            self.log_message(f"❌ Repository bağlama hatası: {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Hata", f"Repository bağlama hatası:\n{error_msg}"))
        
        finally:
            self.root.after(0, self.repository_connect_finished)
    
    def repository_connect_finished(self):
        """Repository bağlama işlemi tamamlandı"""
        self.connect_button.config(state='normal')
        self.main_button.config(state='normal')
        self.progress.stop()
        self.check_git_status()

    def refresh_branches(self):
        """Gerçek branch'leri listele ve combo box'ı güncelle"""
        try:
            if not os.path.exists(os.path.join(self.current_directory, ".git")):
                self.branch_combo['values'] = ["main", "master", "develop"]
                self.log_message("ℹ️ Git repository henüz başlatılmamış - varsayılan branch'ler gösteriliyor")
                return
            
            original_dir = os.getcwd()
            os.chdir(self.current_directory)
            
            # Local branch'leri al
            result = subprocess.run("git branch", shell=True, capture_output=True, text=True, timeout=10)
            local_branches = []
            
            if result.returncode == 0 and result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        branch = line.strip().replace('*', '').strip()
                        if branch and not branch.startswith('('):
                            local_branches.append(branch)
            
            # Remote branch'leri al
            result = subprocess.run("git branch -r", shell=True, capture_output=True, text=True, timeout=10)
            remote_branches = []
            
            if result.returncode == 0 and result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line.strip() and 'origin/' in line:
                        branch = line.strip().replace('origin/', '').strip()
                        if branch and branch != 'HEAD' and not branch.startswith('('):
                            remote_branches.append(branch)
            
            # Tüm branch'leri birleştir ve tekrarları kaldır
            all_branches = list(set(local_branches + remote_branches))
            
            # Varsayılan branch'leri ekle
            default_branches = ["main", "master", "develop"]
            for branch in default_branches:
                if branch not in all_branches:
                    all_branches.append(branch)
            
            # Sırala
            all_branches.sort()
            
            # Combo box'ı güncelle
            self.branch_combo['values'] = all_branches
            
            # Mevcut branch'ı seç
            current_result = subprocess.run("git branch --show-current", shell=True, capture_output=True, text=True, timeout=5)
            if current_result.returncode == 0 and current_result.stdout.strip():
                current_branch = current_result.stdout.strip()
                if current_branch in all_branches:
                    self.selected_branch.set(current_branch)
                    self.log_message(f"🌿 Aktif branch: {current_branch}")
            
            self.log_message(f"🔄 Branch listesi güncellendi: {len(all_branches)} branch bulundu")
            
            os.chdir(original_dir)
            
        except Exception as e:
            self.log_message(f"⚠️ Branch listesi güncellenirken hata: {e}")
            self.branch_combo['values'] = ["main", "master", "develop"]

    def clean_repository(self):
        """Repository'yi temizle - gereksiz dosyaları kaldır"""
        try:
            if not os.path.exists(os.path.join(self.current_directory, ".git")):
                messagebox.showerror("Hata", "Git repository bulunamadı!")
                return
            
            # Onay al
            result = messagebox.askyesno(
                "Repository Temizle",
                "🧹 Repository temizlenecek:\n\n"
                "• Gereksiz dosyalar kaldırılacak\n"
                "• .gitignore güncellenecek\n"
                "• Git cache temizlenecek\n\n"
                "Devam etmek istiyor musunuz?"
            )
            
            if result:
                self.log_message("🧹 Repository temizleme başlatılıyor...")
                
                original_dir = os.getcwd()
                os.chdir(self.current_directory)
                
                # Git cache temizle
                self.log_message("🗑️ Git cache temizleniyor...")
                subprocess.run("git gc", shell=True, capture_output=True, text=True, timeout=30)
                
                # Git ignore güncelle
                gitignore_path = os.path.join(self.current_directory, ".gitignore")
                if not os.path.exists(gitignore_path):
                    self.log_message("📝 .gitignore oluşturuluyor...")
                    with open(gitignore_path, "w", encoding="utf-8") as f:
                        f.write("# GitAuto tarafından oluşturuldu\n")
                        f.write("node_modules/\n")
                        f.write("build/\n")
                        f.write("dist/\n")
                        f.write("*.exe\n")
                        f.write("__pycache__/\n")
                        f.write(".vscode/\n")
                        f.write("*.log\n")
                
                # Gereksiz dosyaları kaldır
                self.log_message("📁 Gereksiz dosyalar kaldırılıyor...")
                subprocess.run("git rm -r --cached .", shell=True, capture_output=True, text=True, timeout=30)
                subprocess.run("git add .", shell=True, capture_output=True, text=True, timeout=60)
                
                # Commit (konfigürasyon kontrolü ile)
                self.log_message("💾 Temizlik commit'i yapılıyor...")
                
                # Git konfigürasyonunu kontrol et
                user_result = subprocess.run("git config user.name", shell=True, capture_output=True, text=True, timeout=5)
                if user_result.returncode != 0 or not user_result.stdout.strip():
                    subprocess.run('git config user.name "GitAuto"', shell=True, capture_output=True, text=True, timeout=5)
                
                email_result = subprocess.run("git config user.email", shell=True, capture_output=True, text=True, timeout=5)
                if email_result.returncode != 0 or not email_result.stdout.strip():
                    subprocess.run('git config user.email "gitauto@users.noreply.github.com"', shell=True, capture_output=True, text=True, timeout=5)
                
                commit_result = subprocess.run('git commit -m "Repository temizlendi - GitAuto"', 
                             shell=True, capture_output=True, text=True, timeout=30)
                
                if commit_result.returncode != 0:
                    self.log_message("⚠️ Commit hatası, alternatif yöntem deneniyor...")
                    subprocess.run('git commit -m "Repository temizlendi - GitAuto" --allow-empty', 
                                 shell=True, capture_output=True, text=True, timeout=30)
                
                os.chdir(original_dir)
                
                self.log_message("✅ Repository başarıyla temizlendi!")
                messagebox.showinfo("Başarılı! 🎉", "Repository temizlendi!\n\nArtık daha hızlı çalışacak.")
                
        except Exception as e:
            self.log_message(f"❌ Repository temizleme hatası: {e}")
            messagebox.showerror("Hata", f"Repository temizleme hatası:\n{e}")

    def create_new_branch(self):
        """Yeni branch oluştur"""
        branch_name = self.new_branch_var.get().strip()
        if not branch_name:
            messagebox.showerror("Hata", "Branch adı boş olamaz!")
            return
        
        # Geçersiz karakterleri kontrol et
        invalid_chars = [' ', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        if any(char in branch_name for char in invalid_chars):
            messagebox.showerror("Hata", f"Branch adında geçersiz karakterler var!\nGeçersiz karakterler: {' '.join(invalid_chars)}")
            return
        
        def create_branch():
            try:
                self.log_message(f"🌱 Yeni branch oluşturuluyor: {branch_name}")
                
                if not os.path.exists(os.path.join(self.current_directory, ".git")):
                    self.log_message("❌ Git repository henüz başlatılmamış!")
                    self.root.after(0, lambda: messagebox.showerror("Hata", "Git repository henüz başlatılmamış!\nÖnce 'Repository Bağla' butonunu kullanın."))
                    return
                
                result = subprocess.run(f"git checkout -b {branch_name}", shell=True, 
                                     capture_output=True, text=True, cwd=self.current_directory, timeout=15)
                
                if result.returncode == 0:
                    self.log_message(f"✅ Branch '{branch_name}' başarıyla oluşturuldu!")
                    
                    # Yeni branch'i hedef branch listesine ekle
                    current_values = list(self.branch_combo['values'])
                    if branch_name not in current_values:
                        current_values.append(branch_name)
                        current_values.sort()
                        self.branch_combo['values'] = current_values
                    
                    # Yeni branch'i otomatik seç
                    self.selected_branch.set(branch_name)
                    self.log_message(f"🎯 Hedef branch otomatik '{branch_name}' olarak seçildi")
                    
                    self.new_branch_var.set("")
                    
                    # Başarı mesajı
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Başarılı! 🎉",
                        f"🌱 Branch '{branch_name}' başarıyla oluşturuldu!\n\n"
                        f"✅ Otomatik olarak hedef branch seçildi\n"
                        f"🚀 Artık yayınlama yapabilirsiniz"
                    ))
                    
                else:
                    error_msg = result.stderr or "Bilinmeyen hata"
                    if "already exists" in error_msg:
                        self.log_message(f"⚠️ Branch '{branch_name}' zaten mevcut!")
                        self.selected_branch.set(branch_name)
                        self.log_message(f"🎯 Mevcut branch '{branch_name}' hedef olarak seçildi")
                    else:
                        self.log_message(f"❌ Branch oluşturma hatası: {error_msg}")
                        self.root.after(0, lambda: messagebox.showerror("Hata", f"Branch oluşturma hatası:\n{error_msg}"))
                        
            except Exception as e:
                error_msg = str(e)  # Hata mesajını string olarak sakla
                self.log_message(f"❌ Branch oluşturma hatası: {error_msg}")
                self.root.after(0, lambda: messagebox.showerror("Hata", f"Branch oluşturma hatası:\n{error_msg}"))
        
        # Thread'de çalıştır
        threading.Thread(target=create_branch, daemon=True).start()

    def list_branches(self):
        """Mevcut branch'leri listele"""
        def list_branches_thread():
            try:
                self.log_message("📋 Mevcut branch'ler listeleniyor...")
                
                if not self.git_repo_exists:
                    self.log_message("ℹ️  Git repository henüz başlatılmamış")
                    return
                
                result = subprocess.run("git branch", shell=True, capture_output=True, 
                                     text=True, cwd=self.current_directory)
                
                if result.returncode == 0 and result.stdout:
                    self.log_message("🌿 Mevcut Branch'ler:")
                    self.log_message("-" * 30)
                    branches = result.stdout.strip().split('\n')
                    for branch in branches:
                        if branch.strip():
                            if branch.startswith('*'):
                                self.log_message(f"  🌟 {branch.strip()} (aktif)")
                            else:
                                self.log_message(f"     {branch.strip()}")
                else:
                    self.log_message("ℹ️  Henüz branch bulunamadı")
                    
            except Exception as e:
                self.log_message(f"❌ Branch listeleme hatası: {e}")
        
        threading.Thread(target=list_branches_thread, daemon=True).start()

    def start_publication(self):
        """Repository yayınlama işlemini başlat"""
        # Giriş kontrolü
        if not self.project_name.get().strip():
            messagebox.showerror("Hata", "Proje adı boş olamaz!")
            return
        
        if not self.github_username.get().strip():
            messagebox.showerror("Hata", "GitHub kullanıcı adı boş olamaz!")
            return
        
        if not self.git_installed:
            messagebox.showerror("Hata", "Git kurulu değil!\nLütfen önce Git'i yükleyin: https://git-scm.com/downloads")
            return
        
        # Onay al
        project_name = self.project_name.get().strip()
        github_username = self.github_username.get().strip()
        commit_message = self.commit_message.get().strip()
        target_branch = self.selected_branch.get()
        readme_option = self.readme_var.get()
        
        confirm_text = f"""📋 Yayınlama Özeti:

📁 Proje: {project_name}
👤 GitHub: {github_username}
💬 Commit: {commit_message}
🌿 Branch: {target_branch}
📖 README: {'Korunacak' if readme_option == 'keep' else 'Yeniden oluşturulacak'}

✅ Devam edilsin mi?"""
        
        if not messagebox.askyesno("Onay", confirm_text):
            return
        
        # İşlemi başlat
        self.main_button.config(state="disabled")
        self.progress.start()
        
        # Thread'de çalıştır
        threading.Thread(target=self.publish_repository, daemon=True).start()

    def publish_repository(self):
        """Repository'yi hızlı ve güvenli yayınla"""
        try:
            project_name = self.project_name.get().strip()
            github_username = self.github_username.get().strip()
            commit_message = self.commit_message.get().strip() or "Repository güncellendi"
            target_branch = self.selected_branch.get() or "main"
            readme_option = self.readme_var.get()
            
            repo_url = f"https://github.com/{github_username}/{project_name}.git"
            
            self.log_message("🚀 Hızlı yayınlama başlatılıyor...")
            
            # README.md işlemi (hızlı)
            readme_path = os.path.join(self.current_directory, "README.md")
            if readme_option == "create" and not os.path.exists(readme_path):
                self.log_message("📝 README.md oluşturuluyor...")
                readme_content = f"# {project_name}\n\nBu proje GitAuto ile otomatik olarak oluşturuldu.\n"
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(readme_content)
                self.log_message("✅ README.md oluşturuldu")
            
            # Git durumu kontrol (hızlı)
            git_dir = os.path.join(self.current_directory, ".git")
            if not os.path.exists(git_dir):
                self.log_message("❌ Git repository bulunamadı! Önce 'Repository Bağla' kullanın.")
                raise Exception("Git repository bulunamadı! Önce 'Repository Bağla' kullanın.")
            
            # Değişiklikleri kontrol et (hızlı)
            self.log_message("🔍 Değişiklikler kontrol ediliyor...")
            status_result = subprocess.run("git status --porcelain", shell=True, capture_output=True, 
                                         text=True, cwd=self.current_directory, timeout=5)
            
            if not status_result.stdout.strip():
                self.log_message("ℹ️ Değişiklik bulunamadı, sadece push yapılıyor...")
                skip_commit = True
            else:
                self.log_message(f"📁 {len(status_result.stdout.strip().split())} değişiklik bulundu")
                skip_commit = False
            
            # Paralel Git işlemleri
            if not skip_commit:
                # Dosyaları ekle (akıllı filtreleme ile)
                self.log_message("📁 Dosyalar ekleniyor...")
                
                # Önce .gitignore'ı kontrol et
                gitignore_path = os.path.join(self.current_directory, ".gitignore")
                if os.path.exists(gitignore_path):
                    self.log_message("📋 .gitignore dosyası bulundu - gereksiz dosyalar filtreleniyor")
                    self.log_message("⏳ Bu işlem büyük projelerde biraz zaman alabilir...")
                    result = subprocess.run("git add -A", shell=True, capture_output=True, 
                                         text=True, cwd=self.current_directory, timeout=60)
                else:
                    self.log_message("⚠️ .gitignore bulunamadı - tüm dosyalar ekleniyor")
                    self.log_message("⏳ Büyük proje tespit edildi - lütfen bekleyin...")
                    result = subprocess.run("git add -A", shell=True, capture_output=True, 
                                         text=True, cwd=self.current_directory, timeout=120)
                
                if result.returncode != 0:
                    raise Exception(f"Git add hatası: {result.stderr}")
                self.log_message("✅ Dosyalar eklendi")
                
                # Commit (hızlı - konfigürasyon kontrolü ile)
                self.log_message(f"💾 Commit yapılıyor: {commit_message}")
                
                # Git konfigürasyonunu kontrol et
                user_result = subprocess.run("git config user.name", shell=True, capture_output=True, text=True, cwd=self.current_directory, timeout=5)
                if user_result.returncode != 0 or not user_result.stdout.strip():
                    subprocess.run(f'git config user.name "{github_username}"', shell=True, capture_output=True, text=True, cwd=self.current_directory, timeout=5)
                
                email_result = subprocess.run("git config user.email", shell=True, capture_output=True, text=True, cwd=self.current_directory, timeout=5)
                if email_result.returncode != 0 or not email_result.stdout.strip():
                    subprocess.run(f'git config user.email "{github_username}@users.noreply.github.com"', shell=True, capture_output=True, text=True, cwd=self.current_directory, timeout=5)
                
                result = subprocess.run(f'git commit -m "{commit_message}"', shell=True, 
                                     capture_output=True, text=True, cwd=self.current_directory, timeout=10)
                if result.returncode != 0:
                    if "nothing to commit" in result.stdout.lower():
                        self.log_message("ℹ️ Commit edilecek değişiklik yok")
                    else:
                        error_msg = result.stderr.strip() if result.stderr else "Bilinmeyen commit hatası"
                        self.log_message(f"⚠️ Commit hatası: {error_msg}")
                        
                        # Alternatif commit yöntemi dene
                        self.log_message("🔄 Alternatif commit yöntemi deneniyor...")
                        result = subprocess.run(f'git commit -m "{commit_message}" --allow-empty', shell=True, 
                                             capture_output=True, text=True, cwd=self.current_directory, timeout=10)
                        if result.returncode != 0:
                            raise Exception(f"Git commit hatası: {result.stderr}")
                else:
                    self.log_message("✅ Commit tamamlandı")
            
            # Remote kontrol ve güncelleme (hızlı)
            self.log_message("🔗 Remote bağlantı kontrol ediliyor...")
            remote_result = subprocess.run("git remote get-url origin", shell=True, capture_output=True, 
                                         text=True, cwd=self.current_directory, timeout=5)
            
            if remote_result.returncode != 0 or repo_url not in remote_result.stdout:
                self.log_message("🔧 Remote origin güncelleniyor...")
                # Eski origin'i kaldır (sessizce)
                subprocess.run("git remote remove origin", shell=True, capture_output=True, 
                             text=True, cwd=self.current_directory, timeout=5)
                # Yeni origin ekle
                result = subprocess.run(f'git remote add origin "{repo_url}"', shell=True, 
                                     capture_output=True, text=True, cwd=self.current_directory, timeout=5)
                if result.returncode == 0:
                    self.log_message("✅ Remote origin güncellendi")
            else:
                self.log_message("✅ Remote origin hazır")
            
            # Push (optimized - büyük projeler için daha uzun timeout)
            self.log_message(f"🚀 '{target_branch}' branch'i GitHub'a yayınlanıyor...")
            push_cmd = f"git push -u origin {target_branch}"
            result = subprocess.run(push_cmd, shell=True, capture_output=True, 
                                 text=True, cwd=self.current_directory, timeout=120)
            
            if result.returncode == 0:
                self.log_message("🎉 Yayınlama başarıyla tamamlandı!")
                self.log_message(f"📍 Repository: {repo_url.replace('.git', '')}")
                self.log_message(f"🌿 Branch: {target_branch}")
                
                # Başarı mesajı
                self.root.after(0, lambda: messagebox.showinfo("Başarılı! 🎉", 
                    f"Repository başarıyla yayınlandı!\n\n"
                    f"📍 URL: {repo_url.replace('.git', '')}\n"
                    f"🌿 Branch: {target_branch}\n"
                    f"⚡ Hızlı yayınlama kullanıldı"))
            else:
                error_msg = result.stderr.strip() if result.stderr else "Bilinmeyen hata"
                self.log_message(f"❌ Push hatası: {error_msg}")
                self.log_message("💡 GitHub'da repository'nin oluşturulduğundan emin olun!")
                
        except Exception as e:
            self.log_message(f"❌ Beklenmeyen hata: {e}")
        finally:
            # UI'ı güncelle
            self.root.after(0, self.publication_finished)

    def publication_finished(self):
        """Yayınlama işlemi tamamlandı"""
        self.main_button.config(state="normal")
        self.progress.stop()
        self.check_git_status()

    def list_folder_contents(self):
        """Seçilen klasördeki dosyaları listele"""
        try:
            if not os.path.exists(self.current_directory):
                return
            
            self.log_message(f"📋 Klasör içeriği ({self.current_directory}):")
            self.log_message("-" * 50)
            
            # Dosya ve klasörleri listele
            items = os.listdir(self.current_directory)
            files = []
            folders = []
            
            for item in items:
                item_path = os.path.join(self.current_directory, item)
                if os.path.isfile(item_path):
                    files.append(item)
                elif os.path.isdir(item_path):
                    folders.append(item)
            
            # Klasörleri göster
            if folders:
                self.log_message("📁 Klasörler:")
                for folder in sorted(folders):
                    self.log_message(f"  📁 {folder}")
            
            # Dosyaları göster
            if files:
                self.log_message("📄 Dosyalar:")
                for file in sorted(files):
                    # Git ve sistem dosyalarını gizle
                    if not file.startswith('.') and file not in ['__pycache__', 'node_modules']:
                        self.log_message(f"  📄 {file}")
            
            # README.md kontrolü
            readme_path = os.path.join(self.current_directory, "README.md")
            if os.path.exists(readme_path):
                self.log_message("✅ README.md dosyası bulundu")
                self.readme_var.set("keep")  # Otomatik olarak koru seçeneğini seç
            else:
                self.log_message("ℹ️  README.md dosyası bulunamadı")
                self.readme_var.set("create")  # Otomatik olarak oluştur seçeneğini seç
            
            self.log_message("-" * 50)
            
        except Exception as e:
            self.log_message(f"❌ Klasör içeriği listelenirken hata: {e}")

def main():
    """Ana uygulama - modern tasarım"""
    root = tk.Tk()
    
    # Modern tema ve stil ayarları
    style = ttk.Style()
    style.theme_use('clam')
    
    # Pencere ikonu ve başlık
    try:
        root.iconbitmap("icon.ico")  # Eğer icon dosyası varsa
    except:
        pass  # Icon yoksa devam et
    
    # Modern pencere ayarları
    root.configure(bg="#ffffff")
    root.option_add('*TFrame*background', '#ffffff')
    root.option_add('*TLabel*background', '#ffffff')
    
    app = GitAutoGUI(root)
    
    # Pencere kapatma olayı - modern dialog
    def on_closing():
        if messagebox.askokcancel("🚪 Çıkış", 
                                 "GitAuto'dan çıkmak istediğinizden emin misiniz?\n\n"
                                 "Kaydedilmemiş değişiklikler kaybolabilir."):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Pencereyi ekranın ortasına yerleştir
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Pencereyi öne getir
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    root.mainloop()

if __name__ == "__main__":
    main()

