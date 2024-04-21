# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.canteen_display_get_response import CanteenDisplayGetResponse  # noqa: E501
from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCanteenDisplayController(BaseTestCase):
    """CanteenDisplayController integration test stubs"""

    def test_canteen_display_get(self):
        """Test case for canteen_display_get

        CanteenDisplay get
        """
        response = self.client.open(
            '/v1/canteen_display',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
