import { useState } from 'react';
import './gallery.css'
import OurStrenght from '../../components/ourStrenght/OurStrenght';
import PageBanner from '../../components/pageBanner/PageBanner';
import { image } from '../../constants/image';
import { RxCross2 } from 'react-icons/rx';


const GalleryBox = () => {
    const [activeCollapse, setActiveCollapse] = useState('collapseOne');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState({ src: '', title: '', description: '' });
    const [residentialType, setResidentialType] = useState('singleFamily');

    const openModal = (src, title, description = '') => {
        setModalContent({ src, title, description });
        setIsModalOpen(true);
        document.body.style.overflow = 'hidden';
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setModalContent({ src: '', title: '', description: '' });
        document.body.style.overflow = '';
    };

    const ImageCard = ({ img }) => (

        <div className="col-md-4 mb-4 galleryImgBox d-flex flex-column justify-content-center">
            <div
                className="galleryImg"
            // onClick={() => openModal(img.src, img.title, img.description)}
            // style={{ cursor: 'pointer' }}
            >
                <img src={img.src} alt={img.title} className="img-fluid" />
            </div>
            <>{img.title}</>
        </div>
    );

    const GallerySection = ({ data }) => (
        <>
            {data.length > 0 ? (
                data.map((img, index, res) => <ImageCard key={index} img={img} res={res} />)
            ) : (
                <p className="text-center">Comming Soon.</p>
            )}
        </>
    );

    const galleryButtons = [
        { id: 'collapseOne', label: 'Residential' },
        { id: 'collapseTwo', label: 'Commercial' },
        { id: 'collapseThree', label: 'Lots' },
    ];

    const residentialTabs = [
        { key: 'singleFamily', label: 'Single Family House' },
        { key: 'skinnyHomes', label: 'Skinny Homes' },
        { key: 'duplex', label: 'Duplex' },
        { key: 'fourplex', label: '4 Plex' },
        { key: 'eightplex', label: '8 Plex' },
        { key: 'apartments', label: 'Apartments' },
    ];

    const residentialData = {
        singleFamily: [
            {
                src: image.sfh1,
                // title: "3190 checknita way sw - Single family house",  
            },
            {
                src: image.sfh2,
                //  title: "8414 Mayday Link (Orchards Project) - Single Family House",
            },
            {
                src: image.sfh3,
                //  title: "8416 Mayday Link (Orchards Project) - Single Family House",  
            },
            {
                src: image.sfh4,
                //  title: "8431 Mayday link (Orchards Project) - Single Family house", 
            },
            {
                src: image.sfh5,
                //  title: "8914 Mayday way sw (Orchards project) - Single Family House", 
            },
            // { src: image.sfh6, title: "10913 159 street - single family house" },
        ],
        duplex: [
            {
                src: image.kiara,
                // title: "8598 & 8600 Cushing way sw - Duplex"
            },
        ],
        fourplex: [
            {
                src: image.frplx
            }
        ],
        eightplex: [
            {
                src: image.fourplex,
                //  title: "16113 103 Ave 4 Plex"
            },
        ],
        apartments: [{
            src: image.aprtmnt,
            title: 'Opulence in Whyte - Apartments'
        }],
        skinnyHomes: [{
            src: image.livingRoom,
            title: 'Living room '
        },
        {
            src: image.fulKit,
            title: 'Full kitchen'
        },
        {
            src: image.DiningArea,
            title: 'Dining Area'
        },
        {
            src: image.bedRoom,
            title: 'Bed Room'
        },
        {
            src: image.fullBathroom,
            title: 'Full Bathroom'
        },
        {
            src: image.exterior,
            title: 'Exterior'
        }
        ],
    };

    const commercial = [
        { src: image.plaza, title: "Fort Saskatchewan Common Plaza" },
        { src: image.plaza2, title: "Caishen on Windermere Plaza" },
        { src: image.comingSoon, title: "Sehonsee Plaza" },
    ];

    const floorPlansImages = [
        {
            src: image.lots2,
            // title: "Lots",
        },
        //  {
        //     src: image.lots2,
        //     title: "Lots",
        // },
    ];

    return (
        <>
            <section className="gallery">
                <div className="container">
                    <ul className="list-unstyled galleryBtn" data-aos="fade-up">
                        {galleryButtons.map(({ id, label }) => (
                            <li key={id} className="galleryList">
                                <button
                                    type="button"
                                    onClick={() => setActiveCollapse(id)}
                                    className={`text-decoration-none btnTheme ${activeCollapse === id ? 'activated' : ''}`}
                                >
                                    {label}
                                </button>
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="galleryContainer" data-aos="fade-up">
                    <div className="container">
                        <div className={`collapse ${activeCollapse === 'collapseOne' ? 'show' : ''}`} id="collapseOne">
                            <div className="w-100 text-center">
                                <div className="btn-group mb-4 justify-content-center" role="group">
                                    {residentialTabs.map(({ key, label }) => (
                                        <button
                                            key={key}
                                            type="button"
                                            className={`btn ${residentialType === key ? 'active' : ''}`}
                                            onClick={() => setResidentialType(key)}
                                        >
                                            {label}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <div className="card card-body">
                                <GallerySection data={residentialData[residentialType]} />
                            </div>
                        </div>

                        <div className={`collapse ${activeCollapse === 'collapseTwo' ? 'show' : ''}`} id="collapseTwo">
                            <div className="card card-body">
                                <GallerySection data={commercial} />
                            </div>
                        </div>

                        <div className={`collapse ${activeCollapse === 'collapseThree' ? 'show' : ''}`} id="collapseThree">
                            <div className="card card-body">
                                <GallerySection data={floorPlansImages} />
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* MODAL */}
            {isModalOpen && (
                <div
                    className="galleryModal modal fade show d-block"
                    tabIndex="-1"
                    role="dialog"
                    onClick={closeModal}
                    style={{ backgroundColor: 'rgba(0,0,0,0.8)' }}
                >
                    <div className="modal-dialog modal-dialog-centered modal-dialog-scrollable" role="document" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-content">
                            <div className="modal-header border-bottom border-dark-subtle">
                                <h5 className="modal-title">
                                    {/* {modalContent.title} */}
                                </h5>
                                <button type="button" className="btn-close text-warning" onClick={closeModal} aria-label="Close">
                                    <RxCross2 />
                                </button>
                            </div>
                            <div className="modal-body">
                                <img src={modalContent.src} alt={modalContent.title} className="img-fluid galImg rounded" />
                                <p>
                                    {modalContent.description
                                        ? modalContent.description
                                        : 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Deserunt, ullam?...'}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

const Gallery = () => {
    return (
        <>
            {/* banner start */}
            <section className="bannerSection communityBanner">
                <div className="container">
                    <PageBanner bannerTitle='Gallery' bannerLink={image.gallery} />
                </div>
            </section>
            {/* banner end */}

            <GalleryBox />


            {/* our strenght start */}
            <OurStrenght />
            {/* our strenght end */}
        </>
    )
}

export default Gallery
