# -*- coding:utf8 -*-

"""
ucloudauth
~~~~~~~~~~~~~~~

This module contains the authentication handlers for UCloud Service
"""

__version__ = "0.1.0"
__author__ = "SkyLothar"
__email__ = "allothar@gmail.com"
__url__ = "http://github.com/skylothar/requests-ucloud"

__all__ = ["UCloudAuth", "UFileAuth"]

from .common_sign import UCloudAuth
from .ufile import UFileAuth
