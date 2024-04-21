# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.user_department import UserDepartment  # noqa: E501
from swagger_server.models.user_department_get_response import UserDepartmentGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserDepartmentController(BaseTestCase):
    """UserDepartmentController integration test stubs"""

    def test_user_department_delete(self):
        """Test case for user_department_delete

        Department leader delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/user_department',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_department_get(self):
        """Test case for user_department_get

        Department leader get
        """
        query_string = [('user_id', 'user_id_example'),
                        ('department_id', 'department_id_example')]
        response = self.client.open(
            '/v1/user_department',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_department_post(self):
        """Test case for user_department_post

        Department leader add
        """
        user_department = UserDepartment()
        response = self.client.open(
            '/v1/user_department',
            method='POST',
            data=json.dumps(user_department),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_department_put(self):
        """Test case for user_department_put

        Department leader edit
        """
        user_deparment = UserDepartment()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/user_department',
            method='PUT',
            data=json.dumps(user_deparment),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
