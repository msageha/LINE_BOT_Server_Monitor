import sys
import os
import http.client
import urllib
import urllib.request
import subprocess

import token_key
channel_secret = token_key.channel_secret
channel_access_token = token_key.channel_access_token
user_id = token_key.userId


def post_to_line(message='', image_url='', post_type='message'):
  url = "https://api.line.me/v2/bot/message/push"
  headers={
    'Content-type':'application/json',
    'Authorization': f'Bearer {channel_access_token}'
    }
  if post_type == 'message':
    json_str = f'''{{"to":"{user_id}",
      "messages":[
        {{"type":"text", "text":"{message}"}}
        ]
      }}'''
  elif post_type == 'image':
    json_str = f'''{{"to":"{user_id}",
      "messages":[
        {{"type":"image",   "originalContentUrl": "{image_url}",
    "previewImageUrl": "{image_url}"}}
        ]
      }}'''
    print(post_type)
  else:
    json_str = ''
  req = urllib.request.Request(url=url,headers=headers, data=json_str.encode('utf-8'))
  f = urllib.request.urlopen(req)
  print(f.read().decode('utf-8'))