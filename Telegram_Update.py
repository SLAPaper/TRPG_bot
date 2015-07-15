import random, Telegram_API.py

def deal(prefix, update):
    l = update.message.text.split(maxsplit=2)
    command = l[0].strip('/')
    try:
        globals()["do_" + command](prefix, update.message)
    except:
        Telegram_API.sendMessage(prefix, update.message.chat.id_, "Invalid command, type /help for help.")

def roll(query):
    # d = 1#1d20+0
    # [times'#'][count]'d'[faces]['+'addend]' '[description]
    
    if 'd' in query:
        def f(s):
            if s.isnumeric():
                return int(s)
            else:
                return 1
        front, back = query.split('d', maxsplit=2)
        
        if '#' in front:
            times, count = map(f, front.split('#'))
        elif front.isnumeric():
            times = 1
            count = int(front)
        else:
            times = 1
            count = 1
        
        if ' ' in back:
            back2, description = back.split(maxsplit=2)
        else:
            back2 = back
            description = None
        
        if '+' in back2:
            faces, addend = map(f, back2.split('+'))
        elif back2.isnumeric():
            faces = int(back2)
            addend = 0
        else:
            faces = 20
            addend = 0
    
    try:
        result = []
        for i in range(times):
            dice_sum = 0
            for j in range(count):
                dice_sum += random.randrange(faces)
            dice_sum += addend
            result.append(dice_sum)
        return tuple(result)
    except:
        return tuple(random.randrange(20) + 1)

def do_r(prefix, message):
    l = message.text.split(maxsplit=2)
    if len(l) > 1:
        query = l[1]
    else:
        query = None 
    result = roll(query)
    text = query + " = " + result
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