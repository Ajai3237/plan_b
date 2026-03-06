import './banner.css';

const PageBanner = ({ bannerTitle, bannerLink }) => {
    return (
        <>
            <h1 className="oswald pageHeading" data-aos="fade-up">
                {bannerTitle}
            </h1>
            <div className="bannerPic">
                <img src={bannerLink} alt="home page banner" className="w-100 h-100" />
            </div>
        </>
    )
}

export default PageBanner
