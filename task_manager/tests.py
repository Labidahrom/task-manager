import json


def get_test_data():
    with open('task_manager/fixtures/test_data.json', 'r') as f:
        return json.loads(f.read())
