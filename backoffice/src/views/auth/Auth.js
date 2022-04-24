/*eslint-disable*/
import React, { useState} from "react";
import { useHistory } from "react-router";
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as Yup from 'yup';
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import {Login} from "utils/service/Login";
import IndexNavbar from "components/Navbars/IndexNavbar";

import "../../assets/styles/Styles.css"

export default function Index() {
  const token = Login.getCurrentCompte().token;
  const [erreur,setErreur]=useState(false)
  const [errormessage,setErrorMessage]=useState("");

  const validationSchema = Yup.object().shape({
    client: Yup.string(),
    username: Yup.string()
      .required('Username is required'),
    password: Yup.string()
      .required('Password is required')
      .min(6, 'Password must be at least 6 characters')
      .max(40, 'Password must not exceed 40 characters')
  });
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({
    resolver: yupResolver(validationSchema)
  });

  let history = useHistory();
  const onSubmit = (data) => {
        try {
            Login.login( data.username, data.password).then(
                (response) => {
                  if(response.token){
                     history.push('/admin/statistique');
                  }
                  else {
                    setErreur(true);
                    setErrorMessage("Username ou mot de passe incorrecte!");
                  }
                })
        } catch (error) {
          setErreur(true);
          setErrorMessage("Serveur en maintenance");
        }
  }

  const { t, i18n } = useTranslation();

  const changeLanguageHandler = (e) => {
    const languageValue = e.target.value
    i18n.changeLanguage(languageValue);
  }

  return (
    <>
      <IndexNavbar />
      <div className="index">
        <img 
          className="image-illustration"
          alt="..."
          src={require("assets/img/sent.gif").default}
        /> 
          <div className="main">
              { token === undefined ? (
                <div className="signup">
                  <form onSubmit={handleSubmit(onSubmit)}>
                      <label htmlFor="chk" aria-hidden="true">{t('titre-login')}</label>
                      <input className="username" type="text" name="prenom" placeholder={t('placeholder-login')} {...register('username')} /><p className="bold italic text-white" style={{margin: '0px 0px 0px 55px'}}>{errors.username?.message}</p>
                      <input className="password" type="password" name="password" placeholder={t('placeholder-password-login')} {...register('password')} /><p className="bold italic text-white"  style={{margin: '0px 0px 0px 55px'}}>{errors.password?.message}</p>
                      <input type="submit" className="btn btn-login" value={t('bouton-login')} />
                    { erreur &&(
                            <div className="bg-red-500 border border-red-500 text-red-700 px-4 py-3 mx-2 rounded relative" role="alert">
                              <strong className="font-bold">Erreur!</strong>
                              <span className="block sm:inline">{errormessage} </span>
                              <span className="absolute top-0 bottom-0 right-0 px-4 py-3">
                                  <svg onClick={()=>{setErreur(false)}} className="fill-current h-5 w-12 text-red-400" role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><title>Close</title><path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z"/></svg>
                              </span>
                            </div>
                        )}
                  </form>
                </div>
              ) : (
                  <div className="signup mt-32 flex align-middle ite">
                      <Link  className="btn w-full" to="/admin/statistique"><button>{t('bouton-entrer')}</button></Link>
                  </div>
              )

              }
          </div>
      </div>
    </>
  );
}
