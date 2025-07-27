import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const navItems = [
  { to: '/dashboard', label: 'Дашборд' },
  { to: '/spheres', label: 'Сферы' },
  { to: '/locations', label: 'Локации' },
];

export const Navbar: React.FC = () => {
  const location = useLocation();
  return (
    <nav className="bg-white shadow mb-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center space-x-6">
          {navItems.map(item => (
            <Link
              key={item.to}
              to={item.to}
              className={`text-gray-700 hover:text-blue-600 font-medium transition-colors px-3 py-2 rounded-md ${location.pathname.startsWith(item.to) ? 'bg-blue-100 text-blue-700' : ''}`}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}; 