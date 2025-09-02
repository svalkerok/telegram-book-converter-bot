"""
🔒 Безопасность и стабильность GUI
Safety and Stability Improvements for GUI
"""

import threading
import time
import subprocess
from typing import Callable, Any

try:
    import requests
except ImportError:
    requests = None

class SafeGUIExecutor:
    """Безопасный исполнитель для GUI операций"""
    
    def __init__(self, root):
        self.root = root
        self._shutdown = False
        
    def safe_after(self, delay: int, callback: Callable, *args, **kwargs):
        """Безопасный вызов after с проверкой состояния"""
        if self._shutdown:
            return
        
        def safe_callback():
            if not self._shutdown:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"Ошибка в safe_after callback: {e}")
        
        try:
            self.root.after(delay, safe_callback)
        except Exception as e:
            print(f"Ошибка safe_after: {e}")
    
    def safe_thread(self, target: Callable, *args, **kwargs):
        """Безопасный запуск потока с обработкой ошибок"""
        def wrapped_target():
            try:
                target(*args, **kwargs)
            except Exception as e:
                print(f"Ошибка в потоке: {e}")
                if not self._shutdown:
                    self.safe_after(0, lambda: print(f"Thread error: {e}"))
        
        thread = threading.Thread(target=wrapped_target, daemon=True)
        thread.start()
        return thread
    
    def shutdown(self):
        """Безопасное завершение"""
        self._shutdown = True

class TokenValidator:
    """Валидатор токенов с улучшенной обработкой ошибок"""
    
    @staticmethod
    def validate_token_format(token: str) -> tuple[bool, str]:
        """Проверяет формат токена"""
        if not token:
            return False, "Токен не может быть пустым"
        
        if len(token) < 35:
            return False, "Токен слишком короткий"
        
        if ":" not in token:
            return False, "Неверный формат токена"
        
        parts = token.split(":")
        if len(parts) != 2:
            return False, "Неверный формат токена"
        
        try:
            int(parts[0])  # Проверяем что первая часть - число
        except ValueError:
            return False, "Неверный формат токена"
        
        return True, "Формат токена корректен"
    
    @staticmethod
    def validate_token_online(token: str, timeout: int = 10) -> tuple[bool, str, dict]:
        """Проверяет токен онлайн"""
        if requests is None:
            return False, "Модуль requests не установлен", {}
        
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{token}/getMe", 
                timeout=timeout
            )
            result = response.json()
            
            if result.get("ok"):
                bot_info = result.get("result", {})
                bot_name = bot_info.get("username", "Unknown")
                return True, f"Токен валиден! Бот: @{bot_name}", bot_info
            else:
                error = result.get("description", "Unknown error")
                return False, f"Токен невалиден: {error}", {}
                
        except requests.exceptions.Timeout:
            return False, "Таймаут при проверке токена", {}
        except requests.exceptions.ConnectionError:
            return False, "Ошибка соединения", {}
        except requests.exceptions.RequestException as e:
            return False, f"Ошибка запроса: {e}", {}
        except Exception as e:
            return False, f"Неожиданная ошибка: {e}", {}

class ProcessManager:
    """Менеджер процессов с улучшенным контролем"""
    
    def __init__(self):
        self.processes = {}
        self._shutdown = False
    
    def start_process(self, name: str, command: list, **kwargs) -> bool:
        """Запускает процесс с контролем"""
        if self._shutdown:
            return False
        
        try:
            import subprocess
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                **kwargs
            )
            self.processes[name] = process
            return True
        except Exception as e:
            print(f"Ошибка запуска процесса {name}: {e}")
            return False
    
    def stop_process(self, name: str, timeout: int = 10) -> bool:
        """Останавливает процесс с таймаутом"""
        if name not in self.processes:
            return True
        
        process = self.processes[name]
        try:
            process.terminate()
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        except Exception as e:
            print(f"Ошибка остановки процесса {name}: {e}")
            return False
        finally:
            del self.processes[name]
        
        return True
    
    def is_running(self, name: str) -> bool:
        """Проверяет запущен ли процесс"""
        if name not in self.processes:
            return False
        
        process = self.processes[name]
        return process.poll() is None
    
    def shutdown_all(self):
        """Останавливает все процессы"""
        self._shutdown = True
        for name in list(self.processes.keys()):
            self.stop_process(name)

class GUILogger:
    """Логгер для GUI с ротацией и буферизацией"""
    
    def __init__(self, max_lines: int = 1000):
        self.max_lines = max_lines
        self.buffer = []
        self.callbacks = []
    
    def add_callback(self, callback: Callable[[str], None]):
        """Добавляет колбэк для обработки новых логов"""
        self.callbacks.append(callback)
    
    def log(self, message: str):
        """Добавляет сообщение в лог"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.buffer.append(formatted_message)
        
        # Ротация логов
        if len(self.buffer) > self.max_lines:
            self.buffer = self.buffer[-self.max_lines:]
        
        # Уведомляем колбэки
        for callback in self.callbacks:
            try:
                callback(formatted_message)
            except Exception as e:
                print(f"Ошибка в callback логгера: {e}")
    
    def get_logs(self) -> list[str]:
        """Возвращает все логи"""
        return self.buffer.copy()
    
    def clear(self):
        """Очищает логи"""
        self.buffer.clear()
        for callback in self.callbacks:
            try:
                callback("--- Логи очищены ---")
            except Exception as e:
                print(f"Ошибка в callback при очистке: {e}")
