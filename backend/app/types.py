"""
Утилиты и типы для работы с БД
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Типы для SQL
class DatabaseType(str, Enum):
    """Поддерживаемые типы БД"""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"

# Типы для Telegram
class TelegramUser(Dict[str, Any]):
    """Структура пользователя из Telegram"""
    pass

# Типы для финансов
class Money(float):
    """Денежная сумма в рублях"""
    pass

# Типы для рейтинга
class Rating(float):
    """Рейтинг от 0 до 5"""
    
    def __new__(cls, value):
        if not 0 <= value <= 5:
            raise ValueError("Rating must be between 0 and 5")
        return float.__new__(cls, value)

# Типы для ID
UserId = int
ServiceId = int
OrderId = int
MessageId = int
ReviewId = int
TransactionId = int
TelegramId = int

# Общие типы
Pagination = Optional[tuple[int, int]]  # offset, limit
