import { useRef, useEffect } from 'react';
import './index.css';
import { image } from '../../constants/image';
import { icon } from '../../constants/icon';
import { Link } from 'react-router-dom';
import { FaArrowLeft, FaArrowRight, FaFacebookF, FaInstagram } from 'react-icons/fa';
import Slider from "react-slick";
import AOS from 'aos';
import Faq from '../../components/faq/faq';
import OurStrenght from '../../components/ourStrenght/OurStrenght';


const baseSliderSettings = {
    dots: false,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    autoplay: true,
    pauseOnHover: true,
    responsive: [
        {
            breakpoint: 768,
            settings: {
                autoplaySpeed: 1500,
            }
        }
    ]
};

const ServicesSlider = () => {
    const sliderRef = useRef(null);

    const servicesData = [{
        LargePic: image.srv1,
        SmallPic: image.srve1,
        heading: "Custom Home Building",
        content: "Build homes tailored to meet your comfort, style designed to fit your exact needs, preferences, and lifestyle for a truly personalized living experience."
    },
    {
        LargePic: image.servc1,
        SmallPic: image.srvc1,
        heading: "Home Renovations & Interior Design",
        content: "Transform your existing space with personalised renovations and stylish interior designs to enhance functions, look, style and standard of living."
    },
    {
        LargePic: image.srv3,
        SmallPic: image.srve3,
        heading: "Architecture Design",
        content: "Leverage the services of our skilled architects for crafting innovative, functional designs that bring your vision to life, ensuring safety, sustainability, and lasting beauty."
    },
    {
        LargePic: image.srv4,
        SmallPic: image.srve4,
        heading: "Outdoor Design & Landscaping",
        content: "Design outdoor spaces and landscapes from gardens and patios to hardscaping and outdoor living areas that and take your outdoor lifestyle to the next level."
    },
    {
        LargePic: image.srv5,
        SmallPic: image.srve5,
        heading: "Smart Home Integration",
        content: "Meet your modern-day living needs by with advance smart technologies to enhance home automation, security and energy efficiency using our Smart Home Integration services."
    },
    {
        LargePic: image.srv6,
        SmallPic: image.srve6,
        heading: "General Contracting & Construction Management",
        content: "Manage and supervise all your construction projects needs from planning, design to construction and ensure your project quality, timeline, and budget are met."
    },
    {
        LargePic: image.srv7,
        SmallPic: image.srve7,
        heading: "Home & Commercial Plaza Sales",
        content: "Get your newly-built, ready-to-move dream homes and commercial plazas designed to meet modern day lifestyles and business needs that maximize value and convenience."
    },
    ]

    return (
        <>
            <div className="servicesSlider position-absolute" id='services'>
                <Slider ref={sliderRef} {...baseSliderSettings}>
                    {servicesData.map((service, index) => (
                        <div className="d-flex" key={index}>
                            <div className='servicesImgDivArea'>
                                <div className="servicesImgBox">
                                    <img src={service.LargePic} alt="Services" className="w-100 h-100 object-fit-cover" />
                                </div>
                                <div className="servicesSliderImg">
                                    <img src={service.SmallPic} alt="services" className="object-fit-cover w-100 h-100 rounded-circle" />
                                </div>
                            </div>
                            <div className="servicesDesc">
                                <h2 className="p-0 text-uppercase">{service.heading}</h2>
                                <p className="m-0">{service.content}</p>
                            </div>
                        </div>
                    ))}
                </Slider>
            </div>
            <div className="serviceArrow">
                <button className="prev border border-white" onClick={() => sliderRef.current.slickPrev()}>
                    <FaArrowLeft />
                </button>
                <button className="next border border-white" onClick={() => sliderRef.current.slickNext()}>
                    <FaArrowRight />
                </button>
            </div>
        </>
    );
};

