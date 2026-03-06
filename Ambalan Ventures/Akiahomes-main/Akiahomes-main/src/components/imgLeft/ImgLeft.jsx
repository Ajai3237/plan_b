const ImgLeft = ({ image, title, paragraph }) => {
    return (
        <>
            <div className="d-flex flex-column-reverse flex-xl-row justify-content-between align-items-center">
                <div className="servicesImgBox position-relative" data-aos="zoom-in">
                    <img src={image} alt="Services Image"
                        className="w-100 h-100 object-fit-cover" />
                </div>
                <div>
                    <h1 className="heading oswald text-uppercase" data-aos="fade-right">
                        {title}
                    </h1>
                    <p data-aos="fade-right">
                        {paragraph}
                    </p>
                </div>
            </div>
        </>
    )
}

export default ImgLeft
