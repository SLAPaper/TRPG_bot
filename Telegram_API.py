import urllib.request, urllib.parse, ssl

def makeOpener(proxy=None):
	https_handler = urllib.request.HTTPSHandler(context=ssl.create_default_context())
	if proxy:
		opener = urllib.request.build_opener(https_handler, urllib.request.ProxyHandler(proxy)) 
	else:
		opener = urllib.request.build_opener(https_handler)
	return opener
	
# proxy is just for debug
def setWebhook(prefix, url="", proxy=None):
	opener = makeOpener(proxy)
	body = urllib.parse.urlencode({'url':url,})
	return opener.open(prefix + "setWebhook", data=body.encode('utf_8'))

def getMe(prefix):
	opener = makeOpener(proxy)
	return opener.open(prefix + "getMe")

def sendMessage(prefix, chat_id, text, optional={}):
	opener = makeOpener(proxy)
	data = {'chat_id':chat_id, 'text':text,}
	data.update(optional)
	body = urllib.parse.urlencode(data)
	return opener.open(prefix + "sendMessage", data=body)