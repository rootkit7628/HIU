/*eslint-disable*/
import React from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

export default function Navbar(props) {
  const { t, i18n } = useTranslation();

  const changeLanguageHandler = (e) => {
    const languageValue = e.target.value
    i18n.changeLanguage(languageValue);
  }
  return (
    <>
      <nav className="top-0 fixed z-50 w-full flex flex-wrap items-center justify-between px-2 py-3 bg-transparent">
        <div className="container px-4 mx-auto flex flex-wrap items-center justify-between">
          <div className="w-full relative flex justify-between lg:w-auto lg:static block lg:justify-start">
            <Link
              to="/"
              style={{color:"rgba(36, 114, 205, 1"}}
              className="text-xl font-bold leading-relaxed inline-block mr-4 py-2 whitespace-nowrap uppercase"
            >
                <img 
                  style={{width: "50px", height: "50px"}}
                  alt="..."
                  src={require("assets/img/logo.png").default}
                  />
            </Link>
            <ul>
              <li className="flex items-center">
                <a
                  className="hover:text-white text-blueGray-700 px-3 py-4 lg:py-2 flex items-center text-xs uppercase font-bold"
                  href="/"
                  
                >
                  <p className="hover:text-white mt-2 -ml-4 text-2xl leading-lg " style={{color: "rgba(36, 114, 205, 1)"}} >Roso</p> 
                </a>
              </li>
            </ul>
          </div>
          <div
            className={
              "lg:flex hidden flex-grow items-center lg:bg-opacity-0 lg:shadow-none"
            }
            id="example-navbar-warning"
          >
            <ul className="flex flex-col lg:flex-row list-none lg:ml-auto">
              <li className="flex items-center">
                  <select
                      name="type"
                      style={{backgroundColor: "#e0dede", border: "none"}}
                      className=" px-3 py-3 placeholder-blueGray-300 text-blueGray-600  rounded text-sm shadow focus:outline-none focus:ring w-12/12 ease-linear transition-all duration-150"
                      onChange={changeLanguageHandler}
                    >
                        <option  hidden>{t('langue')}</option>
                        <option key="1" value="mg">Malagasy</option>
                        <option key="2" value="fr">Français</option>
                        <option key="3" value="en">Anglais</option>
                  </select>
              </li>

              <li className="flex items-center">
                <a
                  className="hover:text-white text-blueGray-700 px-3 py-4 lg:py-2 flex items-center text-xs uppercase font-bold"
                  href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdemos.creative-tim.com%2Fnotus-react%2F%23%2F"
                  target="_blank"
                >
                  <i className="text-blueGray-600 hover:text-white fab fa-facebook text-2xl leading-lg " />
                </a>
              </li>

              <li className="flex items-center">
                <a
                  className="hover:text-white text-blueGray-700 px-3 py-4 lg:py-2 flex items-center text-xs uppercase font-bold"
                  href="https://twitter.com/intent/tweet?url=https%3A%2F%2Fdemos.creative-tim.com%2Fnotus-react%2F%23%2F&text=Start%20your%20development%20with%20a%20Free%20Tailwind%20CSS%20and%20React%20UI%20Kit%20and%20Admin.%20Let%20Notus%20React%20amaze%20you%20with%20its%20cool%20features%20and%20build%20tools%20and%20get%20your%20project%20to%20a%20whole%20new%20level.%20"
                  target="_blank"
                >
                  <i className="text-blueGray-600 hover:text-white fab fa-linkedin text-2xl leading-lg " />
                </a>
              </li>

              <li className="flex items-center">
                <a
                  className="hover:text-white text-blueGray-700 px-3 py-4 lg:py-2 flex items-center text-xs uppercase font-bold"
                  href="https://github.com/creativetimofficial/notus-react?ref=nr-index-navbar"
                  target="_blank"
                >
                  <i className="text-blueGray-600 hover:text-white fab fa-github text-2xl leading-lg " />
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
}
