
import ampalibe
from ampalibe import Payload
from conf import Configuration
from utils.utils import translate
from ampalibe.ui import QuickReply,Button,Element
from model import UserModel,Attachment,History
import wget 
from random import randint
from secrets import token_hex
import qrcode

conf = Configuration()

model = UserModel(conf)
fichier = Attachment(conf)
history = History(conf)

bot = ampalibe.init(conf)
chat = bot.chat
query = bot.query

class UserView:
    def get_started(self,payload='/'):
        chat.get_started(payload)
    
    def persistant_menu(self,sender_id,lang):
        persistent_menu = [
            {
                "type": "postback",
                "title": translate("persistant1",lang),
                "payload": "/pers1"
            },
            {
                "type": "postback",
                "title": translate("persistant2",lang),
                "payload": "/pers2"
            },
            {
                "type": "postback",
                "title":  translate("persistant3",lang),
                "payload": "/pers3"
            }
        ]
        chat.persistent_menu(sender_id, persistent_menu)
        
    def demande_langue(self, sender_id,lang):
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
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
        chat.send_quick_reply(sender_id,quick_rep,translate("demande_langue",lang))
        query.set_action(sender_id, '/get_lang')
        
    def menu_principale(self,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        quick_rep = [
            QuickReply(
                title=translate("menu1",lang),
                payload="/menu1",
            ),
            QuickReply(
                title=translate("menu2",lang),
                payload="/menu2",
            ),
            QuickReply(
                title=translate("menu3",lang),
                payload="/menu3",
            ),
        ]
        chat.send_quick_reply(sender_id,quick_rep,translate("menu_principale",lang))

    def update_lang(self,sender_id,cmd):
        chat.send_action(sender_id,"mark_seen")
        lang = cmd.split("//")[-1]
        try :
            model.set_lang(sender_id,lang)
        except :
            chat.send_message(sender_id, translate('erreur',lang))
        self.persistant_menu(sender_id,lang)
        chat.send_message(sender_id, translate('c_noter',lang))
        self.menu_principale(sender_id,lang)
        query.set_action(sender_id, None)
        

    def started(self,sender_id,lang):
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        chat.send_message(sender_id, 
            """
                Bienvenue Arlème, Roso 🔥🔥 \n Un bot qui va vous aider dans vos transférer de données 🇬🇧🇫🇷🇲🇬. 
            """
            )

        self.demande_langue(sender_id,lang)

    ### Les peristantes menus
    def persistant1(self ,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        quick_rep = [
            QuickReply(
                title=translate("menu1",lang),
                payload="/menu1",
            ),
            QuickReply(
                title=translate("menu2",lang),
                payload="/menu2",
            ),
            QuickReply(
                title=translate("menu3",lang),
                payload="/menu3",
            ),
        ]
        chat.send_quick_reply(sender_id,quick_rep,translate("menu_principale",lang))

    def persistant2(self ,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        chat.send_message(sender_id,"Persistante menu 2")

    ### Les menus
    def menu1(self ,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        quick_rep = [
            QuickReply(
                title="Token 🛅",
                payload="/token",
            ),
            QuickReply(
                title="Qr code 🔑",
                payload="/qr_code",
            ),
        ]
        chat.send_quick_reply(sender_id,quick_rep,"Voulez-vous le récuperer par : ")

    def menu_token(self,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        chat.send_message(sender_id,"Veuiller envoyer votre token 😊.") 
        query.set_action(sender_id, "attente_code")
      
    def menu_qr_code(self,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        chat.send_message(sender_id,"Veuiller envoyer votre qr code 😊.") 
        query.set_action(sender_id, "attente_code")

    def menu2(self ,sender_id,lang) :
        chat.send_action(sender_id,"mark_seen")
        self.persistant_menu(sender_id,lang)
        chat.send_message(sender_id,"Veuiller envoyer le fichier à envoyer 😊.")
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
            wget.download(cmd, f'/opt/HIU/bot/assets/public/{str(file)}')
            tok = token_hex(16)
            fichier.addAttachment(f"{str(file)}",1,sender_id,tok)
            chat.send_message(sender_id,"Merci votre fichier est envoyé.")
            chat.send_message(sender_id, "Le token de récupération est :")
            chat.send_message(sender_id,f"{tok}")
            img = qrcode.make(tok)
            img.save('assets/public/qr.png')
            res = chat.send_file_url(sender_id, f"{conf.APP_URL}/asset/qr.png",filetype='image')
            print(res)
            query.set_action(sender_id, None)
        except Exception as e:
            chat.send_message(sender_id,"Désolé 😢, il y a eu une érreur lors du télechargement, veuillez réessayez s'il vous plaît")
            query.set_action(sender_id, None)
    def send_file(self,sender_id,cmd):
        chat.send_action(sender_id,"mark_seen")      
        chat.send_message(sender_id,"On va vérifier si votre fichier existe")
        res = fichier.verif_attach(sender_id,cmd)
        if res == False :
            chat.send_message(sender_id,"Votre fichier est introuvable ‼️‼️.")
            query.set_action(sender_id, None)
            return
        chat.send_message(sender_id,"C'est bon✔️, je l'ai trouvé on vous envoie ça de suite.")
        list_items = []

        buttons = [
            Button(
                type="postback",
                title="Télecharger📂",
                payload=Payload("/download", name=res),
            ),
            Button(
                type="postback",
                title="Token 🗝",
                payload=Payload("/tokens", name=item[0]),
            )
        ]
        list_items.append(
            Element(
                title=res,
                subtitle="Date upload : 23-04-2022",
                image_url=f"{conf.APP_URL}/asset/icon_file.jpg",
                buttons=buttons,
            )
        )
        # next=True for displaying directly next page button.
        chat.send_template(sender_id, list_items, next=True)
        query.set_action(sender_id, None)

    def file_send(self,sender_id ,name):
        chat.send_action(sender_id,"mark_seen") 
        chat.send_file_url(sender_id, f"{conf.APP_URL}/asset/{name}")
        query.set_action(sender_id, None)
    def send_tok(self,sender_id ,name):
        chat.send_action(sender_id,"mark_seen") 
        chat.send_message(sender_id,"Voici le token.")
        chat.send_message(sender_id,"49cbfcc292cc9c686aea64d24e1c6333")
        query.set_action(sender_id, None)
    def historique(self,sender_id,lang):
        chat.send_action(sender_id,"mark_seen")  
        chat.send_message(sender_id,"Voici l'historique de vos transferts.")
        list_items = []
        data = history.getAllHistory(sender_id)
        for item in data:
            buttons = [
                Button(
                    type="postback",
                    title="Télecharger📂",
                    payload=Payload("/download", name=item[0]),
                ),
                Button(
                    type="postback",
                    title="Token🗝",
                    payload=Payload("/tokens", name=item[0]),
                )
            ]
            list_items.append(
                Element(
                    title=item[0],
                    subtitle="Date upload : 23-04-2022",
                    image_url=f"{conf.APP_URL}/asset/icon_file.jpg",
                    buttons=buttons,
                )
            )
        # next=True for displaying directly next page button.
        chat.send_template(sender_id, list_items, next=True)
        query.set_action(sender_id, None)
