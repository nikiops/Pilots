import axios from 'axios';
import { User, Service, Order } from '../context/AppContext';

const API_BASE_URL = (import.meta.env.VITE_API_URL as string) || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const authAPI = {
  register: (userData: Partial<User>) =>
    api.post('/api/users/save', userData),
  
  login: (email: string, password: string) =>
    api.get(`/api/users/${email}`).then(res => {
      if (res.data.password === password) {
        return res.data;
      }
      throw new Error('Invalid password');
    }),
};

export const userAPI = {
  getUser: (email: string) =>
    api.get<User>(`/api/users/${email}`),
  
  saveUser: (userData: User) =>
    api.post('/api/users/save', userData),
  
  getAllUsers: () =>
    api.get('/api/users/all'),
};

export const serviceAPI = {
  createService: (service: Service) =>
    api.post('/api/services', service),
  
  deleteService: (serviceId: string) =>
    api.delete(`/api/services/${serviceId}`),
};

export const orderAPI = {
  createOrder: (order: Order) =>
    api.post('/api/orders', order),
  
  deleteOrder: (orderId: string) =>
    api.delete(`/api/orders/${orderId}`),
};

export default api;
