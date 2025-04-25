import apiClient from "./client";
import { AuthResponse, User } from "../types";
import { AxiosResponse } from "axios";

// Interface for login request data
interface LoginRequest {
  username_or_email: string;
  password: string;
}

// Interface for registration request data
interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

/**
 * Log in a user with username/email and password
 */
export const login = async (data: LoginRequest): Promise<AuthResponse> => {
  const response: AxiosResponse<AuthResponse> = await apiClient.post(
    "/auth/login",
    data
  );
  return response.data;
};

/**
 * Register a new user
 */
export const register = async (
  data: RegisterRequest
): Promise<AuthResponse> => {
  const response: AxiosResponse<AuthResponse> = await apiClient.post(
    "/auth/register",
    data
  );
  return response.data;
};

/**
 * Get the current user's profile
 */
export const getCurrentUser = async (): Promise<User> => {
  const response: AxiosResponse<User> = await apiClient.get("/users/me");
  return response.data;
};
