import React from 'react';

function Footer() {
  return (
    <footer className="bg-dark text-light py-3 mt-auto  fixed-bottom">
        
      <div className="container text-center">
        <p className="mb-0">&copy; {new Date().getFullYear()} My Website. All Rights Reserved.</p>
        
        <div>
          <a href="#" className="text-light mx-2">Privacy Policy</a> | 
          <a href="#" className="text-light mx-2">Terms of Service</a> | 
          <a href="#" className="text-light mx-2">Contact</a>
        </div>
       
      </div>
    </footer>
  );
}

export default Footer;
