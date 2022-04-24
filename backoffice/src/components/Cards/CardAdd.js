import React, {useState} from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as Yup from 'yup';
import {useHistory} from "react-router";
import AdminService from "utils/service/AdminService";


export default function CardAdd() {
  const [erreur,setErreur]=useState(false);
  const [errorMesssage,setErrorMessage]=useState("");
 
  let history = useHistory();

  const validationSchema = Yup.object().shape({
        fichier: Yup.mixed()
          .test('required', "N'oubliez pas votre fichier, c'est obligatoire", (value) => {
            return value && value.length;
          })
          .test('fileSize', "Le fichier est trop gros", (value) => {
            return value && value[0] && value[0].size <= 500000000;
          })
      });
      const {
        register,
        handleSubmit,
        formState: { errors }
      } = useForm({
        resolver: yupResolver(validationSchema)
      });

  const  handleAddFile = async(data) => {
        try {
            await AdminService.UploadFile(data.fichier[0]);
            if(data.fichier.length > 0){
                history.push('/admin/liste');
            }else{
                setErreur(true);
                setErrorMessage("Echec à la l'ajout du fichier");
            }


        } catch (error) {
            setErreur(true)
            setErrorMessage(error.response.data.message)
        }
    }
    


   
  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words w-12/12 mb-6 shadow-lg rounded-lg bg-blueGray-200 border-0">
        <form onSubmit={handleSubmit(handleAddFile)}>
          <div className="rounded-t bg-white mb-0 px-6 py-6">
            <div className="text-center flex justify-between">
              <h6 className="text-blueGray-700 text-xl font-bold">Ajouter nouveau fichier</h6>
            </div>
          </div>
          <div className="flex-auto px-4 lg:px-10 py-10 pt-0">
              <div className="flex pt-6">
                <div className="w-full lg:w-6/12 px-4">
                  <div className="relative w-full mb-3">
                    <input
                      type="file"
                      name="file"
                      className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      
                      {...register('fichier')}
                   />
                   <input 
                      className="bg-teal-500 text-white active:bg-lightBlue-600 font-bold uppercase text-xs px-4 py-2 mt-2 rounded shadow hover:shadow-md outline-none focus:outline-none  ease-linear transition-all duration-150"
                      type="submit"              
                      value="Ajouter"
                  />
                   <p className="text-red-500 italic">{errors.fichier?.message}</p>
                  </div>
                </div>
              </div>
          </div>
        </form>
        {erreur &&(
                  <div className="bg-rose-300 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                      <strong className="font-bold">Erreur!</strong>
                          <span className="block sm:inline">{errorMesssage} </span>
                          <span className="absolute top-0 bottom-0 right-0 px-4 py-3">
                              <svg onClick={()=>{setErreur(false)}} className="fill-current h-5 w-12 text-red-500" role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><title>Close</title><path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z"/></svg>
                            </span>
                  </div>
          )}
      </div>
    </>
  );
}
