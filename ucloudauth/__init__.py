# -*- coding:utf8 -*-

"""
ucloudauth
~~~~~~~~~~~~~~~

This module contains the authentication handlers for UCloud Service
"""

__version__ = "0.3.1"
__author__ = "SkyLothar"
__email__ = "allothar@gmail.com"
__url__ = "http://github.com/skylothar/requests-ucloud"

__all__ = ["UCloudOmniAuth", "UCloudAuth", "UFileAuth"]

from .common_sign import UCloudAuth
from .ufile import UFileAuth

import requests


class UCloudOmniAuth(requests.auth.AuthBase):
    def __init__(self, public_key, private_key):
        self._ucloud_auth = UCloudAuth(public_key, private_key)
        self._ufile_auth = UFileAuth(public_key, private_key)

    def __call__(self, req):
        """Sign the request"""
        url = requests.compat.urlsplit(req.url)
        u_host = url.netloc.split(".", 1)[1]
        if u_host.startswith("ufile.") and u_host.endswith(".ucloud.cn"):
            return self._ufile_auth(req)
        else:
            return self._ucloud_auth(req)
