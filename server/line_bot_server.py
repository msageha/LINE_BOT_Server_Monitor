# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
from __future__ import unicode_literals

import os
import sys
from argparse import ArgumentParser
import re
import urllib
import urllib.request

from flask import (
    Flask, request, abort
)
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import token_key

from message_process import MessageProcess

message_process = MessageProcess()

app = Flask(__name__)
channel_secret = token_key.channel_secret
channel_access_token = token_key.channel_access_token
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

def extract_message_user_id(text):
    searched = re.search(r'message=(.*)&user_id=(.*)', text)
    message, user_id = searched.groups()
    return message, user_id

@app.route("/")
def hello_world():
  return "Hello World!"

@app.route("/line_message", methods=['POST'])
def sent_message():
    body = request.get_data().decode('utf8')
    message, user_id = extract_message_user_id(body)
    url = "https://api.line.me/v2/bot/message/push"
    headers={
        'Content-type':'application/json',
        'Authorization': f'Bearer {channel_access_token}'
    }
    json_str = f'''{{"to":"{user_id}",
        "messages":[
            {{"type":"text", "text":"{message}"}}
        ]
    }}'''
    req = urllib.request.Request(url=url,headers=headers, data=json_str.encode('utf-8'))
    f = urllib.request.urlopen(req)
    print(f.read().decode('utf-8'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        print('-------------')
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if event.message.text:
            user_id = event.source.user_id
            text = event.message.text.strip()
            replay = message_process(user_id, text)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=replay)
            )

    return 'OK'

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=5000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    args = arg_parser.parse_args()

    app.run(debug=args.debug, port=args.port)
