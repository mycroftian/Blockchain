import React, { useState } from 'react';
import Navbar from './components/Navbar';
import RecieverDashboard from './components/RecieverDashboard';
import Home from './pages/Home';
import UserDashboard from './pages/UserDashboard';

function App() {
  const [view, setView] = useState('discover');

  const renderContent = () => {
    switch (view) {
      case 'creator':
        return <RecieverDashboard />;
      case 'subscriptions':
        return <UserDashboard />;
      default:
        return <Home />;
    }
  };

  return (
    <div className='min-h-screen bg-gray-50'>
      <Navbar view={view} setView={setView} />
      <main className='container mx-auto px-6 py-8'>{renderContent()}</main>
    </div>
  );
}

export default App;
