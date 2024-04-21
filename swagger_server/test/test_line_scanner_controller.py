# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.edit_line_scanner import EditLineScanner  # noqa: E501
from swagger_server.models.line_scanner_get_response import LineScannerGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLineScannerController(BaseTestCase):
    """LineScannerController integration test stubs"""

    def test_line_scanner_delete(self):
        """Test case for line_scanner_delete

        LineScanner delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/line_scanner',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_line_scanner_get(self):
        """Test case for line_scanner_get

        LineScanner get
        """
        query_string = [('line_id', 'line_id_example'),
                        ('scanner_id', 'scanner_id_example')]
        response = self.client.open(
            '/v1/line_scanner',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_line_scanner_post(self):
        """Test case for line_scanner_post

        LineScanner add
        """
        line_scanner = EditLineScanner()
        response = self.client.open(
            '/v1/line_scanner',
            method='POST',
            data=json.dumps(line_scanner),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_line_scanner_put(self):
        """Test case for line_scanner_put

        LineScanner edit
        """
        line_scanner = EditLineScanner()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/line_scanner',
            method='PUT',
            data=json.dumps(line_scanner),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
