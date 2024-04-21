# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.factory_get_response import FactoryGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestFactoryController(BaseTestCase):
    """FactoryController integration test stubs"""

    def test_factory_get(self):
        """Test case for factory_get

        Factory get
        """
        response = self.client.open(
            '/v1/factory',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
