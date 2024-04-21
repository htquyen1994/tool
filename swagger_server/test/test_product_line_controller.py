# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.product_line_get_response import ProductLineGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProductLineController(BaseTestCase):
    """ProductLineController integration test stubs"""

    def test_product_line_get(self):
        """Test case for product_line_get

        ProductLine get
        """
        query_string = [('department_id', 'department_id_example')]
        response = self.client.open(
            '/v1/product_line',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
