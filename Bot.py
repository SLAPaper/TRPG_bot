import urllib.request, urllib.parse, json, ssl, threading, socket, sys, select

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

f = open("config.json", "r", encoding="utf_8")
dic = json.load(f)
f.close()

TOKEN = dic["TOKEN"]
PORT = int(dic["PORT"])
PATH = dic["PATH"]
CA_FILE = dic["CA_FILE"]
KEY_FILE = dic["KEY_FILE"]

WEB_HOOK_HOST = PATH + TOKEN + "/"
WEB_HOOK_API = "https://api.telegram.org/"
URL = "bot" + TOKEN + "/"

webhook_body = urllib.parse.urlencode({'url':WEB_HOOK_HOST,})
https_handler = urllib.request.HTTPSHandler(context=ssl.create_default_context())
webhook_opener = urllib.request.build_opener(https_handler)
webhook_response = webhook_opener.open(WEB_HOOK_API + URL + "setWebhook", data=webhook_body.encode('utf_8'))

for l in webhook_response:
	print(l.decode("utf_8"))

# webhook setting finished, now building bot server

class BotHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		print(self.headers)
		
		self.send_response(200)
		self.end_headers()
		
		length = int(self.headers['Content-length'])
		message = self.rfile.read(length)
		print("A POST message came!\n", message)
		
		self.wfile.flush()
		self.wfile.write(message)

class ThreadedBotServer(ThreadingMixIn, HTTPServer):
	address_family = socket.AF_INET6

server_address = ('', PORT)
bot_server = ThreadedBotServer(server_address, BotHandler)

server_ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
server_ssl_context.load_cert_chain(CA_FILE, KEY_FILE)

bot_server.socket = server_ssl_context.wrap_socket(bot_server.socket, server_side=True)
print("\nBot server is now builded.")

try:
	server_thread = threading.Thread(target=bot_server.serve_forever())
	server_thread.daemon = True
	server_thread.start()
except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    bot_server.shutdown()