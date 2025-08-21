#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitAuto - Otomatik Git Repository Yayınlama Uygulaması
Proje dosyalarını otomatik olarak GitHub'a yayınlar
"""

import os
import subprocess
import sys
from pathlib import Path

class GitAuto:
    def __init__(self):
        self.current_dir = os.getcwd()
        
    def run_command(self, command, check=True):
        """Komut çalıştır ve sonucu döndür"""
        try:
            print(f"🔄 Çalıştırılıyor: {command}")
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=self.current_dir,
                encoding='utf-8'
            )
            
            if result.stdout:
                print(f"✅ Çıktı: {result.stdout.strip()}")
            
            if result.stderr and result.returncode != 0:
                print(f"❌ Hata: {result.stderr.strip()}")
                if check:
                    raise subprocess.CalledProcessError(result.returncode, command)
            
            return result
        except Exception as e:
            print(f"❌ Komut çalıştırma hatası: {e}")
            if check:
                raise

    def get_user_input(self):
        """Kullanıcıdan gerekli bilgileri al"""
        print("=" * 50)
        print("🚀 GitAuto - Otomatik Git Repository Yayınlama")
        print("=" * 50)
        
        # Proje adını al
        project_name = input("📁 Proje adını girin: ").strip()
        if not project_name:
            print("❌ Proje adı boş olamaz!")
            sys.exit(1)
            
        # GitHub kullanıcı adını al
        github_username = input("👤 GitHub kullanıcı adınızı girin: ").strip()
        if not github_username:
            print("❌ GitHub kullanıcı adı boş olamaz!")
            sys.exit(1)
            
        # Repository URL'sini oluştur
        repo_url = f"https://github.com/{github_username}/{project_name}.git"
        
        # Commit mesajını al
        commit_message = input("💬 Commit mesajı (varsayılan: 'first commit'): ").strip()
        if not commit_message:
            commit_message = "first commit"
            
        return project_name, github_username, repo_url, commit_message

    def check_git_installed(self):
        """Git'in yüklü olup olmadığını kontrol et"""
        try:
            result = self.run_command("git --version", check=False)
            if result.returncode == 0:
                print("✅ Git kurulu ve hazır")
                return True
            else:
                print("❌ Git kurulu değil!")
                return False
        except:
            print("❌ Git kurulu değil!")
            return False

    def list_branches(self):
        """Mevcut branch'leri listele"""
        try:
            result = self.run_command("git branch -a", check=False)
            if result.returncode == 0 and result.stdout:
                print("\n🌿 Mevcut Branch'ler:")
                print("-" * 30)
                branches = result.stdout.strip().split('\n')
                for branch in branches:
                    if branch.strip():
                        if branch.startswith('*'):
                            print(f"  🌟 {branch.strip()} (aktif)")
                        else:
                            print(f"     {branch.strip()}")
                return branches
            else:
                print("ℹ️  Henüz branch bulunamadı")
                return []
        except Exception as e:
            print(f"❌ Branch listeleme hatası: {e}")
            return []

    def get_current_branch(self):
        """Aktif branch'i al"""
        try:
            result = self.run_command("git branch --show-current", check=False)
            if result.returncode == 0 and result.stdout:
                return result.stdout.strip()
            else:
                return "main"
        except:
            return "main"

    def create_new_branch(self, branch_name):
        """Yeni branch oluştur"""
        try:
            print(f"🌱 Yeni branch oluşturuluyor: {branch_name}")
            self.run_command(f"git checkout -b {branch_name}")
            print(f"✅ Branch '{branch_name}' oluşturuldu ve aktif edildi")
            return True
        except Exception as e:
            print(f"❌ Branch oluşturma hatası: {e}")
            return False

    def switch_branch(self, branch_name):
        """Branch değiştir"""
        try:
            print(f"🔄 Branch değiştiriliyor: {branch_name}")
            self.run_command(f"git checkout {branch_name}")
            print(f"✅ Branch '{branch_name}' aktif edildi")
            return True
        except Exception as e:
            print(f"❌ Branch değiştirme hatası: {e}")
            return False

    def branch_management_menu(self):
        """Branch yönetimi menüsü"""
        print("\n" + "=" * 50)
        print("🌿 BRANCH YÖNETİMİ")
        print("=" * 50)
        
        while True:
            print("\n📋 Seçenekler:")
            print("1. 📋 Mevcut branch'leri listele")
            print("2. 🌱 Yeni branch oluştur")
            print("3. 🔄 Branch değiştir")
            print("4. ✅ Devam et (mevcut branch ile)")
            print("5. ❌ Çıkış")
            
            choice = input("\n🎯 Seçiminizi yapın (1-5): ").strip()
            
            if choice == "1":
                self.list_branches()
                
            elif choice == "2":
                branch_name = input("🌱 Yeni branch adını girin: ").strip()
                if branch_name:
                    if self.create_new_branch(branch_name):
                        print(f"✅ Branch '{branch_name}' başarıyla oluşturuldu!")
                    else:
                        print("❌ Branch oluşturulamadı!")
                else:
                    print("❌ Branch adı boş olamaz!")
                    
            elif choice == "3":
                self.list_branches()
                branch_name = input("🔄 Hangi branch'e geçmek istiyorsunuz? ").strip()
                if branch_name:
                    # Branch adından * işaretini temizle
                    clean_branch = branch_name.replace('*', '').strip()
                    if self.switch_branch(clean_branch):
                        print(f"✅ Branch '{clean_branch}' aktif edildi!")
                    else:
                        print("❌ Branch değiştirilemedi!")
                else:
                    print("❌ Branch adı boş olamaz!")
                    
            elif choice == "4":
                current_branch = self.get_current_branch()
                print(f"✅ Mevcut branch '{current_branch}' ile devam ediliyor...")
                return current_branch
                
            elif choice == "5":
                print("❌ İşlem iptal edildi")
                sys.exit(0)
                
            else:
                print("❌ Geçersiz seçim! Lütfen 1-5 arası bir sayı girin.")

    def create_readme(self, project_name):
        """README.md dosyası oluştur"""
        readme_content = f"# {project_name}\n\nBu proje GitAuto ile otomatik olarak oluşturuldu.\n"
        
        try:
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(readme_content)
            print("✅ README.md dosyası oluşturuldu")
        except Exception as e:
            print(f"❌ README.md oluşturma hatası: {e}")
            raise

    def initialize_git(self):
        """Git repository'sini başlat"""
        # Git repository'si zaten varsa uyarı ver
        if os.path.exists(".git"):
            response = input("⚠️  Git repository zaten mevcut. Devam edilsin mi? (e/h): ").lower()
            if response != 'e':
                print("❌ İşlem iptal edildi")
                sys.exit(1)
        else:
            self.run_command("git init")

    def setup_repository(self, project_name, repo_url, commit_message, target_branch):
        """Repository'yi kurulum ve yayınlama"""
        try:
            # README.md oluştur
            self.create_readme(project_name)
            
            # Git başlat
            self.initialize_git()
            
            # Tüm dosyaları ekle
            self.run_command("git add .")
            
            # İlk commit
            self.run_command(f'git commit -m "{commit_message}"')
            
            # Hedef branch'i ayarla (eğer main değilse)
            if target_branch != "main":
                self.run_command(f"git branch -M {target_branch}")
            else:
                self.run_command("git branch -M main")
            
            # Remote origin ekle
            # Önce mevcut origin'i kaldır (varsa)
            self.run_command("git remote remove origin", check=False)
            self.run_command(f"git remote add origin {repo_url}")
            
            # Repository'yi push et
            print(f"🚀 Repository GitHub'a '{target_branch}' branch'i ile yayınlanıyor...")
            self.run_command(f"git push -u origin {target_branch}")
            
            print("\n" + "=" * 50)
            print("🎉 Başarıyla tamamlandı!")
            print(f"📍 Repository URL: {repo_url.replace('.git', '')}")
            print(f"🌿 Yayınlanan Branch: {target_branch}")
            print("=" * 50)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git komutu başarısız: {e}")
            print("💡 GitHub'da repository'nin oluşturulduğundan emin olun!")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
            sys.exit(1)

    def run(self):
        """Ana uygulama çalıştırma fonksiyonu"""
        try:
            # Git kontrolü
            if not self.check_git_installed():
                print("💡 Git'i yüklemek için: https://git-scm.com/downloads")
                sys.exit(1)
            
            # Kullanıcı girdilerini al
            project_name, github_username, repo_url, commit_message = self.get_user_input()
            
            # Branch yönetimi
            target_branch = self.branch_management_menu()
            
            # Onay al
            print(f"\n📋 Özet:")
            print(f"   📁 Proje: {project_name}")
            print(f"   👤 GitHub: {github_username}")
            print(f"   🔗 URL: {repo_url}")
            print(f"   💬 Commit: {commit_message}")
            print(f"   🌿 Branch: {target_branch}")
            
            confirm = input("\n✅ Devam edilsin mi? (e/h): ").lower()
            if confirm != 'e':
                print("❌ İşlem iptal edildi")
                sys.exit(0)
            
            # Repository kurulumu ve yayınlama
            self.setup_repository(project_name, repo_url, commit_message, target_branch)
            
        except KeyboardInterrupt:
            print("\n❌ İşlem kullanıcı tarafından iptal edildi")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Genel hata: {e}")
            sys.exit(1)

if __name__ == "__main__":
    git_auto = GitAuto()
    git_auto.run()
