import React, { useState } from 'react';
import '../styles/Auth.css';
import { authAPI } from '../api/client';
import { useApp } from '../context/AppContext';
import type { User } from '../context/AppContext';

interface AuthPageProps {
  onAuthSuccess: (user: User) => void;
}

export const AuthPage: React.FC<AuthPageProps> = ({ onAuthSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const { setIsLoading } = useApp();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const user = await authAPI.login(email, password);
      onAuthSuccess(user);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Ошибка входа');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const userData: Partial<User> = {
        email,
        password,
        name,
        accountType: 'freelancer',
        services: [],
        orders: [],
        rating: 5,
        reviews: 0,
      };

      await authAPI.register(userData);
      const user = await authAPI.login(email, password);
      onAuthSuccess(user);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Ошибка регистрации');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <h1>💼 TgWork</h1>
          <p>Фриланс Биржа</p>
        </div>

        <form onSubmit={isLogin ? handleLogin : handleRegister} className="auth-form">
          <h2>{isLogin ? 'Вход' : 'Регистрация'}</h2>

          {!isLogin && (
            <input
              type="text"
              placeholder="Ваше имя"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          )}

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="btn-primary">
            {isLogin ? 'Войти' : 'Создать аккаунт'}
          </button>
        </form>

        <button
          className="btn-toggle"
          onClick={() => {
            setIsLogin(!isLogin);
            setError('');
          }}
        >
          {isLogin ? 'Нет аккаунта? Регистрация' : 'Уже есть аккаунт? Вход'}
        </button>
      </div>
    </div>
  );
};
