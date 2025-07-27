import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const navItems = [
  { to: '/dashboard', label: 'Дашборд', icon: '📊' },
  { to: '/spheres', label: 'Сферы', icon: '🎯' },
  { to: '/locations', label: 'Локации', icon: '📍' },
  { to: '/records', label: 'Записи', icon: '📝' },
];

export const Navbar: React.FC = () => {
  const location = useLocation();
  const { user, logout } = useAuth();

  return (
    <nav className="bg-white shadow-lg border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Логотип и название */}
          <div className="flex items-center">
            <Link to="/dashboard" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white text-sm font-bold">LC</span>
              </div>
              <span className="text-xl font-bold text-gray-900">LifeControl</span>
            </Link>
          </div>

          {/* Навигационные ссылки */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map(item => (
              <Link
                key={item.to}
                to={item.to}
                className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  location.pathname === item.to 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
                }`}
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            ))}
          </div>

          {/* Пользователь и выход */}
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-700">
              Привет, <span className="font-medium">{user?.login}</span>!
            </span>
            <button
              onClick={logout}
              className="bg-red-600 hover:bg-red-700 text-white px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
            >
              Выйти
            </button>
          </div>
        </div>

        {/* Мобильная навигация */}
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navItems.map(item => (
              <Link
                key={item.to}
                to={item.to}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-base font-medium ${
                  location.pathname === item.to 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
                }`}
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}; 