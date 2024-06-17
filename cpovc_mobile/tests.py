from django.test import TestCase

import requests
# from django.test import TestCase

base_url = 'http://127.0.0.1:8004/api'
# base_url = 'https://test.cpims.net/api'


url = base_url + '/token/'
payload = {'username': 'admin', 'password': '1P@ss2024!'}

response = requests.post(url, json=payload)
# print(response.text)
resp = response.json()
print(resp)

cpims_id = 3696526
# 4041779

token = resp['access']
headers = {'Authorization': 'Bearer %s' % token}

print(token)

url = base_url + '/mobile/caseload/'
# url = base_url + '/form/HMF/'

response = requests.get(url, headers=headers)
print(response.status_code)
if response.status_code == 200:
   print(response.json())