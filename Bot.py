import urllib.request, urllib.parse, json, ssl, threading, socket, sys

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

if len(sys.argv) < 2:
	DEBUG = False
else:
	DEBUG = True

TOKEN = "119827757:AAFTo0ezhROp-0Ria-zkjkGHfJeHtik8-Ow"
PORT = 8443
WEB_HOOK_HOST = "https://www.slapaper.cn:%d/" % PORT + TOKEN + "/"
WEB_HOOK_API = "https://api.telegram.org/"
URL = "bot" + TOKEN + "/"
CA_FILE = None
KEY_FILE = None

if not DEBUG:
	CA_FILE = "ca.crt"
	KEY_FILE = "ca.key"

webhook_body = urllib.parse.urlencode({'url':WEB_HOOK_HOST,})

https_handler = urllib.request.HTTPSHandler(context=ssl.create_default_context())
proxy_handler = urllib.request.ProxyHandler({'http':'127.0.0.1:1080', 'https':'127.0.0.1:1080', 'socks5':'127.0.0.1:1080'},)

if DEBUG:
	webhook_opener = urllib.request.build_opener(https_handler, proxy_handler)
else:
	webhook_opener = urllib.request.build_opener(https_handler)

webhook_response = webhook_opener.open(WEB_HOOK_API + URL + "setWebhook", data=webhook_body.encode('utf-8'))

for l in webhook_response:
	print(l.decode("utf-8"))

# webhook setting finished, now building bot server

class BotHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		self.send_response(200)
		self.end_headers()
		message = self.rfile.readall()
		print("A POST message came!\n", message)
		self.wfile.write(message)
		self.wfile.flush()
		# multithreading

class ThreadedBotServer(ThreadingMixIn, HTTPServer):
	pass

server_address = ('', 8443)
bot_server = ThreadedBotServer(server_address, BotHandler)
# HTTPS support needed
server_ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH) 
bot_server.socket = server_ssl_context.wrap_socket(bot_server.socket, keyfile=KEY_FILE, certfile=CA_FILE, server_side=True, suppress_ragged_eofs=False)

try:
	bot_server.serve_forever()
except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    bot_server.server_close()