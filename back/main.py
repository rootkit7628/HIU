from pathlib import Path
from PIL import Image
import mysql.connector
from werkzeug.utils import secure_filename
# ---------------------------------------
from flask_cors import CORS
from flask import Flask, request, abort, send_from_directory
from flask_bcrypt import check_password_hash, generate_password_hash
# ---------------------------------------
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token
# ---------------------------------------
from datetime import timedelta
import time
import os
# ---------------------------------------
from conf import database
# ---------------------------------------
import codecs
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)


app = Flask(__name__)
CORS(app)

TRANSPARENCY = 12

# ------------UPLOAD FOLDER CONF---------------
path = os.getcwd()
if not os.path.isdir('data'):
    os.makedirs('data/')

UPLOAD_FOLDER = os.path.join(path, 'data/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ---------------------------------------------

# ----------------TOKEN CONFIG-----------------
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=600)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1000 * 1000
jwt = JWTManager(app)
# ---------------------------------------------

# --------------DATABASE CONNECT---------------
DB = mysql.connector.connect(**database())
CURSOR = DB.cursor(buffered=True)


def verif_db(fonction):
    '''
        Un decorateur de verification de la
        connexion au serveur avant traitement.
    '''
    def trt_verif(*arg, **kwarg):
        if not DB.is_connected():
            DB.reconnect()
        return fonction(*arg, **kwarg)
    return trt_verif
# ---------------------------------------------


# *************************** ERROR Handler *****************************
@app.errorhandler(404)
def page_not_found(e):
    return "Ressource Not Found", 404


@app.errorhandler(500)
def internal_server_error(e):
    return e, 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413
# *************************** ___________ *****************************


# ************************ Handle Allowed file ************************
ALLOWED_EXTENSIONS_VIDEOS = set(['mp4', 'mkv', 'avi', 'webm'])


def allowed_file_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower(
        ) in ALLOWED_EXTENSIONS_VIDEOS
# *************************** ___________ *****************************


@verif_db
@app.route("/api/v1/login", methods=['POST'])
def login():
    """
        DESC : Fonction permettant l'authentification d'un utilisateur
    """
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if email and password:
            CURSOR.execute("SELECT * FROM Compte WHERE email=%s", (email,))
            if CURSOR.rowcount > 0:
                account = dict(zip(CURSOR.column_names, CURSOR.fetchone()))
                if check_password_hash(str(account.get("password")), password):
                    account.pop("password")
                    account["token"] = create_access_token(
                        str(str(account.get("id")) + "+" + account.get("type"))
                    )
                    return account, 200
            DB.commit()
            return {
                "error": True,
                "message": "Email/password incorrect"
            }, 412
        return {
            "error": True,
            "message": "Email/password manquants"
        }, 412

    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/add_account", methods=['POST'])
