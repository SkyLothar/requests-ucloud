UCloud authentication for the awesome requests!
-----------------------------------------------

.. image:: https://travis-ci.org/SkyLothar/requests-ucloud?branch=master
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

.. code-block:: python

    >>> import requests
    >>> from ucloudauth import UCloudAuth
    >>> req = requests.get(
    ...     "https://api.ucloud.cn/",
    ...     params=dict(SomeParams="SomeValue"),
    ...     auth=UCLoudAuth("public-key", "private-key")
    ... )
    <Response [200]>

Or set the auth attribute to the session object

.. code-block:: python

    >>> import requests
    >>> from ucloudauth import UCloudAuth
    >>> session = requests.session()
    >>> session.auth = UCloudAuth("public-key", "private-key")
    >>> req = session.get(
    ...     "https://api.ucloud.cn/",
    ...     params=dict(SomeParams="SomeValue")
    ... )
    <Response [200]>
    
UCloud API
----------
View full `UCloud API`_

.. _UCloud API: http://docs.ucloud.cn/api/apilist.html
