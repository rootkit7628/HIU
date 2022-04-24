import { RouteAxios } from "utils/urlAxios/urlAxios";
import {Login} from "utils/service/Login";

class AdminService{
                /*ADD SERVICE*/
    UploadFile(fichier){
        var content = new FormData();

        content.append("fichier", fichier);

        return RouteAxios.post('/add_file_v1/', content)
    }

                /*GET SERVICE*/
    getOneFile(token){
        return RouteAxios.get(`/get_file_v1/${token}`)
    }

    getAllContenu(){
        return RouteAxios.get("/list_attachements",  {
                headers: {
                    'Authorization': `Bearer ${Login.getCurrentCompte().token}`
                }
        })
    }

    getStat(){
        return RouteAxios.get("/get_stats", {
            headers: {
                    'Authorization': `Bearer ${Login.getCurrentCompte().token}`
            }
        })
    }


                /*DELETE SERVICE*/
    DeleteOneCompte(compte_id){
        return RouteAxios.delete("/delete_account", 
            {
            headers: {
                'Authorization': `Bearer ${Login.getCurrentCompte().token}`
            },
            data: {
                compte_id: compte_id
            }
        },
        ) 
    }

    DeleteOneContent(content_id){
        return RouteAxios.delete("/delete_content", 
            {
            headers: {
                'Authorization': `Bearer ${Login.getCurrentCompte().token}`
            },
            data: {
                content_id: content_id
            }
        }
        ) 
    }
            /*UPDATE SERVICE*/

    UpdateCompte(nom, email, tel, domaine, description, adresse, lien){
        return RouteAxios.patch('/update_account', {
            nom, 
            email, 
            tel, 
            domaine, 
            description, 
            adresse,
            lien
        }, {
            headers: {
                'Authorization': `Bearer ${Login.getCurrentCompte().token}`,
                'Content-Type': 'application/json'
            }
        }
        )

    }
        
    UpdateOneContent(titre, description, type, content_id, file){
        var content = new FormData();

        content.append("titre", titre);
        content.append("description", description);
        content.append("type", type);
        content.append("content_id", content_id);
        content.append("file", file);

        return RouteAxios.patch('/update_content', content,{
            headers: {
                'Authorization': `Bearer ${Login.getCurrentCompte().token}`
            }
        })
    }

    UpdatePassword(old_password, new_password){
        return RouteAxios.patch('/change_password', {
            old_password,
            new_password
        }, {
            headers: {
                'Authorization': `Bearer ${Login.getCurrentCompte().token}`,
                'Content-Type': 'application/json'
            }
        }
        )
    }

    UpdateLogo(logo){
        var content = new FormData();

        content.append("logo", logo);

        return RouteAxios.patch('/update_logo', content,{
            headers: {
                'Authorization': `Bearer ${Login.getCurrentCompte().token}`
            }
        })
    }

}

export default new AdminService();
