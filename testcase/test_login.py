import pytest
from requester.httpService import HttpService
import allure


@allure.feature("个人中心")
@allure.story("用户信息")
@allure.title("用户详情")
def test_userinfo(get_token):
    """
    用户信息详情
    """
    res = HttpService("GET", '/app/user/introinfo').run() \
        .validate("$.data.mobile", '17671105406') \
        .validate("$.data.id", 3033471)


@allure.feature("个人中心")
@allure.story("地址管理")
@allure.title("地址管理")
@allure.description("地址列表")
def test_address():

    res = HttpService("GET", '/app/ec/address/list').run()\
        .validate("$.code", 0)