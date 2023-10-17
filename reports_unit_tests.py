import unittest
from datetime import datetime, timedelta
from data_procession import calculate_average_times, calculate_min_max,generate_report
import json
from unittest.mock import patch, mock_open

class TestReportGeneration(unittest.TestCase):
    def setUp(self):
        self.user = {
            'userId': 'test_user',
            'isOnline': True,
            'lastSeenDate': datetime.now().isoformat(),
            'onlinePeriods': [
                [datetime.now().isoformat(), (datetime.now() + timedelta(seconds=10)).isoformat()],
                [(datetime.now() + timedelta(seconds=20)).isoformat(), (datetime.now() + timedelta(seconds=30)).isoformat()]
            ]
        }

    def test_calculate_average_times(self):
        weekly_average, daily_average = calculate_average_times(self.user)
        self.assertEqual(daily_average, 20)
        self.assertEqual(weekly_average, 140)

    def test_calculate_min_max(self):
        min_time, max_time = calculate_min_max(self.user)
        self.assertEqual(min_time, 10)
        self.assertEqual(max_time, 10)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_generate_report(self, mock_dump, mock_load, mock_open):
        mock_load.return_value = [{"userId": "test_user", "onlinePeriods": [["2023-01-01T00:00:00", "2023-01-01T00:10:00"]]}]
        generate_report('test_report', ['dailyAverage', 'total', 'weeklyAverage'], ['test_user'])
        args, _ = mock_dump.call_args
        report_data = args[0]
        self.assertIn('test_user', report_data)
        self.assertIn('dailyAverage', report_data['test_user'])
        self.assertIn('weeklyAverage', report_data['test_user'])
        self.assertIn('total', report_data['test_user'])



if __name__ == '__main__':
    unittest.main()
