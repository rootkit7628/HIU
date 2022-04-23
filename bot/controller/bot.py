import ampalibe
from view import UserView
from model import UserModel
from conf import Configuration
from ampalibe.ui import QuickReply

user = UserView()
user_model = UserModel(Configuration())


user.get_started('/started')

# ------------------ COMMAND -------------------------------  
@ampalibe.command('/started')
def get_started(sender_id , cmd, **extends):
    lang = user_model.get_lang(sender_id)
    user.started(sender_id,lang)
    
@ampalibe.command('/')
def main(sender_id, cmd, **extends):
    lang = user_model.get_lang(sender_id)
    user.menu_principale(sender_id,lang)

# Les pérsistants menus 

@ampalibe.command('/pers1')
def persis1(sender_id, cmd,**extends):
    lang = user_model.get_lang(sender_id)
    user.persistant1(sender_id,lang)

@ampalibe.command('/pers2')
def persis2(sender_id, cmd,**extends):
    lang = user_model.get_lang(sender_id)
    user.persistant2(sender_id,lang)

@ampalibe.command('/pers3')
def persis3(sender_id, cmd,**extends):
    lang = user_model.get_lang(sender_id)
    user.demande_langue(sender_id,lang)

# Les ménus principales 

@ampalibe.command('/menu1')
def menus1(sender_id, cmd,**extends):
    lang = user_model.get_lang(sender_id)
    user.menu1(sender_id,lang)

@ampalibe.command('/menu2')
def menus2(sender_id, cmd,**extends):
    lang = user_model.get_lang(sender_id)
    user.menu2(sender_id,lang)

@ampalibe.command('/menu3')
def menus3(sender_id, cmd,**extends):
    lang = user_model.get_lang(sender_id)
    user.menu3(sender_id,lang)


# ------------------ ACTION -------------------------------   
@ampalibe.action('/get_lang')
def get_lang(sender_id , cmd, **extends):
    user.update_lang(sender_id,cmd)





