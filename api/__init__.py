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

line_token = 'D9I+Oxtoll926dCqHX3bnx6fhiAqKt28n/PQYmaeGjsmG3Uq+W+tspiRQaAW6AZTQKpZuvi9VAFFpL8+EBhExS1U/zjqRCoVF2lpDwFgDvf6k9bOrlgB8fEcBJCgTd9g41oQ7iTMb3o0t2qPddQskgdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(line_token)
handler = WebhookHandler('e840717929fb3e363919b0b31b86f056')
FileRout='/var/www/line_saying/api/'
#/var/www/line_saying/api/

def USER_GET_MEET_ID(user_id):
    conn = sqlite.connect('%sdata/db/create_check.db'%(FileRout))
    c = conn.cursor()
    meet_id = c.execute('SELECT meet FROM user_in_where WHERE id ="%s"'%(user_id))
    meet_id = meet_id.fetchall()[0][0]
    conn.commit()
    conn.close()
    return meet_id

def INVITE_ID_GET_MEET_ID(invite_id):
    conn = sqlite.connect('%sdata/db/create_check.db'%(FileRout))
    c = conn.cursor()
    meet_id = c.execute('SELECT api_request FROM meet_check WHERE invite_id ="%s"'%(invite_id))
    meet_id = meet_id.fetchall()[0][0]
    conn.commit()
    conn.close()
    return meet_id

def GET_INFO(meet_id,what):
    conn = sqlite.connect('%sdata/db/%s.db'%(FileRout,meet_id))
    c = conn.cursor()
    info = c.execute('SELECT %s FROM info'%(what))
    info = info.fetchall()[0][0]
    conn.commit()
    conn.close()
    return info

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
    if event.message.text=='meeting!':
        # meet_id=''.join(random.choice(string.digits) for x in range(5))
        # invite_id=''.join(random.choice(string.digits) for x in range(5))

        # conn = sqlite.connect('%sdata/db/create_check.db'%(FileRout))
        # c = conn.cursor()
        # c.execute('INSERT INTO meet_check (api_request,user_id,invite_id) VALUES ("%s","%s","%s")'%(meet_id,event.source.user_id,invite_id))
        # conn.commit()
        # conn.close()
        
        # line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text='已創建meeting~\n到網站輸入驗證碼吧！\n%s'%(meet_id)))
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
    print(score)
    return "ok"

if __name__ == "__main__":
    app.run()