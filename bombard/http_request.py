import http.client
import ssl
from typing import Optional
from urllib.parse import urlparse

EXCEPTION_STATUS = "!!!"


def http_request(
    url: str,
    method: str = "GET",
    headers: Optional[dict] = None,
    body: Optional[str] = None,
    timeout: Optional[int] = None,
) -> (int, dict):
    """
    Make HTTP request.

    Returns tuple:
        <HTTP response status>, <response body>
    """
    try:
        url = urlparse(url)
        kwargs = {"timeout": timeout} if timeout is not None else {}
        if url.scheme.lower() == "https":
            conn = http.client.HTTPSConnection(
                url.netloc,
                context=ssl._create_unverified_context(),
                **kwargs,
            )
        else:
            conn = http.client.HTTPConnection(
                url.netloc,
                **kwargs,
            )
        conn.request(method, url.path, body=body, headers=headers if headers is not None else {})
        resp = conn.getresponse()
        resp_body = resp.read()
    except Exception as e:
        return EXCEPTION_STATUS, str(e)
    return resp.status, resp_body
