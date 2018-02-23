import requests

def send_message(text, user_id="U42216535044139a8755fa69bb76be5ea"):
    data = {'message': text, 'user_id': user_id}
    response = requests.post('https://msageha.asuscomm.com/line_message', data=data)