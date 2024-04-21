# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.edit_serving import EditServing  # noqa: E501
from swagger_server.models.serving import Serving  # noqa: E501
from swagger_server.models.serving_get_response import ServingGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestServingController(BaseTestCase):
    """ServingController integration test stubs"""

    def test_serving_delete(self):
        """Test case for serving_delete

        Serving delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/serving',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_serving_get(self):
        """Test case for serving_get

        Serving get
        """
        query_string = [('out_of_service', 'out_of_service_example')]
        response = self.client.open(
            '/v1/serving',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_serving_post(self):
        """Test case for serving_post

        Serving add
        """
        serving = Serving()
        response = self.client.open(
            '/v1/serving',
            method='POST',
            data=json.dumps(serving),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_serving_put(self):
        """Test case for serving_put

        Serving edit
        """
        serving = EditServing()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/serving',
            method='PUT',
            data=json.dumps(serving),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
