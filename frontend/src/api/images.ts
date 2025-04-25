import apiClient from "./client";
import { Image } from "../types";
import { AxiosResponse } from "axios";

/**
 * Get all images for the current user
 */
export const getUserImages = async (): Promise<Image[]> => {
  const response: AxiosResponse<Image[]> = await apiClient.get("/images");
  return response.data;
};

/**
 * Get a single image by ID
 */
export const getImage = async (imageId: number): Promise<Image> => {
  const response: AxiosResponse<Image> = await apiClient.get(
    `/images/${imageId}`
  );
  return response.data;
};

/**
 * Upload a new image
 * @param file The image file to upload
 * @param metadata Optional metadata for the image
 */
export const uploadImage = async (
  file: File,
  metadata?: Record<string, string>
): Promise<Image> => {
  const formData = new FormData();
  formData.append("file", file);

  // Add any metadata as form fields
  if (metadata) {
    Object.entries(metadata).forEach(([key, value]) => {
      formData.append(key, value);
    });
  }

  // Use multipart/form-data for file uploads
  const response: AxiosResponse<Image> = await apiClient.post(
    "/images/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

/**
 * Delete an image by ID
 */
export const deleteImage = async (imageId: number): Promise<void> => {
  await apiClient.delete(`/images/${imageId}`);
};
