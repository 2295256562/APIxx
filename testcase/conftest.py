import pytest
import requests
from env import config
from env.config import USERNAME, PASSWORD
from requester.httpService import HttpService
from utils.write_yaml import write_yaml


@pytest.fixture(scope="session")
def get_token():
    # 1. 调登陆接口
    headers = {
        "user-agent": config.USER_AGENT,
        'Accept': '*/*',
        "api-version": config.API_VERSION,
        "request-source": config.REQUEST_SOURCE,
        "content-type": "application/x-www-form-urlencoded"
    }

    res = requests.post(config.BASE_URL + 'app/user/login/v2?mobile={0}&password={1}'.format("17671105406", "123456"), headers=headers)
    write_yaml("token", res.json()["data"]["token"])
