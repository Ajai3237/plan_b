import React from 'react';
import { Link } from 'react-router-dom';

function Nav() {
    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-dark bg-transparent fixed-top">
                <div className="container-fluid">
                    <img src="public/download-removebg-preview.png" alt="Logo" style={{ height: '90px' }} />
                   
                    <div className="offcanvas offcanvas-end" tabIndex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
                       
                        <div className="offcanvas-body">
                            <ul className="navbar-nav justify-content-end flex-grow-1 pe-5 gap-4 fs-5">
                            <Link style={{textDecoration:'none', color:'white'}} to={"/"}>
                               <span >Home</span>
                               </Link>
                               <Link style={{textDecoration:'none', color:'white'}} to={"/offer"}>
                               <span >Offers</span>
                               </Link>
                               <Link style={{textDecoration:'none', color:'white'}} to={"/Contact"}>
                               <span >Contact</span>
                               </Link>
                            </ul>
                           
                        </div>
                    </div>
                </div>
            </nav>
        </>
    );
}

export default Nav;
