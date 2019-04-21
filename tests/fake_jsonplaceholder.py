import json


FAKE_RESP = {
    ('GET', '/posts'): [
        {'id': 1}, {'id': 2}, {'id': 3}
    ],
    ('GET', '/posts/1'): '',
    ('GET', '/posts/2'): '',
    ('GET', '/posts/3'): '',
}


class FakeResp:
    status = 200
    body = None

    def __init__(self, resp_body):
        self.body = resp_body

    def read(self):
        return self.body


class FakeJSONPlaceholder:
    def request(self, method, path, body=None, headers=None):
        self.method = method
        self.path = path

    def response(self):
        return FakeResp(json.dumps(
            FAKE_RESP[(self.method, self.path)]
        ))
