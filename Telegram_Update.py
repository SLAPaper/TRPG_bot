import Telegram_API
from bot_utility import roll

def deal(prefix, update):
    if update.message.text.startswith('/'):
        l = update.message.text.split(maxsplit=2)
        command = l[0].strip('/')
        try:
            globals()["do_" + command](prefix, update.message)
        except:
            Telegram_API.sendMessage(prefix, update.message.chat.id_, "Invalid command, type /help for help.".encode('utf_8'))

def do_help(prefix, message):
    # POST help message here
    HELP_MESSAGE = \
    """
    '/'command [query]
    
    command:
    'help': show this help
    'r' [times'#'][count]'d'[faces]['+'addend]' '[description]: roll dices
    'me' [action]: do charactor action
    """
    Telegram_API.sendMessage(prefix, message.chat.id_, HELP_MESSAGE)

def do_r(prefix, message):
    l = message.text.split(maxsplit=3)
    try:
        query = l[1]
    except:
        raise Exception("Empty query")
    
    user = message.from_
    name = user.first_name
    if user.last_name:
        name = name + " " + user.last_name
    if user.username:
        name = name + "(" + user.username + ")"
    
    result = roll(query)
    text = name + " " + query + " = " + str(result)
    if len(l) == 3:
        text = text + " " + l[2]
    
    Telegram_API.sendMessage(prefix, message.chat.id_, text)

def do_me(prefix, message):
    l = message.text.split(maxsplit=2)
    if len(l) > 1:
        query = l[1]
    else:
        query = "do nothing."
    user = message.from_
    name = user.first_name
    if user.last_name:
        name = name + " " + user.last_name
    if user.username:
        name = name + "(" + user.username + ")"
        
    text = name + " " + query
    Telegram_API.sendMessage(prefix, message.chat.id_, text)

class Update:
    def __init__(self, data):
        self.update_id = int(data["update_id"])
        self.message = Message(data["message"])

class Message:
    def __init__(self, data):
        self.message_id = int(data["message_id"])
        self.from_ = User(data["from"])
        self.date = int(data["date"])
        self.chat = Chat(data["chat"])
        
        self.text = data.get("text", "") 
        # others to be continued

class Chat:
    def __init__(self, data):
        self.id_ = data["id"]

class User(Chat):
    def __init__(self, data):
        super().__init__(data)
        self.first_name = data["first_name"]
        self.last_name = data.get("last_name")
        self.username = data.get("username")