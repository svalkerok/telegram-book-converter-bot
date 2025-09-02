#!/usr/bin/env python3
"""
🤖 Telegram Book Converter Bot - GUI Manager
Красивый графический интерфейс для управления ботом
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import subprocess
import os
import sys
import json
import time
from pathlib import Path
import asyncio
from dotenv import load_dotenv, set_key

try:
    import requests
except ImportError:
    print("❌ Модуль requests не найден. Установите: pip install requests")
    sys.exit(1)

# Настройка CustomTkinter
ctk.set_appearance_mode("dark")  # Темная тема
ctk.set_default_color_theme("blue")  # Синяя цветовая схема

class BotManagerGUI:
    def __init__(self):
        # Создаем главное окно
        self.root = ctk.CTk()
        self.root.title("🤖 Telegram Book Converter Bot Manager")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Обработчик закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Переменные состояния
        self.bot_process = None
        self.is_bot_running = False
        self.config_file = Path(".env")
        self._closing = False  # Флаг закрытия приложения
        
        # Создаем интерфейс
        self.create_widgets()
        self.load_config()
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        if self._closing:
            return  # Уже в процессе закрытия
            
        self._closing = True
        
        try:
            # Останавливаем бота если запущен
            if self.is_bot_running and self.bot_process:
                self.log("🛑 Остановка бота перед закрытием...")
                self.stop_bot()
            
            # Закрываем окно
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"Ошибка при закрытии: {e}")
            # Принудительно закрываем
            try:
                self.root.destroy()
            except:
                pass
        
    def create_widgets(self):
        """Создает все виджеты интерфейса"""
        
        # Заголовок
        self.title_label = ctk.CTkLabel(
            self.root, 
            text="🤖 Telegram Book Converter Bot",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)
        
        # Основной фрейм
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # === СЕКЦИЯ КОНФИГУРАЦИИ ===
        self.config_frame = ctk.CTkFrame(self.main_frame)
        self.config_frame.pack(fill="x", padx=20, pady=10)
        
        self.config_label = ctk.CTkLabel(
            self.config_frame, 
            text="⚙️ Конфигурация бота",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.config_label.pack(pady=10)
        
        # Поле ввода токена
        self.token_label = ctk.CTkLabel(self.config_frame, text="🔑 Токен бота:")
        self.token_label.pack(anchor="w", padx=20)
        
        self.token_entry = ctk.CTkEntry(
            self.config_frame,
            placeholder_text="Вставьте токен от @BotFather",
            width=400,
            show="*"  # Скрываем токен
        )
        self.token_entry.pack(pady=5, padx=20, fill="x")
        
        # Кнопки управления токеном
        self.token_buttons_frame = ctk.CTkFrame(self.config_frame)
        self.token_buttons_frame.pack(fill="x", padx=20, pady=5)
        
        self.save_token_btn = ctk.CTkButton(
            self.token_buttons_frame,
            text="💾 Сохранить токен",
            command=self.save_token,
            width=150
        )
        self.save_token_btn.pack(side="left", padx=5)
        
        self.show_token_btn = ctk.CTkButton(
            self.token_buttons_frame,
            text="👁️ Показать/Скрыть",
            command=self.toggle_token_visibility,
            width=150
        )
        self.show_token_btn.pack(side="left", padx=5)
        
        self.test_token_btn = ctk.CTkButton(
            self.token_buttons_frame,
            text="🧪 Проверить токен",
            command=self.test_token,
            width=150
        )
        self.test_token_btn.pack(side="left", padx=5)
        
        # === СЕКЦИЯ УПРАВЛЕНИЯ БОТОМ ===
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.pack(fill="x", padx=20, pady=10)
        
        self.control_label = ctk.CTkLabel(
            self.control_frame, 
            text="🎮 Управление ботом",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.control_label.pack(pady=10)
        
        # Статус бота
        self.status_frame = ctk.CTkFrame(self.control_frame)
        self.status_frame.pack(fill="x", padx=20, pady=5)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="📊 Статус: Остановлен",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(side="left", padx=10, pady=10)
        
        self.status_indicator = ctk.CTkLabel(
            self.status_frame,
            text="🔴",
            font=ctk.CTkFont(size=20)
        )
        self.status_indicator.pack(side="right", padx=10, pady=10)
        
        # Кнопки управления
        self.control_buttons_frame = ctk.CTkFrame(self.control_frame)
        self.control_buttons_frame.pack(fill="x", padx=20, pady=10)
        
        self.start_btn = ctk.CTkButton(
            self.control_buttons_frame,
            text="▶️ Запустить бота",
            command=self.start_bot,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.start_btn.pack(side="left", padx=10, pady=5)
        
        self.stop_btn = ctk.CTkButton(
            self.control_buttons_frame,
            text="⏹️ Остановить бота",
            command=self.stop_bot,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=10, pady=5)
        
        self.restart_btn = ctk.CTkButton(
            self.control_buttons_frame,
            text="🔄 Перезапустить",
            command=self.restart_bot,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.restart_btn.pack(side="left", padx=10, pady=5)
        
        # === СЕКЦИЯ ЛОГОВ ===
        self.logs_frame = ctk.CTkFrame(self.main_frame)
        self.logs_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.logs_label = ctk.CTkLabel(
            self.logs_frame, 
            text="📋 Логи бота",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.logs_label.pack(pady=10)
        
        # Текстовое поле для логов
        self.logs_textbox = ctk.CTkTextbox(
            self.logs_frame,
            width=600,
            height=200,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.logs_textbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Кнопки управления логами
        self.logs_buttons_frame = ctk.CTkFrame(self.logs_frame)
        self.logs_buttons_frame.pack(fill="x", padx=20, pady=5)
        
        self.clear_logs_btn = ctk.CTkButton(
            self.logs_buttons_frame,
            text="🗑️ Очистить логи",
            command=self.clear_logs,
            width=150
        )
        self.clear_logs_btn.pack(side="left", padx=5)
        
        self.save_logs_btn = ctk.CTkButton(
            self.logs_buttons_frame,
            text="💾 Сохранить логи",
            command=self.save_logs,
            width=150
        )
        self.save_logs_btn.pack(side="left", padx=5)
        
        # Автопрокрутка логов
        self.auto_scroll_var = ctk.BooleanVar(value=True)
        self.auto_scroll_cb = ctk.CTkCheckBox(
            self.logs_buttons_frame,
            text="📜 Автопрокрутка",
            variable=self.auto_scroll_var
        )
        self.auto_scroll_cb.pack(side="right", padx=5)
        
        # === НИЖНЯЯ ПАНЕЛЬ ===
        self.bottom_frame = ctk.CTkFrame(self.root)
        self.bottom_frame.pack(fill="x", padx=20, pady=10)
        
        self.info_label = ctk.CTkLabel(
            self.bottom_frame,
            text="📚 Telegram Book Converter Bot GUI Manager v1.0",
            font=ctk.CTkFont(size=10)
        )
        self.info_label.pack(side="left", padx=10, pady=5)
        
        self.theme_btn = ctk.CTkButton(
            self.bottom_frame,
            text="🌙 Тема",
            command=self.toggle_theme,
            width=80
        )
        self.theme_btn.pack(side="right", padx=10, pady=5)
        
    def load_config(self):
        """Загружает конфигурацию из .env файла"""
        try:
            if self.config_file.exists():
                load_dotenv(self.config_file)
                bot_token = os.getenv("BOT_TOKEN", "")
                if bot_token:
                    self.token_entry.insert(0, bot_token)
                    self.log("✅ Токен загружен из конфигурации")
                else:
                    self.log("⚠️ Токен не найден в конфигурации")
            else:
                self.log("📝 Файл конфигурации не найден, создается новый")
                self.config_file.touch()
        except Exception as e:
            self.log(f"❌ Ошибка загрузки конфигурации: {e}")
    
    def save_token(self):
        """Сохраняет токен в .env файл"""
        token = self.token_entry.get().strip()
        if not token:
            messagebox.showerror("Ошибка", "Введите токен бота!")
            return
        
        try:
            # Создаем или обновляем .env файл
            set_key(self.config_file, "BOT_TOKEN", token)
            set_key(self.config_file, "PRODUCTION", "0")
            set_key(self.config_file, "LOG_LEVEL", "INFO")
            
            self.log("✅ Токен сохранен в конфигурации")
            messagebox.showinfo("Успех", "Токен успешно сохранен!")
        except Exception as e:
            self.log(f"❌ Ошибка сохранения токена: {e}")
            messagebox.showerror("Ошибка", f"Не удалось сохранить токен: {e}")
    
    def toggle_token_visibility(self):
        """Переключает видимость токена"""
        if self.token_entry.cget("show") == "*":
            self.token_entry.configure(show="")
            self.show_token_btn.configure(text="🙈 Скрыть")
        else:
            self.token_entry.configure(show="*")
            self.show_token_btn.configure(text="👁️ Показать")
    
    def test_token(self):
        """Проверяет валидность токена"""
        if self._closing:
            return  # Не запускаем проверку если приложение закрывается
            
        token = self.token_entry.get().strip()
        if not token:
            messagebox.showerror("Ошибка", "Введите токен бота!")
            return
        
        # Блокируем кнопку во время проверки
        self.test_token_btn.configure(state="disabled", text="⏳ Проверка...")
        self.log("🧪 Проверка токена...")
        
        def check_token():
            if self._closing:
                return  # Прерываем если приложение закрывается
                
            try:
                response = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
                
                if self._closing:
                    return  # Проверяем снова после запроса
                
                result = response.json()
                
                if result.get("ok"):
                    bot_info = result.get("result", {})
                    bot_name = bot_info.get("username", "Unknown")
                    # Безопасное обновление GUI из главного потока
                    if not self._closing:
                        self.root.after(0, lambda: self._on_token_valid(bot_name))
                else:
                    error = result.get("description", "Unknown error")
                    if not self._closing:
                        self.root.after(0, lambda: self._on_token_invalid(error))
            except Exception as e:
                if not self._closing:
                    self.root.after(0, lambda: self._on_token_error(str(e)))
        
        # Запускаем проверку в отдельном потоке
        threading.Thread(target=check_token, daemon=True).start()
    
    def _on_token_valid(self, bot_name):
        """Обработка валидного токена (вызывается в главном потоке)"""
        if self._closing:
            return  # Не обновляем GUI если приложение закрывается
            
        try:
            self.test_token_btn.configure(state="normal", text="🧪 Проверить токен")
            self.log(f"✅ Токен валиден! Бот: @{bot_name}")
            
            # Создаем безопасное диалоговое окно
            def show_success_dialog():
                try:
                    messagebox.showinfo("Успех", f"Токен валиден!\nБот: @{bot_name}")
                except Exception as e:
                    self.log(f"Ошибка показа диалога: {e}")
            
            # Показываем диалог с небольшой задержкой
            self.root.after(100, show_success_dialog)
        except Exception as e:
            self.log(f"Ошибка обработки валидного токена: {e}")
    
    def _on_token_invalid(self, error):
        """Обработка невалидного токена (вызывается в главном потоке)"""
        if self._closing:
            return
            
        try:
            self.test_token_btn.configure(state="normal", text="🧪 Проверить токен")
            self.log(f"❌ Токен невалиден: {error}")
            
            def show_error_dialog():
                try:
                    messagebox.showerror("Ошибка", f"Токен невалиден: {error}")
                except Exception as e:
                    self.log(f"Ошибка показа диалога: {e}")
            
            self.root.after(100, show_error_dialog)
        except Exception as e:
            self.log(f"Ошибка обработки невалидного токена: {e}")
    
    def _on_token_error(self, error):
        """Обработка ошибки проверки токена (вызывается в главном потоке)"""
        if self._closing:
            return
            
        try:
            self.test_token_btn.configure(state="normal", text="🧪 Проверить токен")
            self.log(f"❌ Ошибка проверки токена: {error}")
            
            def show_error_dialog():
                try:
                    messagebox.showerror("Ошибка", f"Ошибка проверки: {error}")
                except Exception as e:
                    self.log(f"Ошибка показа диалога: {e}")
            
            self.root.after(100, show_error_dialog)
        except Exception as e:
            self.log(f"Ошибка обработки ошибки токена: {e}")
    
    def start_bot(self):
        """Запускает бота"""
        if self.is_bot_running:
            self.log("⚠️ Бот уже запущен!")
            return
        
        token = self.token_entry.get().strip()
        if not token:
            messagebox.showerror("Ошибка", "Сначала введите и сохраните токен!")
            return
        
        try:
            self.log("🚀 Запуск бота...")
            
            # Запускаем бота в отдельном процессе
            self.bot_process = subprocess.Popen(
                [sys.executable, "bot.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.is_bot_running = True
            self.update_status("Запущен", "🟢")
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.restart_btn.configure(state="normal")
            
            # Запускаем мониторинг логов
            self.start_log_monitoring()
            
            self.log("✅ Бот успешно запущен!")
            
        except Exception as e:
            self.log(f"❌ Ошибка запуска бота: {e}")
            messagebox.showerror("Ошибка", f"Не удалось запустить бота: {e}")
    
    def stop_bot(self):
        """Останавливает бота"""
        if not self.is_bot_running or not self.bot_process:
            self.log("⚠️ Бот не запущен!")
            return
        
        try:
            self.log("⏹️ Остановка бота...")
            
            # Завершаем процесс
            self.bot_process.terminate()
            self.bot_process.wait(timeout=10)
            
            self.is_bot_running = False
            self.bot_process = None
            
            self.update_status("Остановлен", "🔴")
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.restart_btn.configure(state="disabled")
            
            self.log("✅ Бот остановлен!")
            
        except subprocess.TimeoutExpired:
            # Принудительное завершение
            self.bot_process.kill()
            self.log("⚠️ Бот принудительно завершен!")
        except Exception as e:
            self.log(f"❌ Ошибка остановки бота: {e}")
    
    def restart_bot(self):
        """Перезапускает бота"""
        self.log("🔄 Перезапуск бота...")
        self.stop_bot()
        time.sleep(2)  # Небольшая пауза
        self.start_bot()
    
    def start_log_monitoring(self):
        """Запускает мониторинг логов бота"""
        def monitor_logs():
            try:
                while self.is_bot_running and self.bot_process:
                    line = self.bot_process.stdout.readline()
                    if line:
                        self.log(line.strip())
                    elif self.bot_process.poll() is not None:
                        # Процесс завершился
                        self.log("⚠️ Процесс бота завершился")
                        self.is_bot_running = False
                        self.root.after(0, lambda: self.update_status("Остановлен", "🔴"))
                        self.root.after(0, lambda: self.start_btn.configure(state="normal"))
                        self.root.after(0, lambda: self.stop_btn.configure(state="disabled"))
                        self.root.after(0, lambda: self.restart_btn.configure(state="disabled"))
                        break
            except Exception as e:
                self.log(f"❌ Ошибка мониторинга логов: {e}")
        
        # Запускаем мониторинг в отдельном потоке
        threading.Thread(target=monitor_logs, daemon=True).start()
    
    def update_status(self, status, indicator):
        """Обновляет статус бота"""
        self.status_label.configure(text=f"📊 Статус: {status}")
        self.status_indicator.configure(text=indicator)
    
    def log(self, message):
        """Добавляет сообщение в логи"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.logs_textbox.insert("end", log_message)
        
        # Автопрокрутка
        if self.auto_scroll_var.get():
            self.logs_textbox.see("end")
    
    def clear_logs(self):
        """Очищает логи"""
        self.logs_textbox.delete("1.0", "end")
        self.log("🗑️ Логи очищены")
    
    def save_logs(self):
        """Сохраняет логи в файл"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".log",
                filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                logs_content = self.logs_textbox.get("1.0", "end")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(logs_content)
                self.log(f"💾 Логи сохранены в {filename}")
                messagebox.showinfo("Успех", f"Логи сохранены в {filename}")
        except Exception as e:
            self.log(f"❌ Ошибка сохранения логов: {e}")
            messagebox.showerror("Ошибка", f"Не удалось сохранить логи: {e}")
    
    def toggle_theme(self):
        """Переключает тему оформления"""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="🌞 Тема")
            self.log("🌞 Переключено на светлую тему")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="🌙 Тема")
            self.log("🌙 Переключено на темную тему")
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        if self.is_bot_running:
            if messagebox.askokcancel("Закрытие", "Бот запущен. Остановить его перед закрытием?"):
                self.stop_bot()
                time.sleep(1)
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Запускает GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.log("🎉 Telegram Book Converter Bot GUI Manager запущен!")
        self.log("💡 Введите токен бота и нажмите 'Сохранить токен'")
        self.root.mainloop()

def main():
    """Главная функция"""
    try:
        # Проверяем, есть ли необходимые файлы
        if not Path("bot.py").exists():
            messagebox.showerror(
                "Ошибка", 
                "Файл bot.py не найден!\nЗапустите GUI из директории с ботом."
            )
            return
        
        # Создаем и запускаем GUI
        app = BotManagerGUI()
        app.run()
        
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Не удалось запустить GUI: {e}")

if __name__ == "__main__":
    main()
