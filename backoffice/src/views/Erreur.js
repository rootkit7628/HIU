import React from 'react';
import { Link } from "react-router-dom"

import '../assets/styles/error.css';

export default function Erreur (){
    return(
        <div id="notfound">
            <div className="notfound">
                <div className="notfound-404">
                    <h1>4<span></span>4</h1>
                </div>
                <h2>Oops! Page Not Be Found</h2>
                <p>Sorry but the page you are looking for does not exist, have been removed. name changed or is temporarily unavailable</p>
                <Link to='/'>
                    Go to home
                </Link>
            </div>
        </div>
    )
}
