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
	# [times'#'][count]'d'[faces]['+'addend]' '[description]
	
	try:
		if 'd' in query:
			def f(s):
				if s.isnumeric():
					return int(s)
				else:
					return 1
			front, back = query.split('d', maxsplit=2)
			
			if '#' in front:
				times, count = map(f, front.split('#'))
			else if front.isnumeric():
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
			else if: back2.isnumeric():
				faces = int(back2)
				addend = 0
			else:
				faces = 20
				addend = 0
		
		result = []
		for i in range(times):
			dice_sum = 0
			for j in range(count):
				dice_sum += random.randrange(faces)
			dice_sum += addend
			result.append(dice_sum)
		return tuple(result)
	except:
		return random.randrange(20) + 1