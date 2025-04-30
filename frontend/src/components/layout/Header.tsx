import { useState, useEffect, useRef } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../store/auth/AuthContext';

const Header = () => {
    const { isAuthenticated, user, logout } = useAuth();
    const [menuOpen, setMenuOpen] = useState(false);
    const location = useLocation();
    const dropdownRef = useRef<HTMLDivElement>(null);
    const buttonRef = useRef<HTMLButtonElement>(null);

    // Close dropdown on route change
    useEffect(() => {
        setMenuOpen(false);
    }, [location.pathname]);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            // Only close if dropdown is open and click is outside both dropdown and button
            if (menuOpen &&
                dropdownRef.current &&
                buttonRef.current &&
                !dropdownRef.current.contains(event.target as Node) &&
                !buttonRef.current.contains(event.target as Node)) {
                setMenuOpen(false);
            }
        };

        // Add click handler to document
        document.addEventListener('mousedown', handleClickOutside);

        // Cleanup
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [menuOpen]);

    const handleLogout = (e: React.MouseEvent) => {
        e.preventDefault();
        logout();
    };

    // Toggle dropdown menu
    const handleDropdownToggle = (e: React.MouseEvent) => {
        // Stop propagation to prevent document click handler from firing immediately
        e.stopPropagation();
        setMenuOpen(prevState => !prevState);
    };

    // Helper to check if a link is active
    const isActive = (path: string) => location.pathname === path;

    return (
        <header className="navbar">
            <div className="navbar-container">
                <div>
                    <Link to="/" className="navbar-brand">
                        <strong>AI Image Analyser</strong>
                    </Link>
                </div>
                {/* Mobile toggle */}
                <details className="md-hidden" open={menuOpen}
                    onToggle={(e) => e.preventDefault()}>
                    <summary aria-haspopup="menu" role="button" onClick={() => setMenuOpen(!menuOpen)}>
                        Menu
                    </summary>
                    <nav className="navbar-list" style={{ flexDirection: 'column', gap: '0.25rem' }}>
                        {isAuthenticated ? (
                            <>
                                <Link to="/images" className="navbar-link">Images</Link>
                                <Link to="/images/upload" className="navbar-link">Upload Image</Link>
                                <Link to="/profile" className="navbar-link">Profile</Link>
                                <a href="#" onClick={handleLogout} className="navbar-link">Logout</a>
                            </>
                        ) : (
                            <>
                                <Link to="/login" className="navbar-link">Login</Link>
                                <Link to="/register" className="navbar-link navbar-link-register">Register</Link>
                            </>
                        )}
                    </nav>
                </details>
                {/* Desktop menu */}
                <nav className="navbar-list sm-hidden" style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', margin: 0, padding: 0 }}>
                    {isAuthenticated ? (
                        <>
                            <Link
                                to="/images"
                                className={`navbar-link${isActive('/images') ? ' active' : ''}`}
                            >
                                Images
                            </Link>
                            <Link
                                to="/images/upload"
                                className={`navbar-link${isActive('/images/upload') ? ' active' : ''}`}
                            >
                                Upload Image
                            </Link>
                            <div className="navbar-user-dropdown">
                                <button
                                    className={`navbar-link navbar-user-btn${menuOpen ? ' open' : ''}`}
                                    type="button"
                                    onClick={handleDropdownToggle}
                                    aria-haspopup="menu"
                                    aria-expanded={menuOpen}
                                    ref={buttonRef}
                                >
                                    <span className="navbar-user-label">{user?.username || 'Account'}</span>
                                    <span className="navbar-caret" aria-hidden="true">▼</span>
                                </button>
                                {menuOpen && (
                                    <div
                                        className="navbar-dropdown-menu"
                                        ref={dropdownRef}
                                    >
                                        <Link
                                            to="/profile"
                                            className={`navbar-link${isActive('/profile') ? ' active' : ''}`}
                                        >
                                            Profile
                                        </Link>
                                        <a
                                            href="#"
                                            onClick={(e) => {
                                                e.preventDefault();
                                                handleLogout(e);
                                            }}
                                            className="navbar-link"
                                        >
                                            Logout
                                        </a>
                                    </div>
                                )}
                            </div>
                        </>
                    ) : (
                        <>
                            <Link
                                to="/login"
                                className={`navbar-link${isActive('/login') ? ' active' : ''}`}
                            >
                                Login
                            </Link>
                            <Link
                                to="/register"
                                className={`navbar-link navbar-link-register${isActive('/register') ? ' active' : ''}`}
                            >
                                Register
                            </Link>
                        </>
                    )}
                </nav>
            </div>
        </header>
    );
};

export default Header;