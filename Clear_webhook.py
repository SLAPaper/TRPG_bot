import urllib.request, urllib.parse, json, ssl

f = open("config.json", "r", encoding="utf-8")
dic = json.load(f)
f.close()

TOKEN = dic["TOKEN"]

API = "https://api.telegram.org/"
URL = "bot" + TOKEN + "/"

https_handler = urllib.request.HTTPSHandler(context=ssl.create_default_context())
proxy_handler = urllib.request.ProxyHandler({'https':'127.0.0.1:8090',})
webhook_opener = urllib.request.build_opener(https_handler, proxy_handler)

webhook_response = webhook_opener.open(API + URL + "setWebhook")

for l in webhook_response:
	print(l.decode("utf_8"))