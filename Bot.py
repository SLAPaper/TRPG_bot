import urllib, http.client, http.server, json, socketserver, ssl

TOKEN = "119827757:AAFTo0ezhROp-0Ria-zkjkGHfJeHtik8-Ow"
PORT = 8443
WEB_HOOK_HOST = "https://www.slapaper.cn:%d/" % PORT + TOKEN
WEB_HOOK_API = "api.telegram.org"
URL = "/bot" + TOKEN + "/"

webhook_connection = http.client.HTTPSConnection(WEB_HOOK_API, context=ssl.create_default_context())
webhook_connection.connect()
webhook_body = json.JSONEncoder().encode({"url":WEB_HOOK_HOST,})
webhook_head = {"Content-Type":"application/x-www-form-urlencoded",}
webhook_connection.request("POST", URL + "setWebhook", body = webhook_body, headers = webhook_head)
response = webhook_connection.getresponse()
for l in response:
	print(l.decode("utf_8"))

webhook_connection.close()