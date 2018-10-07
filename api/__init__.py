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
    JoinEvent, FollowEvent, CarouselTemplate, TemplateSendMessage, URITemplateAction, MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, AudioMessage, PostbackEvent, CarouselColumn, PostbackTemplateAction, MessageTemplateAction
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
    if event.message.text=="讓我飛":    
        sent_Column_list = []
        print(event.source.group_id)
        conn = sqlite.connect('%sdata/db/%s.db'%(FileRout,event.source.group_id))
        c = conn.cursor()
        user_id_list = c.execute('SELECT user_id FROM info WHERE score = (SELECT MAX(score) FROM info)')
        user_id_list = user_id_list.fetchall()
        for item in user_id_list:
            user_id = item[0]
            user_score_list = c.execute('SELECT score FROM info WHERE user_id = "%s"'%(item[0]))
            user_score = user_score_list.fetchall()[0][0]

            profile = line_bot_api.get_profile(user_id)

            sent_Column=CarouselColumn(
            thumbnail_image_url=profile.picture_url,
            title="%s要開飛了"%(profile.display_name),
            text="%s分"%(user_score),
            actions=[
                PostbackTemplateAction(
                    label="幫助他",
                    data='好道具'
                    ),
                PostbackTemplateAction(
                    label="陷害他",
                    data='壞道具'
                    ),
                URITemplateAction(
                    label='點我開始!!',
                    uri='line://app/1612063818-VeyxR31w?group_id=%s&pipe_item=%s'%(event.source.group_id,'100')
                    )
                ]
            )
            sent_Column_list += [sent_Column]
        # print("in%s"%user_score)
        conn.commit()
        conn.close()
        # print(user_id_list)
        # print(user_score_list)
        carousel_template_message = TemplateSendMessage(
            alt_text='飛吧~',
            template=CarouselTemplate(
                columns=sent_Column_list
                )
        )
        line_bot_api.reply_message(event.reply_token,carousel_template_message)
    elif event.message.text=='欸嘿':
        sent_Column_list = []
        print(event.source.group_id)
        conn = sqlite.connect('%sdata/db/%s.db'%(FileRout,event.source.group_id))
        c = conn.cursor()
        user_id_list = c.execute('SELECT user_id FROM info WHERE score = (SELECT MAX(score) FROM info)')
        user_id_list = user_id_list.fetchall()
        for item in user_id_list:
            user_id = item[0]
            user_score_list = c.execute('SELECT score FROM info WHERE user_id = "%s"'%(item[0]))
            user_score = user_score_list.fetchall()[0][0]

            profile = line_bot_api.get_profile(user_id)

            sent_Column=CarouselColumn(
            thumbnail_image_url=profile.picture_url,
            title="哪呢!%s 獲得了"%(profile.display_name),
            text="%s分"%(user_score),
            actions=[
                PostbackTemplateAction(
                    label="幫助他",
                    data='好道具'
                    ),
                PostbackTemplateAction(
                    label="陷害他",
                    data='壞道具'
                    ),
                URITemplateAction(
                    label='點我向他挑戰!!',
                    uri='line://app/1612063818-VeyxR31w?group_id=%s&pipe_item=%s'%(event.source.group_id,'100')
                    )
                ]
            )
            sent_Column_list += [sent_Column]
        # print("in%s"%user_score)
        conn.commit()
        conn.close()
        # print(user_id_list)
        # print(user_score_list)
        carousel_template_message = TemplateSendMessage(
            alt_text='飛吧~',
            template=CarouselTemplate(
                columns=sent_Column_list
                )
        )
        line_bot_api.reply_message(event.reply_token,carousel_template_message)
        

    elif event.message.text=='test':
        print(event.source.group_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text="目前最高分!\n%s\n%s分!!\n\n點入他挑戰!：line://app/1612063818-VeyxR31w"%(profile.display_name,user_score)))

