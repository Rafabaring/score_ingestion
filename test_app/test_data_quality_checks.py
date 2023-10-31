import unittest

from data_quality_check.data_quality_check import (
    check_data_types,
    check_null,
    check_empty_string,
    check_data_ranges,
    check_mandatory_fields,
    check_event_type,
    check_score_format,
)

class TestDataQualityChecks(unittest.TestCase):
    def test_check_data_types(self):
        payload = {'studentId': 'Avis49', 'exam': 13251, 'score': 0.6702194158299797, 'eventType': 'score'}
        self.assertTrue(check_data_types(payload))

    def test_check_null(self):
        payload = {'studentId': 'Avis49', 'exam': 13251, 'score': 0.6702194158299797, 'eventType': 'score'}
        self.assertTrue(check_null(payload))

    def test_check_empty_string(self):
        payload = {'studentId': 'Avis49', 'exam': 13251, 'score': 0.6702194158299797, 'eventType': 'score'}
        self.assertTrue(check_empty_string(payload))

    def test_check_data_ranges(self):
        payload = {'studentId': 'Avis49', 'exam': 13251, 'score': 0.6702194158299797, 'eventType': 'score'}
        self.assertTrue(check_data_ranges(payload))

    def test_check_mandatory_fields(self):
        payload = {'studentId': 'Avis49', 'exam': 13251, 'score': 0.6702194158299797, 'eventType': 'score'}
        self.assertTrue(check_mandatory_fields(payload))

    def test_check_event_type(self):
        payload = {'studentId': 'Avis49', 'exam': 13251, 'score': 0.6702194158299797, 'eventType': 'score'}
        self.assertTrue(check_event_type(payload))

    def test_check_score_format(self):
        payload = {'studentId': 'Avis49', 'exam': 13251, 'score': 0.67, 'eventType': 'score'}
        self.assertTrue(check_score_format(payload))

if __name__ == '__main__':
    unittest.main()