"""
Скрипт для инициализации БД и создания таблиц
"""
import sys
import os

# Добавляем текущую директорию в path
sys.path.insert(0, os.getcwd())

def main():
    print("🔄 Инициализация БД...")
    try:
        from app.db.base import Base
        from app.db.session import engine
        from app.models import User, Service, Order, Message, Review, Transaction
        
        print("✓ Модели загружены")
        
        # Создаём таблицы
        Base.metadata.create_all(bind=engine)
        print("✓ БД инициализирована успешно!")
        print("✓ Все таблицы созданы:")
        print("  - users")
        print("  - services")
        print("  - orders")
        print("  - messages")
        print("  - reviews")
        print("  - transactions")
        
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
