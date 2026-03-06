import { useCallback, useEffect, useRef, useState } from 'react';
import { icon } from '../../constants/icon';
import { Link, useLocation } from 'react-router-dom';
import AOS from "aos";
import './navbar.css';
import { HashLink } from 'react-router-hash-link';

function Navbar() {
    const navRef = useRef(null);
    const [isOpen, setIsOpen] = useState(false);
    const { pathname } = useLocation();

    const handleToggle = useCallback(() => setIsOpen(prev => !prev), []);
    const closeNav = useCallback(() => setIsOpen(false), []);
    const isActive = useCallback((path) => (pathname === path ? "active" : ""), [pathname]);

    // Collapse menu on outside click
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (navRef.current && !navRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);


    useEffect(() => {
        AOS.init({ duration: 1200 });
        closeNav();
    }, [pathname, closeNav]);

    return (
        <header className={`sticky-top ${isOpen ? "nav-open" : ""}`} ref={navRef}>
            <nav className="navbar navbar-expand-xxl">
                <div className="container-fluid p-0">
                    <a className="navbar-brand m-0" href="#">
                        <img src={icon.logo} alt="company logo" className="w-100" />
                    </a>

                    <button
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navbarNav"
                        aria-controls="navbarNav"
                        aria-expanded={isOpen}
                        aria-label="Toggle navigation"
                        className={`navbar-toggler ${isOpen ? '' : 'collapsed'}`}
                        onClick={handleToggle}
                    >
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>

                    <div className={`collapse navbar-collapse ${isOpen ? "show" : ""}`} id="navbarNav">
                        <ul className="navbar-nav navbar-nav1 w-100 justify-content-center">
                            {[
                                { path: "/", label: "Home" },
                                { path: "/about", label: "About Us" },
                                { path: "/models", label: "Models" },
                            ].map(({ path, label }) => (
                                <li className="nav-item" key={path}>
                                    <Link
                                        className={`nav-link ${isActive(path)}`}
                                        to={path}
                                        onClick={closeNav}
                                    >
                                        {label}
                                    </Link>
                                </li>
                            ))}

                            {/* Services link - handled separately */}
                            <li className="nav-item">
                                <HashLink smooth to="/#services" className="nav-link" onClick={closeNav}>
                                    Services
                                </HashLink>
                            </li>
                            {[
                                { path: "/gallery", label: "Gallery" },
                                { path: "/contact", label: "Contact Us" },
                            ].map(({ path, label }) => (
                                <li className="nav-item" key={path}>
                                    <Link
                                        className={`nav-link ${isActive(path)}`}
                                        to={path}
                                        onClick={closeNav}
                                    >
                                        {label}
                                    </Link>
                                </li>
                            ))}
                        </ul>

                        <ul className="navbar-nav navbar-nav2 justify-content-end m-auto">
                            <li className="nav-item">
                                <Link to="/contact" className="nav-link bookNow" onClick={closeNav}>
                                    Book Now
                                </Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
    );
}

export default Navbar;
