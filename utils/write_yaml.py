import os

import yaml


def write_yaml(key, value):
    """
    把获取到的token值写入到yaml文件
    :param value:
    :return:
    """
    path2 = os.getcwd()
    ypath = os.path.join('/Users/kxm/qa2/自动化脚本/APIkuang', 'env/token.yaml')
    print(ypath)
    # 需写入的内容
    t = {key: value}
    # 写入到yaml文件
    with open(ypath, "w", encoding="utf-8") as f:
        yaml.dump(t, f)


def read_yaml(local):
    path2 = os.getcwd()
    ypath = os.path.join('/Users/kxm/qa2/自动化脚本/APIkuang', 'env/token.yaml')
    print(ypath)
    with open(ypath, 'r') as yaml_file:
        yaml_obj = yaml.load(yaml_file.read(), Loader=yaml.FullLoader)
        local = yaml_obj[local]
        return local

path2 = os.path.abspath('.')
print(path2)