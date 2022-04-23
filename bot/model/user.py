from select import select
from ampalibe import Model


class UserModel(Model):

    def __init__(self, conf):
        super().__init__(conf)
    
    @Model.verif_db
    def get_lang(self,id):
        req = "SELECT lang from amp_user WHERE user_id = %s"
        self.cursor.execute(req,(id,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @Model.verif_db
    def set_lang(self, user_id, lang):
        req = 'UPDATE amp_user set lang = %s WHERE user_id = %s'
        self.cursor.execute(req, (lang, user_id))
        self.db.commit()
    

class Login(Model):
    def __init__(self, conf):
        super().__init__(conf)
    
    # ======================= CONNEXION USER ========================
    @Model.verif_db
    def loginFacebook(self, username):
        requete = """SELECT True, id, username, last_use, lang
            FROM amp_user WHERE username = %s"""
        self.cursor.execute(requete, (username,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data


    @Model.verif_db
    def loginAmp_user(self, username, password):
        requete = """SELECT True, id, username, last_use, lang
            FROM amp_user WHERE username = %s AND password = SHA2(%s, 256)"""
        self.cursor.execute(requete, (username, password))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data


class Amp_user(Model):
    def __init__(self, conf):
        super().__init__(conf)

    
    # ============================== GET USER ======================
    @Model.verif_db
    def getAllAmp_user(self):
        requete = """SELECT id, username, last_use, lang
            FROM amp_user"""
        self.cursor.execute(requete)
        data = self.cursor.fetchall()[0]
        self.db.commit()
        return data

    
    @Model.verif_db
    def getAmp_user(self, id):
        requete = """SELECT id, username, last_use, lang
            FROM amp_user WHERE (id = %s OR username = %s)"""
        self.cursor.execute(requete, (id, id))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    
    # ============================== ADD USER =========================
    @Model.verif_db
    def addAmp_user(self, username, password, user_id):
        requete = """INSERT INTO amp_user(username, password, user_id)
            VALUES(%s, %s, %s)"""
        self.cursor.execute(requete, (username, password, user_id))
        self.db.commit()
        return 1
    

    # ============================= UPDATE USER =======================
    @Model.verif_db
    def updateAmp_userAction(self, action, id):
        requete = """UPDATE amp_user 
            SET action = %s WHERE (id = %s OR id = %s)"""
        self.cursor.execute(requete, (action, id, id))
        self.db.commit()
        return 1


    @Model.verif_db
    def verifyPassword(self, password, id):
        requete = """SELECT True FROM amp_user
            WHERE (password =%s AND id = %s)"""
        self.cursor.execute(requete, (password, id))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data if data == 1 else 0


    @Model.verif_db
    def updateAmp_userPassword(self, lastPassword, newPassword, id):
        status = 0
        if(self.verifyPassword(password=lastPassword, identifiant=id) == 1):
            requete = """UPDATE amp_user SET password = %s WHERE id = %s"""
            self.cursor.execute(requete, (newPassword, id))
            self.db.commit()
            status = 1
        return status


    @Model.verif_db
    def updateAmp_userLang(self, lang, id):
        requete = """UPDATE amp_user SET lang = %s WHERE id = %s"""
        self.cursor.execute(requete, (lang, id))
        self.db.commit()
        return 1

    
    # ============================= DELETE USER =======================
    # ******************** à penser encore ****************************


class Attachment(Model):
    def __init__(self, conf):
        super().__init__(conf)


    # ===================== GET ATTACHMENT ===================
    @Model.verif_db
    def getAllAttachment(self):
        requete = """SELECT id, nom, status, user_id
            FROM attachment"""
        self.cursor.execute(requete)
        data = self.cursor.fetchall()[0]
        self.db.commit()
        return data

    
    @Model.verif_db
    def getAttachment(self, user_id):
        requete = """SELECT id, nom, status, user_id
            FROM attachmemnt WHERE user_id = %s"""
        self.cursor.execute(requete, (user_id,))
        data = self.cursor.fetchall()[0]
        self.db.commit()
        return data


    # ======================== ADD ATTACHEMENT =====================
    @Model.verif_db
    def addAttachment(self, nom, status, user_id):
        requete = """INSERT INTO attachment(nom, status, user_id)
            VALUES(%s, %s, %s)"""
        self.cursor.execute(requete, (nom, status, user_id))
        self.db.commit()
        return 1

    # ====================== UPDATE ATTACHMENT =======================
    @Model.verif_db
    def updateAttachmentStatus(self, status, id, user_id):
        requete = """UPDATE attachment SET status = %s 
            WHERE (id = %s AND user_id = %s)"""
        self.cursor.execute(requete, (status, id, user_id))
        self.db.commit()
        return 1

    
    # ==================== DELETE ATTACHMENT =======================
    def deleteAttachment(self, id, user_id):
        requete = """DELETE FROM attachment WHERE (id = %s AND user_id = %s)"""
        self.cursor.execute(requete, (id, user_id))
        self.db.commit()
        return 1


class History(Model):
    def __init__(self, conf):
        super().__init__(conf)

    
    # ========================= GET HISTORY ===========================
    def getAllHistory(self):
        requete = """SELECT id, """
