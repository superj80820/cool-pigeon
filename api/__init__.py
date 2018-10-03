# coding: utf-8

import string
import json
import re
import random
import time
import ast
import requests
import pandas
import sqlite3 as sqlite
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, AudioMessage, PostbackEvent
)

app = Flask(__name__)
CORS(app)

line_token = '6DfdurnUmoyp3qgK5NtPl0AP6R5fzFOkWLLz8cBschKrvO+CxbO0XiztfD/ueyX965Mr3zRYUX3In9zZ/lPH7nHt3LDjlUCXzCLsk9OB+duge6EZ2s4m1K5LAL8NXfvcOIIjbxLSEoPDhwhPBsc8xAdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(line_token)
handler = WebhookHandler('b078e77e360a6f04b42ed9425a9e4e7b')
FileRout='/var/www/cool-pigeon/api/'
#/var/www/cool-pigeon/api/

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text=='test':
        # meet_id=''.join(random.choice(string.digits) for x in range(5))
        # invite_id=''.join(random.choice(string.digits) for x in range(5))

        # conn = sqlite.connect('%sdata/db/create_check.db'%(FileRout))
        # c = conn.cursor()
        # c.execute('INSERT INTO meet_check (api_request,user_id,invite_id) VALUES ("%s","%s","%s")'%(meet_id,event.source.user_id,invite_id))
        # conn.commit()
        # conn.close()
        
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="test"))
        None

@handler.add(MessageEvent, message=(ImageMessage))
def handle_content_message(event):
    None

@handler.add(PostbackEvent)
def handle_postback(event):
    None

@app.route('/update_user', methods=['POST'])
def update_user():
    score=request.get_json()['score']
    user_id=request.get_json()['user_id']
    print(score)
    print(user_id)
    return "ok"

if __name__ == "__main__":
    app.run()