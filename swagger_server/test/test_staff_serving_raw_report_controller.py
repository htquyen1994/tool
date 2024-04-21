# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.staff_serving_filter import StaffServingFilter  # noqa: E501
from swagger_server.models.staff_serving_get_response import StaffServingGetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStaffServingRawReportController(BaseTestCase):
    """StaffServingRawReportController integration test stubs"""

    def test_staff_serving_raw_report_post(self):
        """Test case for staff_serving_raw_report_post

        StaffServingRawReport post request
        """
        staff_ShiftMealServingInfoServing = StaffServingFilter()
        response = self.client.open(
            '/v1/staff_serving_raw_report',
            method='POST',
            data=json.dumps(staff_ShiftMealServingInfoServing),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
