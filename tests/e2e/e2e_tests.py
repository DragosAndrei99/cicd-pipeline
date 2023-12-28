from http import HTTPStatus
import requests
import json

api_gw_url = "https://p6vcd8nfv9.execute-api.us-east-1.amazonaws.com/prod/posts"

def test_get_handler():
    response = requests.get(api_gw_url)
    assert response.status_code == HTTPStatus.OK


def test_post_handler():
    body = {
        "item_data": {
            "id": "12345",
            "title": "Test2"
        }
    }

    response = requests.post(api_gw_url, data=json.dumps(body))
    assert response.status_code == HTTPStatus.OK


def test_put_handler():
    body = {
        "item_key": {
            "id": "12345"
        },
        "update_data": {
            "title": "Test3"
        }
    }
    response = requests.put(api_gw_url, data=json.dumps(body))
    assert response.status_code == HTTPStatus.OK

def test_delete_handler():
    body = {
        "item_key": {
            "id": "12345"
        }
    }
    response = requests.delete(api_gw_url, data=json.dumps(body))
    assert response.status_code == HTTPStatus.OK


test_get_handler()
test_post_handler()
test_put_handler()
test_delete_handler()