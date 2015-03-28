UCloud authentication for the awesome requests!
-----------------------------------------------

.. image:: https://travis-ci.org/SkyLothar/requests-ucloud.svg?branch=master
    :target: https://travis-ci.org/SkyLothar/requests-ucloud

.. image:: https://coveralls.io/repos/SkyLothar/requests-ucloud/badge.png
    :target: https://coveralls.io/r/SkyLothar/requests-ucloud

.. image:: https://requires.io/github/SkyLothar/requests-ucloud/requirements.svg?branch=master
    :target: https://requires.io/github/SkyLothar/requests-ucloud/requirements/?branch=master

.. image:: https://pypip.in/py_versions/requests-ucloud/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/requests-ucloud/
    :alt: Supported Python versions

.. image:: https://pypip.in/license/requests-ucloud/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/requests-ucloud/
    :alt: License


How to Install
--------------
Just

.. code-block:: bash

   pip install requests-ucloud

How to Use
----------
Just pass the auth object to requests

Omni API Auth
^^^^^^^^^^^^^
For common api and ufile authentication

.. code-block:: python

   >>> import requests
   >>> from ucloudauth import UCloudOmniAuth
   >>> session = reqeusts.session()
   >>> session.auth = UCloudOmniAuth("public-key", "private-key")
   >>> session.get(
   ...     "http://api.ucloud.cn",
   ...     params=dict(Action="SomeAction")  # demo of common api
   ... )
   <Response [200]>
   >>> session.put(
   ...     "http://bucket.ufile.ucloud.cn/key",
   ...     data="test-data"  # demo of ufile api
   ... )
   <Response [200]>


Common UCloud Auth
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> import requests
    >>> from ucloudauth import UCloudAuth
    >>> requests.get(
    ...     "https://api.ucloud.cn/",
    ...     params=dict(SomeParams="SomeValue"),
    ...     auth=UCLoudAuth("public-key", "private-key")
    ... )
    <Response [200]>


UFile Object Auth
^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> import requests
    >>> from ucloudauth import UFile
    >>> session = requests.session()
    >>> session.auth = UFileAuth(
    ...     "public-key",
    ...     "private-key",
    ...     expires=None,  # for signing in url, expires is unix `timestamp`
    ...     expires_in=None,  # for signing in url, expires in `x` seconds
    ...     allow_empty_md5=False  # if no content-md5 was provided, UFileAuth will calculate for you
    ...     # set to `True` to disable this function
    ... )
    >>> req = session.put(
    ...     "http://bucket-name.ufile.ucloud.cn/test-key.txt",
    ...     data="test-data"
    ... )
    <Response [200]>
    >>> url_auth = UFileAuth(
    ...     "public-key",
    ...     "private-key",
    ...     expires=None,  # for signing in url, expires is unix `timestamp`
    ...     expires_in=10,  # for signing in url, expires in 10 seconds
    ... )
    >>> req = requests.Request(
    ...     "GET",  # http method
    ...     "http://bucket-name.ufile.ucloud.cn/test-key.txt",  # url
    ...     auth=url_auth
    ... )
    >>> req.prepare().url
    "http://bucket-name.ufile.cloud.cn/test-key.txt?Signature&Other&Params"

UCloud API
----------
View full `UCloud API`_

UFile API
----------
View full `UFile API`_

.. _UCloud API: http://docs.ucloud.cn/api/apilist.html
.. _UFile API: http://docs.ucloud.cn/api/ufile/index.html
