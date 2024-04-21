# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.kitchen_display_get_response import KitchenDisplayGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestKitchenDisplayController(BaseTestCase):
    """KitchenDisplayController integration test stubs"""

    def test_serving_register_display(self):
        """Test case for serving_register_display

        CanteenDisplay get
        """
        response = self.client.open(
            '/v1/kitchen_display',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
