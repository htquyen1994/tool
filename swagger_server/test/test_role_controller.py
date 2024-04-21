# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.edit_role import EditRole  # noqa: E501
from swagger_server.models.role import Role  # noqa: E501
from swagger_server.models.role_get_response import RoleGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestRoleController(BaseTestCase):
    """RoleController integration test stubs"""

    def test_role_delete(self):
        """Test case for role_delete

        Role delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/role',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_role_get(self):
        """Test case for role_get

        Role get
        """
        query_string = [('factory_id', 'factory_id_example')]
        response = self.client.open(
            '/v1/role',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_role_post(self):
        """Test case for role_post

        Role add
        """
        role = Role()
        response = self.client.open(
            '/v1/role',
            method='POST',
            data=json.dumps(role),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_role_put(self):
        """Test case for role_put

        Role edit
        """
        role = EditRole()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/role',
            method='PUT',
            data=json.dumps(role),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
