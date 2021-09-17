import json
from typing import Any, Dict, Optional

FAKE_RESP = {
    ("GET", "/posts"): [{"id": 1}, {"id": 2}, {"id": 3}],
    ("GET", "/posts/1"): "",
    ("GET", "/posts/2"): "",
    ("GET", "/posts/3"): "",
}


class FakeResp:
    status = 200
    body: Optional[str] = None

    def __init__(self, resp_body: str) -> None:
        self.body = resp_body

    def read(self) -> Optional[str]:
        return self.body


class FakeJSONPlaceholder:
    def request(
        self,
        method: str,
        path: str,
        body: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.method = method
        self.path = path

    def response(self) -> FakeResp:
        return FakeResp(json.dumps(FAKE_RESP[(self.method, self.path)]))
