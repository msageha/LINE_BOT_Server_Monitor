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

from check_var_log import reject_ssh
from check_var_log import allow_ssh
import getting_pc_info
import token_key
import notification

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
# channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_secret = token_key.channel_secret
# channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_access_token = token_key.channel_access_token
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

def text_processing(text):
    text = text.strip()
    message = ''
    if 'DROP' in text:
        print("in DROP")
        print(text)
        ip = text.split()[1]
        reject_ssh(ip)
        message = f'drop {ip}'
    elif 'ACCEPT' in text:
        ip = text.split()[1]
        allow_ssh(ip)
        message = f'accept {ip}'
    elif 'MEMORY' == text:
        message = execute_command.memory()
    elif 'CPU' == text:
        message = execute_command.cpu()
    elif 'どう？' == text:
        message = f'快適ですよ！\n{execute_command.cpu()}\n{execute_command.memory()}'
    elif 'おはよう' in text:
        post_line.post_to_line(image_url='https://goo.gl/tJJDGR', post_type='image')
    print(f'message:::{message}, type:::{type(message)}')
    return message

@app.route("/")
def hello_world():
  return "Hello World!"

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
        message = str(event)
        message = 'unko'
        if event.message.text:
            text = event.message.text.strip()
            message = text_processing(str(text))
            print(f'message:::{message}')
            if message == '':
                continue
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=message)
            )
    return 'OK'

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)