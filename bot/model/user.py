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