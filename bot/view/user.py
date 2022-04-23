
import ampalibe
from conf import Configuration
from utils.utils import translate
from ampalibe.ui import QuickReply
from model import UserModel

model = UserModel(Configuration())
bot = ampalibe.init(Configuration())
chat = bot.chat
query = bot.query


class UserView:
    def get_started(self, payload='/'):
        chat.get_started(payload)

    def persistant_menu(self, sender_id, lang):
        persistent_menu = [
            {
                "type": "postback",
                "title": translate("persistant1", lang),
                "payload": "/pers1"
            },
            {
                "type": "postback",
                "title": translate("persistant2", lang),
                "payload": "/pers2"
            },
            {
                "type": "postback",
                "title": translate("persistant3", lang),
                "payload": "/pers3"
            }
        ]
        chat.persistent_menu(sender_id, persistent_menu)

    def demande_langue(self, sender_id, lang):
        chat.send_action(sender_id, "mark_seen")
        self.persistant_menu(sender_id, lang)
        quick_rep = [
            QuickReply(
                title="MG🇲🇬",
                payload="//mg",
            ),
            QuickReply(
                title="FR🇫🇷",
                payload="//fr",
            ),
            QuickReply(
                title="EN🇬🇧",
                payload="//en",
            ),
        ]
        chat.send_quick_reply(sender_id, quick_rep, translate("demande_langue", lang))
        query.set_action(sender_id, '/get_lang')

    def menu_principale(self, sender_id, lang):
        chat.send_action(sender_id, "mark_seen")
        self.persistant_menu(sender_id, lang)
        quick_rep = [
            QuickReply(
                title=translate("menu1", lang),
                payload="/menu1",
            ),
            QuickReply(
                title=translate("menu2", lang),
                payload="/menu2",
            ),
            QuickReply(
                title=translate("menu3", lang),
                payload="/menu3",
            ),
        ]
        chat.send_quick_reply(sender_id, quick_rep, translate("menu_principale", lang))

    def update_lang(self, sender_id, cmd):
        chat.send_action(sender_id, "mark_seen")
        lang = cmd.split("//")[-1]
        try:
            model.set_lang(sender_id, lang)
        except Exception as err:
            print(err)
            chat.send_message(sender_id, translate('erreur', lang))
        self.persistant_menu(sender_id, lang)
        chat.send_message(sender_id, translate('c_noter', lang))
        self.menu_principale(sender_id, lang)
        query.set_action(sender_id, None)

    def started(self, sender_id, lang):
        chat.send_action(sender_id, "mark_seen")
        self.persistant_menu(sender_id, lang)
        chat.send_message(sender_id, "Zian 🔥🔥 \n Un bot qui va vous aider dans vos transférer de données 🇬🇧🇫🇷🇲🇬 .")
        self.demande_langue(sender_id, lang)

    # Les peristantes menus
    def persistant1(self, sender_id, lang):
        chat.send_action(sender_id, "mark_seen")
        self.persistant_menu(sender_id, lang)
        chat.send_message(sender_id, "Persistante menu 1")

    def persistant2(self, sender_id, lang):
        chat.send_action(sender_id, "mark_seen")
        self.persistant_menu(sender_id, lang)
        chat.send_message(sender_id, "Persistante menu 2")

    # Les menus
    def menu1(self, sender_id, lang):
        chat.send_action(sender_id, "mark_seen")
        self.persistant_menu(sender_id, lang)
        chat.send_message(sender_id, "Menu 1")

    def menu2(self, sender_id, lang):
        chat.send_action(sender_id, "mark_seen")
        self.persistant_menu(sender_id, lang)
        chat.send_message(sender_id, "Menu 2")

    def menu3(self, sender_id, lang):
        chat.send_action(sender_id, "mark_seen")
        self.persistant_menu(sender_id, lang)
        chat.send_message(sender_id, "Menu 3")
