import './error.css'
import { image } from '../../constants/image';

const Error = () => {
    return (
        <>
            <div className="container py-5">
                <div className="text-center py-5 my-5 error-box" >
                    <img src={image.error} alt="error" className='errorPicture' data-aos="fade-up" />
                </div>
            </div>
        </>
    )
}

export default Error
