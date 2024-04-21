# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.edit_scanner import EditScanner  # noqa: E501
from swagger_server.models.scanner import Scanner  # noqa: E501
from swagger_server.models.scanner_get_response import ScannerGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestScannerController(BaseTestCase):
    """ScannerController integration test stubs"""

    def test_scanner_delete(self):
        """Test case for scanner_delete

        Scanner delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/scanner',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_scanner_get(self):
        """Test case for scanner_get

        Scanner get
        """
        response = self.client.open(
            '/v1/scanner',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_scanner_post(self):
        """Test case for scanner_post

        Scanner add
        """
        scanner = Scanner()
        response = self.client.open(
            '/v1/scanner',
            method='POST',
            data=json.dumps(scanner),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_scanner_put(self):
        """Test case for scanner_put

        Scanner edit
        """
        scanner = EditScanner()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/scanner',
            method='PUT',
            data=json.dumps(scanner),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
