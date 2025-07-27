import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import apiService from '../services/api';
import type { DashboardData, RecordRead, PaginatedRecordRead } from '../types/index';

export const DashboardPage: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [records, setRecords] = useState<RecordRead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError('');
      try {
        const dashboardData = await apiService.getDashboardData();
        setDashboard(dashboardData);
        const recordsData: PaginatedRecordRead = await apiService.getRecords(1, 10);
        setRecords(recordsData.items);
      } catch (err: any) {
        setError('Ошибка загрузки данных');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-gray-900">LifeControl</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Привет, {user?.login}!</span>
              <button
                onClick={logout}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Выйти
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {loading ? (
            <div className="text-center text-gray-500">Загрузка...</div>
          ) : error ? (
            <div className="text-center text-red-500">{error}</div>
          ) : dashboard ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                          <span className="text-white text-sm font-medium">💰</span>
                        </div>
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">
                            Общий баланс
                          </dt>
                          <dd className="text-lg font-medium text-gray-900">
                            ₽{dashboard.total_balance.toLocaleString('ru-RU', { minimumFractionDigits: 2 })}
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                          <span className="text-white text-sm font-medium">📍</span>
                        </div>
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">
                            Локаций
                          </dt>
                          <dd className="text-lg font-medium text-gray-900">
                            {dashboard.locations_balance.length}
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="w-8 h-8 bg-purple-500 rounded-md flex items-center justify-center">
                          <span className="text-white text-sm font-medium">🟣</span>
                        </div>
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">
                            Сфер
                          </dt>
                          <dd className="text-lg font-medium text-gray-900">
                            {dashboard.spheres_balance.length}
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="w-8 h-8 bg-gray-500 rounded-md flex items-center justify-center">
                          <span className="text-white text-sm font-medium">📊</span>
                        </div>
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">
                            Записей
                          </dt>
                          <dd className="text-lg font-medium text-gray-900">
                            {records.length}
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Баланс по локациям */}
              <div className="mb-8">
                <h2 className="text-lg font-medium text-gray-900 mb-2">Баланс по локациям</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {dashboard.locations_balance.map(loc => (
                    <div key={loc.id} className="bg-white p-4 rounded shadow flex flex-col items-center">
                      <div className="font-semibold text-gray-700">{loc.name}</div>
                      <div className="text-xl font-bold text-blue-700">₽{loc.balance.toLocaleString('ru-RU', { minimumFractionDigits: 2 })}</div>
                    </div>
                  ))}
                  {dashboard.locations_balance.length === 0 && <div className="text-gray-400">Нет данных</div>}
                </div>
              </div>

              {/* Баланс по сферам */}
              <div className="mb-8">
                <h2 className="text-lg font-medium text-gray-900 mb-2">Баланс по сферам</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {dashboard.spheres_balance.map(sph => (
                    <div key={sph.id} className="bg-white p-4 rounded shadow flex flex-col items-center">
                      <div className="font-semibold text-gray-700">{sph.name}</div>
                      <div className="text-xl font-bold text-purple-700">₽{sph.balance.toLocaleString('ru-RU', { minimumFractionDigits: 2 })}</div>
                    </div>
                  ))}
                  {dashboard.spheres_balance.length === 0 && <div className="text-gray-400">Нет данных</div>}
                </div>
              </div>

              {/* Последние записи */}
              <div className="mb-8">
                <div className="flex justify-between items-center mb-2">
                  <h2 className="text-lg font-medium text-gray-900">Последние записи</h2>
                  <button
                    onClick={() => navigate('/records')}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 text-sm"
                  >
                    Добавить запись
                  </button>
                </div>
                <div className="bg-white shadow overflow-hidden sm:rounded-md">
                  {records.length === 0 ? (
                    <div className="px-4 py-5 sm:p-6 text-gray-400 text-center">Записей пока нет</div>
                  ) : (
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Дата</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Тип</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Сумма</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Локация</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Сфера</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Описание</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {records.map(rec => (
                          <tr key={rec.id}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{rec.date ? new Date(rec.date).toLocaleDateString('ru-RU') : ''}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{rec.operation_type}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-right">₽{rec.sum.toLocaleString('ru-RU', { minimumFractionDigits: 2 })}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{rec.location?.name || '-'}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{rec.sphere?.name || '-'}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{rec.description || '-'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              </div>
            </>
          ) : null}
        </div>
      </main>
    </div>
  );
}; 