import http.client
import ssl
from typing import Any, Dict, Optional, Tuple, Union
from urllib.parse import urlparse

EXCEPTION_STATUS = "!!!"


def http_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, Any]] = None,
    body: Optional[str] = None,
    timeout: Optional[int] = None,
) -> Tuple[Union[int, str], Any]:
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
                context=ssl._create_unverified_context(),  # pylint: disable=protected-access
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
    except Exception as e:
        return EXCEPTION_STATUS, str(e)
    return resp.status, resp_body
