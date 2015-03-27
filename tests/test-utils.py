# -*- coding:utf8 -*-

import hashlib
import base64
import io

from nose.tools import eq_
from requests import compat

from ucloudauth import utils

DATA_B = b"data-bytes"
DATA_S = u"data-string"

DATA_FB = io.BytesIO(DATA_B)
DATA_FS = io.StringIO(DATA_S)


def cal_md5(content):
    return base64.b64encode(hashlib.md5(content).digest()).decode("utf8")


def gen(data):
    for d in data:
        yield d


MD5_B = cal_md5(DATA_B)
MD5_S = cal_md5(DATA_S.encode("utf8"))


def test_to_bytes():
    eq_(type(utils.to_bytes(DATA_B)), compat.bytes)
    eq_(type(utils.to_bytes(DATA_S)), compat.bytes)
    eq_(type(utils.to_bytes(ord(b"1"))), compat.bytes)
    eq_(utils.to_bytes(49), b"1")


def check_md5(data, file_data, md5):
    eq_(utils.cal_content_md5(data), (data, md5))

    file_content, file_md5 = utils.cal_content_md5(file_data)
    eq_(file_content.read(), data)
    eq_(file_md5, md5)

    g_content, g_md5 = utils.cal_content_md5(gen(data))
    eq_(
        g_content.read(),
        data if isinstance(data, compat.bytes) else data.encode("utf8")
    )
    eq_(g_md5, md5)


def test_md5_str():
    check_md5(DATA_S, DATA_FS, MD5_S)


def test_md5_bytes():
    check_md5(DATA_B, DATA_FB, MD5_B)
