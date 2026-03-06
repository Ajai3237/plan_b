import { useState } from 'react';
import './contact.css'
import Faq from '../../components/faq/faq';
import { VscDeviceMobile } from 'react-icons/vsc';
import { GoMail } from 'react-icons/go';
import { toast } from 'react-toastify';


const ContactForm = () => {
    const [loading, setLoading] = useState(false);

    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        message: ''
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const googleFormURL = 'https://docs.google.com/forms/d/e/1FAIpQLSdonWwgBDPvh-xIC9DTznH3wKMIcO1qzPRRgMCsw4Nh9PIGEw/formResponse';

        const formBody = new URLSearchParams();
        formBody.append('entry.964294235', formData.firstName);
        formBody.append('entry.1767686650', formData.lastName);
        formBody.append('entry.1292076436', formData.email);
        formBody.append('entry.1429082648', formData.phone);
        formBody.append('entry.1003684990', formData.message);

        try {
            await fetch(googleFormURL, {
                method: 'POST',
                mode: 'no-cors',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formBody.toString(),
            });

            toast.success('Form submitted successfully!', {
                position: 'top-center',
                autoClose: 3000,
            });
            setFormData({ firstName: '', lastName: '', email: '', phone: '', message: '' });

        } catch (error) {
            toast.error('Failed to submit form. Please try again.', {
                position: 'top-center',
                autoClose: 3000,
            });
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="contactSection">
            <div className="container">
                <div className="sectionContactBox d-flex flex-column-reverse flex-xl-row justify-content-between">

                    {/* Contact Info Area */}
                    <div className="contactArea" data-aos="fade-up">
                        <h1 className="heading oswald text-uppercase">Customer Care</h1>

                        <div className="queryBox">
                            <h4 className="contactHead">For any query call us</h4>
                            <div className="d-flex align-items-center">
                                <label htmlFor="phone">
                                    <VscDeviceMobile />
                                </label>
                                <a
                                    href="tel:+1 (587) 334-8808"
                                    id="phone"
                                    className="text-white text-decoration-none"
                                >
                                    +1 (587) 334-8808
                                </a>
                            </div>
                        </div>

                        <div className="queryBox">
                            <h4 className="contactHead">General query</h4>
                            <div className="d-flex align-items-center">
                                <label htmlFor="emailContact">
                                    <GoMail />
                                </label>
                                <a
                                    href="mailto:akiahomesinc@gmail.com"
                                    id="emailContact"
                                    className="text-white text-decoration-none"
                                >
                                    Akiahomesinc@gmail.com
                                </a>
                            </div>
                        </div>
                    </div>

                    {/* Contact Form Area */}
                    <div className="contactForm" data-aos="fade-right">
                        <h1 className="heading oswald text-uppercase">Contact akiahomes</h1>
                        <p>
                            We love taking questions. If you're looking for something specific, we may have already
                            answered it in our <a href="#" className="text-white">FAQ</a>. Otherwise, send us your
                            question by filling out the form below.
                        </p>
                        <form onSubmit={handleSubmit}>
                            <label htmlFor="firstname" className="form-label">First Name</label>
                            <input
                                type="text"
                                className="form-control"
                                id="firstname"
                                placeholder="First Name"
                                value={formData.firstName}
                                onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                                required
                            />
                            <label htmlFor="lastname" className="form-label">Last Name</label>
                            <input
                                type="text"
                                className="form-control"
                                id="lastname"
                                placeholder="Last Name"
                                value={formData.lastName}
                                onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                                required
                            />

                            <label htmlFor="email" className="form-label">Email</label>
                            <input
                                type="email"
                                className="form-control"
                                id="email"
                                placeholder="Email"
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                required
                            />

                            <label htmlFor="phone" className="form-label">Phone</label>
                            <input
                                type="number"
                                className="form-control"
                                id="phone"
                                placeholder="7037012950"
                                value={formData.phone}
                                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                                required
                            />
                            {/* <label htmlFor="Topic" className="form-label">Topic</label>
                            <select className="form-select" id="Topic" aria-label="Select">
                                <option defaultValue>Topic</option>
                                <option value="1">Select Topic 1</option>
                                <option value="2">Select Topic 2</option>
                                <option value="3">Select Topic 3</option>
                            </select> */}

                            <label htmlFor="message" className="form-label">Message</label>
                            <textarea
                                className="form-control"
                                id="message"
                                rows="3"
                                placeholder="Write here..."
                                value={formData.message}
                                onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                                required
                            ></textarea>

                            <button type="submit" className="btnTheme" disabled={loading}>
                                {loading ? 'Submitting...' : 'Submit'}
                            </button>
                        </form>
                    </div>

                </div>
            </div>
        </section>
    );
};

const Contact = () => {
    return (
        <>
            {/* banner start */}
            <section className="bannerSection contactBanner">
                <div className="container">
                    <h1 className="oswald pageHeading" data-aos="fade-up">
                        Contact us
                    </h1>
                </div>
            </section>
            {/* banner end */}
            <ContactForm />
            {/* faq  */}
            <Faq />

            {/* map section */}
            <section className="mapSection">
                <div className="container">
                    <div className="bannerPic">
                        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2378.626646484345!2d-113.5120522234087!3d53.403618272305984!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x53a01ddaa161fcb9%3A0xb30fcd2999f15747!2s3190%20Checknita%20Way%20SW%2C%20Edmonton%2C%20AB%20T6W%204W7%2C%20Canada!5e0!3m2!1sen!2sin!4v1749664503534!5m2!1sen!2sin" width="600" height="450" className='border-0 w-100 bnp h-100' allowFullScreen="" loading="lazy" referrerPolicy="no-referrer-when-downgrade"></iframe>
                    </div>
                </div>
            </section>


        </>
    )
}

export default Contact
