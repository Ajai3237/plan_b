import React from 'react';
import { Parallax, ParallaxProvider } from 'react-scroll-parallax';


function Content() {
    return (
        <div>
         
            <div
                style={{
                    backgroundImage: "url('/pexels-nurseryart-346885.jpg')",
                    height: "100vh",
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    backgroundAttachment: "fixed",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "white",
                    textAlign: "center",
                    fontSize: "2rem",
                    fontWeight: "bold",
                    textShadow: "2px 2px 10px rgba(0, 0, 0, 0.8)",
                    marginTop: "0",
                    paddingTop: "0"
                }}
            >
                <Parallax speed={-20}>
                    <h1>Explore the world with us</h1>
                </Parallax>
            </div>


            <div className="container my-5 text-center">
                <h2>Places we gonna explore</h2>
                <p>"Travel isn’t about the destination it’s about the journey, the people you meet, and the memories you create along the way." ✈️🌍✨</p>
            </div>


            <div
                style={{
                    backgroundImage: "url('/pexels-pierre-blache-651604-2901208.jpg')",
                    height: "90vh",
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    backgroundAttachment: "fixed",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "white",
                    textAlign: "center",
                    fontSize: "2rem",
                    textShadow: "2px 2px 10px rgba(0, 0, 0, 0.8)"
                }}
            >

                <Parallax scale={[0.5, 1.5]}>
                    <h1 className="fw-bold">FRANCE</h1>
                </Parallax>



            </div>

            <div style={{ fontFamily: 'cursive' }} className=" my-2 text-center fs-5">
                "The world is a book, and those who do not travel read only one page." – Saint Augustine
            </div>

            <div
                style={{
                    backgroundImage: "url('/pexels-masoodaslami-19235943.jpg')",
                    height: "90vh",
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    backgroundAttachment: "fixed",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "white",
                    textAlign: "center",
                    fontSize: "2rem",
                    textShadow: "2px 2px 10px rgba(0, 0, 0, 0.8)"
                }}
            >
                <Parallax opacity={[0, 2]}>
                    <h2 className="fw-bold">Hong Kong</h2>
                </Parallax>
            </div>

            <div style={{ fontFamily: 'cursive' }} className=" my-2 text-center fs-5">
                "Take only memories, leave only footprints." – Chief Seattle
            </div>

            <div
                style={{
                    backgroundImage: "url('/pexels-pixabay-158398.jpg')",
                    height: "90vh",
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    backgroundAttachment: "fixed",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "white",
                    textAlign: "center",
                    fontSize: "2rem",
                    textShadow: "2px 2px 10px rgba(0, 0, 0, 0.8)"
                }}
            >
                <div className="container text-center mt-5">
                    <Parallax blur={[10, 0]}>
                        <h1>Canada</h1>
                    </Parallax>



                </div>
            </div>

            <div style={{ fontFamily: 'cursive' }} className=" my-2 text-center fs-5">
                "Traveling – it leaves you speechless, then turns you into a storyteller." – Ibn Battuta
            </div>

            <div
                style={{
                    backgroundImage: "url('/pexels-pham-ngoc-anh-170983008-28218398.jpg')",
                    height: "90vh",
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    backgroundAttachment: "fixed",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "white",
                    textAlign: "center",
                    fontSize: "2rem",
                    textShadow: "2px 2px 10px rgba(0, 0, 0, 0.8)"
                }}
            >
                <div className="container text-center mt-5">
                    <Parallax translateX={[-50, 50]}>
                        <h1>Germany</h1>
                    </Parallax>

                </div>
            </div>
        </div>




    );
}

export default Content;
