# -*- coding:utf8 -*-

"""
ucloudauth.utils
~~~~~~~~~~~~~~~~

This module contains the some utils for ucloudauth
"""


import base64
import hashlib
import inspect
import io

from requests.compat import basestring, str


CHUNK_SIZE = 100 * 1024  # 100k


def to_bytes(content, encoding="utf8"):
    if isinstance(content, str):
        content = content.encode(encoding)
    elif isinstance(content, int):
        # single-char bytes
        content = chr(content).encode("utf8")
    return content


def cal_content_md5(content):
    md5_hash = hashlib.md5()
    if isinstance(content, basestring):
        md5_hash.update(to_bytes(content))
    elif hasattr(content, "read"):
        # file-like object
        partial = content.read(CHUNK_SIZE)
        while partial:
            md5_hash.update(to_bytes(partial))
            partial = content.read(CHUNK_SIZE)
        content.seek(0, 0)
    elif inspect.isgenerator(content):
        io_content = io.BytesIO()
        for partial in content:
            data_piece = to_bytes(partial)
            io_content.write(data_piece)
            md5_hash.update(data_piece)
        content = io_content
        content.seek(0, 0)
    else:
        raise TypeError(
            "can not calculate content-md5 for {0}".format(type(content))
        )
    return content, base64.b64encode(md5_hash.digest()).decode("utf8")
