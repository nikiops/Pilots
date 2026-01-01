import React, { useState, useEffect } from 'react';
import '../styles/MyServicesPage.css';
import { userAPI } from '../api/client';
import type { Service, User } from '../context/AppContext';

interface MyServicesPageProps {
  user: User;
  onUpdate: (updatedUser: User) => void;
  onNavigate: (page: string) => void;
}

export const MyServicesPage: React.FC<MyServicesPageProps> = ({ user, onUpdate, onNavigate }) => {
  const [services, setServices] = useState<Service[]>(user.services || []);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'web',
    price: 0,
  });

  const handleCreateService = async (e: React.FormEvent) => {
    e.preventDefault();

    const newService: Service = {
      id: Date.now().toString(),
      ...formData,
      author_email: user.email,
      created_at: new Date().toISOString(),
      status: 'active',
    };

    const updatedServices = [...services, newService];
    setServices(updatedServices);

    const updatedUser = { ...user, services: updatedServices };
    try {
      await userAPI.saveUser(updatedUser);
      onUpdate(updatedUser);
    } catch (error) {
      console.error('Error saving service:', error);
    }

    setFormData({ title: '', description: '', category: 'web', price: 0 });
    setShowForm(false);
  };

  const handleDeleteService = async (serviceId: string) => {
    const updatedServices = services.filter((s) => s.id !== serviceId);
    setServices(updatedServices);

    const updatedUser = { ...user, services: updatedServices };
    try {
      await userAPI.saveUser(updatedUser);
      onUpdate(updatedUser);
    } catch (error) {
      console.error('Error deleting service:', error);
    }
  };

  return (
    <div className="my-services-page">
      <div className="page-header">
        <h1>📦 Мои услуги</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? '✕ Отмена' : '➕ Новая услуга'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreateService} className="service-form">
          <input
            type="text"
            placeholder="Название услуги"
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
            placeholder="Цена (₽)"
            value={formData.price}
            onChange={(e) => setFormData({ ...formData, price: parseInt(e.target.value) })}
            required
          />
          <button type="submit" className="btn-primary">
            ✅ Создать услугу
          </button>
        </form>
      )}

      <div className="services-list">
        {services.length > 0 ? (
          services.map((service) => (
            <div key={service.id} className="service-card">
              <h3>{service.title}</h3>
              <p>{service.description}</p>
              <div className="service-footer">
                <span className="price">{service.price} ₽</span>
                <button
                  className="btn-danger"
                  onClick={() => handleDeleteService(service.id)}
                >
                  🗑️ Удалить
                </button>
              </div>
            </div>
          ))
        ) : (
          <p className="empty-message">Услуг нет. Создайте первую! 📝</p>
        )}
      </div>
    </div>
  );
};
