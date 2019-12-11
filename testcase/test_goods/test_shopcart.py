import pytest
import allure

from env.url import SETACCOUNTS, ADD_SHOPCART, RECORDS, GET_TOKEN, SUMBIT_ORDER, ORDER_PAY, ORDER_DETAIL
from requester.httpService import HttpService


@pytest.mark.parametrize('sid, sku_id', [(2, 10)])
def test_setAccounts(sid, sku_id):
    data = {"sid": sid, "amount": 1, "sku_id": sku_id}
    # 加入购物车
    HttpService("POST", ADD_SHOPCART, data=data).run().validate('$.code', 0)
    # 购物车商品
    HttpService("GET", RECORDS, params={"page_index": 1, "page_size": 100}).run()

    # 获取下单token
    res = HttpService("GET", GET_TOKEN).run().extract('$.data')[0]
    data = {"is_shopping_car": True, "products": [{"num": 2, "sid": sid, "sku_id": sku_id}], "user_addr_id": 107334,
            "order_type": "normal"}

    # 确认订单
    cc = HttpService("POST", SETACCOUNTS, data=data).run() \
        .validate('$.data.normal_order_products[0].sid', sid) \
        .validate('$.data.normal_order_products[0].sku_id', sku_id)

    # 商品数量
    goodsNum = cc.response.json()['data']['normal_order_products'][0]['num']
    # 商品单价
    goodPrice = cc.response.json()['data']['normal_order_products'][0]['sale_price']
    # 邮费
    expressFees = (cc.response.json()['data']['normal_order_products'][0]['product_delivery']['delivery_fee'])

    # 支付金额
    should_amount = goodsNum * goodPrice + expressFees

    # 提交订单
    data = {"user_addr_id": 107334, "type": "normal", "buy_message": "", "channel": "h5",
            "idempotent_token": res, "is_shopping_car": True,
            "productSubmits": [{"num": 2, "sid": sid, "sku_id": sku_id}], "source": "h5", "user_coupons": [],
            "discount_amount": 0, "should_amount": should_amount, "total_amount": goodsNum * goodPrice,
            "total_freight": expressFees, "discount_freight": 0,
            "freight": 10}

    order_id = HttpService("POST", SUMBIT_ORDER, data=data).run().extract('$.data.trade_order_id')

    # 支付
    HttpService("GET", ORDER_PAY, params={'orderId': order_id}).run().validate('$.data', True)

    # 商品详情
    HttpService("GET", ORDER_DETAIL, params={'id': order_id}).run() \
        .validate('$.data.trade_order.pay_amount', should_amount) \
        .validate('$.data.trade_order.total_amount', goodsNum * goodPrice) \
        .validate('$.data.trade_order.type', 1) \
        .validate('$.data.trade_order.uid', 3033471) \
        .validate('$.data.trade.pay_stauts', '1') \
        .validate('$.data.trade.pay_type', 1) \
        .validate('$.data.trade.trade_amount', should_amount)
