import React, { useState, useEffect } from 'react';
import '../styles/Marketplace.css';
import { userAPI } from '../api/client';
import type { Service, Order } from '../context/AppContext';

const CATEGORIES = [
  { id: 'web', name: '🌐 Веб-разработка' },
  { id: 'design', name: '🎨 Дизайн' },
  { id: 'writing', name: '✍️ Написание текстов' },
  { id: 'marketing', name: '📱 Маркетинг' },
  { id: 'seo', name: '🔍 SEO' },
  { id: 'video', name: '🎬 Видеомонтаж' },
  { id: 'music', name: '🎵 Музыка' },
  { id: 'translation', name: '🌍 Переводы' },
];

interface MarketplacePageProps {
  userEmail: string;
  isFreelancer: boolean;
}

export const MarketplacePage: React.FC<MarketplacePageProps> = ({ userEmail, isFreelancer }) => {
  const [items, setItems] = useState<(Service | Order)[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('web');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadItems();
  }, [selectedCategory]);

  const loadItems = async () => {
    setIsLoading(true);
    try {
      const response = await userAPI.getAllUsers();
      const allUsers = response.data;

      let filteredItems: (Service | Order)[] = [];

      Object.values(allUsers).forEach((user: any) => {
        if (isFreelancer && user.services) {
          filteredItems.push(...user.services);
        } else if (!isFreelancer && user.orders) {
          filteredItems.push(...user.orders);
        }
      });

      filteredItems = filteredItems.filter(
        (item) =>
          item.category === selectedCategory &&
          item.status !== 'deleted' &&
          ('author_email' in item && item.author_email !== userEmail)
      );

      setItems(filteredItems);
    } catch (error) {
      console.error('Error loading marketplace:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="marketplace-page">
      <div className="category-filter">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.id}
            className={`category-btn ${selectedCategory === cat.id ? 'active' : ''}`}
            onClick={() => setSelectedCategory(cat.id)}
          >
            {cat.name}
          </button>
        ))}
      </div>

      <div className="items-list">
        {isLoading ? (
          <p>Загрузка...</p>
        ) : items.length > 0 ? (
          items.map((item) => (
            <div key={item.id} className="item-card">
              <h3>{item.title}</h3>
              <p className="description">{item.description}</p>
              <div className="item-footer">
                <span className="price">
                  {('budget' in item ? item.budget : item.price) + ' ₽'}
                </span>
                <button className="btn-primary">
                  {isFreelancer ? '💬 Оставить предложение' : '✏️ Изменить'}
                </button>
              </div>
            </div>
          ))
        ) : (
          <p>Нет товаров в этой категории</p>
        )}
      </div>
    </div>
  );
};
