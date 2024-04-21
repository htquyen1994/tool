# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.edit_line import EditLine  # noqa: E501
from swagger_server.models.line import Line  # noqa: E501
from swagger_server.models.line_get_response import LineGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLineController(BaseTestCase):
    """LineController integration test stubs"""

    def test_line_delete(self):
        """Test case for line_delete

        Line delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/line',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_line_get(self):
        """Test case for line_get

        Line get
        """
        response = self.client.open(
            '/v1/line',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_line_post(self):
        """Test case for line_post

        Line add
        """
        line = Line()
        response = self.client.open(
            '/v1/line',
            method='POST',
            data=json.dumps(line),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_line_put(self):
        """Test case for line_put

        Line edit
        """
        line = EditLine()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/line',
            method='PUT',
            data=json.dumps(line),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
