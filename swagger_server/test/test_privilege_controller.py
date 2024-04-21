# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.privilege_get_response import PrivilegeGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPrivilegeController(BaseTestCase):
    """PrivilegeController integration test stubs"""

    def test_privilege_get(self):
        """Test case for privilege_get

        Privilege get
        """
        response = self.client.open(
            '/v1/privilege',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
