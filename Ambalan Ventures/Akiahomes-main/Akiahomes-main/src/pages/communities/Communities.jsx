import './communities.css';
import PageBanner from '../../components/pageBanner/PageBanner';
import { image } from '../../constants/image';
import ImageRight from '../../components/imgRIght/ImageRight';
import ImgLeft from '../../components/imgLeft/ImgLeft';
import OurStrenght from '../../components/ourStrenght/OurStrenght';

const Communities = () => {

    const communityLink = [
        { name: "#about1", address: "Ivy" },
        { name: "#about2", address: "⁠Rosè" },
        { name: "#about3", address: "⁠Kiara" },
        { name: "#about4", address: "Azalea" },
        { name: "#about5", address: "Orchid" },
    ]
    return (
        <>
            {/* banner start */}
            <section className="bannerSection communityBanner">
                <div className="container">
                    <PageBanner bannerTitle='Models' bannerLink={image.communityBanner} />
                </div>
            </section>
            {/* banner end */}

            {/* community link start */}
            <section className="communityLinks" data-aos="fade-up">
                <div className="container">
                    <ul className="list-unstyled">
                        {communityLink.map((content, index) => (
                            <li className="communityLink" key={index}>
                                <a href={content.name} className="text-decoration-none btnTheme">{content.address}</a>
                            </li>
                        ))}
                    </ul>
                </div>
            </section>
            {/* community link end */}

            {/* aboutProject */}
            <section id="about1" className="servicesSection aboutVision aboutMision">
                <div className="container">
                    <ImageRight
                        title={"Timeless charm with a modern twist."}
                        src={image.ivy}
                        paragraph={"The Ivy blends clean lines and open-concept living with the comfort of classic architecture. With natural light cascading through generous windows and thoughtful design in every corner, Ivy is perfect for families looking for a space that grows with them."}
                    />
                </div>
            </section>

            <section id="about2" className="servicesSection aboutVision">
                <div className="container">
                    <ImgLeft
                        image={image.rose}
                        title={"Graceful. Sophisticated. Effortlessly beautiful."}
                        paragraph={"The Rose exudes refined elegance with its grand entrance, flowing interiors, and luxurious finishes. Designed to impress and built to last, this home flourishes in both form and function—just like its namesake."}
                    />
                </div>
            </section>

            <section id="about3" className="servicesSection aboutVision aboutMision">
                <div className="container">
                    <ImageRight
                        title={"Bold design meets everyday brilliance."}
                        src={image.kiara}
                        paragraph={"Kiara is a statement in contemporary living, featuring sleek architecture, smart layouts, and stylish details. Perfect for the modern homeowner who values comfort without compromising on flair."}
                    />
                </div>
            </section>

            <section id="about4" className="servicesSection aboutVision">
                <div className="container">
                    <ImgLeft
                        image={image.azalea}
                        title={"A warm welcome every time you come home."}
                        paragraph={"Azalea captures the essence of cozy luxury. With its thoughtfully designed spaces, inviting atmosphere, and lush indoor-outdoor connection, this home feels like a weekend getaway—every single day."}
                    />
                </div>
            </section>

            <section id="about5" className="servicesSection aboutVision aboutMision">
                <div className="container">
                    <ImageRight
                        title={"Where elegance meets innovation."}
                        src={image.orchid}
                        paragraph={"The Orchid stands out with its architectural grace and forward-thinking design. Inspired by nature's artistry, it offers a harmonious balance of tranquility and sophistication for those seeking something truly special."}
                    />
                </div>
            </section>
            {/* aboutProject end */}

            {/* our strenght start */}
            <OurStrenght />
            {/* our strenght end */}
        </>
    )
}

export default Communities
