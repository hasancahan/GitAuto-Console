#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitAuto GUI - Windows Uygulaması
Adım adım ilerleyen modern arayüz ile Git repository yönetimi
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
        self.root.title("🚀 GitAuto - Adım Adım Git Repository Yönetimi")
        self.root.geometry("900x900")
        self.root.resizable(True, True)
        
        # Modern stil tanımlamaları
        self.setup_styles()
        
        # Ana değişkenler
        self.project_name = tk.StringVar()
        self.github_username = tk.StringVar()
        self.commit_message = tk.StringVar(value="first commit")
        self.selected_branch = tk.StringVar(value="main")
        self.readme_var = tk.StringVar(value="keep")
        self.current_directory = os.getcwd()
        
        # Git durumu
        self.git_installed = False
        self.git_repo_exists = False
        
        # Adım yönetimi
        self.current_step = 0
        self.total_steps = 5
        
        # Log mesajları için queue
        self.log_queue = queue.Queue()
        
        # Arayüz oluştur
        self.create_widgets()
        
        # İlk adımı göster
        self.show_step(0)
        
        # Git durumunu kontrol et
        self.check_git_status()
        
        # Log güncellemelerini başlat
        self.update_log()

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

    def create_widgets(self):
        """Adım adım ilerleyen widget'ları oluştur"""
        # Ana frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid ağırlıkları
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Başlık frame
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        title_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(title_frame, 
                               text="🚀 GitAuto", 
                               font=("Segoe UI", 24, "bold"),
                               foreground="#2563eb")
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        subtitle_label = ttk.Label(title_frame, 
                                   text="Adım Adım Git Repository Yönetimi", 
                                   font=("Segoe UI", 12),
                                   foreground="#64748b")
        subtitle_label.grid(row=1, column=0)
        
        # Adım göstergesi
        step_frame = ttk.Frame(main_frame)
        step_frame.grid(row=1, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        step_frame.columnconfigure(0, weight=1)
        
        self.step_label = ttk.Label(step_frame, 
                                   text="Adım 1/5: Proje Bilgileri", 
                                   font=("Segoe UI", 14, "bold"),
                                   foreground="#1e293b")
        self.step_label.grid(row=0, column=0, pady=(0, 10))
        
        # Adım progress bar
        self.step_progress = ttk.Progressbar(step_frame, 
                                            mode='determinate', 
                                            style="Accent.Horizontal.TProgressbar",
                                            length=400)
        self.step_progress.grid(row=1, column=0)
        self.step_progress['value'] = 20
        
        # İçerik frame - her adımda değişecek
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        self.content_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Navigasyon butonları
        nav_frame = ttk.Frame(main_frame)
        nav_frame.grid(row=3, column=0, pady=(20, 0), sticky=(tk.W, tk.E))
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=1)
        
        self.prev_button = ttk.Button(nav_frame, text="⬅️ Önceki", 
                                     command=self.previous_step, 
                                     style="Secondary.TButton",
                                     state="disabled")
        self.prev_button.grid(row=0, column=0, padx=(0, 10))
        
        self.next_button = ttk.Button(nav_frame, text="Sonraki ➡️", 
                                    command=self.next_step, 
                                    style="Primary.TButton")
        self.next_button.grid(row=0, column=1, padx=(10, 0))
        
        # Log frame - her adımda görünür
        log_frame = ttk.LabelFrame(main_frame, text="📋 İşlem Logları", padding="20")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        log_frame.columnconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80, 
                                                font=("Consolas", 9), 
                                                bg="#f8fafc", fg="#1e293b",
                                                insertbackground="#2563eb")
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Progress bar
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate', 
                                       style="Accent.Horizontal.TProgressbar")
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status bar
        self.status_bar = ttk.Label(progress_frame, text="Hazır", 
                                   font=("Segoe UI", 9), foreground="#64748b")
        self.status_bar.grid(row=1, column=0, sticky=tk.W)

    def show_step(self, step_number):
        """Belirtilen adımı göster"""
        self.current_step = step_number
        
        # İçerik frame'i temizle
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Adım göstergesini güncelle
        step_names = [
            "Proje Bilgileri",
            "README.md Yönetimi", 
            "Git Durumu",
            "Branch Yönetimi",
            "Repository İşlemleri"
        ]
        
        self.step_label.config(text=f"Adım {step_number + 1}/5: {step_names[step_number]}")
        self.step_progress['value'] = (step_number + 1) * 20
        
        # Navigasyon butonlarını güncelle
        if step_number == 0:
            self.prev_button.config(state="disabled")
        else:
            self.prev_button.config(state="normal")
            
        if step_number == self.total_steps - 1:
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")
        
        # Adıma özel içeriği göster
        if step_number == 0:
            self.show_project_info_step()
        elif step_number == 1:
            self.show_readme_step()
        elif step_number == 2:
            self.show_git_status_step()
        elif step_number == 3:
            self.show_branch_step()
        elif step_number == 4:
            self.show_repository_step()

    def show_project_info_step(self):
        """Adım 1: Proje bilgileri"""
        # Proje bilgileri frame
        project_frame = ttk.LabelFrame(self.content_frame, text="📁 Proje Bilgileri", padding="20")
        project_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        project_frame.columnconfigure(1, weight=1)
        
        # Proje klasörü seçimi
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

    def show_readme_step(self):
        """Adım 2: README.md yönetimi"""
        readme_frame = ttk.LabelFrame(self.content_frame, text="📖 README.md Yönetimi", padding="20")
        readme_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        readme_frame.columnconfigure(0, weight=1)
        
        # README seçenekleri
        readme_keep = ttk.Radiobutton(readme_frame, text="📝 Mevcut README.md'yi koru (önerilen)", 
                                     variable=self.readme_var, value="keep")
        readme_keep.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        readme_create = ttk.Radiobutton(readme_frame, text="🔄 GitAuto ile yeni README.md oluştur", 
                                       variable=self.readme_var, value="create")
        readme_create.grid(row=1, column=0, sticky=tk.W, pady=(0, 15))
        
        readme_view = ttk.Radiobutton(readme_frame, text="👁️ Mevcut README.md'yi görüntüle", 
                                     variable=self.readme_var, value="view")
        readme_view.grid(row=2, column=0, sticky=tk.W, pady=(0, 15))
        
        # README önizleme butonu
        preview_btn = ttk.Button(readme_frame, text="👁️ README Önizle", 
                                command=self.preview_readme, style="Secondary.TButton")
        preview_btn.grid(row=3, column=0, pady=(15, 0))
        
        # Repository durumu kontrolü ve bağlama butonu
        repo_status_frame = ttk.Frame(readme_frame)
        repo_status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        repo_status_frame.columnconfigure(0, weight=1)
        
        # Repository durumu etiketi
        self.repo_status_readme_label = ttk.Label(repo_status_frame, 
                                                 text="Repository durumu kontrol ediliyor...", 
                                                 font=("Segoe UI", 10))
        self.repo_status_readme_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        # Repository bağlama butonu (sadece repository yoksa görünür)
        self.connect_button_readme = ttk.Button(repo_status_frame, text="🔗 Repository Bağla", 
                                               command=self.connect_repository, style="Primary.TButton")
        self.connect_button_readme.grid(row=1, column=0, pady=(0, 15))
        
        # Repository durumunu kontrol et ve butonları güncelle
        self.update_readme_repo_status()

    def update_readme_repo_status(self):
        """README adımında repository durumunu güncelle"""
        try:
            # Widget'ların mevcut olup olmadığını kontrol et
            if not hasattr(self, 'repo_status_readme_label') or not hasattr(self, 'connect_button_readme'):
                return  # Widget'lar henüz oluşturulmamışsa çık
            
            # Widget'ların gerçekten mevcut olup olmadığını kontrol et
            try:
                if not self.repo_status_readme_label.winfo_exists() or not self.connect_button_readme.winfo_exists():
                    return  # Widget'lar artık mevcut değilse çık
            except tk.TclError:
                return  # Widget referans hatası durumunda çık
            
            # Repository durumunu gerçek zamanlı kontrol et
            git_dir = os.path.join(self.current_directory, ".git")
            repo_exists = os.path.exists(git_dir) and os.path.isdir(git_dir)
            
            # Eğer .git klasörü varsa ama repository bozuksa
            if repo_exists:
                try:
                    # Git status komutu ile repository sağlığını kontrol et
                    result = subprocess.run("git status", shell=True, capture_output=True, 
                                          text=True, cwd=self.current_directory, timeout=5)
                    if result.returncode != 0:
                        repo_exists = False
                        self.log_message("⚠️ README: Git repository bozuk veya geçersiz")
                except:
                    repo_exists = False
                    self.log_message("⚠️ README: Git repository erişilemez durumda")
            
            if repo_exists:
                # Repository varsa
                try:
                    self.repo_status_readme_label.config(text="✅ Git repository mevcut ve sağlıklı", foreground="green")
                    self.connect_button_readme.grid_remove()  # Butonu gizle
                    self.log_message("✅ README: Repository mevcut - Bağlama butonu gizlendi")
                except tk.TclError:
                    # Widget referans hatası durumunda sadece log'a yaz
                    self.log_message("⚠️ README widget'ları güncellenirken referans hatası")
            else:
                # Repository yoksa
                try:
                    self.repo_status_readme_label.config(text="❌ Git repository bulunamadı", foreground="red")
                    self.connect_button_readme.grid()  # Butonu göster
                    self.log_message("❌ README: Repository bulunamadı - Bağlama butonu gösterildi")
                except tk.TclError:
                    # Widget referans hatası durumunda sadece log'a yaz
                    self.log_message("⚠️ README widget'ları güncellenirken referans hatası")
                
        except Exception as e:
            # Widget mevcutsa hata mesajını göster
            try:
                if hasattr(self, 'repo_status_readme_label') and self.repo_status_readme_label.winfo_exists():
                    self.repo_status_readme_label.config(text="❌ Repository durumu kontrol edilemedi", foreground="red")
            except tk.TclError:
                pass  # Widget referans hatası durumunda sessizce devam et
            self.log_message(f"❌ Repository durum kontrolü hatası: {e}")

    def check_repository_before_proceed(self):
        """README adımından sonra repository kontrolü yap"""
        repo_exists = os.path.exists(os.path.join(self.current_directory, ".git"))
        
        if not repo_exists:
            result = messagebox.askyesno(
                "Repository Gerekli", 
                "❌ Git repository henüz başlatılmamış!\n\n"
                "Devam etmek için önce 'Repository Bağla' butonunu kullanarak\n"
                "bir Git repository oluşturmanız gerekiyor.\n\n"
                "Repository oluşturmak ister misiniz?"
            )
            
            if result:
                # README adımına geri dön
                self.show_step(1)
                return False
            else:
                return False
        
        return True

    def show_branch_step(self):
        """Adım 3: Branch yönetimi"""
        branch_frame = ttk.LabelFrame(self.content_frame, text="🌿 Branch Yönetimi", padding="20")
        branch_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        branch_frame.columnconfigure(1, weight=1)
        
        # Branch seçimi
        branch_label = ttk.Label(branch_frame, text="Hedef Branch:", font=("Segoe UI", 10, "bold"))
        branch_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        
        self.branch_combo = ttk.Combobox(branch_frame, textvariable=self.selected_branch, 
                                        values=["main", "master", "develop"], width=25, 
                                        state="readonly", font=("Segoe UI", 10))
        self.branch_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        
        refresh_btn = ttk.Button(branch_frame, text="🔄", command=self.refresh_branches, 
                                width=4, style="Accent.TButton")
        refresh_btn.grid(row=0, column=2, padx=(15, 0), pady=(0, 8))
        
        # Yeni branch oluştur
        new_branch_label = ttk.Label(branch_frame, text="Yeni Branch:", font=("Segoe UI", 10, "bold"))
        new_branch_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        
        self.new_branch_var = tk.StringVar()
        new_branch_entry = ttk.Entry(branch_frame, textvariable=self.new_branch_var, 
                                   width=25, font=("Segoe UI", 10))
        new_branch_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 15), pady=(0, 8))
        
        create_branch_btn = ttk.Button(branch_frame, text="🌱 Branch Oluştur", 
                                      command=self.create_new_branch, style="Accent.TButton")
        create_branch_btn.grid(row=1, column=2, padx=(15, 0), pady=(0, 8))
        
        # Branch işlemleri
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
        
        # Branch listesini güncelle
        self.refresh_branches()

    def show_git_status_step(self):
        """Adım 4: Git durumu"""
        status_frame = ttk.LabelFrame(self.content_frame, text="🔍 Git Durumu", padding="20")
        status_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        status_frame.columnconfigure(1, weight=1)
        
        # Git durum etiketleri
        self.git_status_label = ttk.Label(status_frame, text="Git durumu kontrol ediliyor...", 
                                         font=("Segoe UI", 10))
        self.git_status_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 8))
        
        self.repo_status_label = ttk.Label(status_frame, text="Repository durumu kontrol ediliyor...", 
                                          font=("Segoe UI", 10))
        self.repo_status_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 8))
        
        # Git kurulum kontrolü
        git_check_btn = ttk.Button(status_frame, text="🔍 Git Durumunu Kontrol Et", 
                                  command=self.check_git_status, style="Accent.TButton")
        git_check_btn.grid(row=2, column=0, columnspan=2, pady=(15, 0))

    def show_repository_step(self):
        """Adım 5: Repository işlemleri"""
        repo_frame = ttk.LabelFrame(self.content_frame, text="🚀 Repository Yayınlama", padding="20")
        repo_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        repo_frame.columnconfigure(0, weight=1)
        
        # Ana işlem butonu - Adım 5'te direkt aktif
        self.main_button = ttk.Button(repo_frame, text="🚀 Repository'yi Yayınla", 
                                      command=self.start_publication, style="Primary.TButton",
                                      state="normal")
        self.main_button.grid(row=0, column=0, pady=(0, 15))
        
        # Bilgi etiketi
        info_label = ttk.Label(repo_frame, 
                              text="💡 Repository bağlama işlemi README.md adımında yapılmıştır.\n🚀 Yayınlama butonu aktif - Dosyaları yayınlayabilirsiniz!",
                              font=("Segoe UI", 10),
                              foreground="#64748b",
                              justify="center")
        info_label.grid(row=1, column=0, pady=(15, 0))

    def next_step(self):
        """Sonraki adıma geç"""
        # Adım 1 (Proje Bilgileri) bitince repository kontrolü yap
        if self.current_step == 0:  # Proje Bilgileri adımından sonra
            self.log_message("🔍 Adım 1 tamamlandı - Repository durumu kontrol ediliyor...")
            self.check_repository_status()
            
            # Repository durumuna göre UI'ı güncelle
            self.refresh_ui_after_repo_check()
        
        # README adımından sonra repository kontrolü yap
        elif self.current_step == 1:  # README adımından sonra
            if not self.check_repository_before_proceed():
                return
        
        if self.current_step < self.total_steps - 1:
            self.show_step(self.current_step + 1)

    def previous_step(self):
        """Önceki adıma geç"""
        if self.current_step > 0:
            self.show_step(self.current_step - 1)



    def preview_readme(self):
        """README.md önizlemesi göster"""
        readme_path = os.path.join(self.current_directory, "README.md")
        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Önizleme penceresi
                preview_window = tk.Toplevel(self.root)
                preview_window.title("README.md Önizleme")
                preview_window.geometry("600x400")
                preview_window.configure(bg="#ffffff")
                
                # İçerik
                text_widget = scrolledtext.ScrolledText(preview_window, 
                                                      font=("Consolas", 10),
                                                      bg="#f8fafc", fg="#1e293b")
                text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                text_widget.insert(tk.END, content)
                text_widget.config(state=tk.DISABLED)
                
            except Exception as e:
                messagebox.showerror("Hata", f"README.md okunamadı:\n{e}")
        else:
            messagebox.showinfo("Bilgi", "README.md dosyası bulunamadı.")

    def check_git_status(self):
        """Git durumunu kontrol et - gerçek zamanlı"""
        try:
            # Git kurulum kontrolü
            result = subprocess.run("git --version", shell=True, capture_output=True, text=True)
            self.git_installed = result.returncode == 0
            
            # Git durumu etiketini güncelle (eğer varsa)
            if hasattr(self, 'git_status_label'):
                try:
                    if self.git_status_label.winfo_exists():
                        if self.git_installed:
                            self.git_status_label.config(text="✅ Git kurulu ve hazır", foreground="green")
                        else:
                            self.git_status_label.config(text="❌ Git kurulu değil", foreground="red")
                except tk.TclError:
                    pass  # Widget referans hatası durumunda sessizce devam et
            
            # Repository kontrolü - gerçek zamanlı
            git_dir = os.path.join(self.current_directory, ".git")
            self.git_repo_exists = os.path.exists(git_dir) and os.path.isdir(git_dir)
            
            # Eğer .git klasörü varsa ama boşsa (bozuk repository)
            if os.path.exists(git_dir) and os.path.isdir(git_dir):
                try:
                    # Git status komutu ile repository sağlığını kontrol et
                    result = subprocess.run("git status", shell=True, capture_output=True, 
                                          text=True, cwd=self.current_directory, timeout=5)
                    if result.returncode != 0:
                        self.git_repo_exists = False
                        self.log_message("⚠️ Git repository bozuk veya geçersiz")
                except:
                    self.git_repo_exists = False
                    self.log_message("⚠️ Git repository erişilemez durumda")
            
            # Repository durumu etiketini güncelle (eğer varsa)
            if hasattr(self, 'repo_status_label'):
                try:
                    if self.repo_status_label.winfo_exists():
                        if self.git_repo_exists:
                            self.repo_status_label.config(text="✅ Git repository mevcut", foreground="green")
                        else:
                            self.repo_status_label.config(text="❌ Git repository bulunamadı", foreground="red")
                except tk.TclError:
                    pass  # Widget referans hatası durumunda sessizce devam et
            
            # Yayın butonu durumunu güncelle
            if self.git_repo_exists:
                # Eğer repository zaten mevcutsa yayın butonunu aktif hale getir
                if hasattr(self, 'main_button'):
                    try:
                        if self.main_button.winfo_exists():
                            self.root.after(0, lambda: self.main_button.config(state="normal"))
                    except tk.TclError:
                        pass  # Widget referans hatası durumunda sessizce devam et
                        
                self.log_message("✅ Repository mevcut - Yayınlama aktif")
            else:
                # Repository yoksa yayın butonunu devre dışı bırak
                if hasattr(self, 'main_button'):
                    try:
                        if self.main_button.winfo_exists():
                            self.root.after(0, lambda: self.main_button.config(state="disabled"))
                    except tk.TclError:
                        pass  # Widget referans hatası durumunda sessizce devam et
                        
                self.log_message("❌ Repository bulunamadı - Yayınlama devre dışı")
            
            # README adımındaki repository durumunu güncelle (eğer varsa)
            if hasattr(self, 'update_readme_repo_status'):
                try:
                    self.update_readme_repo_status()
                except Exception as e:
                    # Hata durumunda sadece log'a yaz, uygulamayı durdurma
                    self.log_message(f"⚠️ README repository durumu güncellenirken hata: {e}")
                    
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
            
            # Repository durumunu kontrol et
            self.check_repository_status()
            
            # Git durumunu yeni klasör için güncelle
            self.check_git_status()
            
            # UI'ı repository durumuna göre güncelle
            self.refresh_ui_after_folder_change()
            
            # README adımındaki repository durumunu güncelle (eğer o adımdaysak)
            if hasattr(self, 'update_readme_repo_status'):
                try:
                    self.update_readme_repo_status()
                except Exception as e:
                    # Hata durumunda sadece log'a yaz, uygulamayı durdurma
                    self.log_message(f"⚠️ README repository durumu güncellenirken hata: {e}")
            
            # Klasördeki dosyaları listele
            self.list_folder_contents()

    def check_repository_status(self):
        """Repository durumunu kontrol et ve log'a yaz"""
        try:
            if not self.current_directory:
                return
                
            git_dir = os.path.join(self.current_directory, ".git")
            if os.path.exists(git_dir):
                # Git repository mevcut
                self.log_message("🔍 Repository durumu kontrol ediliyor...")
                
                # Git status kontrol et
                try:
                    result = subprocess.run("git status --porcelain", shell=True, 
                                          capture_output=True, text=True, cwd=self.current_directory, timeout=10)
                    if result.returncode == 0:
                        if result.stdout.strip():
                            self.log_message("📝 Repository'de değişiklikler mevcut")
                        else:
                            self.log_message("✅ Repository temiz (değişiklik yok)")
                    else:
                        self.log_message("⚠️ Git status kontrol edilemedi")
                except Exception as e:
                    self.log_message(f"⚠️ Git status hatası: {e}")
                
                # Remote origin kontrol et
                try:
                    result = subprocess.run("git remote -v", shell=True, 
                                          capture_output=True, text=True, cwd=self.current_directory, timeout=10)
                    if result.returncode == 0 and result.stdout.strip():
                        self.log_message("🔗 Remote origin bağlı")
                    else:
                        self.log_message("⚠️ Remote origin bulunamadı")
                except Exception as e:
                    self.log_message(f"⚠️ Remote kontrol hatası: {e}")
                
                # Branch bilgisi
                try:
                    result = subprocess.run("git branch --show-current", shell=True, 
                                          capture_output=True, text=True, cwd=self.current_directory, timeout=10)
                    if result.returncode == 0:
                        current_branch = result.stdout.strip()
                        self.log_message(f"🌿 Aktif branch: {current_branch}")
                    else:
                        self.log_message("⚠️ Aktif branch bilgisi alınamadı")
                except Exception as e:
                    self.log_message(f"⚠️ Branch kontrol hatası: {e}")
                    
            else:
                # Git repository yok
                self.log_message("❌ Bu klasörde Git repository bulunamadı")
                self.log_message("💡 Repository bağlamak için 'Repository Bağla' butonunu kullanın")
                
        except Exception as e:
            self.log_message(f"⚠️ Repository durumu kontrol edilirken hata: {e}")

    def refresh_ui_after_repo_check(self):
        """Repository kontrolünden sonra UI'ı güncelle"""
        try:
            if not self.current_directory:
                return
                
            git_dir = os.path.join(self.current_directory, ".git")
            repo_exists = os.path.exists(git_dir)
            
            if repo_exists:
                self.log_message("🔄 Repository mevcut - UI güncelleniyor...")
                
                # Repository bilgilerini al
                try:
                    # Aktif branch
                    result = subprocess.run("git branch --show-current", shell=True, 
                                          capture_output=True, text=True, cwd=self.current_directory, timeout=10)
                    current_branch = result.stdout.strip() if result.returncode == 0 else "main"
                    
                    # Remote origin
                    result = subprocess.run("git remote get-url origin", shell=True, 
                                          capture_output=True, text=True, cwd=self.current_directory, timeout=10)
                    remote_url = result.stdout.strip() if result.returncode == 0 else "Bilinmiyor"
                    
                    # Commit sayısı
                    result = subprocess.run("git rev-list --count HEAD", shell=True, 
                                          capture_output=True, text=True, cwd=self.current_directory, timeout=10)
                    commit_count = result.stdout.strip() if result.returncode == 0 else "0"
                    
                    self.log_message(f"📊 Repository Bilgileri:")
                    self.log_message(f"  🌿 Aktif Branch: {current_branch}")
                    self.log_message(f"  🔗 Remote: {remote_url}")
                    self.log_message(f"  💾 Commit Sayısı: {commit_count}")
                    
                except Exception as e:
                    self.log_message(f"⚠️ Repository bilgileri alınamadı: {e}")
                
                # UI güncellemeleri
                self.log_message("✅ UI güncellemeleri tamamlandı")
                
            else:
                self.log_message("🆕 Repository bulunamadı - Yeni repository oluşturulabilir")
                self.log_message("💡 Repository bağlamak için README adımında 'Repository Bağla' butonunu kullanın")
                
        except Exception as e:
            self.log_message(f"⚠️ UI güncellenirken hata: {e}")

    def refresh_ui_after_folder_change(self):
        """Klasör değişikliği sonrası UI'ı güncelle"""
        try:
            self.log_message("🔄 Klasör değişikliği - UI güncelleniyor...")
            
            # Repository durumunu kontrol et
            git_dir = os.path.join(self.current_directory, ".git")
            repo_exists = os.path.exists(git_dir) and os.path.isdir(git_dir)
            
            # Repository sağlığını kontrol et
            if repo_exists:
                try:
                    result = subprocess.run("git status", shell=True, capture_output=True, 
                                          text=True, cwd=self.current_directory, timeout=5)
                    if result.returncode != 0:
                        repo_exists = False
                        self.log_message("⚠️ Repository bozuk - UI güncelleniyor")
                except:
                    repo_exists = False
                    self.log_message("⚠️ Repository erişilemez - UI güncelleniyor")
            
            # Tüm UI bileşenlerini güncelle
            if repo_exists:
                self.log_message("✅ Repository mevcut - Tüm UI bileşenleri güncelleniyor")
                
                # Yayın butonunu aktif hale getir
                if hasattr(self, 'main_button'):
                    try:
                        if self.main_button.winfo_exists():
                            self.main_button.config(state="normal")
                    except tk.TclError:
                        pass
                
                # README durumunu güncelle
                self.update_readme_repo_status()
                
            else:
                self.log_message("❌ Repository bulunamadı - UI devre dışı bırakılıyor")
                
                # Yayın butonunu devre dışı bırak
                if hasattr(self, 'main_button'):
                    try:
                        if self.main_button.winfo_exists():
                            self.main_button.config(state="disabled")
                    except tk.TclError:
                        pass
                
                # README durumunu güncelle
                self.update_readme_repo_status()
            
            self.log_message("✅ UI güncelleme tamamlandı")
            
        except Exception as e:
            self.log_message(f"⚠️ UI güncelleme hatası: {e}")

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
            
            # README adımındaki butonu devre dışı bırak (eğer varsa)
            if hasattr(self, 'connect_button_readme'):
                try:
                    if self.connect_button_readme.winfo_exists():
                        self.connect_button_readme.config(state='disabled')
                except tk.TclError:
                    pass  # Widget referans hatası durumunda sessizce devam et
            
            # Yayın butonunu devre dışı bırak (eğer varsa)
            if hasattr(self, 'main_button'):
                try:
                    if self.main_button.winfo_exists():
                        self.main_button.config(state='disabled')
                except tk.TclError:
                    pass  # Widget referans hatası durumunda sessizce devam et
            
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
            
            # 3. Büyük dosyaları kontrol et ve filtrele
            self.log_message("🔍 Büyük dosyalar kontrol ediliyor...")
            self.detect_and_filter_large_files()
            
            # 4. Önce tüm dosyaları cache'den kaldır ve temizle
            self.log_message("🧹 Git cache temizleniyor...")
            try:
                # Tüm dosyaları cache'den kaldır
                subprocess.run("git rm -r --cached .", shell=True, capture_output=True, text=True, timeout=30)
                self.log_message("✅ Git cache temizlendi")
                
                # .gitignore'ı güncelle
                self.update_gitignore_for_large_files()
                
                # Sadece gerekli dosyaları ekle (node_modules hariç)
                self.log_message("📁 Sadece gerekli dosyalar ekleniyor...")
                
                # Önce .gitignore'ı ekle
                subprocess.run("git add .gitignore", shell=True, capture_output=True, text=True, timeout=10)
                
                # Sonra diğer dosyaları ekle (node_modules hariç)
                result = subprocess.run("git add .", shell=True, capture_output=True, text=True, timeout=60)
            except Exception as e:
                self.log_message(f"⚠️ Cache temizliği sırasında hata: {e}")
                # Normal git add yap
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
            self.log_message("⏳ Bu işlem büyük projelerde biraz zaman alabilir...")
            result = subprocess.run(f"git push -u origin {target_branch}", shell=True, capture_output=True, text=True, timeout=120)
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
            
            # Yayın butonunu aktif hale getir
            self.root.after(0, lambda: self.main_button.config(state="normal"))
             
            # README adımındaki repository durumunu güncelle
            self.root.after(0, self.update_readme_repo_status)
            
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
        # README adımındaki butonu aktif hale getir (eğer varsa)
        if hasattr(self, 'connect_button_readme'):
            try:
                if self.connect_button_readme.winfo_exists():
                    self.connect_button_readme.config(state='normal')
            except tk.TclError:
                pass  # Widget referans hatası durumunda sessizce devam et
        
        # Repository bağlandıktan sonra yayın butonunu aktif hale getir
        if hasattr(self, 'main_button'):
            try:
                if self.main_button.winfo_exists():
                    self.main_button.config(state='normal')
            except tk.TclError:
                pass  # Widget referans hatası durumunda sessizce devam et
        
        self.progress.stop()
        self.check_git_status()

    def refresh_branches(self):
        """Gerçek branch'leri listele ve combo box'ı güncelle"""
        try:
            # branch_combo henüz oluşturulmamışsa bekle
            if not hasattr(self, 'branch_combo'):
                return
                
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
                        f.write("# Dependencies\n")
                        f.write("node_modules/\n")
                        f.write("npm-debug.log*\n")
                        f.write("yarn-debug.log*\n")
                        f.write("yarn-error.log*\n")
                        f.write("package-lock.json\n")
                        f.write("yarn.lock\n")
                        f.write("\n# Build outputs\n")
                        f.write("build/\n")
                        f.write("dist/\n")
                        f.write("out/\n")
                        f.write("target/\n")
                        f.write("*.exe\n")
                        f.write("*.msi\n")
                        f.write("*.dmg\n")
                        f.write("*.app\n")
                        f.write("\n# Large files\n")
                        f.write("*.zip\n")
                        f.write("*.tar.gz\n")
                        f.write("*.rar\n")
                        f.write("*.7z\n")
                        f.write("*.iso\n")
                        f.write("*.dmg\n")
                        f.write("*.pkg\n")
                        f.write("\n# Python\n")
                        f.write("__pycache__/\n")
                        f.write("*.pyc\n")
                        f.write("*.pyo\n")
                        f.write("*.pyd\n")
                        f.write("*.so\n")
                        f.write("\n# IDE\n")
                        f.write(".vscode/\n")
                        f.write(".idea/\n")
                        f.write("*.swp\n")
                        f.write("*.swo\n")
                        f.write("\n# Logs\n")
                        f.write("*.log\n")
                        f.write("logs/\n")
                        f.write("*.pid\n")
                        f.write("*.seed\n")
                        f.write("\n# OS\n")
                        f.write(".DS_Store\n")
                        f.write("Thumbs.db\n")
                        f.write("desktop.ini\n")
                        f.write("\n# Cache\n")
                        f.write(".cache/\n")
                        f.write("*.cache\n")
                        f.write("tmp/\n")
                        f.write("temp/\n")
                
                # Büyük dosyaları tespit et ve filtrele
                self.log_message("🔍 Büyük dosyalar tespit ediliyor...")
                self.detect_and_filter_large_files()
                
                # Gereksiz dosyaları kaldır
                self.log_message("📁 Gereksiz dosyalar kaldırılıyor...")
                
                # Önce büyük dosyaları Git cache'inden kaldır
                self.log_message("🗑️ Büyük dosyalar Git cache'inden kaldırılıyor...")
                self.remove_large_files_from_git()
                
                # Tüm dosyaları cache'den kaldır
                subprocess.run("git rm -r --cached .", shell=True, capture_output=True, text=True, timeout=30)
                
                # .gitignore'ı güncelle ve tekrar ekle
                subprocess.run("git add .gitignore", shell=True, capture_output=True, text=True, timeout=10)
                
                # Temizlenmiş dosyaları ekle
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

    def detect_and_filter_large_files(self):
        """Büyük dosyaları tespit et ve .gitignore'a ekle"""
        try:
            self.log_message("🔍 Büyük dosyalar taranıyor...")
            gitignore_path = os.path.join(self.current_directory, ".gitignore")
            
            # .gitignore yoksa oluştur
            if not os.path.exists(gitignore_path):
                with open(gitignore_path, "w", encoding="utf-8") as f:
                    f.write("# GitAuto tarafından oluşturuldu\n")
            
            # Önce node_modules klasörünü tamamen yoksay
            node_modules_path = os.path.join(self.current_directory, "node_modules")
            if os.path.exists(node_modules_path):
                self.log_message("🚫 node_modules klasörü tespit edildi - tamamen yoksayılıyor")
                
                # .gitignore'a node_modules ekle
                with open(gitignore_path, "a", encoding="utf-8") as f:
                    f.write("\n# Node.js dependencies - COMPLETELY IGNORED\n")
                    f.write("node_modules/\n")
                    f.write("node_modules/**\n")
                    f.write("**/node_modules/\n")
                    f.write("**/node_modules/**\n")
                
                # Git cache'den de kaldır
                try:
                    subprocess.run("git rm -r --cached node_modules", shell=True, 
                                 capture_output=True, text=True, cwd=self.current_directory, timeout=30)
                    self.log_message("✅ node_modules Git cache'den kaldırıldı")
                except:
                    pass
            
            large_file_threshold = 50 * 1024 * 1024  # 50MB
            large_files = []
            
            # Proje klasöründeki tüm dosyaları tara
            for root, dirs, files in os.walk(self.current_directory):
                # .git ve node_modules klasörlerini atla
                if '.git' in dirs:
                    dirs.remove('.git')
                if 'node_modules' in dirs:
                    dirs.remove('node_modules')
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        if file_size > large_file_threshold:
                            # Dosya yolını proje klasörüne göre relatif yap
                            rel_path = os.path.relpath(file_path, self.current_directory)
                            large_files.append((rel_path, file_size))
                    except (OSError, PermissionError):
                        continue
            
            if large_files:
                self.log_message(f"🚨 {len(large_files)} büyük dosya tespit edildi:")
                for file_path, file_size in sorted(large_files, key=lambda x: x[1], reverse=True):
                    size_mb = file_size / (1024 * 1024)
                    self.log_message(f"  📁 {file_path} ({size_mb:.1f} MB)")
                
                # .gitignore dosyasını güncelle
                if os.path.exists(gitignore_path):
                    with open(gitignore_path, "a", encoding="utf-8") as f:
                        f.write("\n# Large files detected by GitAuto\n")
                        for file_path, _ in large_files:
                            # Dosya yolını .gitignore formatına çevir
                            if os.path.sep == '\\':  # Windows
                                file_path = file_path.replace('\\', '/')
                            f.write(f"{file_path}\n")
                    
                    self.log_message("✅ .gitignore dosyası büyük dosyalarla güncellendi")
                else:
                    self.log_message("⚠️ .gitignore dosyası bulunamadı, büyük dosyalar eklenebilir")
            else:
                self.log_message("✅ Büyük dosya tespit edilmedi")
                
        except Exception as e:
            self.log_message(f"⚠️ Büyük dosya tespiti sırasında hata: {e}")

    def remove_large_files_from_git(self):
        """Git cache'inden büyük dosyaları kaldır"""
        try:
            # Git cache'deki büyük dosyaları bul
            self.log_message("🔍 Git cache'deki büyük dosyalar aranıyor...")
            
            # Git ls-files ile cache'deki dosyaları listele
            result = subprocess.run("git ls-files", shell=True, capture_output=True, 
                                  text=True, cwd=self.current_directory, timeout=30)
            
            if result.returncode != 0:
                self.log_message("⚠️ Git cache listesi alınamadı")
                return
            
            large_files_in_git = []
            large_file_threshold = 50 * 1024 * 1024  # 50MB
            
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                
                file_path = os.path.join(self.current_directory, line)
                if os.path.exists(file_path):
                    try:
                        file_size = os.path.getsize(file_path)
                        if file_size > large_file_threshold:
                            large_files_in_git.append((line, file_size))
                    except (OSError, PermissionError):
                        continue
            
            if large_files_in_git:
                self.log_message(f"🚨 Git cache'de {len(large_files_in_git)} büyük dosya bulundu:")
                
                for file_path, file_size in sorted(large_files_in_git, key=lambda x: x[1], reverse=True):
                    size_mb = file_size / (1024 * 1024)
                    self.log_message(f"  📁 {file_path} ({size_mb:.1f} MB)")
                    
                    # Büyük dosyayı Git cache'inden kaldır
                    try:
                        subprocess.run(f'git rm --cached "{file_path}"', shell=True, 
                                     capture_output=True, text=True, cwd=self.current_directory, timeout=10)
                        self.log_message(f"  ✅ {file_path} Git cache'den kaldırıldı")
                    except Exception as e:
                        self.log_message(f"  ❌ {file_path} kaldırılamadı: {e}")
                
                # .gitignore'a ekle
                gitignore_path = os.path.join(self.current_directory, ".gitignore")
                if os.path.exists(gitignore_path):
                    with open(gitignore_path, "a", encoding="utf-8") as f:
                        f.write("\n# Large files removed from Git cache\n")
                        for file_path, _ in large_files_in_git:
                            # Dosya yolını .gitignore formatına çevir
                            if os.path.sep == '\\':  # Windows
                                file_path = file_path.replace('\\', '/')
                            f.write(f"{file_path}\n")
                    
                    self.log_message("✅ .gitignore dosyası güncellendi")
                
                # Özel olarak node_modules klasörünü kaldır
                if any('node_modules' in file_path for file_path, _ in large_files_in_git):
                    self.log_message("🚫 node_modules klasörü Git cache'den kaldırılıyor...")
                    try:
                        # Önce tüm node_modules dosyalarını tek tek kaldır
                        subprocess.run("git rm -r --cached node_modules", shell=True, 
                                     capture_output=True, text=True, cwd=self.current_directory, timeout=30)
                        
                        # Git history'den de temizle (daha agresif)
                        subprocess.run("git filter-branch --force --index-filter 'git rm -r --cached --ignore-unmatch node_modules' --prune-empty --tag-name-filter cat -- --all", 
                                     shell=True, capture_output=True, text=True, cwd=self.current_directory, timeout=60)
                        
                        # Git garbage collection yap
                        subprocess.run("git gc --prune=now", shell=True, 
                                     capture_output=True, text=True, cwd=self.current_directory, timeout=30)
                        
                        self.log_message("✅ node_modules klasörü Git history'den tamamen temizlendi")
                    except Exception as e:
                        self.log_message(f"⚠️ node_modules temizlenemedi: {e}")
                        
                        # Alternatif yöntem: Force clean
                        self.log_message("🔄 Alternatif temizlik yöntemi deneniyor...")
                        try:
                            subprocess.run("git clean -fdx", shell=True, 
                                         capture_output=True, text=True, cwd=self.current_directory, timeout=30)
                            subprocess.run("git reset --hard HEAD", shell=True, 
                                         capture_output=True, text=True, cwd=self.current_directory, timeout=30)
                            self.log_message("✅ Alternatif temizlik tamamlandı")
                        except Exception as e2:
                            self.log_message(f"❌ Alternatif temizlik de başarısız: {e2}")
                            
                            # Son çare: Repository'yi tamamen yeniden başlat
                            self.log_message("🚨 Son çare: Repository tamamen yeniden başlatılıyor...")
                            try:
                                # .git klasörünü yedekle
                                git_backup = os.path.join(self.current_directory, ".git_backup")
                                if os.path.exists(os.path.join(self.current_directory, ".git")):
                                    import shutil
                                    shutil.move(os.path.join(self.current_directory, ".git"), git_backup)
                                    self.log_message("✅ .git klasörü yedeklendi")
                                
                                # Yeni repository başlat
                                subprocess.run("git init", shell=True, 
                                             capture_output=True, text=True, cwd=self.current_directory, timeout=10)
                                
                                # .gitignore'ı güncelle
                                self.update_gitignore_for_large_files()
                                
                                self.log_message("✅ Repository yeniden başlatıldı")
                                self.log_message("💡 Artık büyük dosyalar olmadan commit yapabilirsiniz")
                                
                            except Exception as e3:
                                self.log_message(f"❌ Repository yeniden başlatılamadı: {e3}")
                                # Yedekten geri yükle
                                if os.path.exists(git_backup):
                                    import shutil
                                    shutil.move(git_backup, os.path.join(self.current_directory, ".git"))
                                    self.log_message("✅ .git klasörü yedekten geri yüklendi")
            else:
                self.log_message("✅ Git cache'de büyük dosya bulunamadı")
                
        except Exception as e:
            self.log_message(f"⚠️ Git cache temizliği sırasında hata: {e}")

    def update_gitignore_for_large_files(self):
        """Büyük dosyalar için kapsamlı .gitignore oluştur"""
        try:
            gitignore_path = os.path.join(self.current_directory, ".gitignore")
            
            # Kapsamlı .gitignore içeriği
            gitignore_content = """# GitAuto tarafından oluşturuldu - Büyük dosyalar için optimize edildi

# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json
yarn.lock
pnpm-lock.yaml

# Build outputs
build/
dist/
out/
target/
*.exe
*.msi
*.dmg
*.app
*.deb
*.rpm
*.pkg

# Large files
*.zip
*.tar.gz
*.rar
*.7z
*.iso
*.dmg
*.pkg
*.bin
*.dat
*.db
*.sqlite
*.sqlite3

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.so
*.egg
*.egg-info/
*.whl

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/
*.pid
*.seed
*.out

# OS
.DS_Store
Thumbs.db
desktop.ini
*.tmp
*.temp

# Cache
.cache/
*.cache
tmp/
temp/
.tmp/

# Electron specific
node_modules/electron/
node_modules/electron-builder/
node_modules/electron-packager/

# Large media files
*.mp4
*.avi
*.mov
*.wmv
*.flv
*.mkv
*.webm
*.mp3
*.wav
*.flac
*.aac
*.ogg

# Archives
*.zip
*.tar
*.gz
*.bz2
*.xz
*.rar
*.7z
*.lzma
*.lz4

# Database files
*.db
*.sqlite
*.sqlite3
*.mdb
*.accdb

# Virtual environments
venv/
env/
.venv/
.env/
ENV/

# Backup files
*.bak
*.backup
*.old
*.orig
*.save
"""
            
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write(gitignore_content)
            
            self.log_message("✅ Kapsamlı .gitignore dosyası oluşturuldu")
            
        except Exception as e:
            self.log_message(f"⚠️ .gitignore oluşturulurken hata: {e}")

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
        """Repository yayınlama işlemini başlat - Sadece boş commit"""
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
        
        # Repository varlığını kontrol et
        if not os.path.exists(os.path.join(self.current_directory, ".git")):
            messagebox.showerror("Hata", "Git repository bulunamadı!\nÖnce README adımında 'Repository Bağla' butonunu kullanın.")
            return
        
        # Onay al - Boş commit için
        project_name = self.project_name.get().strip()
        github_username = self.github_username.get().strip()
        commit_message = self.commit_message.get().strip() or "Empty commit for repository setup"
        target_branch = self.selected_branch.get()
        
        confirm_text = f"""📋 Boş Commit Yayınlama:

📁 Proje: {project_name}
👤 GitHub: {github_username}
💬 Commit: {commit_message}
🌿 Branch: {target_branch}

⚠️ Bu işlem sadece boş commit atacak.
🚀 Dosya yayınlama son adımda yapılacak.

✅ Devam edilsin mi?"""
        
        if not messagebox.askyesno("Onay", confirm_text):
            return
        
        # İşlemi başlat
        self.main_button.config(state="disabled")
        self.progress.start()
        
        # Thread'de çalıştır
        threading.Thread(target=self.publish_repository, daemon=True).start()

    def publish_repository(self):
        """Sadece boş commit at - Dosya yayınlama son adımda"""
        try:
            project_name = self.project_name.get().strip()
            github_username = self.github_username.get().strip()
            commit_message = self.commit_message.get().strip() or "Empty commit for repository setup"
            target_branch = self.selected_branch.get() or "main"
            
            repo_url = f"https://github.com/{github_username}/{project_name}.git"
            
            self.log_message("🚀 Boş commit yayınlama başlatılıyor...")
            
            # Git repository kontrolü
            git_dir = os.path.join(self.current_directory, ".git")
            if not os.path.exists(git_dir):
                self.log_message("❌ Git repository bulunamadı! Önce 'Repository Bağla' kullanın.")
                raise Exception("Git repository bulunamadı! Önce 'Repository Bağla' kullanın.")
            
            # Git konfigürasyonunu kontrol et
            self.log_message("⚙️ Git konfigürasyonu kontrol ediliyor...")
            
            user_result = subprocess.run("git config user.name", shell=True, capture_output=True, 
                                       text=True, cwd=self.current_directory, timeout=5)
            if user_result.returncode != 0 or not user_result.stdout.strip():
                subprocess.run(f'git config user.name "{github_username}"', shell=True, 
                             capture_output=True, text=True, cwd=self.current_directory, timeout=5)
                self.log_message("👤 Git user.name ayarlandı")
            
            email_result = subprocess.run("git config user.email", shell=True, capture_output=True, 
                                        text=True, cwd=self.current_directory, timeout=5)
            if email_result.returncode != 0 or not email_result.stdout.strip():
                subprocess.run(f'git config user.email "{github_username}@users.noreply.github.com"', 
                             shell=True, capture_output=True, text=True, cwd=self.current_directory, timeout=5)
                self.log_message("📧 Git user.email ayarlandı")
            
            # Boş commit at
            self.log_message(f"💾 Boş commit atılıyor: {commit_message}")
            result = subprocess.run(f'git commit --allow-empty -m "{commit_message}"', shell=True, 
                                 capture_output=True, text=True, cwd=self.current_directory, timeout=10)
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else "Bilinmeyen commit hatası"
                self.log_message(f"⚠️ Boş commit hatası: {error_msg}")
                raise Exception(f"Boş commit hatası: {error_msg}")
            
            self.log_message("✅ Boş commit başarıyla atıldı")
            
            # Push işlemi
            self.log_message(f"🚀 '{target_branch}' branch'i GitHub'a push ediliyor...")
            result = subprocess.run(f"git push origin {target_branch}", shell=True, capture_output=True, 
                                 text=True, cwd=self.current_directory, timeout=60)
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else "Bilinmeyen push hatası"
                self.log_message(f"⚠️ Push hatası: {error_msg}")
                raise Exception(f"Push hatası: {error_msg}")
            
            self.log_message("✅ Boş commit GitHub'a başarıyla push edildi!")
            self.log_message("🎉 Repository hazırlandı - Son adımda dosyalar yayınlanacak")
            
            # Başarı mesajı göster
            self.root.after(0, lambda: messagebox.showinfo(
                "Başarılı! 🎉",
                f"✅ Boş commit başarıyla yayınlandı!\n\n"
                f"📍 Repository: {repo_url}\n"
                f"🌿 Branch: {target_branch}\n"
                f"💬 Commit: {commit_message}\n\n"
                "🚀 Son adımda tüm dosyalar yayınlanacak!"
            ))
            
        except Exception as e:
            self.log_message(f"❌ Boş commit yayınlama hatası: {e}")
            self.root.after(0, lambda: messagebox.showerror("Hata", f"Boş commit yayınlama hatası:\n{e}"))
        
        finally:
            # UI'ı güncelle
            self.root.after(0, self.publication_finished)

    def publication_finished(self):
        """Yayınlama işlemi tamamlandı"""
        # Yayınlama tamamlandıktan sonra butonları güncelle
        if hasattr(self, 'main_button'):
            try:
                if self.main_button.winfo_exists():
                    self.main_button.config(state="normal")
            except tk.TclError:
                pass  # Widget referans hatası durumunda sessizce devam et
        
        # README adımındaki butonu da güncelle (eğer varsa)
        if hasattr(self, 'connect_button_readme'):
            try:
                if self.connect_button_readme.winfo_exists():
                    self.connect_button_readme.config(state="normal")
            except tk.TclError:
                pass  # Widget referans hatası durumunda sessizce devam et
        
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
                    # Git, sistem ve gereksiz dosyaları gizle
                    if not file.startswith('.') and file not in ['__pycache__', 'node_modules', 'build', 'dist', 'out', 'target']:
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

    def publication_finished(self):
        """Yayınlama işlemi tamamlandı"""
        # Yayınlama tamamlandıktan sonra butonları güncelle
        if hasattr(self, 'main_button'):
            try:
                if self.main_button.winfo_exists():
                    self.main_button.config(state="normal")
            except tk.TclError:
                pass  # Widget referans hatası durumunda sessizce devam et
        
        # README adımındaki butonu da güncelle (eğer varsa)
        if hasattr(self, 'connect_button_readme'):
            try:
                if self.connect_button_readme.winfo_exists():
                    self.connect_button_readme.config(state="normal")
            except tk.TclError:
                pass  # Widget referans hatası durumunda sessizce devam et
        
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
                    # Git, sistem ve gereksiz dosyaları gizle
                    if not file.startswith('.') and file not in ['__pycache__', 'node_modules', 'build', 'dist', 'out', 'target']:
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

