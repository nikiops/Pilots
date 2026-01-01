"""
Версия WebApp для обхода кеша Telegram браузера
Увеличивайте при обновлении кода чтобы браузер загрузил свежую версию
"""

WEBAPP_VERSION = "1"

def get_webapp_url_with_version():
    """Получить URL WebApp с версией"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    ngrok_url = os.getenv('NGROK_URL', 'https://localhost:3000')
    return f"{ngrok_url}/index.html?v={WEBAPP_VERSION}"

def increment_version():
    """Увеличить версию на 1"""
    global WEBAPP_VERSION
    current = int(WEBAPP_VERSION)
    WEBAPP_VERSION = str(current + 1)
    return WEBAPP_VERSION