const WorkDoneSection = () => {
    const sectionRef = useRef(null);

    useEffect(() => {
        AOS.init();
        const counters = sectionRef.current.querySelectorAll('.counter span');

        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    const el = entry.target;
                    el.classList.add('counted');
                    const target = +el.getAttribute('data-count');
                    const duration = 5000;
                    const frames = Math.round((duration / 1000) * 60);
                    let frame = 0;

                    const countUp = () => {
                        frame++;
                        const progress = Math.min(frame / frames, 1);
                        el.textContent = Math.floor(progress * target);
                        if (progress < 1) requestAnimationFrame(countUp);
                        else el.textContent = target;
                    };

                    requestAnimationFrame(countUp);
                }
            });
        }, { threshold: 0.6 });

        counters.forEach(counter => observer.observe(counter));
        return () => observer.disconnect();
    }, []);


    return (
        <section className="sectionworkDoneSection" ref={sectionRef}>
            <div className="container">
                <div className="workDone d-flex justify-content-between align-items-center" data-aos="fade-right">
                    <div className="counter oswald"><span className="oswald" data-count="90">0</span>+</div>
                    <div className="d-flex projectBox align-items-center">
                        <div>
                            <h1 className="heading oswald text-uppercase">
                                Residential Projects
                            </h1>
                            {/* <p>Lorem ipsum dolor sit amet consectetur. Ultrices neque lacus imperdiet fames sed
                                tincidunt nunc integer.</p> */}
                        </div>
                        <div className="workdoneProjImg position-relative">
                            <img src={image.img51} alt="working projects"
                                className="object-fit-cover w-100 h-100 rounded-circle" />
                        </div>
                    </div>
                </div>

                <div className="workDone d-flex justify-content-between align-items-center" data-aos="fade-right">
                    <div className="counter oswald"> <span className="oswald" data-count="20">0</span>+</div>
                    <div className="d-flex squaresBox align-items-center">
                        <div className="workdoneProjImg position-relative">
                            <img src={image.img52} alt="working projects"
                                className="object-fit-cover w-100 h-100" />
                        </div>
                        <div>
                            <h1 className="heading oswald text-uppercase">
                                Commercial Projects
                            </h1>
                            {/* <p>Lorem ipsum dolor sit amet consectetur. Ultrices neque.</p> */}
                        </div>
                    </div>
                </div>

                {/* <div className="workDone d-flex justify-content-between align-items-center" data-aos="fade-right">
                    <div className="counter oswald"><span className="oswald" data-count="250000">0</span></div>
                    <div className="d-flex squaresBox align-items-center">
                        <div className="workdoneProjImg sqft me-0 ms-xxl-0 ms-lg-5  position-relative">
                            <img src={image.img53} alt="working projects"
                                className="object-fit-cover w-100 h-100" />
                        </div>
                        <div>
                            <h1 className="heading oswald text-uppercase">
                                square foot
                            </h1>
                            <p>
                                Lorem ipsum dolor sit amet consectetur. Ultrices neque lacus imperdiet fames sed
                                tincidunt nunc integer.
                            </p>
                        </div>
                    </div>
                </div> */}
            </div>
        </section>
    );
};

const Testimonial = () => {
    const sliderRef = useRef(null);

    const testimonials = [{
        comment: "Lorem ipsum dolor sit amet consectetur. Ultrices neque lacus imperdiet fames sed tincidunt nunc integer. Facilisis in ullamcorper varius quam eu.",
        picture: image.testimonial1,
        name: "Jose M.",
        role: "home user"
    },
    {
        comment: "Lorem ipsum dolor sit amet consectetur. Ultrices neque lacus imperdiet fames sed tincidunt nunc integer.",
        picture: image.testimonial2,
        name: "T Marlin.",
        role: "office user"
    },
    {
        comment: "Lorem ipsum Facilisis in ullamcorper varius quam eu dolor sit amet consectetur. Ultrices neque Facilisis in ullamcorper varius quam eu lacus imperdiet fame s sed tincidunt nunc integer. Facilisis in ullamcorper varius quam eu.",
        picture: image.testimonial3,
        name: "Sticky K.",
        role: "Corporate user"
    },
        // {
        //         comment: "",
        //         picture:"",
        //         name:"",
        //         role:""
        //     },
    ];


    // return (
    //     <section className="testimonial">
    //         <div className="container">
    //             <div className="sectionTop d-flex flex-column flex-lg-row justify-content-lg-between align-items-lg-end align-items-start">
    //                 <div className="faqTitle" data-aos="fade-up">
    //                     <h1 className="heading oswald text-uppercase">testimonials</h1>
    //                     <h2 className="subHead text-uppercase">look at those who have worked with us</h2>
    //                 </div>
    //                 <div className="serviceArrow" data-aos="fade-right">
    //                     <button className="prev border border-white" onClick={() => sliderRef.current.slickPrev()}><FaArrowLeft /></button>
    //                     <button className="next border border-white" onClick={() => sliderRef.current.slickNext()}><FaArrowRight /></button>
    //                 </div>
    //             </div>
    //             <div className="testimonialSliders" data-aos="zoom-in">
    //                 <Slider ref={sliderRef} {...{ ...baseSliderSettings, autoplaySpeed: 2000 }}>
    //                     {testimonials.map((t, i) => (
    //                         <div key={i} className="d-flex flex-column justify-content-between">
    //                             <div className="testimonialText">“{t.comment}”</div>
    //                             <div className="testimonialAuthor d-flex justify-content-center align-items-center">
    //                                 <div className="authorDiv">
    //                                     <img src={t.picture} alt="author" className="w-100 rounded-circle object-fit-cover h-100" />
    //                                 </div>
    //                                 <div className="authorDesc">
    //                                     <h1 className="m-0">{t.name}</h1>
    //                                     <div className="text-uppercase">{t.role}</div>
    //                                 </div>
    //                             </div>
    //                         </div>
    //                     ))}
    //                 </Slider>
    //             </div>
    //         </div>
    //     </section>
    // );
}

