const ImageRight = ({ src, title, paragraph }) => {
    return (
        <>
            <div className="d-flex flex-column flex-xl-row justify-content-between align-items-center">
                <div>
                    <h1 className="heading oswald text-uppercase" data-aos="fade-right">
                        {title}
                    </h1>
                    <p data-aos="fade-right">
                        {paragraph}
                    </p>
                </div>
                <div className="servicesImgBox position-relative" data-aos="zoom-in">
                    <img src={src} alt="Services Image"
                        className="w-100 h-100 object-fit-cover" />
                </div>
            </div>
        </>
    )
}

export default ImageRight
