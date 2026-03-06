import { image } from '../../constants/image';
import { icon } from '../../constants/icon';
import { Link } from 'react-router-dom';


const OurStrenght = () => {
    return (
        <section className="ourSternghtSect">
            <div className="container">
                <div>
                    <h1 className="pageHeading oswald">
                        let's combine
                    </h1>
                    <h1 className="pageHeading oswald">
                        our strengths
                    </h1>
                </div>
                <div className="strenghtBox position-relative">
                    <div className=" bannerPic">
                        <img src={image.image53} alt="our strenght picture" className="w-100 h-100" />
                    </div>
                    <Link to={'/contact'}
                        className="position-absolute d-flex align-items-center justify-content-center top-50 start-50 translate-middle">
                        <img src={icon.arrRght} alt="click here" />
                    </Link>
                </div>
            </div>
        </section>
    )
}

export default OurStrenght
