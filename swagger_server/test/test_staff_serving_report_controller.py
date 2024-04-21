# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.report_filter import ReportFilter  # noqa: E501
from swagger_server.models.staff_serving_report_response import StaffServingReportResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStaffServingReportController(BaseTestCase):
    """StaffServingReportController integration test stubs"""

    def test_staff_serving_report_post(self):
        """Test case for staff_serving_report_post

        StaffServingReport post request
        """
        staff_ShiftMealServingInfoServing = ReportFilter()
        response = self.client.open(
            '/v1/staff_serving_report',
            method='POST',
            data=json.dumps(staff_ShiftMealServingInfoServing),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
