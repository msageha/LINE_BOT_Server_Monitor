import sys
import os
import http.client
import urllib
import subprocess

import token_key
channel_secret = token_key.channel_secret
channel_access_token = token_key.channel_access_token

def read_file_continue():
  while True:
    line = sys.stdin.readline()
    print(line, end='')
    #Oct  8 09:08:25 raspberrypi sshd[10358]: Failed password for root from 186.42.238.101 port 38352 ssh2
    line_list = line.split()
    if len(line_list) < 14:
      continue
    time, from_ip, protocol = line_list[2], line_list[10], line_list[13]
    if 'Failed password' in line:
      in_if_times += 1
      if in_if_times == 3:
        post_to_line(f'{time} illegal access. {protocol} failed password from {from_ip}')
        in_if_times = 0
    else:
      in_if_times = 0

def post_to_line(message):
  url = "https://api.line.me/v2/bot/message/push"
  headers={
    'Content-type':'application/json',
    'Authorization': f'Bearer {channel_access_token}'
    }
  json_str = f'''{{"to":"{channel_secret}",
    "messages":[
      {{"type":"text", "text":"{message}"}}
      ]
    }}'''
  req = urllib.request.Request(url=url,headers=headers, data=json_str.encode('utf-8'))
  f = urllib.request.urlopen(req)
  print(f.read().decode('utf-8'))


# /sbin/iptables
#sudo iptables -A INPUT -s 222.145.97.118/32 -p tcp -m tcp --dport 22 -j ACCEPT
#sudo iptables -D INPUT -s 222.145.97.118/32 -p tcp -m tcp --dport 22 -j ACCEPT
def reject_ssh(ip):
  subprocess.call(f'sudo iptables -A INPUT -s {ip} -p tcp -m tcp --dport 22 -j DROP', shell=True)

def allow_ssh(ip):
  subprocess.call(f'sudo iptables -D INPUT -s {ip} -p tcp -m tcp --dport 22 -j DROP', shell=True)

if __name__ =='__main__':
  pass
  # read_file_continue()