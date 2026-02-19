import csv
from pathlib import Path
from config import LOG_FILE


def view_stats() -> None:
    """Показывает статистику скачиваний."""
    if not Path(LOG_FILE).exists():
        print("Пока нет данных о скачиваниях")
        return
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    unique_users: set[str] = set()
    print(f"\n📊 СТАТИСТИКА СКАЧИВАНИЙ\n")
    print(f"Всего скачиваний: {len(lines)}")
    
    for line in lines:
        unique_users.add(line.strip())
    
    print(f"Уникальных пользователей: {len(unique_users)}\n")
    print("Последние скачивания:\n")
    
    for line in lines[-10:]:
        print(f"  {line.strip()}")


def export_to_csv() -> None:
    """Экспортирует статистику в CSV для Excel."""
    if not Path(LOG_FILE).exists():
        print("Пока нет данных о скачиваниях")
        return
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    with open("stats.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Time", "User ID", "Username"])
        
        for line in lines:
            parts = line.strip().split(" | ")
            if len(parts) >= 3:
                datetime_str = parts[0]
                user_id = parts[1].replace("User ID: ", "")
                username = parts[2].replace("Username: ", "")
                
                date, time = datetime_str.split(" ")
                writer.writerow([date, time, user_id, username])
    
    print("✅ Файл stats.csv создан!")


if __name__ == "__main__":
    view_stats()
    print("\n" + "=" * 50 + "\n")
    export_to_csv()
