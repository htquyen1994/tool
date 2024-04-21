# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.edit_shift_meal import EditShiftMeal  # noqa: E501
from swagger_server.models.shift_meal import ShiftMeal  # noqa: E501
from swagger_server.models.shift_meal_get_response import ShiftMealGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestShiftMealController(BaseTestCase):
    """ShiftMealController integration test stubs"""

    def test_shift_meal_delete(self):
        """Test case for shift_meal_delete

        ShiftMeal delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/shift_meal',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_shift_meal_get(self):
        """Test case for shift_meal_get

        ShiftMeal get
        """
        query_string = [('shift_id', 'shift_id_example'),
                        ('meal_id', 'meal_id_example')]
        response = self.client.open(
            '/v1/shift_meal',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_shift_meal_post(self):
        """Test case for shift_meal_post

        ShiftMeal add
        """
        shift_meal = ShiftMeal()
        response = self.client.open(
            '/v1/shift_meal',
            method='POST',
            data=json.dumps(shift_meal),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_shift_meal_put(self):
        """Test case for shift_meal_put

        ShiftMeal edit
        """
        shift_meal = EditShiftMeal()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/shift_meal',
            method='PUT',
            data=json.dumps(shift_meal),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
