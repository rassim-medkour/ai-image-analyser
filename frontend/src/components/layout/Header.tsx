import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../store/auth/AuthContext';

/**
 * Header component with responsive navigation
 * Full-width header that sits at the very top of the page
 */
const Header = () => {
    const { isAuthenticated, user, logout } = useAuth();
    const [menuOpen, setMenuOpen] = useState(false);

    const handleLogout = (e: React.MouseEvent) => {
        e.preventDefault();
        logout();
    };

    // Style definitions for true full-width header
    const headerStyle: React.CSSProperties = {
        width: '100%',
        backgroundColor: 'var(--pico-background-color)',
        borderBottom: '1px solid var(--pico-muted-border-color)',
        boxShadow: '0 2px 4px rgba(0,0,0,.1)',
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 1000,
        padding: '0.5rem 0',
    };

    // Inner nav container with proper padding
    const navStyle: React.CSSProperties = {
        width: '100%',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 1rem',
        maxWidth: '100%',
    };

    return (
        <header style={headerStyle}>
            <div style={navStyle}>
                <div>
                    <Link to="/" className="contrast" style={{ textDecoration: 'none' }}>
                        <strong>AI Image Analyser</strong>
                    </Link>
                </div>

                {/* Mobile toggle */}
                <details className="md-hidden" open={menuOpen}
                    onToggle={() => setMenuOpen(!menuOpen)}>
                    <summary aria-haspopup="listbox" role="button">
                        Menu
                    </summary>
                    <ul role="listbox">
                        {isAuthenticated ? (
                            <>
                                <li><Link to="/dashboard" onClick={() => setMenuOpen(false)}>Dashboard</Link></li>
                                <li><Link to="/images" onClick={() => setMenuOpen(false)}>Images</Link></li>
                                <li><Link to="/images/upload" onClick={() => setMenuOpen(false)}>Upload Image</Link></li>
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
                <ul className="sm-hidden" style={{ display: 'flex', gap: '1rem', margin: 0, padding: 0, listStyle: 'none' }}>
                    {isAuthenticated ? (
                        <>
                            <li><Link to="/dashboard">Dashboard</Link></li>
                            <li><Link to="/images">Images</Link></li>
                            <li><Link to="/images/upload">Upload Image</Link></li>
                            <li>
                                <details role="list">
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
            </div>
        </header>
    );
};

export default Header;