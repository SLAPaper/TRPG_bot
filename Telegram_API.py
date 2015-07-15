import urllib.request, urllib.parse, ssl, mimetypes, mmap, http.client

def makeOpener(proxy=None):
    https_handler = urllib.request.HTTPSHandler(context=ssl.create_default_context())
    if proxy:
        opener = urllib.request.build_opener(https_handler, urllib.request.ProxyHandler(proxy)) 
    else:
        opener = urllib.request.build_opener(https_handler)
    return opener

opener = makeOpener()
    
# proxy is just for debug
def setWebhook(prefix, url="", proxy=None):
    global opener
    if proxy:
        opener = makeOpener(proxy)
    body = urllib.parse.urlencode({'url':url,})
    return opener.open(prefix + "setWebhook", data=body.encode('utf_8'))

def getMe(prefix):
    global opener
    return opener.open(prefix + "getMe")

def sendMessage(prefix, chat_id, text, optional={}):
    global opener
    data = {'chat_id':chat_id, 'text':text,}
    data.update(optional)
    body = urllib.parse.urlencode(data)
    return opener.open(prefix + "sendMessage", data=body)

def forwardMessage(prefix, chat_id, from_chat_id, message_id):
    global opener
    data = {'chat_id':chat_id, 'from_chat_id':from_chat_id, 'message_id':message_id,}
    body = urllib.parse.urlencode(data)
    return opener.open(prefix + "forwardMessage", data=body)

def sendFile(prefix, chat_id, filedata, filetype, optional={}):
    # It is a replacement of sendPhoto, sendAudio, sendDocument, sendSticker, sendVideo
    global opener
    data = {'chat_id':chat_id, filetype:filedata,}
    data.update(optional)
    
    if hasattr(filedata, "fileno"):
        # here shall use "multipart/form-data" instead
        
        boundary = "AaB03x"
        request = urllib.request.Request(prefix + "send" + filetype.capitalize(), headers={"Content-type":"multipart/form-data", "boundary":boundary})
        # use mmap to deal with huge file
        mmap_file = mmap.mmap(filedata.fileno(), 0, access=mmap.ACCESS_READ)
        
        # the generator of body data
        def body():
            # Add boundary and header
            yield('--' + boundary + '\r\n')
            yield('Content-Disposition: form-data; name=chat_id;' + '\r\n')
            yield('\r\n')
            
            yield chat_id
            yield('--' + boundary + '\r\n')
            yield('Content-Disposition: form-data; name={0}; filename={0}'.format(filetype) + '\r\n')
            yield('Content-Type: application/octet-stream' + '\r\n')
            yield('Content-Transfer-Encoding: binary' +'\r\n')
            yield('\r\n')
            
            yield mmap_file
            for key, value in optional.items():
                yield('--' + boundary + '\r\n')
                yield('Content-Disposition: form-data; name={};'.format(key) + '\r\n')
                yield('\r\n')
                
                yield value
            yield('--'+boundary+'--' + '\r\n')
        
        response = opener.open(request, data=body) 
    else:
        body = urllib.parse.urlencode(data)
        response = opener.open(prefix + "send" + filetype.capitalize() , data=body) 
    return response