
import ampalibe
from ampalibe import Payload
from conf import Configuration
from utils.utils import translate
from ampalibe.ui import QuickReply,Button,Element
from model import UserModel
import wget 
from random import randint

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

    def started(self,sender_id,lang):
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        chat.send_message(sender_id, "Roso 🔥🔥 \n Un bot qui va vous aider dans vos transférer de données 🇬🇧🇫🇷🇲🇬 .")
        self.demande_langue(sender_id,lang)

    # Les peristantes menus
    def persistant1(self, sender_id, lang):
        chat.send_action(sender_id, "mark_seen")
        self.persistant_menu(sender_id, lang)
        chat.send_message(sender_id, "Persistante menu 1")

    def persistant2(self, sender_id, lang):
        chat.send_action(sender_id, "mark_seen")
        self.persistant_menu(sender_id, lang)
        chat.send_message(sender_id, "Persistante menu 2")

    ### Les menus
    def menu1(self ,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        quick_rep = [
            QuickReply(
                title="Token🛅",
                payload="/token",
            ),
            QuickReply(
                title="Qr code🔑",
                payload="/qr_code",
            ),
        ]
        chat.send_quick_reply(sender_id,quick_rep,"Voulez-vous le récuperer par : ")

    def menu_token(self,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        chat.send_message(sender_id,"Veuiller envoyer votre token.") 
        query.set_action(sender_id, "attente_code")
      
    def menu_qr_code(self,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        chat.send_message(sender_id,"Veuiller envoyer votre qr code.") 
        query.set_action(sender_id, "attente_code")


    def menu2(self ,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        chat.send_message(sender_id,"Veuiller envoyer le fichier à envoyer.")
        query.set_action(sender_id, "attente_file")
        

    def menu3(self ,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        chat.send_message(sender_id,"Menu 3")


    def upload_file(self,sender_id,cmd) :
        chat.send_action(sender_id,"mark_seen")
        try :
            file =  cmd.split('/')[-1]
            file = file.split('?')[0]
            extension = file.split('.')[-1]
            name_file = randint(100000,2000000)
            wget.download(cmd, f'/home/rivo2302/Public/Projets/HIU/bot/assets/public/{str(name_file)}.{extension}')
            chat.send_message(sender_id,"Merci votre fichier est uploader")
            query.set_action(sender_id, None)
        except :
            chat.send_message(sender_id,"Désolé , il y a eu une érreur lors du télechargement, veuillez réessayez s'il vous plaît")
    
    def send_file(self,sender_id,cmd):
        chat.send_action(sender_id,"mark_seen")      
        print(cmd)
        chat.send_message(sender_id,"On va vérifier si votre fichier existe")
        ### Eto no jerena hoe misy ao am base de données ve ficheir 
        chat.send_message(sender_id,"C'est voici votre fichier.")
        list_items = []

        for i in range(1):
            buttons = [
                Button(
                    type="postback",
                    title="Télecharger",
                    payload=Payload("/download", name=i+1),
                )
            ]

            list_items.append(
                Element(
                    title="Fichier  ",
                    image_url="https://i.imgflip.com/6b45bi.jpg",
                    buttons=buttons,
                )
            )

        # next=True for displaying directly next page button.
        chat.send_template(sender_id, list_items, next=True)
        query.set_action(sender_id, None)


    def file_send(self,sender_id ,name):
        chat.send_action(sender_id,"mark_seen") 
        chat.send_file_url(sender_id, 'https://i.imgflip.com/6b45bi.jpg',filetype='file')
        query.set_action(sender_id, None)

    def historique(self,sender_id,lang):
        chat.send_action(sender_id,"mark_seen")  
        chat.send_message(sender_id,"Voici la liste de vos fichiers.")
        list_items = []

        for i in range(30):
            buttons = [
                Button(
                    type="postback",
                    title="Télecharger",
                    payload=Payload("/file", id_item=i+1),
                )
            ]
            list_items.append(
                Element(
                    title="Fichier  ",
                    image_url="https://i.imgflip.com/6b45bi.jpg",
                    buttons=buttons,
                )
            )

        # next=True for displaying directly next page button.
        chat.send_template(sender_id, list_items, next=True)
        query.set_action(sender_id, None)
