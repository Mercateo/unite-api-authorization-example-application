#!/usr/bin/env python

from app import app

ENVIRONMENT = 'INTEGRATION'

if ENVIRONMENT == 'PRODUCTION':
    config = {
        'token_request_uri': 'mercateo.eu.auth0.com',
        'authorize_uri': 'https://auth.unite.eu/approve',
        'user_registration_uri': 'https://portal.unite.eu/Registration',
        'unite_id': '<--client id-->',
        'unite_secret': '<--client secret-->'
    }
elif ENVIRONMENT == 'INTEGRATION':
    config = {
        'token_request_uri': 'mercateo-stage06.eu.auth0.com',
        'authorize_uri': 'https://auth.integration.unite.eu/approve',
        'user_registration_uri': 'https://portal.integration.unite.eu/Registration',
        'unite_id': '<--client id-->',
        'unite_secret': '<--client secret-->'
    }
else:
    raise Exception("Environment not correctly defined. Please set ENVIRONMENT variable to INTEGRATION or PRODUCTION")

app.config.update(config)
app.run(host='localhost', port=8080)
