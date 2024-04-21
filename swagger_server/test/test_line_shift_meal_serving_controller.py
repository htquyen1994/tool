# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.line_shift_meal_serving import LineShiftMealServing  # noqa: E501
from swagger_server.models.line_shift_meal_serving_edit import LineShiftMealServingEdit  # noqa: E501
from swagger_server.models.line_shift_meal_serving_get_response import LineShiftMealServingGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLineShiftMealServingController(BaseTestCase):
    """LineShiftMealServingController integration test stubs"""

    def test_line_shift_meal_serving_delete(self):
        """Test case for line_shift_meal_serving_delete

        Line shift meal serving delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/line_shift_meal_serving',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_line_shift_meal_serving_get(self):
        """Test case for line_shift_meal_serving_get

        LineShiftMealServing get
        """
        response = self.client.open(
            '/v1/line_shift_meal_serving',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_line_shift_meal_serving_post(self):
        """Test case for line_shift_meal_serving_post

        LineShiftMealServing get
        """
        line_shift_meal_serving = LineShiftMealServing()
        response = self.client.open(
            '/v1/line_shift_meal_serving',
            method='POST',
            data=json.dumps(line_shift_meal_serving),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_line_shift_meal_serving_put(self):
        """Test case for line_shift_meal_serving_put

        LineShiftMealServing get
        """
        line_shift_meal_serving = LineShiftMealServingEdit()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/line_shift_meal_serving',
            method='PUT',
            data=json.dumps(line_shift_meal_serving),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
