import urllib.request, urllib.parse, json, ssl, threading, socket, sys

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

TOKEN = "119827757:AAFTo0ezhROp-0Ria-zkjkGHfJeHtik8-Ow"
PORT = 8443
WEB_HOOK_HOST = "https://www.slapaper.cn:%d/" % PORT + TOKEN + "/"
WEB_HOOK_API = "https://api.telegram.org/"
URL = "bot" + TOKEN + "/"
CA_FILE = "ca.crt"
KEY_FILE = "ca.key"

# webhook_body = urllib.parse.urlencode({'url':WEB_HOOK_HOST,})
# https_handler = urllib.request.HTTPSHandler(context=ssl.create_default_context())
# webhook_opener = urllib.request.build_opener(https_handler)
# webhook_response = webhook_opener.open(WEB_HOOK_API + URL + "setWebhook", data=webhook_body.encode('utf-8'))
# 
# for l in webhook_response:
# 	print(l.decode("utf-8"))

# webhook setting finished, now building bot server

class BotHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		self.send_response(200)
		self.end_headers()
		message = self.rfile.read()
		print("A POST message came!\n", message)
		self.wfile.write(message)
		self.wfile.flush()
		# multithreading

class ThreadedBotServer(ThreadingMixIn, HTTPServer):
	pass

class ThreadedBotServer_v6(ThreadedBotServer):
	address_family = socket.AF_INET6

server_address = ('', PORT)
server_address_v6 = ('', PORT)
bot_server = ThreadedBotServer(server_address, BotHandler)
bot_server_v6 = ThreadedBotServer_v6(server_address_v6, BotHandler)

# HTTPS support needed
server_ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
server_ssl_context.load_cert_chain(CA_FILE, KEY_FILE)

bot_server.socket = server_ssl_context.wrap_socket(bot_server.socket, server_side=True)
bot_server_v6.socket = server_ssl_context.wrap_socket(bot_server_v6.socket, server_side=True)
print("\nBot servers is now working.")

try:
	server_thread = threading.Thread(target=bot_server.serve_forever())
	server_thread.daemon = True
	server_thread.start()
	
	server_thread_v6 = threading.Thread(target=bot_server_v6.serve_forever())
	server_thread_v6.daemon = True
	server_thread_v6.start()
	
	print("\nBot servers are now working.")
except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    bot_server.shutdown()
    bot_server_v6.shutdown()