from flask import request, url_for, redirect

from . import app
from .utility import get_authorization_payload, get_refresh_payload
from .views import rendered_error_page, rendered_request_authorization_form, rendered_response_page


@app.route('/')
def root():
    return redirect(url_for('callback'))


# request.args should correspond to one of the following possibilities (possibilities 1-3 should be encounted in order
# during this example flow)
#
#   Position in Flow        print(request.args) example
#
# 1 empty:                  ImmutableMultiDict([])
#
#       Render the starting page which is used to start the authorization flow.
#
# 2 authorization code:     ImmutableMultiDict([('code', 'VEbcb247rnNvFEvr'), ('state', '883fe550-c32d-4b7d-8c23-7f63fb032fd8')])
#
#       Authorization code and state. This code can be used to simultaneously request a Refresh Token and Access Token.
#
#       Example Response: {'access_token': '<--Access Token-->', 'refresh_token': '<--Refresh Token-->', 'expires_in': 86400, 'token_type': 'Bearer'}
#
# 3 refresh token:          ImmutableMultiDict([('refresh_token', '<--Refresh Token-->'), ('scope', 'offline_access')])
#
#       Refresh token that can be used to request another Access Token
#
#       Example Response: {'access_token': '<--Access Token-->', 'expires_in': 86400, 'token_type': 'Bearer'}
#
# 4 error:                  ImmutableMultiDict([('error', 'unauthorized'), ('error_description', 'The requested audience is allowed for company resource owners only '), ('state', '575293f6-0885-42cf-adb1-5c6a451de58e')])
#
#       Will indicate and error that occured during authorization. For example, requesting a token with the Company Audience without specifying a company.
#
#
# Note if you have requested an alternate "callback url" @app.route('/custom callback url', methods=['GET'])
@app.route('/callback', methods=['GET'])
def callback():
    if request.args.get('error'):
        return rendered_error_page()

    if not request.args:
        return rendered_request_authorization_form()

    authorization_code = request.args.get('code')
    refresh_token = request.args.get('refresh_token')
    scope = request.args.get('scope')

    if authorization_code:
        return rendered_response_page(
            authorization_code,
            refresh_token,
            get_authorization_payload(authorization_code)
        )

    elif refresh_token:
        return rendered_response_page(
            authorization_code,
            refresh_token,
            get_refresh_payload(refresh_token, scope)
        )

    else:
        raise Exception("Unexpected Arguments {}".format(request.args))
