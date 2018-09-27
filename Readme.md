# Unite Integration Example Application

## How to use the application

* Set the environment that should be used in `app.py`. This should be either `INTEGRATION` or `PRODUCTION`
* Enter `unite_id` and `unite_secret` for the relevant environment in `app.py`.
* Create and activate a python3 virtualenv
    * `pip install virtualenv`
    * `virtualenv unite-integration-test-app`
    * `source unite-integration-test-app/bin/activate`
* install required packages: `$ pip install -r requirements.txt`
* run application `$ ./app.py`
* enter `http://localhost:8080` in your browser to try out the example application

## Important

This application is to be used by companies that are integrating with the Unite Platform. 
Additional documentation describing this authorization process can be found at 
https://portal.unite.eu/developers/api-access-for-3rd-party-client

## Requirements

Unite Credentials are required to use this example application.