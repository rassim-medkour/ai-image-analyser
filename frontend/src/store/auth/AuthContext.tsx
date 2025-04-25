import { createContext, useContext, useReducer, ReactNode, useEffect } from 'react';
import { AuthState, AuthContextType } from './authTypes';
import * as authApi from '../../api/auth';

// Initial auth state
const initialState: AuthState = {
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: Boolean(localStorage.getItem('token')),
    isLoading: false,
    error: null
};

// Context implementation
const AuthContext = createContext<AuthContextType | null>(null);

// Action types
type AuthAction =
    | { type: 'LOGIN_REQUEST' | 'REGISTER_REQUEST' | 'USER_LOADING' }
    | { type: 'LOGIN_SUCCESS' | 'REGISTER_SUCCESS'; payload: { user: AuthState['user']; token: string } }
    | { type: 'USER_LOADED'; payload: { user: AuthState['user'] } }
    | { type: 'AUTH_ERROR' | 'LOGIN_FAIL' | 'REGISTER_FAIL' | 'LOGOUT'; payload?: { error?: string } }
    | { type: 'CLEAR_ERRORS' };

// Reducer function
const authReducer = (state: AuthState, action: AuthAction): AuthState => {
    switch (action.type) {
        case 'USER_LOADING':
        case 'LOGIN_REQUEST':
        case 'REGISTER_REQUEST':
            return {
                ...state,
                isLoading: true,
                error: null
            };
        case 'USER_LOADED':
            return {
                ...state,
                isLoading: false,
                user: action.payload.user,
                isAuthenticated: true
            };
        case 'LOGIN_SUCCESS':
        case 'REGISTER_SUCCESS':
            localStorage.setItem('token', action.payload.token);
            return {
                ...state,
                user: action.payload.user,
                token: action.payload.token,
                isAuthenticated: true,
                isLoading: false,
                error: null
            };
        case 'AUTH_ERROR':
        case 'LOGIN_FAIL':
        case 'REGISTER_FAIL':
            localStorage.removeItem('token');
            return {
                ...state,
                user: null,
                token: null,
                isAuthenticated: false,
                isLoading: false,
                error: action.payload?.error || 'Authentication error'
            };
        case 'LOGOUT':
            localStorage.removeItem('token');
            return {
                ...state,
                user: null,
                token: null,
                isAuthenticated: false,
                isLoading: false,
                error: null
            };
        case 'CLEAR_ERRORS':
            return {
                ...state,
                error: null
            };
        default:
            return state;
    }
};

// Provider component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [state, dispatch] = useReducer(authReducer, initialState);

    // Load user on initial load if token exists
    useEffect(() => {
        const loadUser = async () => {
            if (!state.token) return;

            try {
                dispatch({ type: 'USER_LOADING' });
                const user = await authApi.getCurrentUser();
                dispatch({ type: 'USER_LOADED', payload: { user } });
            } catch (err) {
                console.error('Failed to load user', err);
                dispatch({ type: 'AUTH_ERROR' });
            }
        };

        if (state.token && !state.user) {
            loadUser();
        }
    }, [state.token]);

    // Login functionality
    const login = async (username_or_email: string, password: string): Promise<boolean> => {
        try {
            dispatch({ type: 'LOGIN_REQUEST' });
            const response = await authApi.login({ username_or_email, password });

            dispatch({
                type: 'LOGIN_SUCCESS',
                payload: { user: response.user, token: response.access_token }
            });
            return true;
        } catch (err: any) {
            const errorMessage = err.response?.data?.errors || 'Login failed';
            dispatch({
                type: 'LOGIN_FAIL',
                payload: { error: typeof errorMessage === 'string' ? errorMessage : 'Login failed' }
            });
            return false;
        }
    };

    // Register functionality
    const register = async (username: string, email: string, password: string): Promise<boolean> => {
        try {
            dispatch({ type: 'REGISTER_REQUEST' });
            const response = await authApi.register({ username, email, password });

            dispatch({
                type: 'REGISTER_SUCCESS',
                payload: { user: response.user, token: response.access_token }
            });
            return true;
        } catch (err: any) {
            const errorMessage = err.response?.data?.errors || 'Registration failed';
            dispatch({
                type: 'REGISTER_FAIL',
                payload: { error: typeof errorMessage === 'string' ? errorMessage : 'Registration failed' }
            });
            return false;
        }
    };

    // Logout functionality
    const logout = () => {
        dispatch({ type: 'LOGOUT' });
    };

    // Clear errors
    const clearErrors = () => {
        dispatch({ type: 'CLEAR_ERRORS' });
    };

    // Create value object with state and functions
    const authContextValue: AuthContextType = {
        ...state,
        login,
        register,
        logout,
        clearErrors
    };

    return (
        <AuthContext.Provider value={authContextValue}>
            {children}
        </AuthContext.Provider>
    );
};

// Custom hook to use the auth context
export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};