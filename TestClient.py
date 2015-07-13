import urllib.request, urllib.parse, json, ssl

f = open("config.json", "r", encoding="utf_8")
dic = json.load(f)
f.close()

TOKEN = dic["TOKEN"]
PORT = dic["PORT"]
PATH = dic["PATH"]

WEB_HOOK_HOST = "https://" + PATH + TOKEN + "/"

https_handler = urllib.request.HTTPSHandler(context=ssl.create_default_context())
proxy_handler = urllib.request.ProxyHandler({'https':'127.0.0.1:8090',})
opener = urllib.request.build_opener(https_handler, proxy_handler)

data = "Hello World!".encode('utf_8')
response = opener.open(WEB_HOOK_HOST, data=data)

for l in response:
	print(l.decode("utf_8"))