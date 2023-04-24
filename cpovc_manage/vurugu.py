import requests

base_url = 'https://vm.cpims.net/json'
# base_url = 'http://127.0.0.1:8080/json'
user_name = 'nmugaya'
user_pass = '1P@ss2022!'


def login_api():
    """Method to login to get key details."""
    try:
        url = '%s/auth/login' % base_url
        logins = {'userName': user_name, 'password': user_pass}
        r = requests.post(url, json=logins)
        print(r.json())
    except Exception as e:
        print('Error with API - %s' % (str(e)))
        return {'key': ''}
    else:
        return r.json()


def save_vm_changes(case_id, payload):
    """Method to save changes to VM."""
    try:
        response = login_api()
        key = response['key']
        headers = {'userId': user_name, 'key': key}
        url = '%s/app/answer/single/%s' % (base_url, case_id)
        print(url, payload)
        r = requests.put(url, headers=headers, json=payload)
    except Exception:
        return {'key': ''}
    else:
        return r.json()


if __name__ == '__main__':
    case_id = 'f318c2c7-e650-48b0-9681-f2dc6fea4719'
    payload = {"verification_status": "002"}
    # payload = {"case_serial" : "CCO/39/221/5/29/1197/2020"}
    # payload = {"case_reporter" : "CRCO"}
    resp = save_vm_changes(case_id, payload)
    print(resp)
