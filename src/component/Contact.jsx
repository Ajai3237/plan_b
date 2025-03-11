import React from 'react'

function Contact() {
return (
    <>
    <div style={{marginTop:'300px'}} className="con">
        <h2 className='m-5' style={{ textAlign: 'center', textShadow: '2px 2px 4px #000000',  }}>Contact us for more details</h2>

        <div style={{ textAlign: 'center', marginTop: '20px' }}>
            <input type="text" placeholder="Search..." style={{ padding: '10px', width: '350px', marginRight: '10px', borderRadius: '20px', border: 'none' }} />
            <button style={{width:'100px', padding: '10px 20px', backgroundColor: 'lightblue', borderRadius: '20px', border: 'none', fontWeight: 'bold' }}>Search</button>
        </div>
        <div  style={{ textAlign: 'center', marginTop: '20px', }}>
            <i className="fa-brands fa-instagram fa-2x" style={{ margin: '0 10px'  }}></i>
            <i className="fa-brands fa-facebook fa-2x" style={{ margin: '0 10px' }}></i>
            <i className="fa-brands fa-whatsapp fa-2x" style={{ margin: '0 10px' }}></i>
            <i className="fa-brands fa-square-x-twitter fa-2x" style={{ margin: '0 10px' }}></i>
        </div>
        </div>
    </>
)
}

export default Contact