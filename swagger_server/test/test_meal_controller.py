# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.edit_meal import EditMeal  # noqa: E501
from swagger_server.models.meal import Meal  # noqa: E501
from swagger_server.models.meal_get_response import MealGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMealController(BaseTestCase):
    """MealController integration test stubs"""

    def test_meal_delete(self):
        """Test case for meal_delete

        Meal delete
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/meal',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_meal_get(self):
        """Test case for meal_get

        Meal get
        """
        response = self.client.open(
            '/v1/meal',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_meal_post(self):
        """Test case for meal_post

        Meal add
        """
        meal = Meal()
        response = self.client.open(
            '/v1/meal',
            method='POST',
            data=json.dumps(meal),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_meal_put(self):
        """Test case for meal_put

        Meal edit
        """
        meal = EditMeal()
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/v1/meal',
            method='PUT',
            data=json.dumps(meal),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
