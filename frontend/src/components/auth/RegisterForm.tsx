import { Link } from 'react-router-dom';
import { UseFormReturn } from 'react-hook-form';
import { RegisterFormInputs } from '../../utils/validation/authSchemas';

interface RegisterFormProps {
    form: UseFormReturn<RegisterFormInputs>;
    onSubmit: (data: RegisterFormInputs) => void;
    isSubmitting: boolean;
    error: string | null;
}

/**
 * Presentational component for registration form
 * Only handles UI rendering and form input
 */
const RegisterForm: React.FC<RegisterFormProps> = ({
    form,
    onSubmit,
    isSubmitting,
    error
}) => {
    const { register, handleSubmit, formState: { errors } } = form;

    return (
        <article className="grid">
            <div>
                <hgroup>
                    <h1>Register</h1>
                    <h2>Create a new account</h2>
                </hgroup>

                {error && (
                    <div className="error">
                        <p className="text-error">{error}</p>
                    </div>
                )}

                <form onSubmit={handleSubmit(onSubmit)}>
                    <label htmlFor="username">
                        Username
                        <input
                            type="text"
                            id="username"
                            placeholder="johndoe"
                            aria-invalid={errors.username ? "true" : "false"}
                            disabled={isSubmitting}
                            {...register("username")}
                        />
                    </label>
                    {errors.username && <small className="text-error">{errors.username.message}</small>}

                    <label htmlFor="email">
                        Email
                        <input
                            type="email"
                            id="email"
                            placeholder="john.doe@example.com"
                            aria-invalid={errors.email ? "true" : "false"}
                            disabled={isSubmitting}
                            {...register("email")}
                        />
                    </label>
                    {errors.email && <small className="text-error">{errors.email.message}</small>}

                    <label htmlFor="password">
                        Password
                        <input
                            type="password"
                            id="password"
                            placeholder="••••••••"
                            aria-invalid={errors.password ? "true" : "false"}
                            disabled={isSubmitting}
                            {...register("password")}
                        />
                    </label>
                    {errors.password && <small className="text-error">{errors.password.message}</small>}

                    <label htmlFor="confirmPassword">
                        Confirm Password
                        <input
                            type="password"
                            id="confirmPassword"
                            placeholder="••••••••"
                            aria-invalid={errors.confirmPassword ? "true" : "false"}
                            disabled={isSubmitting}
                            {...register("confirmPassword")}
                        />
                    </label>
                    {errors.confirmPassword && <small className="text-error">{errors.confirmPassword.message}</small>}

                    <button
                        type="submit"
                        disabled={isSubmitting}
                        aria-busy={isSubmitting}
                    >
                        {isSubmitting ? 'Registering...' : 'Register'}
                    </button>
                </form>

                <p>
                    Already have an account? <Link to="/login">Sign in</Link>
                </p>
            </div>
        </article>
    );
};

export default RegisterForm;