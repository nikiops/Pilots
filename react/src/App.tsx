import { useState } from 'react';
import { AppProvider, useApp } from './context/AppContext';
import { AuthPage } from './pages/AuthPage';
import { HomePage } from './pages/HomePage';
import { MarketplacePage } from './pages/MarketplacePage';
import type { User } from './context/AppContext';

function AppContent() {
  const { currentUser, setCurrentUser, isLoading } = useApp();
  const [currentPage, setCurrentPage] = useState('home');

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Загрузка...</p>
      </div>
    );
  }

  if (!currentUser) {
    return (
      <AuthPage
        onAuthSuccess={(user) => {
          setCurrentUser(user);
          setCurrentPage('home');
        }}
      />
    );
  }

  return (
    <div className="app">
      {currentPage === 'home' && (
        <HomePage
          user={currentUser}
          onLogout={() => {
            setCurrentUser(null);
            setCurrentPage('home');
          }}
          onNavigate={setCurrentPage}
        />
      )}
      {currentPage === 'marketplace' && (
        <MarketplacePage
          userEmail={currentUser.email}
          isFreelancer={currentUser.accountType === 'freelancer'}
        />
      )}
    </div>
  );
}

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;
