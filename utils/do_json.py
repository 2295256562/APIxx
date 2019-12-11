import json


def read_json(filepath):
    with open(filepath, 'r') as jsonfile:
        json_obj = json.load(jsonfile)

        data = json_obj[1]['test']
        interface = data['name']
        method = data['request']['method']
        headers = data['request']['headers']
        request_data = data['request'].setdefault('json')
        validate = data['validate']

        # print(interface, method, headers, request_data, validate)
        return interface, method, headers, request_data, validate


read_json('test.json')
