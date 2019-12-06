import os

import yaml

print(os.getcwd())

print(os.path.join(os.getcwd(), 'env/token.yaml'))


print (os.path.abspath(os.curdir))
path2 = os.path.abspath('..')
y = os.path.join(path2, 'APIkuang/env/token.yaml')

with open(y, 'r') as yaml_file:
    yaml_obj = yaml.load(yaml_file.read(), Loader=yaml.FullLoader)
    local = yaml_obj["token"]
    print(local)


print(os.path.abspath(os.path.dirname(__file__)))