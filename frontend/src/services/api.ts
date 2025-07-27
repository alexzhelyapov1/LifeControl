import axios from 'axios';
import type { AxiosInstance, AxiosResponse } from 'axios';
import type {
  UserCreate,
  UserRead,
  Token,
  SphereCreate,
  SphereRead,
  LocationCreate,
  LocationRead,
  RecordCreate,
  RecordRead,
  PaginatedRecordRead
} from '../types/index';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: 'http://localhost:8000/api/v1',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle auth errors
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(username: string, password: string): Promise<Token> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response: AxiosResponse<Token> = await this.api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async register(userData: UserCreate): Promise<UserRead> {
    const response: AxiosResponse<UserRead> = await this.api.post('/auth/register', userData);
    return response.data;
  }

  async getCurrentUser(): Promise<UserRead> {
    const response: AxiosResponse<UserRead> = await this.api.get('/auth/me');
    return response.data;
  }

  // Sphere endpoints
  async getSpheres(): Promise<SphereRead[]> {
    const response: AxiosResponse<SphereRead[]> = await this.api.get('/spheres/');
    return response.data;
  }

  async createSphere(sphereData: SphereCreate): Promise<SphereRead> {
    const response: AxiosResponse<SphereRead> = await this.api.post('/spheres/', sphereData);
    return response.data;
  }

  async getSphere(id: number): Promise<SphereRead> {
    const response: AxiosResponse<SphereRead> = await this.api.get(`/spheres/${id}`);
    return response.data;
  }

  async updateSphere(id: number, sphereData: Partial<SphereCreate>): Promise<SphereRead> {
    const response: AxiosResponse<SphereRead> = await this.api.put(`/spheres/${id}`, sphereData);
    return response.data;
  }

  async deleteSphere(id: number): Promise<void> {
    await this.api.delete(`/spheres/${id}`);
  }

  // Location endpoints
  async getLocations(): Promise<LocationRead[]> {
    const response: AxiosResponse<LocationRead[]> = await this.api.get('/locations/');
    return response.data;
  }

  async createLocation(locationData: LocationCreate): Promise<LocationRead> {
    const response: AxiosResponse<LocationRead> = await this.api.post('/locations/', locationData);
    return response.data;
  }

  async getLocation(id: number): Promise<LocationRead> {
    const response: AxiosResponse<LocationRead> = await this.api.get(`/locations/${id}`);
    return response.data;
  }

  async updateLocation(id: number, locationData: Partial<LocationCreate>): Promise<LocationRead> {
    const response: AxiosResponse<LocationRead> = await this.api.put(`/locations/${id}`, locationData);
    return response.data;
  }

  async deleteLocation(id: number): Promise<void> {
    await this.api.delete(`/locations/${id}`);
  }

  // Record endpoints
  async getRecords(page: number = 1, size: number = 20): Promise<PaginatedRecordRead> {
    const response: AxiosResponse<PaginatedRecordRead> = await this.api.get('/records/', {
      params: { page, size }
    });
    return response.data;
  }

  async createRecord(recordData: RecordCreate): Promise<RecordRead> {
    const response: AxiosResponse<RecordRead> = await this.api.post('/records/', recordData);
    return response.data;
  }

  async getRecord(id: number): Promise<RecordRead> {
    const response: AxiosResponse<RecordRead> = await this.api.get(`/records/${id}`);
    return response.data;
  }

  async updateRecord(id: number, recordData: Partial<RecordCreate>): Promise<RecordRead> {
    const response: AxiosResponse<RecordRead> = await this.api.put(`/records/${id}`, recordData);
    return response.data;
  }

  async deleteRecord(id: number): Promise<void> {
    await this.api.delete(`/records/${id}`);
  }
}

export const apiService = new ApiService();
export default apiService; 