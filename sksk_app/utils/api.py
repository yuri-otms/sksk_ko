import urllib.request
import json
from google.cloud import texttospeech
import os

import sksk_app.config as config
from sksk_app import db
from sksk_app.models import Question



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

class GoogleCloud:
    def create_audio_file(question_id):
        question = db.session.get(Question, question_id)
        text= question.foreign_l
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.GOOGLE_APPLICATION_CREDENTIALS
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.7
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        file_name = 'sksk_app/static/audio/'+ str(question_id).zfill(5) + '.mp3'

        with open(file_name, "wb") as out:
            out.write(response.audio_content)