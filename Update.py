import random, Telegram_API.py

def deal(data):
	l = data["message"]["text"].split(maxsplit=2)
	command = l[0].strip('/')
	try:
		globals()["do_" + command](data)
	except:
		# Not valid command

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

def do_r(data):
	l = data["message"]["text"].split(maxsplit=2)
	if len(l) > 1:
		query = l[1]
	else:
		query = None 
	result = roll(query)
	# POST the result

def do_me(data):
	# POST the result