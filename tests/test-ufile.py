# -*- coding:utf8 -*-

import base64
import hashlib

import requests
import mock

from nose.tools import eq_
from requests.compat import urlsplit

if requests.compat.is_py2:
    from urlparse import parse_qsl
elif requests.compat.is_py3:
    from urllib.parse import parse_qsl

from ucloudauth import UFileAuth


DATA = b"test-data"
DATA_MD5 = base64.b64encode(hashlib.md5(DATA).digest()).decode("utf8")

HEADERS = {
    "X-ucloud-1": "1",
    "x-uCloud-0": "2"
}
STR_TO_SIGN = """
PUT
{0}
text/html
test-time
x-ucloud-0:2
x-ucloud-1:1/bucket-name/key.html
""".format(DATA_MD5).strip()
AUTHORIZATION = "UCloud public-key:vex1mk5WI2fe/i5TzXm7QY19p64="
PARAMS = dict(
    UCloudPublicKey="public-key",
    Signature="JHrQ1u087Gv0ktLlBAyfYclnI/I=",
    Expires="1"
)


class TestUFileAuth(object):
    def setup(self):
        self.auth = UFileAuth("public-key", "private-key")
        self.request = requests.Request(
            "PUT", "http://bucket-name.ufile.ucloud.cn/key.html", data=DATA,
            headers=HEADERS
        )

    def test_headers_empty_md5(self):
        request = self.request.prepare()
        empty_md5_auth = UFileAuth(
            "public-key", "private-key", allow_empty_md5=True
        )
        empty_md5_req = empty_md5_auth.fill_all_headers(request)
        eq_(empty_md5_req.headers["Content-Md5"], None)

    def test_header_no_md5(self):
        request = self.request.prepare()
        no_md5_req = self.auth.fill_all_headers(request)
        eq_(no_md5_req.headers["Content-Md5"], DATA_MD5)

    def test_header_md5(self):
        request = self.request.prepare()
        request.headers["Content-Md5"] = "content-md5"
        md5_req = self.auth.fill_all_headers(request)
        eq_(md5_req.headers["Content-Md5"], "content-md5")

    def test_headers_empty_content_type(self):
        request = self.request.prepare()
        with mock.patch("mimetypes.guess_type") as mock_guess:
            mock_guess.return_value = (None, None)
            req = self.auth.fill_all_headers(request)
            eq_(req.headers["Content-Type"], self.auth.DEFAULT_TYPE)

    def test_headers_no_content_type(self):
        request = self.request.prepare()
        no_ct_req = self.auth.fill_all_headers(request)
        eq_(no_ct_req.headers["Content-Type"], "text/html")

    def test_headers_content_type(self):
        request = self.request.prepare()
        request.headers["Content-Type"] = "test-type"
        ct_req = self.auth.fill_all_headers(request)
        eq_(ct_req.headers["Content-Type"], "test-type")

    @mock.patch("time.time")
    @mock.patch("time.strftime")
    def test_headers_date(self, mock_strftime, mock_time):
        mock_time.return_value = 0
        mock_strftime.return_value = "test-time"
        request = self.request.prepare()

        auth_expires = UFileAuth(
            "public-key", "private-key", expires=1, expires_in=2
        )
        expires_req = auth_expires.fill_all_headers(request)
        eq_(expires_req.headers.get("Date"), None)
        eq_(auth_expires._expires, "1")

        auth_expires_in = UFileAuth("public-key", "private-key", expires_in=2)
        expires_in_req = auth_expires_in.fill_all_headers(request)
        eq_(expires_in_req.headers.get("Date"), None)
        eq_(auth_expires_in._expires, "2")

        req = self.auth.fill_all_headers(request)
        eq_(req.headers.get("Date"), "test-time")

    @mock.patch("time.strftime")
    def test_str_to_sign(self, mock_strftime):
        mock_strftime.return_value = "test-time"

        request = self.request.prepare()
        req = self.auth.fill_all_headers(request)
        eq_(self.auth.gen_str_to_sign(req), STR_TO_SIGN)

    @mock.patch("time.strftime")
    def test_sign_in_header(self, mock_strftime):
        mock_strftime.return_value = "test-time"

        req = self.auth(self.request.prepare())
        eq_(req.headers["Authorization"], AUTHORIZATION)

    @mock.patch("time.time")
    def test_sign_in_url(self, mock_strftime):
        mock_strftime.return_value = 0

        auth = UFileAuth("public-key", "private-key", expires=1)
        req = auth(self.request.prepare())

        url = urlsplit(req.url)
        params = dict(parse_qsl(url.query))
        eq_(params, PARAMS)
