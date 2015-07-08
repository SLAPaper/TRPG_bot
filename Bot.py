import urllib, http, json, socketserver, ssl

TOKEN = "119827757:AAFTo0ezhROp-0Ria-zkjkGHfJeHtik8-Ow"
PORT = 8443
WEB_HOOK_HOST = "https://www.slapaper.cn:8443/" + TOKEN
API = "https://api.telegram.org/"
"bot" + TOKEN + "/"

webhook_connection = http.client.HTTPConnection()