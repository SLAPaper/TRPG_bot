import json, Telegram_API

f = open("config.json", "r", encoding="utf-8")
dic = json.load(f)
f.close()

TOKEN = dic["TOKEN"]

API = "https://api.telegram.org/"
URL = "bot" + TOKEN + "/"

response = Telegram_API.setWebhook(globals(), proxy={"https":"127.0.0.1:8090"})

for l in response:
	print(l.decode("utf_8"))