// User types
export interface UserBase {
  login: string;
  description?: string;
}

export interface UserCreate extends UserBase {
  password: string;
}

export interface UserUpdate extends UserBase {
  password?: string;
}

export interface UserInDBBase extends UserBase {
  id: number;
  is_admin: boolean;
}

export interface UserRead extends UserInDBBase {}

// Sphere types
export interface SphereBase {
  name: string;
  description?: string;
}

export interface SphereCreate extends SphereBase {
  reader_ids: number[];
  editor_ids: number[];
}

export interface SphereUpdate {
  name?: string;
  description?: string;
  reader_ids?: number[];
  editor_ids?: number[];
}

export interface SphereInDBBase extends SphereBase {
  id: number;
  owner_id: number;
}

export interface SphereRead extends SphereInDBBase {
  owner: UserRead;
}

// Location types
export interface LocationBase {
  name: string;
  description?: string;
}

export interface LocationCreate extends LocationBase {
  reader_ids: number[];
  editor_ids: number[];
}

export interface LocationUpdate {
  name?: string;
  description?: string;
  reader_ids?: number[];
  editor_ids?: number[];
}

export interface LocationInDBBase extends LocationBase {
  id: number;
  owner_id: number;
}

export interface LocationRead extends LocationInDBBase {
  owner: UserRead;
}

// Accounting Record types
export type OperationType = 'Income' | 'Spend' | 'Transfer';

export interface RecordBase {
  description?: string;
  date?: string; // ISO string
}

export interface RecordCreateIncome {
  type: 'Income';
  sum: number;
  location_id: number;
  sphere_id: number;
  description?: string;
  date?: string;
}

export interface RecordCreateSpend {
  type: 'Spend';
  sum: number;
  location_id: number;
  sphere_id: number;
  description?: string;
  date?: string;
}

export interface RecordCreateTransfer {
  type: 'Transfer';
  sum: number;
  description?: string;
  date?: string;
  transfer_type: 'location' | 'sphere';
  from_location_id?: number;
  to_location_id?: number;
  sphere_id?: number;
  from_sphere_id?: number;
  to_sphere_id?: number;
  location_id?: number;
}

export type RecordCreate = RecordCreateIncome | RecordCreateSpend | RecordCreateTransfer;

export interface RecordRead extends RecordBase {
  id: number;
  accounting_id: number;
  operation_type: OperationType;
  is_transfer: boolean;
  sum: number;
  owner_id: number;
  location: LocationRead | null;
  sphere: SphereRead | null;
}

// Pagination types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface PaginatedRecordRead extends PaginatedResponse<RecordRead> {}

// Auth types
export interface Token {
  access_token: string;
  token_type: string;
}

export interface TokenData {
  username?: string;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ErrorResponse {
  detail: string;
}

// Dashboard types
export interface BalanceItem {
  id: number;
  name: string;
  balance: number;
}

export interface DashboardData {
  total_balance: number;
  locations_balance: BalanceItem[];
  spheres_balance: BalanceItem[];
} 