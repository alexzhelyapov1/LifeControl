import React, { useEffect, useState } from 'react';
import apiService from '../services/api';
import type { LocationRead, LocationCreate, LocationUpdate } from '../types/index';

export const LocationsPage: React.FC = () => {
  const [locations, setLocations] = useState<LocationRead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newName, setNewName] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [adding, setAdding] = useState(false);
  const [editingLocation, setEditingLocation] = useState<LocationRead | null>(null);
  const [showForm, setShowForm] = useState(false);

  const fetchLocations = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await apiService.getLocations();
      setLocations(data);
    } catch (err) {
      setError('Ошибка загрузки локаций');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLocations();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAdding(true);
    try {
      if (editingLocation) {
        const locationUpdate: LocationUpdate = {
          name: newName,
          description: newDescription,
        };
        await apiService.updateLocation(editingLocation.id, locationUpdate);
        setEditingLocation(null);
      } else {
        const location: LocationCreate = {
          name: newName,
          description: newDescription,
          reader_ids: [],
          editor_ids: [],
        };
        await apiService.createLocation(location);
      }
      setNewName('');
      setNewDescription('');
      setShowForm(false);
      fetchLocations();
    } catch (err) {
      setError(editingLocation ? 'Ошибка обновления локации' : 'Ошибка добавления локации');
    } finally {
      setAdding(false);
    }
  };

  const handleEdit = (location: LocationRead) => {
    setEditingLocation(location);
    setNewName(location.name);
    setNewDescription(location.description || '');
    setShowForm(true);
  };

  const handleCancel = () => {
    setEditingLocation(null);
    setNewName('');
    setNewDescription('');
    setShowForm(false);
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Удалить локацию?')) return;
    try {
      await apiService.deleteLocation(id);
      fetchLocations();
    } catch (err) {
      setError('Ошибка удаления локации');
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Локации</h1>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Добавить локацию
        </button>
      </div>

      {/* Форма создания/редактирования */}
      {showForm && (
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h3 className="text-lg font-medium mb-4">
            {editingLocation ? 'Редактировать локацию' : 'Новая локация'}
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Название</label>
              <input
                type="text"
                placeholder="Название"
                value={newName}
                onChange={e => setNewName(e.target.value)}
                required
                className="w-full border rounded px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Описание</label>
              <input
                type="text"
                placeholder="Описание (необязательно)"
                value={newDescription}
                onChange={e => setNewDescription(e.target.value)}
                className="w-full border rounded px-3 py-2"
              />
            </div>
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={handleCancel}
                className="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400"
              >
                Отмена
              </button>
              <button
                type="submit"
                disabled={adding || !newName.trim()}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
              >
                {editingLocation ? 'Сохранить' : 'Добавить'}
              </button>
            </div>
          </form>
        </div>
      )}
      {loading ? (
        <div className="text-gray-500">Загрузка...</div>
      ) : error ? (
        <div className="text-red-500">{error}</div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          {locations.length === 0 ? (
            <div className="px-4 py-5 sm:p-6 text-gray-400 text-center">Локаций пока нет</div>
          ) : (
            <ul className="divide-y divide-gray-200">
              {locations.map(location => (
                <li key={location.id} className="flex items-center justify-between py-4 px-6">
                  <div className="flex-1">
                    <div className="font-semibold text-gray-900">{location.name}</div>
                    <div className="text-gray-500 text-sm">{location.description}</div>
                  </div>
                  <div className="flex space-x-3">
                    <button
                      onClick={() => handleEdit(location)}
                      className="text-blue-600 hover:text-blue-900 text-sm"
                    >
                      Изменить
                    </button>
                    <button
                      onClick={() => handleDelete(location.id)}
                      className="text-red-600 hover:text-red-900 text-sm"
                    >
                      Удалить
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}; 