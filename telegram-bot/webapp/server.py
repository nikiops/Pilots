import http.server
import socketserver
import json
import urllib.parse
from pathlib import Path
from datetime import datetime

PORT = 3000
WEBAPP_DIR = Path(__file__).parent
USERS_DB_FILE = WEBAPP_DIR / 'users_db.json'

def log(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}", flush=True)

def load_users_db():
    if USERS_DB_FILE.exists():
        try:
            with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            log("❌ Ошибка при загрузке users_db.json")
            return {}
    return {}

def save_users_db(users):
    with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

users_db = load_users_db()
log(f"✅ Загруженных пользователей: {len(users_db)}")

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBAPP_DIR, **kwargs)
    
    def do_GET(self):
        if self.path.startswith('/api/users/all'):
            log(f"📥 GET /api/users/all")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = json.dumps(users_db)
            log(f"📤 Отправка {len(users_db)} пользователей ({len(response)} байт)")
            self.wfile.write(response.encode())
            return
        
        if self.path.startswith('/api/users/'):
            email = urllib.parse.unquote(self.path.replace('/api/users/', '').strip()).lower()
            log(f"📥 GET /api/users/{email}")
            
            if email in users_db:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = json.dumps(users_db[email])
                log(f"✅ Пользователь найден ({len(response)} байт)")
                self.wfile.write(response.encode())
            else:
                log(f"❌ Пользователь не найден: {email}")
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'User not found'}).encode())
            return
        
        super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/users/save':
            log(f"📥 POST /api/users/save")
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode()
            
            try:
                user_data = json.loads(body)
                email = user_data.get('email', '').lower()
                
                if email:
                    users_db[email] = user_data
                    save_users_db(users_db)
                    
                    log(f"✅ Сохранён пользователь: {email}")
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True}).encode())
                else:
                    log(f"❌ Email не указан")
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Email required'}).encode())
            except Exception as e:
                log(f"❌ Ошибка при сохранении: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            return
        
        self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Переопределяем log_message чтобы использовать нашу функцию log
        pass

def run_server():
    global users_db
    users_db = load_users_db()
    
    handler = MyHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        log(f"🚀 WebApp запущен на http://localhost:{PORT}")
        log(f"📂 Файл БД: {USERS_DB_FILE}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            log("⛔ Сервер остановлен")

if __name__ == "__main__":
    run_server()
