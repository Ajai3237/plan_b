import Content from './component/Content';
import Footer from './component/Footer';
import { ParallaxProvider } from 'react-scroll-parallax';
import Nav from './component/Nav';
import Offer from './component/Offer';
import { Route, Routes } from 'react-router-dom';
import Contact from './component/Contact';

function App() {
  return (
    <>
      <Nav />

      <ParallaxProvider>
        <Routes>
          <Route path="/" element={<Content />} />
          <Route path="/offer" element={<Offer />} />
          <Route path="/Contact" element={<Contact/>} />
        </Routes>
      </ParallaxProvider>

      <Footer />
    </>
  );
}

export default App;
