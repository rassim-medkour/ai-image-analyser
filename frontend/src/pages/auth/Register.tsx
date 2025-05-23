import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../store/auth/AuthContext';
import RegisterForm from '../../components/auth/RegisterForm';
import { registerSchema, RegisterFormInputs } from '../../utils/validation/authSchemas';

/**
 * Container component for user registration
 * Handles form state, validation, and API interactions
 */
const Register = () => {
    const { register: registerUser, isAuthenticated, isLoading, error, clearErrors } = useAuth();
    const navigate = useNavigate();
    const [submitting, setSubmitting] = useState(false);

    // Initialize form with Zod resolver
    const form = useForm<RegisterFormInputs>({
        resolver: zodResolver(registerSchema),
        mode: 'onChange',
        defaultValues: {
            username: '',
            email: '',
            password: '',
            confirmPassword: ''
        }
    });

    // Redirect if already authenticated
    useEffect(() => {
        if (isAuthenticated) {
            navigate('/images/');
        }
        // Only clear errors on unmount

        return () => { clearErrors(); };
    }, [isAuthenticated, navigate]);

    const handleSubmit = async (data: RegisterFormInputs) => {
        setSubmitting(true);
        try {
            const success = await registerUser(data.username, data.email, data.password);
            if (success) {
                navigate('/images/');
            }
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="container auth-container">
            <RegisterForm
                form={form}
                onSubmit={handleSubmit}
                isSubmitting={submitting || isLoading}
                error={error}
            />
        </div>
    );
};

export default Register;