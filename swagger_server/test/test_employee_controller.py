# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.employee_response import EmployeeResponse  # noqa: E501
from swagger_server.models.leader_info_param import LeaderInfoParam  # noqa: E501
from swagger_server.models.register_food import RegisterFood  # noqa: E501
from swagger_server.test import BaseTestCase


class TestEmployeeController(BaseTestCase):
    """EmployeeController integration test stubs"""

    def test_employee_get(self):
        """Test case for employee_get

        Get employees
        """
        leader_info = LeaderInfoParam()
        query_string = [('secret_key', 'secret_key_example')]
        response = self.client.open(
            '/v1/employee',
            method='GET',
            data=json.dumps(leader_info),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_food_post(self):
        """Test case for register_food_post

        Food post
        """
        food_register = RegisterFood()
        query_string = [('secret_key', 'secret_key_example')]
        response = self.client.open(
            '/v1/register_food',
            method='POST',
            data=json.dumps(food_register),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
