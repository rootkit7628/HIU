import React from "react";
/*import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as Yup from 'yup';
import {useHistory} from "react-router";*/


export default function CardAdd() {
  /*const [erreur,setErreur]=useState(false);
  const [errorMesssage,setErrorMessage]=useState("");*/
 
  /*let history = useHistory();

  const validationSchema = Yup.object().shape({
        nom: Yup.string()
          .required('Ce champ est obligatoire'),
        email: Yup.string()
          .required('Ce champ est obligatoire')
          .email("Email invalid"),
        tel: Yup.string()
          .required('Ce champ est obligatoire'),
        domaine: Yup.string()
          .required('le choix est obligatoire'),
        lien: Yup.string()
          .nullable()
          .notRequired(),
        type: Yup.string()
          .required('le choix est obligatoire'),
        password: Yup.string()
          .required('Ce champ est obligatoire')
          .min(6, 'Password must be at least 6 characters')
          .max(40, 'Password must not exceed 40 characters'),
        adresse:Yup.string()
        .required("Ce champ est obligatoire")
      });
      const {
        register,
        handleSubmit,
        formState: { errors }
      } = useForm({
        resolver: yupResolver(validationSchema)
      });

  const  handleAddAccount = async(data) => {
        try {
            let newCompte = {}
            const res = await CompteService.AddAccount(data.nom,data.email,data.tel,data.domaine,data.type,data.password,data.adresse);
            if(compt !== null && compt.type === 'ADMIN'){
                history.push('/admin/TablesEntreprises');
            }else{
                setErreur(true);
                setErrorMessage("Echec à la registration");
            }

            newCompte = JSON.parse(res.config.data)
            newCompte['id'] = res.data.id;
            newCompte['visiteurs'] = 0;
            newCompte['video'] = null;
            newCompte['logo'] = null;
            setCompte([...compte, newCompte]);
            addCompte(newCompte);

        } catch (error) {
            setErreur(true)
            setErrorMessage(error.response.data.message)
        }
    }
    */


   
  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-200 border-0">
        <form /*</div>onSubmit={handleSubmit(handleAddAccount)}*/>
          <div className="rounded-t bg-white mb-0 px-6 py-6">
            <div className="text-center flex justify-between">
              <h6 className="text-blueGray-700 text-xl font-bold">Nouvelle étudiant</h6>
              <input 
                className="bg-teal-500 text-white active:bg-lightBlue-600 font-bold uppercase text-xs px-4 py-2 rounded shadow hover:shadow-md outline-none focus:outline-none mr-1 ease-linear transition-all duration-150"
                type="submit"              
                value="Ajouter"
              />
            </div>
          </div>
          <div className="flex-auto px-4 lg:px-10 py-10 pt-0">
              <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
                Information de l'étudiant
              </h6>
              <div className="flex flex-wrap">
                <div className="w-full lg:w-6/12 px-4">
                  <div className="relative w-full mb-3">
                    <label
                      className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                      htmlFor="grid-password"
                    >
                      Nom
                    </label>
                    <input
                      type="text"
                      name="nom"
                      className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      placeholder="Nom de l'entreprise"
                      //{...register('nom')}
                   />
                   <p className="text-red-500 italic">{/*{errors.nom?.message}*/}</p>
                  </div>
                </div>
                <div className="w-full lg:w-6/12 px-4">
                  <div className="relative w-full mb-3">
                    <label
                      className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                      htmlFor="grid-password"
                    >
                      Matière
                    </label>
                    <select
                      name="domaine"
                      className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      //{...register('domaine')}
                    >
                         <option  value="" hidden>Choisir la classe</option>
                         <option key="1" value="seconde">seconde</option>
                         <option key="2" value="première">première</option>
                         <option key="3" value="terminale">terminale</option>
                    </select>
                    <p className="text-red-500 italic">{/*{errors.domaine?.message}*/}</p>
                  </div>
                </div>
                <div className="w-full lg:w-12/12 px-4">
                  <div className="relative w-full mb-3">
                    <label
                      className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                      htmlFor="grid-password"
                    >
                      Mot de passe
                    </label>
                    <input
                      type="password"
                      name="password"
                      className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      //{...register('password')}
                    />
                    <p className="text-red-500 italic">{/*{errors.password?.message}*/}</p>
                  </div>
                </div>
              </div>

              <hr className="mt-6 border-b-1 border-blueGray-300" />

              <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
                Information sur les contacts
              </h6>
              <div className="flex flex-wrap">
                <div className="w-full lg:w-6/12 px-4">
                  <div className="relative w-full mb-3">
                    <label
                      className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                      htmlFor="grid-password"
                    >
                      Contact
                    </label>
                    <input
                      type="text"
                      name="tel"
                      placeholder="VOtre numéro téléphone..."
                      className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      //{...register('tel')}
                    />
                    <p className="text-red-500 italic">{/*{errors.tel?.message}*/}</p>
                  </div>
                </div>
                <div className="w-full lg:w-6/12 px-4">
                  <div className="relative w-full mb-3">
                    <label
                      className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                      htmlFor="grid-password"
                    >
                      Email
                    </label>
                    <input
                      type="email"
                      name="email"
                      className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      //{...register('email')}
                    />
                    <p className="text-red-500 italic">{/*{errors.email?.message}*/}</p>
                  </div>
                </div>
            <div className="w-full lg:w-12/12 px-4">
                  <div className="relative w-full mb-3">
                    <label
                      className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                      htmlFor="grid-password"
                    >
                      Adresse
                    </label>
                    <input
                      type="text"
                      name="adresse"
                      className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      placeholder="Votre adresse..."
                      //{...register('adresse')}
                    />
                    <p className="text-red-500 italic">{/*{errors.adresse?.message}*/}</p>
                  </div>
                </div>
              </div>
          </div>
        </form>
        {/*{erreur &&(
                  <div className="bg-rose-300 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                      <strong className="font-bold">Erreur!</strong>
                          <span className="block sm:inline">{errorMesssage} </span>
                          <span className="absolute top-0 bottom-0 right-0 px-4 py-3">
                              <svg onClick={()=>{setErreur(false)}} className="fill-current h-5 w-12 text-red-500" role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><title>Close</title><path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z"/></svg>
                            </span>
                  </div>
          )}*/}
      </div>
    </>
  );
}
