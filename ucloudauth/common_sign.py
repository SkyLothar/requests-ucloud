# -*- coding:utf8 -*-

"""
ucloudauth.common_sign
~~~~~~~~~~~~~~~

This module contains the authentication handlers for Common UCloud Service
"""

import itertools
import hashlib
import logging

import requests
from requests.compat import urlencode, urlsplit

if requests.compat.is_py2:
    from urlparse import parse_qsl
else:
    from urllib.parse import parse_qsl

__all__ = ["UCloudAuth"]
logger = logging.getLogger(__name__)


class UCloudAuth(requests.auth.AuthBase):
    """Attach UCloud Authentication to the given request

    :param public_key: your UCloud public_key
    :param private_key: your UCloud private_key

    Usage::

        >>> import requests
        >>> from ucloudauth import UCloudAuth
        >>> req = request.get(
        ...     "https://api.ucloud.cn",
        ...     params=dict(Action="CreateUHostInstance", CPU=2),
        ...     auth=UCloudAuth("public-key", "private-key")
        ... )
        <Response [200]>

    """

    def __init__(self, public_key, private_key):
        self._public_key = public_key
        self._private_key = private_key

    def __call__(self, req):
        """sign the request"""
        url = urlsplit(req.url)
        params = dict(parse_qsl(url.query))
        params["PublicKey"] = self._public_key
        sorted_params = sorted(params.items())

        params_data = list(itertools.chain.from_iterable(sorted_params))

        str_to_sign = "".join(params_data + [self._private_key]).encode("utf8")
        logger.debug("string to sign is:\n".format(str_to_sign))
        signature = hashlib.sha1(str_to_sign).hexdigest()

        req.url = "{0}://{1}{2}?{3}&Signature={4}".format(
            url.scheme, url.netloc, url.path,
            urlencode(sorted_params), signature
        )
        return req
