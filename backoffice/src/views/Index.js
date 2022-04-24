/*eslint-disable*/
import React, {useState} from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as Yup from 'yup';

import "../assets/styles/Styles.css"
import IndexNavbar from "components/Navbars/IndexNavbar";
import AdminService from "utils/service/AdminService";

export default function Index() {
  const { t, i18n } = useTranslation();

  const changeLanguageHandler = (e) => {
    const languageValue = e.target.value
    i18n.changeLanguage(languageValue);
  }
  const [isUrlGet, setIsUrlget] = useState(false);
  const [uploadF, setIsUploadF] = useState(false);
  const [urlFile, setUrlFile] = useState("");

  const [erreur,setErreur]=useState(false)
  const [errormessage,setErrorMessage]=useState("");

  const validationSchema = Yup.object().shape({
    token: Yup.string()
      .required('token is required'),
    fichier: Yup.mixed()
      .required("Votre fichier, n'oubliez pas!!!")
  });
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({
    resolver: yupResolver(validationSchema)
  });


  const getUrlFile = async(data) => {
      try{
          await AdminService.getOneFile(data.token).then((response) => {
            if(response.status === 200){
                setIsUrlget(true);
                setUrlFile(response.data.url);
            } else {
                setErreur(true);
                setErrorMessage("Désolé ce token n'existe pas...");
            }
        })
      } catch (error){
          setErreur(true);
          setErrorMessage("Désolé ce token n'existe pas...");
      }
  }
  
  const uploadFichier = async(data) => {
       try{
          await AdminService.UploadFile(data.fichier[0]).then((response) => {
            if(data.fichier.length > 0){
                uploadF(true);
                return response.data;
            } else {
                setErreur(true);
                setErrorMessage("Désolé le fichier n'a pas pu être envoyé...");
            }
        })
      } catch (error){
          setErreur(true);
          setErrorMessage("Désolé le fichier n'a pas pu être envoyé...");
      }
  }
  return (
    <>
      <IndexNavbar />
      <section className="header relative  items-center accueil">
        <div className="container flex items-center  ">
          <div className="upload">
              <div className="main">
                <input type="checkbox" id="chk" aria-hidden="true" />
                  <div className="signup">
                    <form onSubmit={handleSubmit(getUrlFile)}>
                        <label htmlFor="chk" aria-hidden="true">{t('titre-telecharge')}</label>
                        <input className="username" type="text" name="token" placeholder={t('placeholder-telecharge')} {...register('token')} /><p className="bold italic text-white" style={{margin: '0px 0px 0px 55px'}}>{errors.token?.message}</p>
                        <input type="submit" className="btn btn-login" value={t('bouton-verification')} />
                    </form>
                    {isUrlGet && (
                            <>
                              <label htmlFor="chk" aria-hidden="true" style={{fontSize: "16px", marginLeft: "55px", color: "rgb(5, 238, 129)"}} >Ok, vous pouvez telecharger votre fichier...</label>
                              <a href={urlFile} download={urlFile} target="_blank" ><input type="button" className="btn btn-login" value={t('bouton-telecharger')}  /></a>
                            </>
                        ) 
                    }
                  </div>

                  <div className="login">
                    <form onSubmit={handleSubmit(uploadFichier)}>
                        <label htmlFor="chk" aria-hidden="true">{t('titre-upload')}</label>
                        <input type="file" name="file" {...register('fichier')} /> <p className="text-red-500 italic">{errors.fichier?.message}</p>
                        <input type="submit" className="btn btn-upload" value={t('bouton-upload')} />
                    </form>
                  </div>
              </div>
          </div>

          <div className="w-4/12 md:w-10/12 flex flex-wrap items-start flex-col ml-3">
                  <h2 className="font-semibold text-4xl text-blueGray-500">
                      {t('titre')} <span style={{color: "rgba(36, 114, 205, 1"}}> Roso </span>
                      
                  </h2>
                  <p className=" text-lg leading-relaxed text-blueGray-600 flex flex-wrap">
                    {t('description')}
                    </p>
                  <div className="mt-12 flex flex-row">
                    <Link
                      to="/authentification"
                      style={{backgroundColor: "rgba(36, 114, 205, 1"}}
                      className="text-white font-bold px-6 py-4 rounded outline-none focus:outline-none mb-1 btn-vers-connexion uppercase text-sm shadow hover:shadow-lg ease-linear transition-all duration-150"
                    >
                      {t('connexion')}
                    </Link>
                        <img 
                      style={{width: "80px", height: "50px"}}
                      alt="..."
                      src={require("assets/img/logo.png").default}
                      className="animate-waving-hand "
                      /> 
                  </div>              
            </div>
          
          
        </div>
      </section>
    </>
  );
}
