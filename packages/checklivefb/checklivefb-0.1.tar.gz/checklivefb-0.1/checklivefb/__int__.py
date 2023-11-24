import requests


def check_uid(__id):
    html = requests.get('https://graph.facebook.com/{}/picture?redirect=0'.format(__id)).json()['data']
    if "height" in html:
        return 1
    return 0
