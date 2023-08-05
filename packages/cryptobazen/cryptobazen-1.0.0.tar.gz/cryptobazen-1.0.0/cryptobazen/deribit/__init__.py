import os
import sys
basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(basedir)
import requests
import random
import hmac
import hashlib
import time
from cryptobazen.deribit import _authentication, _account_management, _market_data, _trading, _wallet


class DeribitSync(_authentication.Mixin, _account_management.Mixin, _market_data.Mixin, _trading.Mixin, _wallet.Mixin):

    def __init__(self, client_id, client_secret, test_mode=False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://test.deribit.com/api/v2' if test_mode else 'https://www.deribit.com/api/v2'
        self.base_wss = 'wss://test.deribit.com/ws/api/v2' if test_mode else 'wss://www.deribit.com/ws/api/v2'
        self.session = requests.Session()

    def api_query(self, method, params, endpoint, body=""):
        # Create a signature according to the deribit documentation and create a header for all requests.
        timestamp = int(time.time() * 1000)
        nonce = ''.join([str(random.randint(0, 9)) for i in range(8)])
        string_to_sign = f'{timestamp}\n{nonce}\n{method}\n/api/v2{endpoint}?{params}\n{body}\n'
        signature = hmac.new(bytes(self.client_secret, 'utf8'), bytes(string_to_sign, 'utf8'), digestmod=hashlib.sha256).hexdigest()
        headers = {'Authorization': f'deri-hmac-sha256 id={self.client_id},ts={timestamp},nonce={nonce},sig={signature}'}

        if method == 'POST':
            response = self.session.post(f'{self.base_url}{endpoint}', data=params, headers=headers)
        elif method == 'GET':
            response = self.session.get(f'{self.base_url}{endpoint}?{params}', headers=headers)
        elif method == 'DELETE':
            response = self.session.delete(f'{self.base_url}{endpoint}', data=params, headers=headers)
        elif method == 'PUT':
            response = self.session.put(f'{self.base_url}{endpoint}', data=params, headers=headers)
        else:
            response = {'code': 999, 'msg': 'Invalid requests method. Choose POST, GET, DELETE or PUT.'}

        return response.json()['result']

