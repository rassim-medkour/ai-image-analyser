import { z } from 'zod';

export const uploadImageSchema = z.object({
  file: z
    .any()
    .refine((files) => files && files.length === 1, 'Please select an image file.'),
  title: z.string().max(100, 'Title must be at most 100 characters.').optional(),
  description: z.string().max(500, 'Description must be at most 500 characters.').optional(),
});

export type UploadImageSchemaType = z.infer<typeof uploadImageSchema>;
