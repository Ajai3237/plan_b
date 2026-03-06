import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './App.css';
import "slick-carousel/slick/slick.css";
import "aos/dist/aos.css";
import "slick-carousel/slick/slick-theme.css";
import Layout from './layout/Layout';
import HomePage from './pages/LandingPage/HomePage';
import About from './pages/about/About';
import Contact from './pages/contact/Contact';
import Communities from './pages/communities/Communities';
import Gallery from './pages/gallery/Gallery';
import Error from './pages/error/Error';
import ScrollToTop from './hooks/ScrollToTop';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {

  return (
    <>
      <ToastContainer position="top-center" autoClose={2000} hideProgressBar={false} />

      <Router>
        <ScrollToTop />
        <Routes>
          <Route path="/" element={< Layout />} >
            <Route index element={<HomePage />} />
            <Route path="about" element={<About />} />
            <Route path="models" element={<Communities />} />
            <Route path="gallery" element={<Gallery />} />
            <Route path="contact" element={<Contact />} />
            <Route path="*" element={<Error />} />
          </Route>
        </Routes>
      </Router>
    </>
  )
}

export default App