@jwt_required()
def add_account():
    """
        DESC : Fonction permettant d'ajouter un compte
        Juste pour les comptes  avec access admin
    """
    try:
        data = request.get_json()
        access = get_jwt_identity().split("+")[1]

        nom = data.get("nom")
        email = data.get("email")
        tel = data.get("tel")
        domaine = data.get("domaine")
        password = data.get("password")
        adresse = data.get("adresse")
        type = data.get("type")
        lien = data.get("lien")
        classe = data.get("classe") or 5

        if access == "ADMIN":
            if nom and email and type and classe and password:
                CURSOR.execute("SELECT * FROM Compte WHERE email=%s", (email,))
                if CURSOR.rowcount < 1:
                    password = str(generate_password_hash(password).decode())
                    CURSOR.execute(
                        """
                        INSERT INTO
                            Compte(
                                nom, tel, email, type, lien,
                                domaine, password, adresse, classe
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            nom, tel, email, type, lien,
                            domaine, password, adresse, str(classe)
                        )
                    )
                    DB.commit()

                    return {
                        "error": False,
                        "message": "Account created",
                        "account_id": CURSOR.lastrowid
                    }, 200
                return {
                        "error": False,
                        "message": "Email already exists."
                }, 409
            return {
                "error": True,
                "message": "Données obligatoires manquants"
            }, 412
        return {
            "error": True,
            "message": "Pas d'access"
        }, 403

    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/add_content", methods=['POST'])
@jwt_required()
def add_content():
    """
        DESC : Fonction permettant d'ajouter du contenu
    """
    try:
        compte_id = get_jwt_identity().split("+")[0]

        if request.form:
            filenames, filename = [], None
            titre = request.form.get("titre")
            description = request.form.get("description") or None
            type = request.form.get("type")
            media = request.form.get("media")

            if request.files.getlist("media"):
                compte_folder = os.path.join(
                    app.config['UPLOAD_FOLDER'], str(compte_id)
                )
                Path(compte_folder).mkdir(parents=True, exist_ok=True)
                files = request.files.getlist("media")
                for file in files:
                    filename = str(
                        time.time()) + '_' + secure_filename(file.filename)
                    file.save(
                        os.path.join(compte_folder, filename))
                    filenames.append(filename)

            if titre and type and compte_id:
                req = """
                    INSERT INTO
                        Contenu(titre, description, type, fichier, compte_id)
                    VALUES (%s, %s, %s, %s, %s)
                """

                if filenames:
                    CURSOR.executemany(req, [(
                        titre,
                        description,
                        type,
                        filename,
                        compte_id) for filename in filenames]
                    )
                else:
                    CURSOR.execute(req, (
                            titre,
                            description,
                            type,
                            media,
                            compte_id
                        )
                    )

                DB.commit()
                return {
                    "error": False,
                    "message": "Contenu inserted"
                }, 200

            return {
                "error": True,
                "message": "Donnees obligatoires manquants"
            }, 412

        return {
            "error": True,
            "message": "Pas de donnee envoye dans le formulaire."
        }, 412

    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/add_fiche_metier", methods=['POST'])
@jwt_required()
def add_fiche_metier():
    """
        DESC : Fonction permettant d'ajouter des fiche metier
        Juste pour les comptes  avec access admin
    """
    try:
        compte_id, access = get_jwt_identity().split("+")

        filename = None
        titre = request.form.get("titre")
        domaine_id = request.form.get("domaine_id")
        if access == "ADMIN":
            if request.files:
                fichier = request.files['file']

                compte_folder = os.path.join(
                    app.config['UPLOAD_FOLDER'], str(compte_id)
                )
                Path(compte_folder).mkdir(parents=True, exist_ok=True)

                filename = str(time.time()) + '_' + secure_filename(
                    fichier.filename)
                fichier.save(
                    os.path.join(compte_folder, filename)
                )

                image = Image.open(os.path.join(compte_folder, filename))
                watermark = Image.open('./filigramme.png')
                if watermark.mode != 'RGBA':
                    print("HER")
                    alpha = Image.new('L', watermark.size, 255)
                    watermark.putalpha(alpha)
                paste_mask = watermark.split()[3].point(
                    lambda i: i * TRANSPARENCY / 100)
                image.paste(watermark, (70, 600), mask=paste_mask)
                image.save(os.path.join(compte_folder, filename))

                if titre and domaine_id:
                    CURSOR.execute("""
                        INSERT INTO
                            Fiche_metier(titre, fichier, domaine_id, compte_id)
                            VALUES (%s, %s, %s, %s)
                        """, (titre, filename, domaine_id, compte_id)
                    )
                    DB.commit()

                    return {
                        "error": False,
                        "message": "Contenu inserted",
                        "id": CURSOR.lastrowid
                    }, 200

                return {
                    "error": True,
                    "message": "Donnees obligatoires manquants"
                }, 412

    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


# -------------------- GET LIST API ----------------
@verif_db
@app.route("/api/v1/list_accounts", methods=['GET'])
@jwt_required()
def list_accounts():
    """
        DESC : Fonction permettant d'obtenir la liste
        des comptes entreprises existants
        Juste pour les comptes  avec access admin
    """
    try:
        access = get_jwt_identity().split("+")[1]

        if access == "ADMIN" or access == "ENTREPRISE":
            CURSOR.execute("""
                SELECT
                   Cp.id,
                   Cp.nom,
                   Cp.tel,
                   Cp.email,
                   Cp.type,
                   Cp.lien,
                   Cp.logo,
                   Cp.description,
                   Cp.domaine,
                   Cp.video,
                   Cp.actif,
                   Cp.adresse,
                   COUNT(DISTINCT Cs.id) visiteurs
                FROM
                    Compte Cp
                LEFT JOIN
                    Contenu Ct
                ON
                    Cp.id = Ct.compte_id
                LEFT JOIN
                    Consultation Cs
                ON
                    Ct.id = Cs.dimension
                GROUP BY
                    Cp.id;
            """)
            accounts = CURSOR.fetchall()
            DB.commit()
            if accounts:
                return {
                    accounts.index(account):
                        dict(
                            zip(CURSOR.column_names, account)
                        ) for account in accounts
                }, 200
            else:
                return {
                    "error": False,
                    "message": "No account finded!"
                }, 200
        return {
            "error": True,
            "message": "Pas d'access admin"
        }, 403

    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/list_contents", methods=['GET'])
@jwt_required()
def list_contents():
    """
        DESC : Fonction permettant d'obtenir la liste
        des contenus d'un stands
    """
    try:
        compte_id = get_jwt_identity().split("+")[0]

        if compte_id:
            CURSOR.execute(
                """
                    SELECT
                        Ct.id,
                        Ct.titre,
                        Ct.description,
                        Ct.type,
                        Ct.fichier,
                        COUNT(DISTINCT Cs.id) Vues
                    FROM
                        `Contenu` Ct
                    LEFT JOIN
                        `Consultation` Cs
                    ON
                        Ct.id = Cs.dimension
                    AND
                        Cs.type=%s
                    WHERE
                        Ct.compte_id=%s
                    GROUP BY
                        Ct.id;
                """, ('CONTENU', compte_id)
            )
            contents = CURSOR.fetchall()
            DB.commit()
            if contents:
                return {
                    contents.index(content):
                        dict(
                            zip(CURSOR.column_names, content)
                        ) for content in contents
                }, 200
            else:
                return {
                    "error": False,
                    "message": "No content finded!"
                }, 200
        return {
            "error": True,
            "message": "Pas d'access"
        }, 403

    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


# ---------------------------------------------------
@verif_db
@app.route("/api/v1/list_fiche_metier", methods=['GET'])
@jwt_required()
def list_fiche_metier():
    """
        DESC : Fonction permettant d'obtenir la liste
        listes des fiches metiers
    """
    try:
        compte_id = get_jwt_identity().split("+")[0]
        access = get_jwt_identity().split("+")[1]

        if access == "ADMIN":
            CURSOR.execute(
                """
                    SELECT
                        Fm.id,
                        Fm.titre,
                        Fm.fichier,
                        Fm.domaine_id,
                        COUNT(DISTINCT Cs.id) Vues
                    FROM
                        Fiche_metier Fm
                    LEFT JOIN
                        Consultation Cs
                    ON
                        Fm.id = Cs.dimension
                    AND
                        Cs.type = %s
                    GROUP BY
                        Fm.id;
                """, ("FICHE_METIER",)
            )
            fiche_metiers = CURSOR.fetchall()
            DB.commit()
            if fiche_metiers:
                return {
                    fiche_metiers.index(fiche_metier):
                        dict(
                            zip(CURSOR.column_names, fiche_metier)
                        ) for fiche_metier in fiche_metiers
                }, 200
            else:
                return {
                    "error": False,
                    "message": "No Fiche Metier finded!"
                }, 200
        return {
            "error": True,
            "message": "Pas d'access admin"
        }, 403

    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/delete_content", methods=['DELETE'])
@jwt_required()
def delete_content():
    """
        DESC : Fonction permettant de supprimer un contenu
    """
    try:
        compte_id, access = get_jwt_identity().split("+")
        content_id = request.get_json().get("content_id")

        if compte_id:
            try:
                CURSOR.execute("""
                    DELETE FROM
                        Contenu
                    WHERE
                        id=%s AND compte_id=%s;
                """, (content_id, compte_id))

                DB.commit()

                return {
                    "error": False,
                    "message": "Content Deleted!"
                }, 200
            except Exception as err:
                print(f"[ERROR] : { err }")
                DB.close()
                return {
                    "error": True,
                    "message": "le contenu est encore utilisé !"
                }, 400

        return {
            "error": True,
            "message": "Pas d'access admin"
        }, 403

    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/delete_account", methods=['DELETE'])
@jwt_required()
def delete_account():
    """
        DESC : Fonction permettant de supprimer
        un compte de stand
    """
    try:
        access = get_jwt_identity().split("+")[1]
        data = request.get_json()
        if data:
            account_id = data.get("compte_id")
        else:
            return {
                "error": True,
                "message": "Pas de compte à suprimmé"
            }, 400

        if access == "ADMIN" and account_id:
            try:
                CURSOR.execute("""
                    DELETE FROM
                        Compte
                    WHERE
                        id=%s;
                """, (account_id,))

                DB.commit()

                return {
                    "error": False,
                    "message": "Account Deleted!"
                }, 200
            except Exception as err:
                print(f"[ERROR] : { err }")
                return {
                    "error": True,
                    "message": "le compte est encore utilisé !"
                }, 400

        return {
            "error": True,
            "message": "Pas d'access admin"
        }, 403

    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/delete_fiche_metier", methods=['DELETE'])
@jwt_required()
def delete_fiche_metier():
    """
        DESC : Fonction permettant de supprimer un
        Fiche Metier
    """
    try:
        access = get_jwt_identity().split("+")[1]
        fiche_metier_id = int(request.get_json().get("fiche_metier_id"))

        if access == "ADMIN" and fiche_metier_id:
            try:
                CURSOR.execute("""
                    DELETE FROM
                        Fiche_metier
                    WHERE
                        id=%s;
                """, (fiche_metier_id,))

                DB.commit()

                return {
                    "error": False,
                    "message": "Fiche Metier Deleted!"
                }, 200
            except Exception as err:
                print(f"[ERROR] : { err }")
                DB.close()
                return {
                    "error": True,
                    "message": "le fiche metier est encore utilisé !"
                }, 400

        return {
            "error": True,
            "message": "Pas d'access admin"
        }, 403

    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/update_account", methods=['PATCH'])
@jwt_required()
def update_account():
    """
        DESC : Fonction permettant de mettre à jour
        les données du compte
    """
    try:
        compte_id = get_jwt_identity().split("+")[0]
        data = request.get_json()

        if compte_id:
            account = (
                data.get("nom"),
                data.get("email"),
                data.get("tel"),
                data.get("domaine"),
                data.get("description"),
                data.get("adresse"),
                data.get("lien"),
                int(compte_id)
            )
            try:
                CURSOR.execute("""
                    UPDATE
                        Compte
                    SET
                        nom = %s,
                        email = %s,
                        tel = %s,
                        domaine = %s,
                        description = %s,
                        adresse = %s,
                        lien = %s
                    WHERE
                        id=%s;
                """, account)

                DB.commit()

                return {
                    "error": False,
                    "message": "Account Updated!"
                }, 200
            except Exception as err:
                print(f"[ERROR] : { err }")
                DB.close()
                return {
                    "error": True,
                    "message": "le Compte est encore utilisé !"
                }, 400

        return {
            "error": True,
            "message": "Pas d'access"
        }, 403

    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/update_content", methods=['PATCH'])
@jwt_required()
def update_content():
    """
        DESC : Fonction permettant de mettre à jour
        les infos sur un contenus
    """
    try:
        filename = None
        compte_id = int(get_jwt_identity().split("+")[0])

        if compte_id:
            content_id = int(request.form.get("content_id"))
            content = [
                request.form.get("titre"),
                request.form.get("description"),
                request.form.get("type"),
            ]

            if request.files:
                fichier = request.files['file']

                compte_folder = os.path.join(
                    app.config['UPLOAD_FOLDER'], str(compte_id)
                )
                Path(compte_folder).mkdir(parents=True, exist_ok=True)

                filename = str(time.time()) + '_' + secure_filename(
                    fichier.filename)
                fichier.save(
                     os.path.join(compte_folder, filename)
                )

                if filename:
                    content.append(filename)
            content += [content_id, compte_id]

            try:
                CURSOR.execute(f"""
                    UPDATE
                        Contenu
                    SET
                        titre = %s,
                        description = %s,
                        type = %s
                        {", fichier = %s " if filename else " "}
                    WHERE
                        id=%s AND compte_id=%s;
                """, content)

                DB.commit()

                return {
                    "error": False,
                    "message": "Account Updated!"
                }, 200
            except Exception as err:
                print(f"[ERROR] : { err }")
                CURSOR.close()
                return {
                    "error": True,
                    "message": "le Contenu est encore utilisé !"
                }, 400

        return {
            "error": True,
            "message": "Pas d'access"
        }, 403

    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/update_fiche_metier", methods=['PATCH'])
@jwt_required()
def update_fiche_metier():
    """
        DESC : Fonction permettant de mettre à jour
        les infos sur un contenus
    """
    try:
        filename = None
        compte_id = int(get_jwt_identity().split("+")[0])

        if compte_id:
            fiche_metier_id = int(request.form.get("fiche_metier_id"))
            fiche_metier = [
                request.form.get("titre"),
                request.form.get("domaine_id"),
            ]

            if request.files:
                fichier = request.files['file']

                compte_folder = os.path.join(
                    app.config['UPLOAD_FOLDER'], str(compte_id)
                )
                Path(compte_folder).mkdir(parents=True, exist_ok=True)

                filename = str(time.time()) + '_' + secure_filename(
                    fichier.filename)
                fichier.save(
                     os.path.join(compte_folder, filename)
                )

                if filename:
                    fiche_metier.append(filename)

            fiche_metier += [fiche_metier_id, compte_id]
            try:
                CURSOR.execute(f"""
                    UPDATE
                        Fiche_metier
                    SET
                        titre = %s,
                        domaine_id = %s
                        {", fichier = %s " if filename else " "}
                    WHERE
                        id=%s AND compte_id=%s;
                """, fiche_metier)

                DB.commit()

                return {
                    "error": False,
                    "message": "Fiche Metier Updated!"
                }, 200
            except Exception as err:
                print(f"[ERROR] : { err }")
                CURSOR.close()
                DB.close()
                return {
                    "error": True,
                    "message": "le Fiche metier est encore utilisé !"
                }, 400

        return {
            "error": True,
            "message": "Pas d'access"
        }, 403

    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@app.route(
    '/api/v1/get_attachement/<compte_id>/<attachement>', methods=['GET'])
def get_attachement(compte_id, attachement):
    """
        DESC : Fonction permettant de récuperer un fichier
    """
    try:
        if compte_id:
            compte_folder = os.path.join(
                app.config['UPLOAD_FOLDER'], str(compte_id)
            )
            return send_from_directory(
                directory=compte_folder, path=attachement)
    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route('/api/v1/get_stats', methods=['GET'])
@jwt_required()
def get_stats():
    compte_id = int(get_jwt_identity().split("+")[0])
    content_type = request.args.get("content_type")

    try:
        if compte_id:
            CURSOR.execute(
                f"""
                    SELECT
                        Cs.date, Ct.type, COUNT(Cs.id) Vues
                    FROM
                        `Contenu` Ct
                    LEFT JOIN
                        `Consultation` Cs
                    ON
                        Ct.id = Cs.dimension
                    WHERE
                        Ct.compte_id = %s AND Cs.date IS NOT NULL
                    {
                        " AND Ct.type = %s " if content_type in (
                            'emploi', 'formation', 'galerie', 'actu') else ''
                    }
                        GROUP BY
                            Cs.date
                """, [compte_id] + (
                    [content_type] if content_type in (
                        'emploi', 'information', 'galerie', 'actu') else []))

            stats = CURSOR.fetchall()
            DB.commit()

            if stats:
                return {
                    stats.index(stat):
                        dict(
                            zip(CURSOR.column_names, stat)
                        ) for stat in stats
                }, 200
            else:
                return {
                    "error": False,
                    "message": "no data for the moment"
                }, 200

        return {
            "error": True,
            "message": "Pas d'access"
        }, 403
    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@app.route('/api/v1/change_password', methods=['PATCH'])
@jwt_required()
def change_password():
    compte_id = int(get_jwt_identity().split("+")[0])
    data = request.get_json()
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if compte_id and old_password and new_password:
        try:
            hashed_new_pass = str(
                generate_password_hash(new_password).decode())

            CURSOR.execute(
                "SELECT password FROM Compte WHERE id=%s", (compte_id,))

            hashed_old_pass = CURSOR.fetchone()[0]
            if hashed_old_pass and check_password_hash(
                hashed_old_pass, old_password
            ):
                CURSOR.execute("""
                    UPDATE
                        Compte
                    SET
                        password=%s
                    WHERE
                        id=%s;
                    """, (hashed_new_pass, compte_id)
                )

                DB.commit()
                if CURSOR.rowcount > 0:
                    return {
                        "error": False,
                        "message": "Password changed successfuly"
                    }, 200

            return {
                "error": True,
                "message": "Password incorrect or account don't exists"
            }, 403

        except Exception as err:
            CURSOR.close()
            print(f"[ERROR] : { err }")
            abort(500, description=f"Something went wrong :  { err }")
    return {
        "error": True,
        "message": "Needed Data not enough"
    }, 412


@app.route('/api/v1/update_logo', methods=['PATCH'])
@jwt_required()
def update_logo():
    compte_id = int(get_jwt_identity().split("+")[0])
    try:
        if request.files:
            logo = request.files['logo']

            compte_folder = os.path.join(
                    app.config['UPLOAD_FOLDER'], str(compte_id)
                )
            Path(compte_folder).mkdir(parents=True, exist_ok=True)

            filename = str(time.time()) + '_' + secure_filename(
                logo.filename)

            logo.save(
                    os.path.join(compte_folder, filename)
            )

            if filename:
                print(filename)
                CURSOR.execute("""
                    UPDATE
                        Compte
                    SET
                        logo=%s
                    WHERE
                        id=%s;
                    """, (filename, compte_id)
                )

                DB.commit()
                return {
                    "error": False,
                    "message": "Logo_updated",
                    "logo": filename
                }, 200
        return {
            "error": True,
            "message": "No file uploaded"
        }, 412

    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@app.route('/api/v1/update_video', methods=['PATCH'])
@jwt_required()
def update_video():
    compte_id = int(get_jwt_identity().split("+")[0])
    video, filename = None, None
    try:
        if request.form:
            filename = request.form.get("video")
        elif request.files:
            video = request.files['video']
            if video:

                if not allowed_file_video(video.filename):
                    return {
                        "error": True,
                        "message":
                            "Video must be less than 25Mo or Format not supported"
                    }, 413
                else:
                    compte_folder = os.path.join(
                        app.config['UPLOAD_FOLDER'], str(compte_id)
                    )

                    filename = str(time.time()) + '_' + secure_filename(
                        video.filename)

                    video.save(
                        os.path.join(compte_folder, filename)
                    )
        try:
            if filename:
                CURSOR.execute("""
                    UPDATE
                        Compte
                    SET
                        video=%s
                    WHERE
                        id=%s;
                    """, (filename, compte_id)
                )

                DB.commit()

                return {
                    "error": False,
                    "message": "Video Updated",
                    "logo": filename
                }, 200
            else:
                return {
                    "error": True,
                    "message": "No file uploaded "
                }, 412

        except Exception as err:
            CURSOR.close()
            print(f"[ERROR] : { err }")
            abort(500, description=f"Something went wrong :  { err }")
    except Exception as err:
            CURSOR.close()
            print(f"[ERROR] : { err }")
            abort(500, description=f"Something went wrong :  { err }")

@app.route('/api/v1/active_account', methods=['PATCH'])
@jwt_required()
def active_account():
    access = get_jwt_identity().split("+")[1]
    data = request.get_json()
    try:
        if data:
            state = data.get("state")
            compte_id = data.get("compte_id")
            if access == "ADMIN" and state and compte_id:
                CURSOR.execute("""
                    UPDATE
                        Compte
                    SET
                        actif=%s
                    WHERE
                        id=%s;
                    """, (str(state), compte_id)
                )

                DB.commit()
                return {
                    "error": False,
                    "message": "ACCOUNT State updated"
                }, 200
            return {
                "error": True,
                "message": "No enough data to update state"
            }, 400
        return {
            "error": True,
            "message": "No data posted"
        }, 400
    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


if __name__ == "__main__":
    app.run(debug=True, port=7878)
