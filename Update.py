import urllib.request, urllib.parse, json, ssl, random

f = open("config.json", "r", encoding="utf-8")
dic = json.load(f)
f.close()

TOKEN = dic["TOKEN"]

API = "https://api.telegram.org/"
URL = "bot" + TOKEN + "/"

def deal(Update):
	text = Update["message"]["text"]
	l = text.split(maxsplit=2)
	if len(l) > 1:
		command, query = l
	else:
		command = l[0]
		query = None 
	
	pass
	return

def roll(query):
	# d = 1#1d20+0
	# [count'#']'d'[max]['+'plus]' '[description]
	if query == None:
		return random.randrange(20) + 1
	
	if ' ' in query:
		expr, description = query.split(maxsplit=2)
	else:
		expr = query
		description = None
	
	result = 0
	return result