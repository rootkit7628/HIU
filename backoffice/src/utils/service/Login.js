import { RouteAxios } from "utils/urlAxios/urlAxios";


function login(client, username, password){
    return RouteAxios.post("/login/",{
        client, username, password
    }, {headers: {
                'Content-Type': 'application/json'
            }})
    .then((response) => {
        if(response.data.token){
            localStorage.setItem("admin", JSON.stringify(response.data));
        }
        return response.data;
    })
    .catch((error) =>{
        return error.message;
    })
}


function logout(){
    localStorage.removeItem('admin');
    
    
}

function getCurrentCompte(){
    return JSON.parse(localStorage.getItem('admin'));
}

/*function getOneCompteContexte(compteFromContexte){
    const compteFromService = getCurrentCompte();
    const compteConv = Object.keys(compteFromContexte).map((cle) =>{
        return compteFromContexte[cle];
    })
    const compteCurrent = compteConv.filter((compteConvertis) => {
        return compteConvertis.id === compteFromService.id;
    })

    return compteCurrent;
}

function getOneItemContexte(AllDataContexte, idParams){
    const dataConvert = Object.keys(AllDataContexte).map((cle) => {
        return AllDataContexte[cle];
    })
    const dataCurrent = dataConvert.filter((data) => {
        return data.id === parseInt(idParams);
    })
    return dataCurrent;
}

function convertItemToArray(itemFromContexte){
     const itemConvertis = Object.keys(itemFromContexte).map((cle) =>{
        return itemFromContexte[cle];
    })
    return itemConvertis;
}

function getComptePerDomaine(item, domaine){
    const itemPerDomaine = item.filter((data) => {
        if(domaine !== ""){
            return data.domaine === domaine;
        } else{
            return data.domaine
        }
    })
    return itemPerDomaine;
}

function getFichePerDomaine(fiche, domaine_id){
    const fichePerDomaine = fiche.filter((data) => {
        if(domaine_id !== 0){
            return data.domaine_id === domaine_id;
        } else {
            return data.domaine_id;
        }
    })
    return fichePerDomaine;
}

function getContenuPerDomaine(contenu, type){
    const contenuPerDomaine = contenu.filter((data) => {
        if(type !== ""){
            return data.type === type;
        } else {
            return data.type;
        }
    })
    return contenuPerDomaine;
}*/

export const Login={
    login,
    logout,
    getCurrentCompte,
}