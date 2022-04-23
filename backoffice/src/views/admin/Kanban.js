import React from "react";
import CardAllContent from "components/Cards/CardAllContent";


export default function Kanban() {
  /*const [type, setType] = useState("");

  const [termSearch, setTermSearch] = useState("");

  const choixType = (e) => {
    let choix = e.target.value;
    return setType(choix);
  }

  const recherche = (e) => {
  let valeur = e.target.value;
  setTermSearch(valeur);
}*/

  return (
    <>
      <div className="flex flex-col flex-wrap bg-blueGray-400 w-full relative mt-20">
        <div className="flex justify-center flex-wrap">
            <h2 className="text-3xl font-bold text-center w-full mt-8 text-blueGray-800">Liste des matières </h2>
            <div className="w-full lg:w-6/12 px-4 mx-4 sm:mb-3">
                  <div className="relative w-full">
                    <input
                      type="text"
                      name="searchBar"
                      id="searchBar"
                      className="border-1 px-3 py-3 placeholder-blueGray-500 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      placeholder="Entrer lae mote clé..."
                      //onChange={(e) => recherche(e)}
                   />
                </div>
              </div>
            <select
                name="type"
                className="border-1 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-4/12 ease-linear transition-all duration-150"
                //onChange={(e) => choixType(e)}
            >
                  <option  hidden>Matières</option>
                  <option key="1" value="science">Science</option>
                  <option key="2" value="mathematique">Mathématique</option>
                  <option key="3" value="informatique">Informatique</option>
                  <option key="4" value="histoire">Histoire</option>
             </select>
        </div>
        <div className="flex flex-wrap">
            <CardAllContent />
        </div>
      </div>
    </>
  );
}
