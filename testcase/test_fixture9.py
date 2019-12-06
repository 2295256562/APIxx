import pytest

@pytest.fixture()
def first():
    print("\n获取用户名")
    a = "yoyo"
    return a

@pytest.fixture(scope="function")
def sencond():
    print("\n获取密码")
    b = "123456"
    return b

def test_1(first):
    '''用例传fixture'''
    print("测试账号：%s" %first)
    assert first == "yoyo"

def test_2(sencond):
    '''用例传fixture'''
    print("测试密码：%s" %sencond)
    assert sencond == "123456"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture9.py"])