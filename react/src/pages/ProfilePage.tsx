import React from 'react';
import '../styles/ProfilePage.css';
import type { User } from '../context/AppContext';

interface ProfilePageProps {
  user: User;
  onUpdate: (updatedUser: User) => void;
  onNavigate: (page: string) => void;
}

export const ProfilePage: React.FC<ProfilePageProps> = ({ user, onUpdate, onNavigate }) => {
  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-header">
          <h1>👤 {user.name}</h1>
          <p className="email">{user.email}</p>
        </div>

        <div className="profile-stats">
          <div className="stat">
            <span className="label">⭐ Рейтинг</span>
            <span className="value">{user.rating.toFixed(1)} / 5</span>
          </div>
          <div className="stat">
            <span className="label">📝 Отзывы</span>
            <span className="value">{user.reviews}</span>
          </div>
          <div className="stat">
            <span className="label">📦 Услуги</span>
            <span className="value">{user.services?.length || 0}</span>
          </div>
          <div className="stat">
            <span className="label">📋 Заказы</span>
            <span className="value">{user.orders?.length || 0}</span>
          </div>
        </div>

        <div className="profile-info">
          <h3>Информация профиля</h3>
          <div className="info-item">
            <span className="label">Аккаунт:</span>
            <span className="value">
              {user.accountType === 'freelancer' ? '🚀 Исполнитель' : '💼 Заказчик'}
            </span>
          </div>
          <div className="info-item">
            <span className="label">Email:</span>
            <span className="value">{user.email}</span>
          </div>
        </div>

        <div className="profile-actions">
          <button className="btn-secondary" onClick={() => onNavigate('marketplace')}>
            🛍️ На биржу
          </button>
          <button className="btn-secondary" onClick={() => onNavigate('home')}>
            🏠 На главную
          </button>
        </div>
      </div>
    </div>
  );
};
