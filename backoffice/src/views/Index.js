/*eslint-disable*/
import React from "react";
import { Link } from "react-router-dom";

import "../assets/styles/Styles.css"
import IndexNavbar from "components/Navbars/IndexNavbar";

export default function Index() {
  return (
    <>
      <IndexNavbar />
      <section className="header relative  items-center accueil">
        <div className="container flex items-center  ">
          <div className="index">
              <div className="main">
                <input type="checkbox" id="chk" aria-hidden="true" />
                  <div className="signup">
                    <form>
                        <label htmlFor="chk" aria-hidden="true">Télechager fichier</label>
                        <input className="username" type="text" name="token" placeholder="Votre token ici..."  />
                        <input type="submit" className="btn btn-login" value="Télecharger" />
                      
                    </form>
                  </div>

                  <div className="login">
                    <form >
                        <label htmlFor="chk" aria-hidden="true">Upload fichier</label>
                        <input type="file" name="file" placeholder="Votre token ici..."  />
                        <input type="submit" className="btn btn-upload" value="Upload" />
                    </form>
                  </div>
              </div>
          </div>

          <div className="w-4/12 md:w-12/12 flex flex-wrap items-center flex-col ml-3">
                  <h2 className="font-semibold text-4xl text-white">
                      Bienvenue sur <span className="text-blueGray-700"> E-Zara </span>
                  </h2>
                  <p className=" text-lg leading-relaxed text-white flex flex-wrap">
                    C'est une application web & mobile{" "}
                    pour toute vos partages fichiers avec simpicité rapidité et sécurisé.
                    Alors n'attendez plus rejoignez-nous!!!!
                    Ad ad pariatur ea minim nisi nulla. Laborum dolore ut mollit irure ex voluptate fugiat occaecat reprehenderit excepteur. Incididunt incididunt reprehenderit cillum et. Pariatur et ipsum adipisicing dolor id fugiat tempor magna. Magna do quis dolor et do do est adipisicing nulla aliqua duis. Sunt proident aliqua est eiusmod fugiat ut mollit pariatur amet dolore do. Aliqua excepteur quis adipisicing mollit aliquip mollit officia laborum nostrud officia magna duis.
                  </p>
                  <div className="mt-12">
                    <Link
                      to="/authentification"
                      className="text-white font-bold px-6 py-4 rounded outline-none focus:outline-none mb-1 bg-blueGray-700 active:bg-lightBlue-600 uppercase text-sm shadow hover:shadow-lg ease-linear transition-all duration-150"
                    >
                      Connexion
                    </Link>
                  </div>              
            </div>
          
          
        </div>
      </section>
    </>
  );
}
