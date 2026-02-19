"""
Утилита для просмотра и анализа статистики скачиваний
Запустите: python stats_viewer.py
"""

from datetime import datetime
from pathlib import Path
from config import LOG_FILE

def view_stats() -> None:
    """Выводит красивую статистику скачиваний"""
    
    if not Path(LOG_FILE).exists():
        print("❌ Файл логов не найден. Никто ещё не скачивал файл.")
        return
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if not lines:
        print("❌ Файл логов пуст. Никто ещё не скачивал файл.")
        return
    
    print("\n" + "="*70)
    print("📊 СТАТИСТИКА СКАЧИВАНИЙ")
    print("="*70)
    print(f"✅ Всего скачиваний: {len(lines)}")
    print("="*70)
    print()
    
    # Выводим все скачивания
    unique_users: set[str] = set()
    today_downloads = 0
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    for i, line in enumerate(lines, 1):
        print(f"{i}. {line.strip()}")
        
        # Подсчитываем уникальных пользователей
        if "User ID:" in line:
            user_id = line.split("User ID: ")[1].split(" |")[0]
            unique_users.add(user_id)
        
        # Подсчитываем скачивания за сегодня
        if today_date in line:
            today_downloads += 1
    
    print()
    print("="*70)
    print(f"👥 Уникальные пользователи: {len(unique_users)}")
    print(f"📅 Скачиваний за сегодня: {today_downloads}")
    print("="*70)
    print()


def export_to_csv() -> None:
    """Экспортирует логи в CSV для Excel"""
    
    if not Path(LOG_FILE).exists():
        print("❌ Файл логов не найден.")
        return
    
    csv_file = "downloads_export.csv"
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    with open(csv_file, "w", encoding="utf-8") as f:
        f.write("№,Дата,Время,User ID,Username\n")
        
        for i, line in enumerate(lines, 1):
            parts = line.strip().split(" | ")
            if len(parts) >= 3:
                datetime_str = parts[0]
                user_id = parts[1].replace("User ID: ", "")
                username = parts[2].replace("Username: ", "")
                
                # Разделяем дату и время
                date_time = datetime_str.split(" ")
                date = date_time[0] if len(date_time) > 0 else ""
                time = date_time[1] if len(date_time) > 1 else ""
                
                f.write(f'{i},"{date}","{time}","{user_id}","{username}"\n')
    
    print(f"✅ Экспортировано в файл: {csv_file}")
    print(f"   Используйте этот файл в Excel для анализа")


if __name__ == "__main__":
    print("\n🔍 Утилита просмотра статистики\n")
    print("Выберите действие:")
    print("1. Просмотреть статистику")
    print("2. Экспортировать в CSV (для Excel)")
    print("0. Выход")
    
    choice = input("\nВаш выбор (0-2): ").strip()
    
    if choice == "1":
        view_stats()
    elif choice == "2":
        export_to_csv()
    elif choice == "0":
        print("До свидания!")
    else:
        print("❌ Неверный выбор")
