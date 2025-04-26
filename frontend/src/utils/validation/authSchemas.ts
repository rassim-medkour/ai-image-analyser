import { z } from 'zod';

// Schema for registration form
export const registerSchema = z.object({
  username: z.string()
    .min(3, "Username must be at least 3 characters")
    .max(30, "Username cannot exceed 30 characters")
    .regex(/^[a-zA-Z0-9_]+$/, "Username can only contain letters, numbers and underscores"),
  
  email: z.string()
    .email("Invalid email address"),
  
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .refine(
      (value) => /[A-Za-z]/.test(value) && /[0-9]/.test(value),
      { message: "Password must contain at least one letter and one number" }
    ),
  
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"],
});

// Type inference for the register schema
export type RegisterFormInputs = z.infer<typeof registerSchema>;

// Schema for login form
export const loginSchema = z.object({
  username_or_email: z.string()
    .min(1, "Username or email is required"),
  
  password: z.string()
    .min(1, "Password is required")
});

// Type inference for the login schema
export type LoginFormInputs = z.infer<typeof loginSchema>;