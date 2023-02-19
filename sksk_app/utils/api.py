import urllib.request
import json
import sksk_app.config as config

class Papago:
    def ja_to_ko(word):
        client_id = config.NAVER_CLIENT_ID
        client_secret = config.NAVER_CLIENT_SECRET
        encText = urllib.parse.quote(word)
        data = "source=ja&target=ko&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            result = json.loads(response_body)
            return result['message']['result']['translatedText']
        else:
            print("Error Code:" + rescode)

    def ko_to_ja(word):
        client_id = config.NAVER_CLIENT_ID
        client_secret = config.NAVER_CLIENT_SECRET
        encText = urllib.parse.quote(word)
        data = "source=ko&target=ja&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            result = json.loads(response_body)
            return result['message']['result']['translatedText']
        else:
            print("Error Code:" + rescode)