"""
Простой HTTP сервер для запуска WebApp профиля
Запуск: python webapp/server.py
"""
import http.server
import socketserver
import os
from pathlib import Path

PORT = 8080
WEBAPP_DIR = Path(__file__).parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBAPP_DIR, **kwargs)
    
    def log_message(self, format, *args):
        """Кастомный лог"""
        print(f"[WebApp Server] {format % args}")

def run_server():
    """Запустить сервер"""
    handler = MyHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"🚀 WebApp сервер запущен на http://localhost:{PORT}")
        print(f"📁 Папка: {WEBAPP_DIR}")
        print(f"🔗 Профиль: http://localhost:{PORT}/profile.html")
        print(f"\nНажми Ctrl+C чтобы остановить сервер...\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")

if __name__ == "__main__":
    run_server()
