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

def post_to_line(message='', image_url='', package_id='', sticker_id='', post_type='message'):
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
    elif post_type == 'sticker':
        json_str = f'''{{"to":"{user_id}",
          "messages":[
              {{"type":"sticker", "packageId": "{package_id}", "stickerId": "{sticker_id}"}}
              ]
          }}'''
    else:
        json_str = ''
    req = urllib.request.Request(url=url,headers=headers, data=json_str.encode('utf-8'))
    f = urllib.request.urlopen(req)
    print(f.read().decode('utf-8'))

if __name__=='__main__':
    argvs = sys.argv
    if len(argvs) < 2:
        print('How to use this script??')
    cmd = ''.join(argvs[1:])
    os.system(cmd)
    post_to_line(message=f'"{cmd}" is finished now.')
    