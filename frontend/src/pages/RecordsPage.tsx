import React, { useEffect, useState } from 'react';
import apiService from '../services/api';
import type { RecordRead, RecordCreate, PaginatedRecordRead, SphereRead, LocationRead } from '../types/index';

interface RecordFormData {
  type: 'Income' | 'Spend' | 'Transfer';
  sum: number;
  description: string;
  date: string;
  location_id: number;
  sphere_id: number;
  transfer_type?: 'location' | 'sphere';
  from_location_id?: number;
  to_location_id?: number;
  from_sphere_id?: number;
  to_sphere_id?: number;
}

export const RecordsPage: React.FC = () => {
  const [records, setRecords] = useState<RecordRead[]>([]);
  const [spheres, setSpheres] = useState<SphereRead[]>([]);
  const [locations, setLocations] = useState<LocationRead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showForm, setShowForm] = useState(false);
  const [editingRecord, setEditingRecord] = useState<RecordRead | null>(null);
  const [formData, setFormData] = useState<RecordFormData>({
    type: 'Income',
    sum: 0,
    description: '',
    date: new Date().toISOString().split('T')[0],
    location_id: 0,
    sphere_id: 0,
  });

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const [recordsData, spheresData, locationsData] = await Promise.all([
        apiService.getRecords(currentPage, 20),
        apiService.getSpheres(),
        apiService.getLocations(),
      ]);
      setRecords(recordsData.items);
      setTotalPages(recordsData.pages);
      setSpheres(spheresData);
      setLocations(locationsData);
    } catch (err) {
      setError('Ошибка загрузки данных');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [currentPage]);

  const resetForm = () => {
    setFormData({
      type: 'Income',
      sum: 0,
      description: '',
      date: new Date().toISOString().split('T')[0],
      location_id: 0,
      sphere_id: 0,
    });
    setEditingRecord(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      let recordData: RecordCreate;

      if (formData.type === 'Transfer') {
        if (formData.transfer_type === 'location') {
          recordData = {
            type: 'Transfer',
            sum: formData.sum,
            description: formData.description,
            date: formData.date,
            transfer_type: 'location',
            sphere_id: formData.sphere_id,
            from_location_id: formData.from_location_id!,
            to_location_id: formData.to_location_id!,
          };
        } else {
          recordData = {
            type: 'Transfer',
            sum: formData.sum,
            description: formData.description,
            date: formData.date,
            transfer_type: 'sphere',
            location_id: formData.location_id,
            from_sphere_id: formData.from_sphere_id!,
            to_sphere_id: formData.to_sphere_id!,
          };
        }
      } else {
        recordData = {
          type: formData.type,
          sum: formData.sum,
          location_id: formData.location_id,
          sphere_id: formData.sphere_id,
        };
        if (formData.description) recordData.description = formData.description;
        if (formData.date) recordData.date = formData.date;
      }

      if (editingRecord) {
        // For transfers, we need to handle both records
        if (formData.type === 'Transfer' && editingRecord.is_transfer) {
          // Delete the old transfer records and create new ones
          await apiService.deleteRecord(editingRecord.id);
          await apiService.createRecord(recordData);
        } else {
          await apiService.updateRecord(editingRecord.id, recordData);
        }
      } else {
        await apiService.createRecord(recordData);
      }

      setShowForm(false);
      resetForm();
      fetchData();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка сохранения записи');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Удалить запись?')) return;
    try {
      await apiService.deleteRecord(id);
      fetchData();
    } catch (err) {
      setError('Ошибка удаления записи');
    }
  };

  const handleEdit = (record: RecordRead) => {
    setEditingRecord(record);
    setFormData({
      type: record.operation_type as 'Income' | 'Spend' | 'Transfer',
      sum: record.sum,
      description: record.description || '',
      date: record.date ? record.date.split('T')[0] : new Date().toISOString().split('T')[0],
      location_id: record.location?.id || 0,
      sphere_id: record.sphere?.id || 0,
      transfer_type: record.is_transfer ? 'location' : undefined, // Default to location transfer
    });
    setShowForm(true);
  };

  const getOperationTypeLabel = (type: string) => {
    switch (type) {
      case 'Income': return 'Доход';
      case 'Spend': return 'Расход';
      case 'Transfer': return 'Перевод';
      default: return type;
    }
  };

  const getOperationTypeColor = (type: string) => {
    switch (type) {
      case 'Income': return 'text-green-600';
      case 'Spend': return 'text-red-600';
      case 'Transfer': return 'text-blue-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Записи</h1>
        <button
          onClick={() => {
            resetForm();
            setShowForm(true);
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          Добавить запись
        </button>
      </div>

      {/* Форма создания/редактирования */}
      {showForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                {editingRecord ? 'Редактировать запись' : 'Новая запись'}
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Тип операции</label>
                  <select
                    value={formData.type}
                    onChange={(e) => setFormData({ ...formData, type: e.target.value as any })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    required
                  >
                    <option value="Income">Доход</option>
                    <option value="Spend">Расход</option>
                    <option value="Transfer">Перевод</option>
                  </select>
                </div>

                {formData.type === 'Transfer' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Тип перевода</label>
                    <select
                      value={formData.transfer_type || 'location'}
                      onChange={(e) => setFormData({ ...formData, transfer_type: e.target.value as any })}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                      required
                    >
                      <option value="location">Между локациями</option>
                      <option value="sphere">Между сферами</option>
                    </select>
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700">Сумма</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.sum}
                    onChange={(e) => setFormData({ ...formData, sum: parseFloat(e.target.value) || 0 })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    required
                  />
                </div>

                {formData.type !== 'Transfer' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Локация</label>
                      <select
                        value={formData.location_id}
                        onChange={(e) => setFormData({ ...formData, location_id: parseInt(e.target.value) })}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                        required
                      >
                        <option value={0}>Выберите локацию</option>
                        {locations.map(loc => (
                          <option key={loc.id} value={loc.id}>{loc.name}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">Сфера</label>
                      <select
                        value={formData.sphere_id}
                        onChange={(e) => setFormData({ ...formData, sphere_id: parseInt(e.target.value) })}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                        required
                      >
                        <option value={0}>Выберите сферу</option>
                        {spheres.map(sph => (
                          <option key={sph.id} value={sph.id}>{sph.name}</option>
                        ))}
                      </select>
                    </div>
                  </>
                )}

                {formData.type === 'Transfer' && formData.transfer_type === 'location' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Сфера</label>
                      <select
                        value={formData.sphere_id}
                        onChange={(e) => setFormData({ ...formData, sphere_id: parseInt(e.target.value) })}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                        required
                      >
                        <option value={0}>Выберите сферу</option>
                        {spheres.map(sph => (
                          <option key={sph.id} value={sph.id}>{sph.name}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">Из локации</label>
                      <select
                        value={formData.from_location_id || 0}
                        onChange={(e) => setFormData({ ...formData, from_location_id: parseInt(e.target.value) })}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                        required
                      >
                        <option value={0}>Выберите локацию</option>
                        {locations.map(loc => (
                          <option key={loc.id} value={loc.id}>{loc.name}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">В локацию</label>
                      <select
                        value={formData.to_location_id || 0}
                        onChange={(e) => setFormData({ ...formData, to_location_id: parseInt(e.target.value) })}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                        required
                      >
                        <option value={0}>Выберите локацию</option>
                        {locations.map(loc => (
                          <option key={loc.id} value={loc.id}>{loc.name}</option>
                        ))}
                      </select>
                    </div>
                  </>
                )}

                {formData.type === 'Transfer' && formData.transfer_type === 'sphere' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Локация</label>
                      <select
                        value={formData.location_id}
                        onChange={(e) => setFormData({ ...formData, location_id: parseInt(e.target.value) })}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                        required
                      >
                        <option value={0}>Выберите локацию</option>
                        {locations.map(loc => (
                          <option key={loc.id} value={loc.id}>{loc.name}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">Из сферы</label>
                      <select
                        value={formData.from_sphere_id || 0}
                        onChange={(e) => setFormData({ ...formData, from_sphere_id: parseInt(e.target.value) })}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                        required
                      >
                        <option value={0}>Выберите сферу</option>
                        {spheres.map(sph => (
                          <option key={sph.id} value={sph.id}>{sph.name}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">В сферу</label>
                      <select
                        value={formData.to_sphere_id || 0}
                        onChange={(e) => setFormData({ ...formData, to_sphere_id: parseInt(e.target.value) })}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                        required
                      >
                        <option value={0}>Выберите сферу</option>
                        {spheres.map(sph => (
                          <option key={sph.id} value={sph.id}>{sph.name}</option>
                        ))}
                      </select>
                    </div>
                  </>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700">Описание</label>
                  <input
                    type="text"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Дата</label>
                  <input
                    type="date"
                    value={formData.date}
                    onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                  />
                </div>

                <div className="flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => {
                      setShowForm(false);
                      resetForm();
                    }}
                    className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400"
                  >
                    Отмена
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
                  >
                    {editingRecord ? 'Сохранить' : 'Создать'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center text-gray-500">Загрузка...</div>
      ) : (
        <>
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
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Действия</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {records.map(record => (
                    <tr key={record.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {record.date ? new Date(record.date).toLocaleDateString('ru-RU') : '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <span className={`font-medium ${getOperationTypeColor(record.operation_type)}`}>
                          {getOperationTypeLabel(record.operation_type)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-right">
                        <span className={getOperationTypeColor(record.operation_type)}>
                          ₽{record.sum.toLocaleString('ru-RU', { minimumFractionDigits: 2 })}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                        {record.location?.name || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                        {record.sphere?.name || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {record.description || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button
                          onClick={() => handleEdit(record)}
                          className="text-blue-600 hover:text-blue-900 mr-3"
                        >
                          Изменить
                        </button>
                        <button
                          onClick={() => handleDelete(record.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          Удалить
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {/* Пагинация */}
          {totalPages > 1 && (
            <div className="flex justify-center mt-6">
              <nav className="flex space-x-2">
                <button
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
                >
                  Предыдущая
                </button>
                <span className="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md">
                  {currentPage} из {totalPages}
                </span>
                <button
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
                >
                  Следующая
                </button>
              </nav>
            </div>
          )}
        </>
      )}
    </div>
  );
}; 