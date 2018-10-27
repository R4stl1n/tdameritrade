import requests
from selenium import webdriver
import urllib.parse as up


def authentication(client_id, redirect_uri):
    client_id = client_id + '@AMER.OAUTHAP'
    url = 'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=' + up.quote(redirect_uri) + '&client_id=' + up.quote(client_id)

    driver = webdriver.Chrome()

    driver.get(url)

    input('after giving access, hit enter to continue')

    code = up.unquote(driver.current_url.split('code=')[1])

    driver.close()

    resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token',
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         data={'grant_type': 'authorization_code',
                               'refresh_token': '',
                               'access_type': 'offline',
                               'code': code,
                               'client_id': client_id,
                               'redirect_uri': redirect_uri})
    if resp.status_code != 200:
        raise Exception('Could not authenticate!')
    return resp.json()


def refresh_token(refresh_token, client_id):
    resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token',
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         json={'grant_type': 'refresh_token',
                               'refresh_token': up.quote(refresh_token),
                               'client_id': up.quote(client_id)})
    if resp.status_code != 200:
        raise Exception('Could not authenticate!')
    return resp.json()
