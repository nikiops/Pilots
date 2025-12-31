"""
Модель транзакции (эскроу и выплаты)
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class TransactionType(str, enum.Enum):
    """Типы транзакций"""
    ORDER_ESCROW = "order_escrow"  # Деньги заморожены в эскроу
    ORDER_RELEASE = "order_release"  # Деньги выданы продавцу после завершения
    BALANCE_TOP_UP = "balance_top_up"  # Пополнение баланса
    WITHDRAWAL = "withdrawal"  # Вывод средств
    REFUND = "refund"  # Возврат денег заказчику
    DISPUTE_REFUND = "dispute_refund"  # Возврат при споре
    PLATFORM_FEE = "platform_fee"  # Комиссия платформы


class TransactionStatus(str, enum.Enum):
    """Статусы транзакции"""
    PENDING = "pending"  # В ожидании
    COMPLETED = "completed"  # Завершена
    FAILED = "failed"  # Ошибка
    REFUNDED = "refunded"  # Возвращена


class Transaction(Base):
    """
    Модель финансовой транзакции
    Используется для отслеживания эскроу, выплат и пополнений
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Пользователь (может быть покупатель или продавец)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", back_populates="transactions")
    
    # Заказ (опционально, может быть и пополнение баланса)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True, index=True)
    order = relationship("Order", back_populates="transactions")
    
    # Тип и сумма
    type = Column(SqlEnum(TransactionType), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    status = Column(SqlEnum(TransactionStatus), default=TransactionStatus.PENDING, index=True)
    
    # Описание
    description = Column(Text, nullable=True)
    
    # Дополнительная информация
    reference = Column(String(255), nullable=True)  # Для платёжных систем
    
    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Transaction {self.id}: {self.type.value} {self.amount}>"
