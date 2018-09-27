import json

import requests
from jose import jwt
from lazy import lazy


class JWTKeyset(object):
    def __init__(self, token_request_uri):
        self.token_request_uri = token_request_uri

    @lazy
    def keys(self):
        jwks_url = "https://{}/.well-known/jwks.json".format(self.token_request_uri)
        return json.loads(requests.get(jwks_url).text)['keys']

    def get_key(self, key_id):
        for key in self.keys:
            if key_id == key['kid']:
                return key
        if len(self.keys) > 0:
            return self.keys[0]

    def decode(self, token, api_audience=None):
        unverified_header = jwt.get_unverified_header(token)
        if unverified_header['typ'] == 'JWT':
            key = self.get_key(unverified_header['kid'] if 'kid' in unverified_header else None)

            return jwt.decode(
                token,
                key,
                algorithms=unverified_header['alg'],
                audience=api_audience,
                issuer=None
            )
