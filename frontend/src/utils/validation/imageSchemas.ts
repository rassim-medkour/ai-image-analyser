import { z } from "zod";

export const uploadImageSchema = z.object({
  file: z
    .any()
    .refine(
      (files) => files && files.length === 1,
      "Please select an image file."
    ),
});

export type UploadImageSchemaType = z.infer<typeof uploadImageSchema>;
