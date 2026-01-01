import React, { useState } from 'react';
import '../styles/HomePage.css';
import type { User } from '../context/AppContext';

interface HomePageProps {
  user: User;
  onLogout: () => void;
  onNavigate: (page: string) => void;
}

export const HomePage: React.FC<HomePageProps> = ({ user, onLogout, onNavigate }) => {
  const [accountType, setAccountType] = useState(user.accountType);

  const handleSwitchMode = () => {
    const newType = accountType === 'freelancer' ? 'client' : 'freelancer';
    setAccountType(newType);
  };

  return (
    <div className="home-page">
      <div className="home-header">
        <h1>💼 TgWork</h1>
        <button className="btn-logout" onClick={onLogout}>
          Выход
        </button>
      </div>

      <div className="home-content">
        <div className="profile-card">
          <h2>{user.name}</h2>
          <p className="email">{user.email}</p>
          <div className="mode-indicator">
            {accountType === 'freelancer' ? '🚀 Исполнитель' : '💼 Заказчик'}
          </div>

          <div className="mode-toggle">
            <button
              className={`mode-btn ${accountType === 'freelancer' ? 'active' : ''}`}
              onClick={handleSwitchMode}
            >
              🚀 Исполнитель
            </button>
            <button
              className={`mode-btn ${accountType === 'client' ? 'active' : ''}`}
              onClick={handleSwitchMode}
            >
              💼 Заказчик
            </button>
          </div>

          <div className="stats">
            <div className="stat">
              <span>⭐</span>
              <span>{user.rating.toFixed(1)} / 5</span>
            </div>
            <div className="stat">
              <span>👤</span>
              <span>{user.reviews} отзывов</span>
            </div>
          </div>
        </div>

        <div className="quick-actions">
          {accountType === 'freelancer' ? (
            <>
              <button
                className="action-btn"
                onClick={() => onNavigate('marketplace')}
              >
                🛍️ Найти заказы
              </button>
              <button
                className="action-btn"
                onClick={() => onNavigate('myServices')}
              >
                📦 Мои услуги ({user.services?.length || 0})
              </button>
            </>
          ) : (
            <>
              <button
                className="action-btn"
                onClick={() => onNavigate('createOrder')}
              >
                ✍️ Новый заказ
              </button>
              <button
                className="action-btn"
                onClick={() => onNavigate('myOrders')}
              >
                📋 Мои заказы ({user.orders?.length || 0})
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
