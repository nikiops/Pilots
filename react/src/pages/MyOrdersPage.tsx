import React, { useState } from 'react';
import '../styles/MyOrdersPage.css';
import { userAPI } from '../api/client';
import type { Order, User } from '../context/AppContext';

interface MyOrdersPageProps {
  user: User;
  onUpdate: (updatedUser: User) => void;
}

export const MyOrdersPage: React.FC<MyOrdersPageProps> = ({ user, onUpdate }) => {
  const [orders, setOrders] = useState<Order[]>(user.orders || []);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'web',
    budget: 0,
  });

  const handleCreateOrder = async (e: React.FormEvent) => {
    e.preventDefault();

    const newOrder: Order = {
      id: Date.now().toString(),
      ...formData,
      author_email: user.email,
      created_at: new Date().toISOString(),
      status: 'open',
      bids: [],
    };

    const updatedOrders = [...orders, newOrder];
    setOrders(updatedOrders);

    const updatedUser = { ...user, orders: updatedOrders };
    try {
      await userAPI.saveUser(updatedUser);
      onUpdate(updatedUser);
    } catch (error) {
      console.error('Error saving order:', error);
    }

    setFormData({ title: '', description: '', category: 'web', budget: 0 });
    setShowForm(false);
  };

  const handleDeleteOrder = async (orderId: string) => {
    const updatedOrders = orders.filter((o) => o.id !== orderId);
    setOrders(updatedOrders);

    const updatedUser = { ...user, orders: updatedOrders };
    try {
      await userAPI.saveUser(updatedUser);
      onUpdate(updatedUser);
    } catch (error) {
      console.error('Error deleting order:', error);
    }
  };

  return (
    <div className="my-orders-page">
      <div className="page-header">
        <h1>📋 Мои заказы</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? '✕ Отмена' : '➕ Новый заказ'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreateOrder} className="order-form">
          <input
            type="text"
            placeholder="Название заказа"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            required
          />
          <textarea
            placeholder="Описание"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            required
          />
          <select
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
          >
            <option value="web">🌐 Веб-разработка</option>
            <option value="design">🎨 Дизайн</option>
            <option value="writing">✍️ Написание текстов</option>
            <option value="marketing">📱 Маркетинг</option>
            <option value="seo">🔍 SEO</option>
            <option value="video">🎬 Видеомонтаж</option>
            <option value="music">🎵 Музыка</option>
            <option value="translation">🌍 Переводы</option>
          </select>
          <input
            type="number"
            placeholder="Бюджет (₽)"
            value={formData.budget}
            onChange={(e) => setFormData({ ...formData, budget: parseInt(e.target.value) })}
            required
          />
          <button type="submit" className="btn-primary">
            ✅ Создать заказ
          </button>
        </form>
      )}

      <div className="orders-list">
        {orders.length > 0 ? (
          orders.map((order) => (
            <div key={order.id} className="order-card">
              <h3>{order.title}</h3>
              <p>{order.description}</p>
              <div className="order-footer">
                <span className="budget">Бюджет: {order.budget} ₽</span>
                <button
                  className="btn-danger"
                  onClick={() => handleDeleteOrder(order.id)}
                >
                  🗑️ Удалить
                </button>
              </div>
            </div>
          ))
        ) : (
          <p className="empty-message">Заказов нет. Создайте первый! 📝</p>
        )}
      </div>
    </div>
  );
};
