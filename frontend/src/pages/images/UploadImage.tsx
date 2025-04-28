import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useNavigate } from 'react-router-dom';
import UploadImageForm, { UploadImageFormInputs } from '../../components/images/UploadImageForm';
import { uploadImageSchema } from '../../utils/validation/imageSchemas';
import { uploadImage } from '../../api/images';

type UploadImageSchemaType = z.infer<typeof uploadImageSchema>;

const UploadImage = () => {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const form = useForm<UploadImageFormInputs>({
    resolver: zodResolver(uploadImageSchema),
    mode: 'onChange',
    defaultValues: {
      file: undefined,
    },
  });

  const handleSubmit = async (data: UploadImageFormInputs) => {
    setError(null);
    setSubmitting(true);
    try {
      const file = data.file && data.file[0];
      if (!file) {
        setError('Please select an image file.');
        setSubmitting(false);
        return;
      }
      await uploadImage(file);
      navigate('/images');
    } catch (err: any) {
      setError(err?.response?.data?.errors || 'Image upload failed.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="container auth-container">
      <UploadImageForm
        form={form}
        onSubmit={handleSubmit}
        isSubmitting={submitting}
        error={error}
      />
    </div>
  );
};

export default UploadImage;
