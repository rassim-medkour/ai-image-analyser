import { Link } from 'react-router-dom';
import { UseFormReturn } from 'react-hook-form';
import { LoginFormInputs } from '../../utils/validation/authSchemas';

interface LoginFormProps {
  form: UseFormReturn<LoginFormInputs>;
  onSubmit: (data: LoginFormInputs) => void;
  isSubmitting: boolean;
  error: string | null;
}

/**
 * Presentational component for login form
 * Only handles UI rendering and form input
 */
const LoginForm: React.FC<LoginFormProps> = ({ 
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
          <h1>Login</h1>
          <h2>Sign in to your account</h2>
        </hgroup>
        
        {error && (
          <div className="error">
            <p className="text-error">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)}>
          <label htmlFor="username_or_email">
            Username or Email
            <input
              type="text"
              id="username_or_email"
              placeholder="johndoe or john@example.com"
              aria-invalid={errors.username_or_email ? "true" : "false"}
              disabled={isSubmitting}
              {...register("username_or_email")}
            />
          </label>
          {errors.username_or_email && <small className="text-error">{errors.username_or_email.message}</small>}

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

          <button 
            type="submit" 
            disabled={isSubmitting}
            aria-busy={isSubmitting}
          >
            {isSubmitting ? 'Signing in...' : 'Login'}
          </button>
        </form>

        <p>
          Don't have an account? <Link to="/register">Sign up</Link>
        </p>
      </div>
    </article>
  );
};

export default LoginForm;