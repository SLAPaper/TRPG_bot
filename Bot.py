import urllib.request, urllib.parse, json, ssl, threading, socket, Telegram_Update, Telegram_API

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

HOST = PATH + TOKEN + "/"
API = "https://api.telegram.org/bot" + TOKEN + "/"

response = Telegram_API.setWebhook(API, HOST)

for l in response:
    print(l.decode("utf_8"))

# webhook setting finished, now building bot server

class BotHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path.strip("/") == TOKEN:
            self.send_response(200)
            self.end_headers()
            length = int(self.headers['Content-length'])
            message = self.rfile.read(length)
            data = json.loads(message.decode("utf_8"))
            
            # Debug output
            print(json.dumps(data, sort_keys=True, indent=4))
            
            update = Telegram_Update.Update(data)
            Update.deal(API, update)
        else:
            self.send_response(404)
            self.end_headers()

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