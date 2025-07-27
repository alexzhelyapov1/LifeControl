import React, { useEffect, useState } from 'react';
import apiService from '../services/api';
import type { LocationRead, LocationCreate } from '../types/index';

export const LocationsPage: React.FC = () => {
  const [locations, setLocations] = useState<LocationRead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newName, setNewName] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [adding, setAdding] = useState(false);

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

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    setAdding(true);
    try {
      const location: LocationCreate = {
        name: newName,
        description: newDescription,
        reader_ids: [],
        editor_ids: [],
      };
      await apiService.createLocation(location);
      setNewName('');
      setNewDescription('');
      fetchLocations();
    } catch (err) {
      setError('Ошибка добавления локации');
    } finally {
      setAdding(false);
    }
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
      <h1 className="text-2xl font-bold mb-4">Локации</h1>
      <form onSubmit={handleAdd} className="flex flex-col md:flex-row gap-2 mb-6">
        <input
          type="text"
          placeholder="Название"
          value={newName}
          onChange={e => setNewName(e.target.value)}
          required
          className="border rounded px-3 py-2 flex-1"
        />
        <input
          type="text"
          placeholder="Описание (необязательно)"
          value={newDescription}
          onChange={e => setNewDescription(e.target.value)}
          className="border rounded px-3 py-2 flex-1"
        />
        <button
          type="submit"
          disabled={adding || !newName.trim()}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          Добавить
        </button>
      </form>
      {loading ? (
        <div className="text-gray-500">Загрузка...</div>
      ) : error ? (
        <div className="text-red-500">{error}</div>
      ) : (
        <ul className="divide-y divide-gray-200">
          {locations.map(location => (
            <li key={location.id} className="flex items-center justify-between py-3">
              <div>
                <div className="font-semibold text-gray-900">{location.name}</div>
                <div className="text-gray-500 text-sm">{location.description}</div>
              </div>
              <button
                onClick={() => handleDelete(location.id)}
                className="text-red-600 hover:underline text-sm"
              >
                Удалить
              </button>
            </li>
          ))}
          {locations.length === 0 && <li className="text-gray-400 py-4 text-center">Нет локаций</li>}
        </ul>
      )}
    </div>
  );
}; 