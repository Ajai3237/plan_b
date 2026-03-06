import { FaArrowUp } from 'react-icons/fa'

const Faq = () => {

    const Faq = [
        {
            question: 'Where does Akia Homes operate?',
            answear: 'We serve clients throughout Alberta, including major cities such as Calgary, Edmonton, and Red Deer.'
        },
        {
            question: 'Can I build a fully customized home with Akia Homes?',
            answear: 'Yes, we specialize in building homes tailored to your specific needs and preferences—from layout to finishes.'
        },
        {
            question: 'What types of clients do you typically work with?',
            answear: "Akia Homes works with a diverse range of clients, including individuals and families looking to build their dream homes from the ground up, commercial investors interested in developing plazas, and landowners who want to design and construct fully customized homes on their own plots. Whether you're building your first home or investing in a multi-unit residential or commercial project, we tailor our services to meet your unique needs."
        },
        {
            question: 'What sets Akia Homes apart from other builders?',
            answear: "We combine over 5 years of hands-on experience with a commitment to quality craftsmanship and fully customizable builds, ensuring every project reflects the client's vision."
        },
    ];

    return (
        <section className="faqsection">
            <div className="container">
                <div className="d-flex faqsectBox justify-content-between flex-column flex-lg-row">
                    <div className="faqTitle" data-aos="fade-up">
                        <h1 className="heading oswald text-uppercase">
                            faq's
                        </h1>
                        <h2 className="subHead text-uppercase">
                            we're ready
                            to answer
                        </h2>
                    </div>
                    <div className="faqAccordian" data-aos="fade-right">
                        <div className="accordion" id="accordionExample">
                            <div className="accordion-item">
                                <h2 className="accordion-header">
                                    <button className="accordion-button" type="button" data-bs-toggle="collapse"
                                        data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                        What does Akia Homes do?
                                        <FaArrowUp />
                                    </button>
                                </h2>
                                <div id="collapseOne" className="accordion-collapse collapse show"
                                    data-bs-parent="#accordionExample">
                                    <div className="accordion-body">
                                        Akia Homes is a construction company specializing in building residential and commercial properties across Alberta. We offer solutions like custom single-family homes, duplexes, apartments, four-plexes, and commercial plazas.
                                    </div>
                                </div>
                            </div>
                            {Faq.map((cintent, index) => (
                                <div className="accordion-item" key={index}>
                                    <h2 className="accordion-header">
                                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                            data-bs-target={`#collapse${index}`} aria-expanded="false" aria-controls={`collapse${index}`}>
                                            {cintent.question}
                                            <FaArrowUp />
                                        </button>
                                    </h2>
                                    <div id={`collapse${index}`} className="accordion-collapse collapse"
                                        data-bs-parent="#accordionExample">
                                        <div className="accordion-body">
                                            {cintent.answear}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default Faq
