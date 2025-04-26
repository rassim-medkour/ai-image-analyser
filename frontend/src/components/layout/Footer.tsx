/**
 * Footer component with copyright and information
 */
const Footer = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="container">
            <small>
                <p>© {currentYear} AI Image Analyser</p>
                <p>
                    <a href="#" className="secondary">Terms</a> •
                    <a href="#" className="secondary"> Privacy</a>
                </p>
            </small>
        </footer>
    );
};

export default Footer;