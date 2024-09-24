import requests


def register_user(name: str, password: str):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "username": name,
        "password": password
    }
    response = requests.post(url='http://127.0.0.1:8001/register', headers=headers, json=payload)
    return response.json()


def get_all_users():
    headers = {'accept': 'application/json'}
    response = requests.get(url='http://127.0.0.1:8001/all_users', headers=headers)
    return response.json()


if __name__ == '__main__':
    # print(register_user('admin@gmail.com', 'password'))
    users = get_all_users()
    print(users)