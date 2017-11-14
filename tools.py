import requests
import simplejson
import json


def make_request(app, user_id, page=1):
    error = None
    data = {}
    uri = "{api_url}/2.2/users/{user_id}/posts?key={api_key}&page={page}" \
          "&pagesize=10&order=desc&sort=activity&site=stackoverflow&filter=!b0OfN629t08FFj"
    uri = uri.format(api_url=app.config['STACKEXCHANGE_BASE_URL'], api_key=app.config['STACKEXCHANGE_API_KEY'],
                     user_id=user_id, page=page)
    try:
        response = requests.get(uri)
        response = response.text
        data = json.loads(response)
    except Exception as e:
        error = e

    return error, data


def build_auth_url(app):
    url = "{base_url}?client_id={client_id}&redirect_uri={redirect_uri}".format(
        base_url=app.config['OAUTH_BASE_URL'],
        client_id=app.config['CLIENT_ID'],
        redirect_uri=app.config['REDIRECT_URI']
    )
    return url


def make_post_auth_url(app, code):
    error = None
    data = None
    url = "{base_url}/access_token/json?client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}" \
          "&code={code}".format(
            base_url=app.config['OAUTH_BASE_URL'],
            client_id=app.config['CLIENT_ID'],
            client_secret=app.config['CLIENT_SECRET'],
            code=code,
            redirect_uri=app.config['REDIRECT_URI'])

    try:
        response = requests.post(url, headers={"content-type": "application/x-www-form-urlencoded"})
        response = response.text
        response = json.loads(response)
        data = response['access_token']
    except Exception as e:
        error = e

    return error, data


def make_get_user_request(app, access_token):
    error = None
    user_id = None
    uri = "{api_url}/2.2/me/associated?key={api_key}&access_token={access_token}"
    uri = uri.format(api_url=app.config['STACKEXCHANGE_BASE_URL'], api_key=app.config['STACKEXCHANGE_API_KEY'],
                     access_token=access_token)
    try:
        response = requests.get(uri)
        response = response.text
        data = json.loads(response)
        for item in data['items']:
            if item['site_name'] == 'Stack Overflow':
                user_id = item['user_id']
    except Exception as e:
        error = e

    return error, user_id
