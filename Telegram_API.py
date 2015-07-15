import urllib.request, urllib.parse, ssl

def setWebhook(globalVars, url="", proxy=None):
	API = globalVars["API"]
	URL = globalVars["URL"]
	
	https_handler = urllib.request.HTTPSHandler(context=ssl.create_default_context())
	if proxy:
		opener = urllib.request.build_opener(https_handler, urllib.request.ProxyHandler(proxy)) 
	else:
		opener = urllib.request.build_opener(https_handler)
	
	body = urllib.parse.urlencode({'url':url,})
	
	return opener.open(API + URL + "setWebhook", data=body.encode('utf_8'))