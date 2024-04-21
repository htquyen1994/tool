# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.department_get_response import DepartmentGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDepartmentController(BaseTestCase):
    """DepartmentController integration test stubs"""

    def test_department_get(self):
        """Test case for department_get

        Department get
        """
        response = self.client.open(
            '/v1/department',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
