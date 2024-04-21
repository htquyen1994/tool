# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.post_staff_serving_register_detail import PostStaffServingRegisterDetail  # noqa: E501
from swagger_server.models.staff_serving_register_get_response import StaffServingRegisterGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStaffServingRegisterController(BaseTestCase):
    """StaffServingRegisterController integration test stubs"""

    def test_staff_serving_register_delete(self):
        """Test case for staff_serving_register_delete

        Staff Serving Register delete
        """
        query_string = [('staff_id', 'staff_id_example')]
        response = self.client.open(
            '/v1/staff_serving_register',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_staff_serving_register_get(self):
        """Test case for staff_serving_register_get

        StaffServingRegister get
        """
        response = self.client.open(
            '/v1/staff_serving_register',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_staff_serving_register_post(self):
        """Test case for staff_serving_register_post

        StaffServingRegister post
        """
        staff_serving_register_list = [PostStaffServingRegisterDetail()]
        response = self.client.open(
            '/v1/staff_serving_register',
            method='POST',
            data=json.dumps(staff_serving_register_list),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
