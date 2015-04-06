import mock

from ucloudauth import UCloudOmniAuth


class TestOmni(object):
    def setup(self):
        self.auth = UCloudOmniAuth("public-key", "private-key")

    def test_ucloud(self):
        with mock.patch.object(self.auth, "_ucloud_auth") as mock_auth:
            mock_req = mock.MagicMock()
            mock_req.url = "http://api.ucloud.cn"

            self.auth(mock_req)
            mock_auth.assert_called_once_with(mock_req)

    def test_ufile(self):
        with mock.patch.object(self.auth, "_ufile_auth") as mock_auth:
            mock_req = mock.MagicMock()
            mock_req.url = "http://bucket.ufile.ucloud.cn/key"

            self.auth(mock_req)
            mock_auth.assert_called_once_with(mock_req)

    def test_internal_ufile(self):
        with mock.patch.object(self.auth, "_ufile_auth") as mock_auth:
            mock_req = mock.MagicMock()
            mock_req.url = "http://bucket.ufile.cn-north-03.ucloud.cn"

            self.auth(mock_req)
            mock_auth.assert_called_once_with(mock_req)
