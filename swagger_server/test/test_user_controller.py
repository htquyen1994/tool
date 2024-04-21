# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.edit_user import EditUser  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_get_response import UserGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_user_delete(self):
        """Test case for user_delete

        User delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/user',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_get(self):
        """Test case for user_get

        User get
        """
        query_string = [('role_id', 'role_id_example')]
        response = self.client.open(
            '/v1/user',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_post(self):
        """Test case for user_post

        User add
        """
        user = User()
        response = self.client.open(
            '/v1/user',
            method='POST',
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_put(self):
        """Test case for user_put

        User edit
        """
        user = EditUser()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/user',
            method='PUT',
            data=json.dumps(user),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
