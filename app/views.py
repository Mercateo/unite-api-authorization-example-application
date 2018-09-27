import json
import textwrap
import uuid

from flask import render_template, request, url_for

from . import app
from .utility import decode_access_token, fetch_access_token, get_access_token_post_uri, Audiences

MAX_FIELD_WIDTH = 80


def rendered_request_authorization_form():
    return render_template(
        "app_start.html",
        action_url=app.config['authorize_uri'],
        tenant_audience=Audiences.tenant_audience.value,
        company_audience=Audiences.company_audience.value,
        audiences=Audiences.list(),
        redirect_uri=url_for('callback', _external=True),
        scope="offline_access",
        client_id=app.config['unite_id'],
        state=uuid.uuid4(),
        company_id="",
        token_request_uri=app.config['token_request_uri'],
        user_registration_uri=app.config['user_registration_uri']
    )


def rendered_response_page(authorization_code: str, refresh_token: str, payload: dict):
    response = fetch_access_token(payload)

    access_token = response['access_token']

    jwt = decode_access_token(access_token)

    return render_template(
        "app_token.html",
        authorization_code=authorization_code,
        state=request.args.get('state'),
        token_request=json.dumps(payload, indent=4, sort_keys=True),
        token_request_uri=get_access_token_post_uri(),
        jwt=json.dumps(jwt, indent=4, sort_keys=True),
        raw_token='\n'.join(textwrap.wrap(access_token, MAX_FIELD_WIDTH)),
        refresh_token=response['refresh_token'] if 'refresh_token' in response else refresh_token,
        scope=jwt['scope'] if 'scope' in jwt else 'n/a'
    )


def rendered_error_page():
    return render_template(
        "app_error.html",
        error=request.args.get('error'),
        error_description=request.args.get('error_description')
    )
