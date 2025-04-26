import { ReactNode } from 'react';
import Header from './Header';
import Footer from './Footer';

interface LayoutProps {
    children: ReactNode;
}

/**
 * Main layout component that wraps the app content
 * Provides consistent header and footer across all pages
 */
const Layout: React.FC<LayoutProps> = ({ children }) => {
    // Calculate necessary spacing to account for fixed header
    const mainStyle: React.CSSProperties = {
        marginTop: '4rem', // Space for fixed header
        padding: '1rem 0',
        flex: 1,
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Header />
            <main className="container" style={mainStyle}>
                {children}
            </main>
            <Footer />
        </div>
    );
};

export default Layout;