from pathlib import Path
from secrets import token_hex
# from PIL import Image
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
if not os.path.isdir('../bot/assets/public'):
    os.makedirs('../bot/assets/public/')

UPLOAD_FOLDER = os.path.join(path, '../bot/assets/public/')
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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_VIDEOS
# *************************** ___________ *****************************


@verif_db
@app.route("/api/v1/login", methods=['POST'])
def login():
    """
        DESC : Fonction permettant l'authentification d'un utilisateur
    """
    try:
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if username and password:
            CURSOR.execute("SELECT * FROM amp_user WHERE username=%s and password=SHA2(%s, 256)", (username, password))
            if CURSOR.rowcount > 0:
                account = dict(zip(CURSOR.column_names, CURSOR.fetchone()))
                account.pop("password")
                account["token"] = create_access_token(
                    str(str(account.get("id")) + "+" + account.get("username"))
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
@app.route("/api/v1/add_user", methods=['POST'])
def add_user():
    """
        DESC : Fonction permettant d'ajouter un compte
        Juste pour les comptes  avec access admin
    """
    try:
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        user_id = data.get("user_id")

        if username and password:
            CURSOR.execute("SELECT * FROM amp_user WHERE username=%s", (username,))
            if CURSOR.rowcount < 1:
                CURSOR.execute(
                    """
                        INSERT INTO
                            amp_user(
                                username, password
                            )
                            VALUES (%s, SHA2(%s, 256))
                    """,
                    (username, password, user_id or None)
                )
                DB.commit()

                return {
                    "error": False,
                    "message": "Account created",
                    "account_id": CURSOR.lastrowid,
                    "username": username
                }, 200
            return {
                "error": False,
                "message": "Email already exists."
            }, 409
        return {
            "error": True,
            "message": "Données obligatoires manquants"
        }, 412

    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/add_file", methods=['POST'])
@jwt_required()
def add_file():
    """
        DESC : Fonction permettant d'ajouter du contenu
    """
    try:
        user_id = get_jwt_identity().split("+")[0]

        if request.form:
            filename = request.form.get("fichier")
        elif request.files:
            fichier = request.files['fichier']
            if fichier:
                compte_folder = app.config['UPLOAD_FOLDER']
                filename = str(time.time()) + '_' + secure_filename(fichier.filename)
                fichier.save(os.path.join(compte_folder, filename))

        try:
            if filename:
                token = token_hex(16)
                CURSOR.execute(
                    "INSERT INTO attachement(nom, token, user_id) VALUES (%s, %s, %s)",
                    (filename, token, user_id)
                )
                return {
                    "token": token
                }
        except Exception as err:
            print(err)
            return {
                "error": True,
                "message": "No file uploaded"
            }, 412
    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong: { err }")

@verif_db
@app.route("/api/v1/list_attachements", methods=['GET'])
@jwt_required()
def list_attachment():
    """
        DESC : Fonction permettant d'obtenir la liste
        des contenus d'un stands
    """
    try:
        user_id = get_jwt_identity().split("+")[0]
        print(user_id)
        if user_id:
            CURSOR.execute("""
                SELECT
                    At.nom,
                    At.status,
                    At.token,
                    At.user_id,
                    COUNT(DISTINCT Hs.id) Download
                FROM
                    `attachment` At
                LEFT JOIN
                    `history` Hs
                ON
                    At.id = Hs.attachment_id
                WHERE
                    At.user_id=%s AND Hs.action=%s
                GROUP BY
                    Hs.id;
            """, (user_id, 'UP')
            )
            attachments = CURSOR.fetchall()
            DB.commit()
            if attachments:
                return {
                    attachments.index(attachment):
                        dict(zip(CURSOR.column_names, attachment)) for attachment in attachments
                }, 200
            else:
                return {
                    "error": False,
                    "message": "No Attachement finded!"
                }, 200
        return {
            "error": True,
            "message": "Pas d'access"
        }, 403

    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/delete_attachement", methods=['DELETE'])
@jwt_required()
def delete_attachement():
    """
        DESC : Fonction permettant de supprimer un contenu
    """
    try:
        user_id = get_jwt_identity().split("+")[0]
        attachment_id = request.get_json().get("attachement_id")

        if user_id:
            try:
                CURSOR.execute("""
                    DELETE FROM
                        attachment
                    WHERE
                        id=%s AND user_id=%s;
                """, (attachment_id, user_id))

                DB.commit()

                return {
                    "error": False,
                    "message": "Attachment Deleted!"
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
            "message": "Pas d'access"
        }, 403

    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/update_attachment", methods=['PATCH'])
@jwt_required()
def update_attachment():
    """
        DESC : Fonction permettant de mettre à jour
        les infos sur un contenus
    """
    try:
        filename = None
        user_id = int(get_jwt_identity().split("+")[0])

        if user_id:
            attachment_id = int(request.form.get("attachment_id"))
            attachment = [
                request.form.get("nom"),
                request.form.get("action"),
            ]

            if request.files:
                fichier = request.files['file']

                compte_folder = os.path.join(
                    app.config['UPLOAD_FOLDER'], str(user_id)
                )
                Path(compte_folder).mkdir(parents=True, exist_ok=True)

                filename = str(time.time()) + '_' + secure_filename(fichier.filename)
                fichier.save(os.path.join(compte_folder, filename))

                if filename:
                    attachment.append(filename)

            attachment += [attachment_id, user_id]

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
                        id=%s AND user_id=%s;
                """, attachment)

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


@app.route('/api/v1/get_attachement/<user_id>/<attachement>', methods=['GET'])
def get_attachement(user_id, attachement):
    """
        DESC : Fonction permettant de récuperer un fichier
    """
    try:
        if user_id:
            compte_folder = os.path.join(
                app.config['UPLOAD_FOLDER'], str(user_id)
            )
            return send_from_directory(
                directory=compte_folder, path=attachement)
    except Exception as err:
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@app.route('/api/v1/change_password', methods=['PATCH'])
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity().split("+")[0])
    data = request.get_json()
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if user_id and old_password and new_password:
        try:
            CURSOR.execute(
                "SELECT 1 FROM Compte WHERE id=%s AND password=SHA2(%s, 256)", (user_id, old_password,))

            exists = CURSOR.fetchone()[0]
            if exists:
                CURSOR.execute("""
                    UPDATE
                        Compte
                    SET
                        password=SHA2(%s, 256)
                    WHERE
                        id=%s;
                    """, (new_password, user_id)
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
    user_id = int(get_jwt_identity().split("+")[0])
    try:
        if request.files:
            logo = request.files['logo']

            compte_folder = os.path.join(
                    app.config['UPLOAD_FOLDER'], str(user_id)
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
                    """, (filename, user_id)
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


@app.route('/api/v1/archive_attachment', methods=['PATCH'])
@jwt_required()
def archive_attachment():
    user_id = get_jwt_identity().split("+")[0]
    data = request.get_json()
    try:
        if data:
            attachement_id = data.get("attachement_id")
            if user_id:
                CURSOR.execute("""
                    UPDATE
                        attachment
                    SET
                        state=%s
                    WHERE
                        id=%s;
                    """, (1, attachement_id)
                )

                DB.commit()
                return {
                    "error": False,
                    "message": "Attachment archived !"
                }, 200
            return {
                "error": True,
                "message": "No enough data to archive"
            }, 400
        return {
            "error": True,
            "message": "No data posted"
        }, 400
    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/get_file_v1/<token>", methods=['GET'])
def get_file_v1(token):
    """
        DESC : Fonction permettant d'ajouter du contenu
    """
    try:
        if token:
            CURSOR.execute("""
                SELECT
                    nom
                FROM
                    `attachment`
                WHERE
                    token=%s;
            """, (token,)
            )

            nom = CURSOR.fetchone()[0]
            DB.commit()

            return {"url": "https://bot-hiu.iteam-s.mg/asset/" + nom}

        return {
            "error": True,
            "message": "Pas de donnee envoye dans le formulaire."
        }, 412

    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong :  { err }")


@verif_db
@app.route("/api/v1/add_file_v1/", methods=['POST'])
def add_file_v1():
    """
        DESC : Fonction permettant d'ajouter du contenu
    """
    try:
        if request.form:
            filename = request.form.get("fichier")
        elif request.files:
            fichier = request.files['fichier']
            if fichier:
                compte_folder = app.config['UPLOAD_FOLDER']
                filename = str(time.time()) + '_' + secure_filename(fichier.filename)
                fichier.save(os.path.join(compte_folder, filename))

        try:
            if filename:
                token = token_hex(16)
                CURSOR.execute(
                    "INSERT INTO attachement(nom, token) VALUES (%s, %s)",
                    (filename, token,)
                )
                return {
                    "token": token
                }
        except Exception as err:
            print(err)
            return {
                "error": True,
                "message": "No file uploaded"
            }, 412
    except Exception as err:
        CURSOR.close()
        print(f"[ERROR] : { err }")
        abort(500, description=f"Something went wrong: { err }")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=7878)
