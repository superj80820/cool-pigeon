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
    CarouselTemplate, TemplateSendMessage, URITemplateAction, MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, AudioMessage, PostbackEvent, CarouselColumn, PostbackTemplateAction, MessageTemplateAction
)

app = Flask(__name__)
CORS(app)

line_token = '6DfdurnUmoyp3qgK5NtPl0AP6R5fzFOkWLLz8cBschKrvO+CxbO0XiztfD/ueyX965Mr3zRYUX3In9zZ/lPH7nHt3LDjlUCXzCLsk9OB+duge6EZ2s4m1K5LAL8NXfvcOIIjbxLSEoPDhwhPBsc8xAdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(line_token)
handler = WebhookHandler('b078e77e360a6f04b42ed9425a9e4e7b')
FileRout=''
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
    if event.message.text=='耿耿~':
        conn = sqlite.connect('%sdata/db/data.db'%(FileRout))
        c = conn.cursor()
        user_id = c.execute('SELECT user_id FROM info WHERE score = (SELECT MAX(score) FROM info)')
        user_id = user_id.fetchall()[0][0]
        user_score = c.execute('SELECT score FROM info WHERE user_id = "%s"'%(user_id))
        user_score = user_score.fetchall()[0][0]
        conn.commit()
        conn.close()

        profile = line_bot_api.get_profile(user_id)
        
        sent_Column=CarouselColumn(
            thumbnail_image_url=profile.picture_url,
            title="目前最高分 %s"%(profile.display_name),
            text="%s分"%(user_score),
            actions=[
                PostbackTemplateAction(
                    label="幫助他",
                    text=' ',
                    data='action=buy&itemid=1'
                    ),
                MessageTemplateAction(
                    label="陷害他",
                    text=' '
                    ),
                URITemplateAction(
                    label='我要與你挑戰!',
                    uri='line://app/1612063818-VeyxR31w'
                    )
                ]
            )
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[sent_Column]
                )
        )
        line_bot_api.reply_message(event.reply_token,carousel_template_message)

        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text="目前最高分!\n%s\n%s分!!\n\n點入他挑戰!：line://app/1612063818-VeyxR31w"%(profile.display_name,user_score)))

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

    conn = sqlite.connect('%sdata/db/data.db'%(FileRout))
    c = conn.cursor()
    check_user_id = c.execute('SELECT user_id FROM info WHERE user_id ="%s"'%(user_id))
    check_user_id = check_user_id.fetchall()
    print(check_user_id)
    if check_user_id == []:
        print('add user')
        c.execute('INSERT INTO info (user_id,score) VALUES ("%s","%s")'%(user_id,score))
    else:
        print('update user')
        c.execute('UPDATE info SET score ="%s" WHERE user_id ="%s"'%(score,user_id))
    conn.commit()
    conn.close()

    print('done')
    return "ok"

if __name__ == "__main__":
    app.run()
