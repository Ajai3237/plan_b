import { useRef } from 'react';
import './about.css';
import PageBanner from '../../components/pageBanner/PageBanner';
import { image } from '../../constants/image';
import ImgLeft from '../../components/imgLeft/ImgLeft';
import ImageRight from '../../components/imgRIght/ImageRight';
import { FaArrowLeft, FaArrowRight } from 'react-icons/fa';
import Slider from "react-slick";



const Testimonial = () => {
    const sliderRef = useRef(null);
    var settings = {
        dots: false,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 1,
        arrows: false,
        autoplay: true,
        pauseOnHover: false,
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 2,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                }
            }
        ]
    };

    const testimonialContent = [
        {
            name: "Sanjeev Joshi",
            role: " Project Manager",
            image: image.frame
        },
        {
            name: "Ekta Gaba",
            role: "Construction Manager",
            image: image.frame1
        },
        {
            name: "D Sharma",
            role: "Project Coordinator ",
            image: image.frame2
        },

    ]

    // return (
    //     <section className="testimonial ourTeam">
    //         <div className="container">
    //             <div
    //                 className="sectionTop d-flex flex-column flex-lg-row justify-content-lg-between align-items-lg-end align-items-start">
    //                 <div className="faqTitle" data-aos="fade-up">
    //                     <h1 className="heading oswald text-uppercase">
    //                         Meet Our Team
    //                     </h1>
    //                     <h2 className="subHead text-uppercase">
    //                         You are only an email away from our support
    //                     </h2>
    //                 </div>
    //                 <div className="serviceArrow" data-aos="fade-right">
    //                     <button className="prev border border-white"
    //                         onClick={() => sliderRef.current.slickPrev()}
    //                     >
    //                         <FaArrowLeft />
    //                     </button>
    //                     <button className="next border border-white"
    //                         onClick={() => sliderRef.current.slickNext()}
    //                     >
    //                         <FaArrowRight />
    //                     </button>
    //                 </div>
    //             </div>
    //             <div className="teams" data-aos="fade-right">
    //                 <Slider ref={sliderRef} {...settings}>
    //                     {testimonialContent.map((content, index) => (
    //                         <div key={index}>
    //                             <div className="text-center m-auto">
    //                                 <div className="teamMember">
    //                                     <img src={content.image} alt="Team Member"
    //                                         className="w-100 object-fit-cover h-100" />
    //                                 </div>
    //                                 <h1>{content.name}</h1>
    //                                 <div className="pt-2">{content.role}</div>
    //                             </div>
    //                         </div>
    //                     ))}
    //                 </Slider>
    //             </div>
    //         </div>
    //     </section>
    // );
}

const About = () => {
    return (
        <>
            <section className="bannerSection">
                <div className="container">
                    <PageBanner bannerTitle='About Us' bannerLink={image.about} />
                </div>
            </section>


            {/* about us section */}
            <section className="aboutSection aboutPage">
                <div className="container">

                    <div className="bannerPic mt-0" data-aos="zoom-in">
                        <img src={image.about1} alt="Kitchen" className="w-100 h-100" />
                    </div>
                    <div className="aboutdescLand">
                        <h2 className="heading text-uppercase oswald">
                            Explore the Akia Homes Experience
                        </h2>
                        <p className="">
                            Akia Homes is a premier construction company dedicated to creating innovative, sustainable, and high-quality spaces that redefine modern living. With a commitment to craftsmanship and customer satisfaction, we turn visions into reality—building homes, commercial projects, and communities that inspire.
                        </p>
                    </div>
                </div>

            </section>
            {/* about us section end  */}

            {/* vision*/}
            <section className="servicesSection aboutVision mt-5 pt-5">
                <div className="container">
                    <ImgLeft
                        image={image.about2}
                        title={'Our Vision: Heart of your Home. Core of the Community.'}
                        paragraph={"At Akia Homes, we envision a future where quality, innovation, and sustainability shape every construction project. We strive to create exceptional spaces that inspire communities, enhance lifestyles, and stand the test of time. Through expert craftsmanship and cutting-edge solutions, we aim to redefine modern living —building not just structures, but lasting legacies."}
                    />
                </div>
            </section>
            {/* vision end */}

            {/* aboutMision  */}
            <section className="servicesSection aboutVision aboutMision">
                <div className="container">
                    <ImageRight
                        title={"Our Mission: Building Space for Life"}
                        src={image.about3}
                        paragraph={"At Akia Homes, our mission is to build excellence by crafting high-quality, sustainable, and innovative spaces that redefine modern living. We are committed to delivering precision, durability, and architectural brilliance, ensuring every project exceeds expectations."}
                    />
                </div>
            </section>
            {/* aboutMision end */}

            {/* ourTeam start */}
            <Testimonial />
            {/* ourTeam end */}

        </>
    )
}

export default About
