# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.user_product_line import UserProductLine  # noqa: E501
from swagger_server.models.user_product_line_get_response import UserProductLineGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserProductLineController(BaseTestCase):
    """UserProductLineController integration test stubs"""

    def test_user_productline_delete(self):
        """Test case for user_productline_delete

        ProductLine leader delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/user_productline',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_productline_get(self):
        """Test case for user_productline_get

        ProductLine leader get
        """
        query_string = [('user_id', 'user_id_example'),
                        ('productline_id', 'productline_id_example')]
        response = self.client.open(
            '/v1/user_productline',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_productline_post(self):
        """Test case for user_productline_post

        ProductLine leader add
        """
        user_productline = UserProductLine()
        response = self.client.open(
            '/v1/user_productline',
            method='POST',
            data=json.dumps(user_productline),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_productline_put(self):
        """Test case for user_productline_put

        ProductLine leader edit
        """
        user_productline = UserProductLine()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/user_productline',
            method='PUT',
            data=json.dumps(user_productline),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
