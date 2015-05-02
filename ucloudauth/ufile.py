# -*- coding:utf8 -*-

"""
ucloudauth.ufile
~~~~~~~~~~~~~~~~

This module contains the authentication handlers for UFile file management
"""

import base64
import hmac
import hashlib
import mimetypes
import time

import logging

import requests
from requests.compat import unquote, urlencode, urlsplit

if requests.compat.is_py2:
    from urlparse import parse_qsl
elif requests.compat.is_py3:
    from urllib.parse import parse_qsl

from . import utils

__all__ = ["UFileAuth"]
logger = logging.getLogger(__name__)


class UFileAuth(requests.auth.AuthBase):
    """Attach UFile Authentication to the given request

    :param public_key: your UCloud public_key
    :param private_key: your UCloud private_key
    :param expires: (optional) the request will expire after the given epoch
    :param expires_in: (optional) the request will expires in x `seconds`,
        this option will cause the *url sign method*
    :param allow_empty_md5: (optional) don't calculate md5. Default is `False`,
        calculate md5 when content-md5 not appears in the headers

    Usage::

        >>> import requests
        >>> from ucloudauth import UFileAuth
        >>> req = request.get(
        ...     "https://example.ufile.ucloud.cn/example.txt",
        ...     auth=UFileAuth("public-key", "private-key")
        ... )
        <Response [200]>

    """

    DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"
    DEFAULT_TYPE = "application/octstream"

    def __init__(
        self,
        public_key, private_key,
        expires=None, expires_in=None,
        allow_empty_md5=False
    ):
        self._public_key = public_key
        self._private_key = utils.to_bytes(private_key)
        self._allow_empty_md5 = allow_empty_md5

        if isinstance(expires, (int, float)):
            self._expires = str(int(expires))
        elif isinstance(expires_in, (int, float)):
            self._expires = str(int(time.time() + expires_in))
        else:
            self._expires = None

    def __call__(self, req):
        """Sign the request"""
        req = self.fill_all_headers(req)
        str_to_sign = self.gen_str_to_sign(req)
        logger.debug("string to sign is:\n{0}".format(str_to_sign))

        hmac_sig = hmac.HMAC(
            self._private_key,
            utils.to_bytes(str_to_sign),
            hashlib.sha1
        )
        signature = base64.b64encode(hmac_sig.digest()).decode("utf8")

        if self._expires:
            url = urlsplit(req.url)
            params = dict(parse_qsl(url.query))
            params.update(dict(
                Expires=self._expires,
                UCloudPublicKey=self._public_key,
                Signature=signature
            ))
            req.url = "{0}://{1}{2}?{3}".format(
                url.scheme, url.netloc, url.path, urlencode(params)
            )
        else:
            req.headers["Authorization"] = "UCloud {0}:{1}".format(
                self._public_key, signature
            )

        # remove empty header
        for key, val in req.headers.copy().items():
            if not val:
                logger.debug("deleting empty header key: {0}".format(key))
                del req.headers[key]

        return req

    def gen_str_to_sign(self, req):
        """Generate string to sign using giving prepared request"""
        url = urlsplit(req.url)
        bucket_name = url.netloc.split(".", 1)[0]

        logger.debug(req.headers.items())
        ucloud_headers = [
            (k, v.strip())
            for k, v in sorted(req.headers.lower_items())
            if k.startswith("x-ucloud-")
        ]
        canonicalized_headers = "\n".join([
            "{0}:{1}".format(k, v) for k, v in ucloud_headers
        ])

        canonicalized_resource = "/{0}{1}".format(
            bucket_name,
            unquote(url.path)
        )

        str_to_sign = "\n".join([
            req.method,
            req.headers.get("content-md5", ""),
            req.headers.get("content-type", ""),
            req.headers.get("date", self._expires),
            canonicalized_headers + canonicalized_resource
        ])
        return str_to_sign

    def fill_all_headers(self, req):
        """Set content-type, content-md5, date to the request."""
        url = urlsplit(req.url)

        content_type, __ = mimetypes.guess_type(url.path)
        if content_type is None:
            content_type = self.DEFAULT_TYPE
            logger.warn("can not determine mime-type for {0}".format(url.path))
        if self._expires is None:
            # sign with url, no content-type for url
            req.headers.setdefault("content-type", content_type)

        if (
            req.body is not None
            and req.headers.get("content-md5") is None
            and self._allow_empty_md5 is False
        ):
            logger.debug("calculating content-md5")
            content, content_md5 = utils.cal_content_md5(req.body)
            req.body = content
            req.headers["content-md5"] = content_md5
            logger.debug("new content-md5 is: {0}".format(content_md5))
        else:
            logger.debug("skip content-md5 calculation")

        if self._expires is None:
            req.headers.setdefault(
                "date",
                time.strftime(self.DATE_FMT, time.gmtime())
            )
        return req