const HomePage = () => {
    return (
        <>
            {/* banner section start  */}
            <section className="bannerSection">
                <div className="container">
                    {/* <PageBanner bannerTitle='embrace life' bannerLink={image.bannerIndex} /> */}
                    <h1 className="oswald pageHeading" data-aos="fade-up">
                        Redefine Architecture
                    </h1>
                    <div className="bannerPic">
                        <img
                            src="/Ak_homes.jpg"
                            alt="banner"
                            className="w-100 h-100 object-fit-cover"
                        />
                    </div>
                    <div className="bannerGrid">
                        <div className="homeBannerBox">
                            <h2 className="text-uppercase fw-bold p-0 m-0">Built for Life, Crafted with Excellence</h2>
                            <p className="py-4 m-auto m-lg-0">
                                Akia Homes stands apart with its commitment to innovation, precision, and sustainability in every construction project.
                            </p>
                            <Link className="btn btnFill" as={Link} to='/contact'>
                                Book Now
                            </Link>
                        </div>
                        <div className="text-center mvdwnBtn">
                            <a href="#aboutSection" className="moveDown bg-transparent position-relative">
                                <img src={icon.mouse} alt="Move Down" />
                            </a>
                        </div>
                        <div className="socialMedia d-flex justify-content-center justify-content-lg-end">
                            <div>
                                Social Media
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
                    </div>
                </div>
            </section>
            {/* banner section end  */}

            {/* about us section start */}
            <section id="aboutSection" className="aboutSection">
                <div className="container">
                    <div
                        className="sectionTop d-flex flex-column flex-lg-row justify-content-lg-between align-items-lg-end align-items-start">
                        <h1 className="heading oswald" data-aos="fade-right">
                            Crafting Your Dream Home
                        </h1>
                        <Link to={'/about'} className="btnTheme" data-aos="fade-up">read more</Link>
                    </div>
                    <div className="bannerPic mt-0" data-aos="zoom-in">
                        <img src={image.backAbout} alt="home page banner" className="w-100 h-100" />
                    </div>
                    <div className="aboutdescLand">
                        <h2 className="heading text-uppercase oswald">
                            about us
                        </h2>
                        <p className="">
                            Akia Homes is a premier construction company dedicated to creating innovative, sustainable, and high-quality spaces that redefine modern living. With a commitment to craftsmanship and customer satisfaction, we turn visions into reality—building homes, commercial projects, and communities that inspire.
                        </p>
                    </div>
                </div>
            </section>
            {/* about us section end */}

            {/* services start */}
            <section className="servicesSection">
                <div className="container">
                    <div className="homeService d-flex flex-column-reverse flex-xl-row justify-content-between">
                        <div className="servicesImgBox" data-aos="zoom-in">
                        </div>
                        <h1 className="heading oswald text-uppercase" data-aos="fade-right">
                            realiable and attuned to your needs
                        </h1>
                    </div>
                    <ServicesSlider />
                </div>
            </section>
            {/* services end */}

            {/* work done start */}
            <WorkDoneSection />
            {/* work done end */}

            {/* faq start  */}
            <Faq />
            {/* faq end  */}

            {/* our strenght start  */}
            <OurStrenght />
            {/* our strenght end  */}

            {/* testimonial start */}
            <Testimonial />
            {/* testimonial end */}
        </>
    )
}

export default HomePage
