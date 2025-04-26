export interface User {
  id: number;
  username: string;
  email: string;
  created_at?: string;
}

export interface Image {
  id: number;
  filename: string;
  original_filename: string;
  s3_url: string;
  s3_key: string;
  upload_date: string;
  file_size: number;
  file_type: string;
  ai_description?: string;
  user_id: number;
}

export interface AuthResponse {
  user: User;
  access_token: string;
}

export interface ApiError {
  errors: string | Record<string, string[]>;
}
