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
    return (
        <>
            <Header />
            <main className="container">
                {children}
            </main>
            <Footer />
        </>
    );
};

export default Layout;