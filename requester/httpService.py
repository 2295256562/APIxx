import json
import logging

import jsonpath as jsonpath
import requests
from env import config
from utils.write_yaml import read_yaml
from logzero import logger


class HttpService:

    def __init__(self, method, url, params=None, data=None, json=None):
        self.method = method
        self.url = url
        self.params = params
        self.data = data
        self.json = json
        self.headers = {
            "user-agent": config.USER_AGENT,
            'Accept': '*/*',
            "Authorization": read_yaml("token"),
            "api-version": config.API_VERSION,
            "request-source": config.REQUEST_SOURCE,
            "content-type": config.CONTENT_TYPE
        }

    def _headers(self):
        """
        更新token
        :return:
        """
        if self.headers['Authorization'] is None:
            self.headers.update({'Authorization': read_yaml('token')})
        return self.headers

    def run(self):
        """
        执行用例方法
        :return:  返回当前self
        """
        if self.method == "POST":
            self.response = self.requests_post()
        else:
            self.response = self.requests_get()
        return self

    def extract(self, field):
        """
        提取变量
        :param field: 提取表达式
        :return:
        """
        value = self.response.json()
        # strvalue = json.dumps(value)
        # tmp = json.loads(strvalue)
        # print(value)
        # for _key in field.split("."):
            # print(_key)
            # from requests import structures
            # if isinstance(value, requests.Response):
            #     if _key == "json()":
            #         value = self.response.json()
            #     else:
            #         value = getattr(value, _key)
            # elif isinstance(value, (structures.CaseInsensitiveDict, dict)):
            #     value = value[_key]
        # json_obj = json.loads(strvalue)

        restul = jsonpath.jsonpath(value, field)
        return restul

    def validate(self, key, expected_value):
        """
        校验返回值字段
        :param key:
        :param expected_value:
        :return:
        """
        actual_value = self.extract(key)
        assert actual_value[0] == expected_value
        logger.info("实际数据:{} *********** 期望数据:{}".format(*actual_value, expected_value))
        return self

    def requests_get(self):
        headers = self._headers()
        # print(headers)
        if self.params is not None:
            res = requests.get(config.BASE_URL + self.url, self.params, headers=headers)
            logger.info("请求地址:{0}".format(config.BASE_URL + self.url))
            logger.info("请求参数:{}".format(self.params))
            logger.debug("请求头:{0}:".format(headers))
        else:
            res = requests.get(config.BASE_URL + self.url, headers=headers)
            logger.info("请求地址:{0}".format(config.BASE_URL + self.url))
            logger.debug("请求头:{0}:".format(headers))

        self.common_check(res)
        logger.info(r"返回的数据结果:{}".format(res.json()))
        return res

    def requests_post(self):
        headers = self._headers()
        res = requests.post(config.BASE_URL + self.url, json=self.data, headers=headers)
        logger.info("请求地址:{0}".format(config.BASE_URL + self.url))
        logger.info("请求body:{0}".format(self.data))
        logger.debug("请求头:{0}:".format(headers))
        self.common_check(res)
        logger.info(r"返回的数据结果:{}".format(res.json()))
        return res

    @classmethod
    def common_check(cls, resp):
        """
        公共Check方法，检查 200 响应码和 msg字段值（'success'）
        :param resp:
        :return:
        """
        assert resp.status_code == 200, cls.error_request_datail(resp, '响应码非200')
        # assert resp.json()['msg'] == 'success', cls.error_request_datail(resp, '响应内容中 msg 不为success')

    @classmethod
    def error_request_datail(cls, resp, error_msg=''):
        """
         打印完整请求信息，用于报错时调试
        :param resp: request.response 对象
        :param error_msg:  错误信息
        :return: 请求信息（字符串
        """
        content = '{}\n{}'.format(cls._get_request_info(resp), error_msg)
        return content

    @staticmethod
    def _get_request_info(resp):
        """
        从 request.response 对象中提取请求和返回的详细信息
        :param resp: request.response 对象
        :return: 请求信息（字符串）
        """
        content = """
                [ 请求信息 ]
                URL: {}
                Headers: {}
                Body: {}
                ------------------------
                [ 响应信息 ]
                Status: {}
                Content: {}
                """.format(resp.request.url, resp.request.headers, resp.request.body, resp.status_code,
                           resp.text)
        return content
