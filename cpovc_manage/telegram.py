import requests

key = '1599998771:AAGUVt_4Tzlo4xyPHbY-fGmQfNQy7jawAMY'
base_url = 'https://api.telegram.org/bot%s' % (key)
SCHAT_ID = '-1001362645711'
CHAT_ID = '-431040191'


def send_message(message):
    try:
        end_point = '/sendMessage'
        url = '%s%s' % (base_url, end_point)
        data = {'chat_id': SCHAT_ID, 'text': message}
        response = requests.post(url, data).json()
        # print('Response', response)
    except Exception as e:
        error = {"message": "error sending to telegram - " % (str(e))}
        return error
    else:
        return response