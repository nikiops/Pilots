# TgWork React Web Application

## Project Setup Status

- [x] Create React + Vite project structure
- [x] Install dependencies
- [ ] Configure backend API connection
- [ ] Create main marketplace components
- [ ] Set up routing and navigation
- [ ] Deploy to Vercel

## Key Requirements

- React 18+ with Vite
- Backend API: http://localhost:5000 (production: API_URL from env)
- Same marketplace features as Telegram WebApp
- Responsive design for mobile
- Dark theme (GitHub mobile style)
- Email/password authentication
- Dual modes: Freelancer/Client
- 8-category marketplace with filtering

## Backend API Endpoints

- `GET /api/users/{email}` - Get user profile
- `POST /api/users/save` - Save user data
- `GET /api/users/all` - Get all users (for marketplace)
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
