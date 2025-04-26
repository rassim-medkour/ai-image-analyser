import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../store/auth/AuthContext';

/**
 * Header component with responsive navigation
 * Shows different navigation options based on authentication state
 */
const Header = () => {
    const { isAuthenticated, user, logout } = useAuth();
    const [menuOpen, setMenuOpen] = useState(false);

    const handleLogout = (e: React.MouseEvent) => {
        e.preventDefault();
        logout();
    };

    return (
        <nav className="container-fluid">
            <ul>
                <li>
                    <Link to="/" className="contrast">
                        <strong>AI Image Analyser</strong>
                    </Link>
                </li>
            </ul>

            {/* Mobile toggle */}
            <details role="list" dir="rtl" className="md-hidden" open={menuOpen}
                onToggle={() => setMenuOpen(!menuOpen)}>
                <summary aria-haspopup="listbox" role="button">
                    Menu
                </summary>
                <ul role="listbox">
                    {isAuthenticated ? (
                        <>
                            <li><Link to="/dashboard" onClick={() => setMenuOpen(false)}>Dashboard</Link></li>
                            <li><Link to="/images" onClick={() => setMenuOpen(false)}>Images</Link></li>
                            <li><Link to="/profile" onClick={() => setMenuOpen(false)}>Profile</Link></li>
                            <li><a href="#" onClick={handleLogout}>Logout</a></li>
                        </>
                    ) : (
                        <>
                            <li><Link to="/login" onClick={() => setMenuOpen(false)}>Login</Link></li>
                            <li><Link to="/register" onClick={() => setMenuOpen(false)}>Register</Link></li>
                        </>
                    )}
                </ul>
            </details>

            {/* Desktop menu */}
            <ul className="sm-hidden">
                {isAuthenticated ? (
                    <>
                        <li><Link to="/dashboard">Dashboard</Link></li>
                        <li><Link to="/images">Images</Link></li>
                        <li>
                            <details role="list" dir="rtl">
                                <summary aria-haspopup="listbox" role="button">
                                    {user?.username || 'Account'}
                                </summary>
                                <ul role="listbox">
                                    <li><Link to="/profile">Profile</Link></li>
                                    <li><a href="#" onClick={handleLogout}>Logout</a></li>
                                </ul>
                            </details>
                        </li>
                    </>
                ) : (
                    <>
                        <li><Link to="/login">Login</Link></li>
                        <li><Link to="/register" className="button">Register</Link></li>
                    </>
                )}
            </ul>
        </nav>
    );
};

export default Header;