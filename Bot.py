import urllib.request, urllib.parse, json, ssl, select, threading, socket

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

TOKEN = "119827757:AAFTo0ezhROp-0Ria-zkjkGHfJeHtik8-Ow"
PORT = 8443
WEB_HOOK_HOST = "https://www.slapaper.cn:%d/" % PORT + TOKEN
WEB_HOOK_API = "https://api.telegram.org/"
URL = "bot" + TOKEN + "/"

webhook_body = urllib.parse.urlencode({"url":WEB_HOOK_HOST,})

https_handler = urllib.request.HTTPSHandler(context=ssl.create_default_context())
proxy_handler = urllib.request.ProxyHandler({'http':'127.0.0.1:1080', 'https':'127.0.0.1:1080', 'socks5':'127.0.0.1:1080'},)

webhook_opener = urllib.request.build_opener(https_handler, proxy_handler)
webhook_response = webhook_opener.open(WEB_HOOK_API + URL + "setWebhook", data=webhook_body.encode('utf-8'))

for l in webhook_response:
	print(l.decode("utf-8"))

# webhook setting finished, now building bot server

class BotHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		self.send_response(200)
		self.end_headers()
		message = ''
		while select.select([self.rfile], [], [], 0)[0]:
			message = self.rfile.readall()
		# multithreading
		print(message)
		self.wfile.write(message)
		self.wfile.write('\n')

class ThreadedBotServer(ThreadingMixIn, HTTPServer):
	pass

server_address = ('', 8443)
bot_server = ThreadedBotServer(server_address, BotHandler)
# HTTPS support needed
# bot_server.socket = ssl.

try:
	bot_server.serve_forever()
except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    bot_server.server_close()