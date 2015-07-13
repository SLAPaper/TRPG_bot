import urllib.request, urllib.parse, json, ssl

TOKEN = "119827757:AAFTo0ezhROp-0Ria-zkjkGHfJeHtik8-Ow"
PORT = 8443
WEB_HOOK_HOST = "https://www.slapaper.cn:8443/" + TOKEN

https_handler = urllib.request.HTTPSHandler(context=ssl.create_default_context())
proxy_handler = urllib.request.ProxyHandler({'https':'127.0.0.1:8090',})
opener = urllib.request.build_opener(https_handler, proxy_handler)

data = "Hello World!".encode('utf-8')
response = opener.open(WEB_HOOK_HOST, data=data)

for l in response:
	print(l.decode("utf-8"))