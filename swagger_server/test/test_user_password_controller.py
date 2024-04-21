# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.user_password import UserPassword  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserPasswordController(BaseTestCase):
    """UserPasswordController integration test stubs"""

    def test_user_password_put(self):
        """Test case for user_password_put

        UserPassword edit
        """
        user_password = UserPassword()
        response = self.client.open(
            '/v1/user_password',
            method='PUT',
            data=json.dumps(user_password),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
