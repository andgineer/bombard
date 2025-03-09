import http.client
import ssl
from typing import Any, Optional, Union
from urllib.parse import urlparse

EXCEPTION_STATUS = "!!!"


def http_request(
    url: str,
    method: str = "GET",
    headers: Optional[dict[str, Any]] = None,
    body: Optional[str] = None,
    timeout: Optional[int] = None,
) -> tuple[Union[int, str], Any]:
    """
    Make HTTP request.

    Returns tuple:
        <HTTP response status>, <response body>
    """
    try:
        url_parsed = urlparse(url)
        kwargs = {"timeout": timeout} if timeout is not None else {}
        if url_parsed.scheme.lower() == "https":
            conn = http.client.HTTPSConnection(
                url_parsed.netloc,
                context=ssl._create_unverified_context(),  # noqa: S323,SLF001
                **kwargs,  # type:ignore
            )
        else:
            conn = http.client.HTTPConnection(  # type:ignore
                url_parsed.netloc,
                **kwargs,  # type:ignore
            )
        conn.request(
            method,
            url_parsed.path,
            body=body,
            headers=headers if headers is not None else {},
        )
        resp = conn.getresponse()
        resp_body = resp.read()
    except Exception as e:  # noqa: BLE001
        return EXCEPTION_STATUS, str(e)
    return resp.status, resp_body
