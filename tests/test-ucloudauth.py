# -*- coding:utf8 -*-

import requests

from nose.tools import eq_
from requests.compat import urlparse


if requests.compat.is_py2:
    from urlparse import parse_qsl
else:
    from urllib.parse import parse_qsl

from ucloudauth import UCloudAuth


class TestUCloudAuth(object):
    url = "https://api.ucloud.cn/"
    params = dict(
        Action="CreateUHostInstance",
        Region="cn-north-01",
        ImageId="f43736e1-65a5-4bea-ad2e-8a46e18883c2",
        CPU="2",
        Memory="2048",
        DiskSpace="10",
        LoginMode="Password",
        Password="UCloudexample01",
        Name="Host01",
        ChargeType="Month",
        Quantity="1"
    )
    public_key = "ucloudsomeone@example.com1296235120854146120"
    private_key = "46f09bb9fab4f12dfc160dae12273d5332b5debe"
    correct = dict(
        PublicKey=public_key,
        PrivateKey=private_key,
        Signature="7a517649e4e9da3b6c82c932d667daa1599ae3a1",
        **params
    )

    def setup(self):
        req = requests.Request(
            "GET", self.url, params=self.params,
            auth=UCloudAuth(self.public_key, self.private_key)
        )
        self.request = req.prepare()

    def test_signature(self):
        url = urlparse(self.request.url)
        params = dict(parse_qsl(url.query))
        for key in params.keys():
            eq_(params[key], self.correct[key])


if __name__ == "__main__":
    t = TestUCloudAuth()
    t.setup()
    t.test_signature()
