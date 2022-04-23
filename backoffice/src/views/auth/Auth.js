/*eslint-disable*/
import React, {useEffect, useState} from "react";
import { useHistory } from "react-router";
/*import { Link } from "react-router-dom";*/
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as Yup from 'yup';

import {Login} from "utils/service/Login";
import AuthNavbar from "components/Navbars/AuthNavbar";

import "../../assets/styles/Styles.css"

export default function Index() {

  const [erreur,setErreur]=useState(false)
  const [errormessage,setErrorMessage]=useState("");
  const [type, setType] = useState("password");

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
        data.client = "back-office";
        try {
            Login.login(data.client, data.username, data.password).then(
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

  function viewPassword(e){
    let check = e.target.checked;
    check ? setType("text") : setType("password");
  }

  return (
    <>
      <AuthNavbar />
      <div className="index">
        <img 
          className="image-illustration"
          alt="..."
          src={require("assets/img/computer-login.gif").default}
        /> 
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
    </>
  );
}
