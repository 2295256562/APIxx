import allure
from requester.httpService import HttpService


@allure.feature("商品模块")
@allure.story("商品列表")
@allure.title("商品搜索")
@allure.description("搜索睡衣商品")
def test_seachGoods():
    res = HttpService("GET", '/app/ec/product/search?pageIndex=1&pageSize=100&filter=%7B%22word%22%3A%22%E7%9D%A1%E8%A1%A3%22%7D').run()
    print(res.response.json())

@allure.feature("商品模块")
@allure.story("商品详情")
@allure.title("商品详情信息")
@allure.description("商品睡衣详情")
def test_goodsInfo():
    pass