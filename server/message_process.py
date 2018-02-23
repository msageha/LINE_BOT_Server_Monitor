import numpy as np
from predict import Predict

import monitor_grpc_client
from collections import defaultdict

class MessageProcess:
    def __init__(self):
        self.message_type_dict = {}
        self.predict = Predict(model_file='model/2018-02-22 13:39:42_epoch-9.npz', gpu=0)

    def __call__(self, user_id, text):
        if not self.message_type_dict.get(user_id):
            self.message_type_dict[user_id] = MessageType(user_id, '', 0)
        message_type = self.message_type_dict[user_id](text)
        print(f'MessageProcess_call_text: {text}')
        print(message_type)
        if 'info' == message_type:
            key = 0
            key, response_dict = monitor_grpc_client.run('info', self.message_type_dict[user_id].host)
            print(key)
            if key == 0:
                reply = 'サーバが応答しないよ？'
            else:
                reply = f'CPU使用率: {response_dict["cpu"]}%\n'
                reply += f'メモリ使用率: {response_dict["memory"]}%\n'
                reply += f'温度: {response_dict["temp"]}度\n'
                reply += f'電源: {response_dict["volts"]}ワット\n'
                reply += 'みたいだね'
        elif 'key_input' == message_type:
            reply = f'{text} が受取ったキーを入力して'
        elif 'certificate' == message_type:
            if self.message_type_dict[user_id].key == 0:
                reply = 'サーバーが応答しないみたい'
            else:
                reply = '登録したよ'
        elif 'host_cancell' == message_type:
            self.message_type_dict[user_id].host = ''
            reply = 'サーバーの登録を解除したよ'
        elif 'host_register' == message_type:
            reply = 'ホスト名を教えて'
        elif 'talk' == message_type:
            reply = self.predict(text)
        else:
            reply = 'エラー'
        return reply

class MessageType:
    def __init__(self, user_id, host, key):
        self.user_id = user_id
        self.host = host
        self.key = key
        self.host_register = False
        self.certificate = False

    def __call__(self, text):
        pc_list = ['パソコン', 'pc', 'PC', 'ＰＣ', 'ｐｃ', 'サーバ']
        info_list = ['状態', '調子', '大丈夫', '様子']
        certificate_list = ['登録']
        cancell_list = ['解除', '削除']
        print(f'MessageType_call_text: {text}')
        if self.certificate:
            self.certificate = False
            return 'certificate'
        if self.host_register:
            self.host_register = False
            self.certificate = True
            self.host = text
            key, _ = monitor_grpc_client.run('certificate', self.host)
            self.key = key
            return 'key_input'
        if np.array([word in text for word in pc_list]).any():
            if np.array([word in text for word in info_list]).any():
                return 'info'
            elif np.array([word in text for word in certificate_list]).any():
                if np.array([word in text for word in cancell_list]).any():
                    return 'host_cancell'
                self.host_register = True
                return 'host_register'
        return 'talk'