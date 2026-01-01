import React, { createContext, useState, useContext, ReactNode } from 'react';

export interface User {
  email: string;
  password?: string;
  name: string;
  accountType: 'freelancer' | 'client';
  services: Service[];
  orders: Order[];
  rating: number;
  reviews: number;
  telegram_id?: string;
}

export interface Service {
  id: string;
  title: string;
  description: string;
  category: string;
  price: number;
  author_email: string;
  created_at: string;
  status: 'active' | 'completed' | 'deleted';
}

export interface Order {
  id: string;
  title: string;
  description: string;
  category: string;
  budget: number;
  author_email: string;
  created_at: string;
  status: 'open' | 'in_progress' | 'completed' | 'deleted';
  bids?: Bid[];
}

export interface Bid {
  id: string;
  order_id: string;
  freelancer_email: string;
  message: string;
  created_at: string;
}

interface AppContextType {
  currentUser: User | null;
  setCurrentUser: (user: User | null) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  return (
    <AppContext.Provider value={{ currentUser, setCurrentUser, isLoading, setIsLoading }}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};
