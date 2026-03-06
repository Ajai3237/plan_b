import './footer.css';
import { icon } from '../../constants/icon';
import { FaFacebookF, FaInstagram } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import { HashLink } from 'react-router-hash-link';


const Footer = () => {
    return (
        <footer>
            <div className="text-center">
                <img src={icon.logo} alt="logo" className="footerLogo" data-aos="fade-up" />
                <div className="companyDesc" data-aos="fade-up">
                    At Akia Homes, we build more than just structures - we design spaces that are as unique as you are. Whether it's a dream home or a commercial hub, we tailor every project to reflect your unique needs, creating lasting spaces where your future story unfolds.
                </div>
                <div className="socialMedia " data-aos="fade-up">
                    <div className="d-flex justify-content-center">
                        <Link to="https://www.facebook.com/profile.php?id=61576856070452" target='_blank' className="">
                            <FaFacebookF />
                        </Link>
                        <Link to="https://www.instagram.com/akia.homes/" target='_blank' className="">
                            <FaInstagram />
                        </Link>
                    </div>
                </div>
            </div>
            <div className="footerEnd">
                <div className="container">
                    {/* <div className="d-flex flex-column flex-lg-row justify-content-between align-items-center h-100">
                        <ul className="list-unstyled d-flex flex-column flex-sm-row py-4 py-sm-2 py-lg-0 m-0">
                            {[
                                { path: "/", label: "Home" },
                                { path: "/about", label: "About Us" },
                                { path: "/models", label: "Models" },
                            ].map(({ path, label }) => (
                                <li key={path}>
                                    <Link to={path}> {label} </Link>
                                </li>
                            ))}
                            <li >
                                <HashLink smooth to="/#services">
                                    Services
                                </HashLink>
                            </li>
                            {[
                                { path: "/gallery", label: "Gallery" },
                                { path: "/contact", label: "Contact Us" },
                            ].map(({ path, label }) => (
                                <li key={path}>
                                    <Link to={path}> {label} </Link>
                                </li>
                            ))}
                        </ul>
                        <div className="mt-3 mt-md-0">
                            &copy;2025 Akiahomes. All rights reserved.
                        </div>
                    </div> */}

                    <div className="d-flex flex-column flex-lg-row justify-content-center align-items-center h-100">
  <div className="mt-3 mt-md-0 text-center">
    &copy;{new Date().getFullYear()} Akiahomes. All rights reserved.
  </div>
</div>

                </div>
            </div>
        </footer>
    )
}

export default Footer
