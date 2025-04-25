import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../store/auth/AuthContext';

interface ProtectedRouteProps {
    redirectPath?: string;
}

/**
 * A route wrapper that checks for authentication
 * Redirects to login if the user isn't authenticated
 */
const ProtectedRoute = ({ redirectPath = '/login' }: ProtectedRouteProps) => {
    const { isAuthenticated, isLoading } = useAuth();

    // Show loading state while checking authentication
    if (isLoading) {
        return <div aria-busy="true">Loading...</div>;
    }

    // Redirect if not authenticated
    if (!isAuthenticated) {
        return <Navigate to={redirectPath} replace />;
    }

    // Render child routes if authenticated
    return <Outlet />;
};

export default ProtectedRoute;