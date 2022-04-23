## Deployement 
Dev : python main.py
Prod : gunicorn wsgi:app

## Login request
```
POST http://<host>:5000/api/v1/login
content-type: application/json

{
    "email": "<account_email>",
    "password": "<account_pass>"
}
```
=> RETOUR:
```
{
  "description": <description>,
  "id": <id>,
  "lien": <lien_vers_site>,
  "logo": <logo_entreprise>,
  "nom": <nom_entreprise>,
  "tel": <tel>,
  "token": <token_expire_12h>,
  "type": <role_compte>,
  "video": <video_presentation>,
  "vu": <nombre_visiteur>
}
```

## Add company(stand) account request
```
  POST http://<host>:5000/api/v1/add_account
  content-type: application/json
  Authorization: Bearer <Token>

  {
    "nom": <stand_name>,
    "email": <email>,
    "tel": <phone_number>,
    "domaine": <stand_domaine>,
    "lien": <site_link>,
    "type": <account_type>,
    "classe": <classe>,
    "password": <account_password>,
    "adresse": "<addresse_of_company>",
    "classe": "<classe>"
  }
```
=> RETOUR:
```
  {
    "error": false,
    "message": "Account created"
    "account_id": <account_id>
  }
```
## Add content request
```
  POST http://<host>:5000/api/v1/add_content
  Enctype: 'multipart/form-data'
  Content-Type: false
  Authorization: Bearer <Token>

  {
    "titre": <stand_name>,
    "description": <stand_domaine>,
    "type": <site_link>,
    "link": <link>,
    "file": <file> (if one file),
    "multi_file": <multi_file> (if many file)
  }
```
=> RETOUR:
```
  {
    "error": False,
    "message": "Contenu inserted",
    "id": <content_inserted_id>
  }
```

## Insert ficher metier (Need ADMIN access)
```
  POST http://<host>:5000/api/v1/add_fiche_metier
  content-type: application/json
  Authorization: Bearer <Token>

  {
    "titre": <titre>,
    "domaine_id": <domaine_id>,
    "file": <file(img/pdf)>
  }
```
=> RETOUR:
```
  {
    "error": false,
    "message": "Fiche Metier inserted"
  }
```


## Get list company
```
  GET http://<host>:5000/api/v1/list_accounts
  Authorization: Bearer <Token>
```
=> RETOUR:
```
  {
    "0": {
        "nom": <stand_name>,
        "email": <email>,
        "tel": <phone_number>,
        "domaine": <stand_domaine>,
        "lien": <site_link>,
        "type": <account_type>,
        "adresse": "<addresse_of_company>",
        "visiteurs": "<visiteurs>",
      },
      "1": {
        "nom": <stand_name>,
        "email": <email>,
        "tel": <phone_number>,
        "domaine": <stand_domaine>,
        "lien": <site_link>,
        "type": <account_type>,
        "adresse": "<addresse_of_company>"
        "visiteurs": "<visiteurs>"
      },
      ....
  }
```

## Get list contents of a company

```
  GET http://<host>:5000/api/v1/list_contents
  Authorization: Bearer <Token>
```
=> RETOUR:
```
{
  "0": {
    "description": <description>,
    "fichier": <fichier> ,
    "titre": <titre> ,
    "type": <type>,
    "vus": <vus>
  },
  "1": {
    "description": <description>,
    "fichier": <fichier> ,
    "titre": <titre> ,
    "type": <type>,
    "vus": <vus>
  },
    "2": {
    "description": <description>,
    "fichier": <fichier> ,
    "titre": <titre> ,
    "type": <type>,
    "vus": <vus>
  },
  ...
}
```

## Get list of Fiche Metier (Need Admin Access)

```
  GET http://<host>:5000/api/v1/list_fiche_metier
  Authorization: Bearer <Token>
```
=> RETOUR:
```
{
  "0": {
    "titre": <description>,
    "domaine_id": <fichier> ,
    "file": <titre>,
    "vues": <vues>
  },
  "1": {
    "titre": <titre>,
    "domaine_id": <domaine_id> ,
    "file": <file>,
    "vues": <vues>
  },
  ...
}
```

