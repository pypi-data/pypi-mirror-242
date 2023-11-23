import json
import requests
from xfhir.cli import token

SETTINGS = {
    'client_id': '',
    'client_secret': '',
    'access_token': '',
    'api_endpoint': ''
}


def init(client_id: str, client_secret: str, endpoint: str = 'https://api.xfhir.com/v1'):
    SETTINGS['client_id'] = client_id
    SETTINGS['client_secret'] = client_secret
    SETTINGS['api_endpoint'] = endpoint
    SETTINGS['access_token'] = token(client_id=client_id, secret_key=client_secret)


def create(fhir_resource: dict):
    if not SETTINGS['access_token']:
        raise Exception('make you have initalized XFHIR by running xfhir.init')

    headers = {
        "Authorization": f"Bearer {SETTINGS['access_token']}",
        "Content-Type": "application/json"
    }

    data = {
        'fhir_resource': fhir_resource,
        'policies': []
    }

    response = requests.post(
        url=SETTINGS['api_endpoint'] + '/fhir',
        data=json.dumps(data),
        headers=headers
    )
    assert response.status_code == 200
    return response


def get(resource_type: str, identifier: str):
    if not SETTINGS['access_token']:
        raise Exception('make you have initalized XFHIR by running xfhir.init')

    endpoint = f'{SETTINGS["api_endpoint"]}/fhir/{resource_type}/{identifier}'

    headers = {
        "Authorization": f"Bearer {SETTINGS['access_token']}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        url=endpoint,
        headers=headers
    )

    assert response.status_code == 200
    return response


def delete(resource_type: str, identifier: str):
    if not SETTINGS['access_token']:
        raise Exception('make you have initalized XFHIR by running xfhir.init')

    endpoint = f'{SETTINGS["api_endpoint"]}/fhir/{resource_type}/{identifier}'

    headers = {
        "Authorization": f"Bearer {SETTINGS['access_token']}",
        "Content-Type": "application/json"
    }

    response = requests.delete(
        url=endpoint,
        headers=headers
    )

    assert response.status_code == 200
    return response
