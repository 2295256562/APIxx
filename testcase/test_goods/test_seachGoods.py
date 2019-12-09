import allure
import pytest

from env.url import baseinfo, GOODS_SKU_INFO, GOODS_IMGTEXT, GOODS_SPEC, GOOD_COLLECTION
from requester.httpService import HttpService


@allure.feature("商品模块")
@allure.story("商品列表")
@allure.title("商品搜索")
@allure.description("搜索睡衣商品")
def test_seachGoods():
    res = HttpService("GET",
                      '/app/ec/product/search?pageIndex=1&pageSize=1&filter=%7B%22word%22%3A%22%E7%9D%A1%E8%A1%A3%22%7D').run()


@allure.feature("商品模块")
@allure.story("商品列表")
@allure.title("错误----错误的参数类型")
@allure.description("传入不正确的数据")
@pytest.mark.parametrize("seach", ['null', ' '])
def test_seachGoodsErr(seach):
    HttpService("GET", '/app/ec/product/search?pageIndex=1&pageSize=1&filter=12121').run() \
        .validate("$.flag", False) \
        .validate("$.msg", "参数不合法")


@allure.feature("商品模块")
@allure.story("正常---正确的商品id")
@allure.title("商品详情信息")
@allure.description("商品睡衣详情")
def test_goodsInfo():
    res = HttpService("GET", baseinfo, params={'id': 2}) \
        .run() \
        .validate("$.data.id", 2) \
        .validate("$.data.is_del", 0)


@allure.feature("商品模块")
@allure.story("异常---错误的商品id")
@allure.title("商品详情信息")
@allure.description("错误的商品详情id")
def test_goodsInfoErr():
    HttpService("GET", baseinfo, params={'id': 999999}).run() \
        .validate("$.msg", "sql: no rows in result set")


@allure.feature("商品模块")
@allure.story("商品详情")
@allure.title("异常---错误的类型")
@allure.description("错误的参数类型")
@pytest.mark.parametrize("parameterTypes", ['null', ' ', ' or 2'])
def test_goodsInfoEps(parameterTypes):
    HttpService("GET", baseinfo, params={'id': parameterTypes}).run() \
        .validate("$.flag", False) \
        .validate("$.code", 306)


@allure.feature("商品模块")
@allure.story("商品sku信息")
@allure.title("正确 -- 商品sku信息")
@allure.description("正常的商品sku信息")
def test_goodsSkuInfo():
    HttpService("GET", GOODS_SKU_INFO, params={'id': 2}).run() \
        .validate('$.code', 0) \
        .validate('$.msg', 'success').validate('$.data[0].sid', 2)


@allure.feature("商品模块")
@allure.story("商品sku信息")
@allure.title("错误 --- 传入错误的sku信息")
@allure.description("错误的商品sku信息")
@pytest.mark.parametrize("parameterTypes", ['null', ' '])
def test_goodsSkuErr(parameterTypes):
    HttpService("GET", GOODS_SKU_INFO, params={'id': parameterTypes}).run() \
        .validate('$.code', 306)


@allure.feature("商品模块")
@allure.story("商品图文详情")
@allure.title("图文详情信息")
@allure.description("正确的图文信息")
def test_goodsImg():
    HttpService("GET", GOODS_IMGTEXT, params={'id': 2}).run().validate('$.data.sid', 2)


@allure.feature("商品模块")
@allure.story("商品图文详情")
@allure.title("图文详情信息")
@allure.description("正确的图文信息")
@pytest.mark.parametrize("parameterTypes", ['null', ' '])
def test_goodsImgErr(parameterTypes):
    HttpService("GET", GOODS_IMGTEXT, params={'id': parameterTypes}).run().validate('$.code', 306)


@allure.feature("商品模块")
@allure.story("商品规格信息")
@allure.title("商品规格信息")
@allure.description("正确的规格信息")
def test_goodsSpec():
    HttpService("GET", GOODS_SPEC, params={'id': 2}).run()


@allure.feature("商品模块")
@allure.story("商品规格信息")
@allure.title("错误商品规格信息")
@allure.description("错误的规格信息入参")
@pytest.mark.parametrize("parmsType", ['null', '', ' or 1'])
def test_goodsSpecErr(parmsType):
    HttpService("GET", GOODS_SPEC, params={'id': parmsType}).run().validate('$.code', 306)


@allure.feature("商品模块")
@allure.story("商品收藏")
@allure.title("正确的商品id,收藏")
def test_goodsCollection():
    req_data = {"is_del": 0, "sid": 2, "reason": ""}
    HttpService("POST", GOOD_COLLECTION, data=req_data).run().validate('$.code', 0)


@allure.feature("商品模块")
@allure.story("商品收藏")
@allure.title("正确的商品id,取消收藏")
def test_goodsCollectionEsc():
    req_data = {"is_del": 1, "sid": 2}
    HttpService("POST", GOOD_COLLECTION, data=req_data).run()