## Delete stand account (Need Admin Access)

```
  DELETE http://<host>:5000/api/v1/delete_account
  Authorization: Bearer <Token>
  content-type: application/json
    
  {
    "compte_id": <compte_id>
  }
```
=> RETOUR:
```
  {
    "error": False,
    "message": "Account Deleted!"
  }
}
```

## Delete content of an account

```
  DELETE http://<host>:5000/api/v1/delete_content
  Authorization: Bearer <Token>
  content-type: application/json
    
  {
    content_id": <content_id>
  }
```
=> RETOUR:
```
  {
    "error": False,
    "message": "Content Deleted!"
  }
```

## Delete Fiche metier ( Need admin access )

```
  DELETE http://<host>:5000/api/v1/delete_fiche_metier
  Authorization: Bearer <Token>
  content-type: application/json
    
  {
    "fiche_metier_id": <fiche_metier_id>
  }
```
=> RETOUR:
```
  {
    "error": False,
    "message": "Fiche Metier Deleted!"
  }
```

## Update account information 

```
  PATCH http://<host>:5000/api/v1/update_account
  Authorization: Bearer <Token>
  content-type: application/json
    
  {
    "nom": <nom>,
    "email": <email>,
    "tel": <tel>,
    "domaine": <domaine>,
    "description": <description>,
    "adresse": <adresse>,
    "lien": <lien>
  }
```
=> RETOUR:
```
  {
    "error": False,
    "message": "Compte Updated!"
  }
```

## Update content data 

```
  PATCH http://<host>:5000/api/v1/update_content
  Authorization: Bearer <Token>
  content-type: application/json
    
  {
    "titre": <titre>,
    "description": <description>,
    "type": <type>,
    "content_id": <content_id>,
    "file": <fichier>
  }
```
=> RETOUR:
```
  {
    "error": False,
    "message": "Content Updated!"
  }
```

## Update fiche metier 
```
  PATCH http://<host>:5000/api/v1/update_fiche_metier
  Authorization: Bearer <Token>
  content-type: application/json
    
  {
    "titre": <titre>,
    "domaine_id": <domaine_id>,
    "fiche_metier_id": <fiche_metier_id>,
    "file": <fichier>
  }
```
=> RETOUR:
```
  {
    "error": False,
    "message": "Fiche Metier Updated!"
  }
```

## Get file link (image, video, pdf, ...) 
```
  GET http://<host>:5000/api/v1/get_attachement/<compte_id>/<attachement_name>
```

## Get stats data (number of consultation within per day )
NB : Can specify content_type (mandatory)
```
  GET http://<host>:5000/api/v1/get_stats?content_type=<content_type>
  Authorization: Bearer <Token>
```

## Change Password
```
  PATCH http://<host>:5000/api/v1/change_password
  Authorization: Bearer <Token>
  Content-Type: application/json
  {
      "old_password": <old_password>,
      "new_password": <new_password>
  }
```

## Update enterprise logo
```
  PATCH http://<host>:5000/api/v1/update_logo
  Authorization: Bearer <Token>
  enctype: 'multipart/form-data'
  Content-Type: false
  {
      "logo": <file_logo>
  }
```

## Update enterprise video
```
  PATCH http://<host>:5000/api/v1/update_video
  Authorization: Bearer <Token>
  enctype: 'multipart/form-data'
  Content-Type: false
  {
      "video": <file_video> or <facebook_linl>
  }
```

## Update account state (activate/deactivate)
```
PATCH http://localhost:7878/api/v1/active_account
Authorization: Bearer <token>
Content-Type: application/json

{
    "state": <0 or 1>,
    "compte_id": <compte_id>
}
```
==> RETOUR 
```
  {
      "error": False,
      "message": "ACCOUNT State updated"
  }
```