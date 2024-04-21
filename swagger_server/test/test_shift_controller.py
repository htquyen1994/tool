# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.edit_shift import EditShift  # noqa: E501
from swagger_server.models.shift import Shift  # noqa: E501
from swagger_server.models.shift_get_response import ShiftGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestShiftController(BaseTestCase):
    """ShiftController integration test stubs"""

    def test_shift_delete(self):
        """Test case for shift_delete

        Shift delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/shift',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_shift_get(self):
        """Test case for shift_get

        Shift get
        """
        response = self.client.open(
            '/v1/shift',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_shift_post(self):
        """Test case for shift_post

        Shift add
        """
        shift = Shift()
        response = self.client.open(
            '/v1/shift',
            method='POST',
            data=json.dumps(shift),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_shift_put(self):
        """Test case for shift_put

        Shift edit
        """
        shift = EditShift()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/shift',
            method='PUT',
            data=json.dumps(shift),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
