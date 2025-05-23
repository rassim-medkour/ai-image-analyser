import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../store/auth/AuthContext';
import LoginForm from '../../components/auth/LoginForm';
import { loginSchema, LoginFormInputs } from '../../utils/validation/authSchemas';

/**
 * Container component for user login
 * Handles form state, validation, and API interactions
 */
const Login = () => {
    const { login, isAuthenticated, isLoading, error, clearErrors } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [submitting, setSubmitting] = useState(false);

    // Get the return URL from location state or default to images
    const from = (location.state as { from?: string })?.from || '/images/';

    // Initialize form with Zod resolver
    const form = useForm<LoginFormInputs>({
        resolver: zodResolver(loginSchema),
        mode: 'onChange',
        defaultValues: {
            username_or_email: '',
            password: ''
        }
    });

    // Redirect if already authenticated
    useEffect(() => {
        if (isAuthenticated) {
            navigate(from, { replace: true });
        }
        // Only clear errors on unmount

        return () => { clearErrors(); };
    }, [isAuthenticated, navigate, from]);

    const handleSubmit = async (data: LoginFormInputs) => {
        setSubmitting(true);
        try {
            const success = await login(data.username_or_email, data.password);
            if (success) {
                navigate(from, { replace: true });
            }
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="container auth-container">
            <LoginForm
                form={form}
                onSubmit={handleSubmit}
                isSubmitting={submitting || isLoading}
                error={error}
            />
        </div>
    );
};

export default Login;