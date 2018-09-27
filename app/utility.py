import json
from enum import Enum

import requests
from flask import url_for
from jose import jwt

from app.lib.jwks import JWTKeyset
from . import app


def get_authorization_payload(authorization_code: str) -> dict:
    return {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': url_for('callback', _external=True),
        **get_unite_credentials()
    }


def get_refresh_payload(refresh_token: str, scope: str) -> dict:
    return {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'scope': scope,
        **get_unite_credentials()
    }


def get_unite_credentials() -> dict:
    return {
        "client_id": app.config['unite_id'],
        "client_secret": app.config['unite_secret']
    }


def get_access_token_post_uri() -> str:
    return "https://{}/oauth/token".format(app.config['token_request_uri'])


def fetch_access_token(payload: dict) -> dict:
    response = requests.post(
        get_access_token_post_uri(),
        json=payload
    )

    if response.status_code != 200:
        return "ERROR: " + response.text

    return json.loads(response.text)


def decode_access_token(access_token: str):
    unverified_claims = jwt.get_unverified_claims(access_token)
    audience = extract_audience(unverified_claims)

    return JWTKeyset(app.config['token_request_uri']) \
        .decode(access_token, audience)


def extract_audience(token: dict):
    audience = token['aud'] if 'aud' in token else None

    if isinstance(audience, list):
        return audience[0]
    else:
        return audience


class Audiences(Enum):
    tenant_audience = 'https://unite.eu/tenant-administration-api'
    company_audience = 'https://unite.eu/api'

    @staticmethod
    def list() -> list:
        return list(map(lambda aud: aud.value, Audiences))
