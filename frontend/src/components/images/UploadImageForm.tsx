import { UseFormReturn } from 'react-hook-form';

export interface UploadImageFormInputs {
    file: FileList;
}

interface UploadImageFormProps {
    form: UseFormReturn<UploadImageFormInputs>;
    onSubmit: (data: UploadImageFormInputs) => void;
    isSubmitting: boolean;
    error: string | null;
}

const UploadImageForm: React.FC<UploadImageFormProps> = ({ form, onSubmit, isSubmitting, error }) => {
    const { register, handleSubmit, formState: { errors } } = form;

    return (
        <article className="grid">
            <div>
                <hgroup>
                    <h1>Upload Image</h1>
                    <h2>Select an image to upload</h2>
                </hgroup>
                {error && (
                    <div className="error">
                        <p className="text-error">{error}</p>
                    </div>
                )}
                <form onSubmit={handleSubmit(onSubmit)} encType="multipart/form-data">
                    <label htmlFor="file">
                        Image File
                        <input
                            type="file"
                            id="file"
                            accept="image/*"
                            {...register('file', { required: 'Please select an image file.' })}
                            aria-invalid={!!errors.file}
                            disabled={isSubmitting}
                        />
                    </label>
                    {errors.file && <small className="text-error">{errors.file.message as string}</small>}

                    <button type="submit" disabled={isSubmitting} aria-busy={isSubmitting}>
                        {isSubmitting ? 'Uploading...' : 'Upload Image'}
                    </button>
                </form>
            </div>
        </article>
    );
};

export default UploadImageForm;