@handler.add(MessageEvent, message=(ImageMessage))
def handle_content_message(event):
    None

@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == '好道具':
        profile = line_bot_api.get_profile(event.source.user_id)
        user_name = profile.display_name
        quick = {
            "type": "text", 
            "text": "%s 竟然在幫人!?"%(user_name),
            "quickReply": { 
                "items": [
                    {
                        "type": "action",
                        "action": {
                            "type":"message",
                            "label":"公開分數",
                            "text":"公開分數"
                        }
                    },
                    {
                        "type": "action",
                        "action": {
                            "type":"message",
                            "label":"公開分數",
                            "text":"公開分數"
                        }
                    },
                    {
                        "type": "action",
                        "action": {
                            "type":"message",
                            "label":"公開分數",
                            "text":"公開分數"
                        }
                    }
                ]
            }
        }
        headers = {'Content-Type':'application/json','Authorization':'Bearer %s'%(line_token)}
        payload = {
            'replyToken':event.reply_token,
            'messages':[quick]
            }
        res=requests.post('https://api.line.me/v2/bot/message/reply',headers=headers,json=payload)
    elif event.postback.data == '壞道具':
        profile = line_bot_api.get_profile(event.source.user_id)
        user_name = profile.display_name
        quick = {
            "type": "text", 
            "text": "%s 開始害人了"%(user_name),
            "quickReply": { 
                "items": [
                    {
                        "type": "action",
                        "action": {
                            "type":"message",
                            "label":"公開分數",
                            "text":"公開分數"
                        }
                    },
                    {
                        "type": "action",
                        "action": {
                            "type":"message",
                            "label":"公開分數",
                            "text":"公開分數"
                        }
                    },
                    {
                        "type": "action",
                        "action": {
                            "type":"message",
                            "label":"公開分數",
                            "text":"公開分數"
                        }
                    }
                ]
            }
        }
        headers = {'Content-Type':'application/json','Authorization':'Bearer %s'%(line_token)}
        payload = {
            'replyToken':event.reply_token,
            'messages':[quick]
            }
        res=requests.post('https://api.line.me/v2/bot/message/reply',headers=headers,json=payload)

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))

@handler.add(JoinEvent)
def handle_join(event):
    print(event.source.group_id)
    conn = sqlite.connect('%sdata/db/%s.db'%(FileRout,event.source.group_id))
    c = conn.cursor()
    c.execute('CREATE TABLE info(user_id TEXT UNIQUE,score TEXT)')
    conn.commit()
    conn.close()

@app.route('/update_user', methods=['POST'])
def update_user():
    score=request.get_json()['score']
    user_id=request.get_json()['user_id']
    group_id=request.get_json()['group_id']
    print("sent%s"%score)
    print(user_id)
    print(group_id)

    conn = sqlite.connect('%sdata/db/%s.db'%(FileRout,group_id))
    c = conn.cursor()
    check_user_id = c.execute('SELECT user_id FROM info WHERE user_id ="%s"'%(user_id))
    check_user_id = check_user_id.fetchall()
    print(check_user_id)
    if check_user_id == []:
        print('add user')
        c.execute('INSERT INTO info (user_id,score) VALUES ("%s","%s")'%(user_id,score))
    else:
        old_score = c.execute('SELECT score FROM info WHERE user_id ="%s"'%(user_id)).fetchall()[0][0]
        if int(score) > int(old_score):
            print('update user')
            c.execute('UPDATE info SET score ="%s" WHERE user_id ="%s"'%(score,user_id))
    conn.commit()
    conn.close()

    print('done')
    return "ok"

@app.route('/user_info', methods=['GET'])
def user_info():
    user_id=request.args.get('user_id')
    group_id=request.args.get('group_id')
    print(user_id)
    print(group_id)
    ret={}
    ret['pipe_item']='-30'
    return jsonify(ret)

if __name__ == "__main__":
    app.run()
