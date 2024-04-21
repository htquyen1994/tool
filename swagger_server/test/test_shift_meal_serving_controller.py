# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.edit_shift_meal_serving import EditShiftMealServing  # noqa: E501
from swagger_server.models.shift_meal_serving import ShiftMealServing  # noqa: E501
from swagger_server.models.shift_meal_serving_get_response import ShiftMealServingGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestShiftMealServingController(BaseTestCase):
    """ShiftMealServingController integration test stubs"""

    def test_shift_meal_serving_get(self):
        """Test case for shift_meal_serving_get

        ShiftMealServing get
        """
        query_string = [('shiftmeal_id', 'shiftmeal_id_example'),
                        ('serving_id', 'serving_id_example')]
        response = self.client.open(
            '/v1/shift_meal_serving',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_shift_meal_serving_post(self):
        """Test case for shift_meal_serving_post

        ShiftMealServing add
        """
        shiftmealserving = ShiftMealServing()
        response = self.client.open(
            '/v1/shift_meal_serving',
            method='POST',
            data=json.dumps(shiftmealserving),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_shift_meal_serving_put(self):
        """Test case for shift_meal_serving_put

        ShiftMealServing edit
        """
        shiftmealserving = EditShiftMealServing()
        response = self.client.open(
            '/v1/shift_meal_serving',
            method='PUT',
            data=json.dumps(shiftmealserving),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_shiftmealserving_delete(self):
        """Test case for shiftmealserving_delete

        ShiftMealServing delete
        """
        query_string = [('shift_meal_id', 'shift_meal_id_example')]
        response = self.client.open(
            '/v1/shift_meal_serving',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
