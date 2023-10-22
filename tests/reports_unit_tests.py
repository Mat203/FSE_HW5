import unittest
from datetime import datetime, timedelta
from data_procession import calculate_average_times, calculate_min_max,generate_report, get_reports_in_date_range
import json
from unittest.mock import patch, mock_open
from dateutil.parser import parse

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

    def test_Should_Calculate_Average_Times(self):
        weekly_average, daily_average = calculate_average_times(self.user)
        self.assertEqual(daily_average, 20)
        self.assertEqual(weekly_average, 140)

    def test_Should_Calculate_Min_Max(self):
        min_time, max_time = calculate_min_max(self.user)
        self.assertEqual(min_time, 10)
        self.assertEqual(max_time, 10)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_ShouldGenerate_Report_When_Data_Presented(self, mock_dump, mock_load, mock_open):
        mock_load.return_value = [{"userId": "test_user", "onlinePeriods": [["2023-01-01T00:00:00", "2023-01-01T00:10:00"]]}]
        generate_report('test_report', ['dailyAverage', 'total', 'weeklyAverage'], ['test_user'])
        args, _ = mock_dump.call_args
        report_data = args[0]
        self.assertIn('test_user', report_data)
        self.assertIn('dailyAverage', report_data['test_user'])
        self.assertIn('weeklyAverage', report_data['test_user'])
        self.assertIn('total', report_data['test_user'])

class TestIntegrationGenerateAndFilterReport(unittest.TestCase):
    def test_integration_generate_and_filter_report(self):
        all_data = [
            {
                "userId": "user1",
                "onlinePeriods": [["2023-10-15T08:00:00.000000", "2023-10-15T12:00:00.000000"]],
                "totalSecondsOnline": 14400,
            },
            {
                "userId": "user2",
                "onlinePeriods": [["2023-10-15T09:00:00.000000", "2023-10-15T11:00:00.000000"]],
                "totalSecondsOnline": 7200,
            },
        ]

        with open("all_data.json", "w") as f:
            json.dump(all_data, f)
        generate_report("integration_test_report", ["total"], ["user1", "user2"])

        from_date = parse("2023-10-15T08:00:00.000000")
        to_date = parse("2023-10-15T11:00:00.000000")

        with open("integration_test_report.json", "r") as f:
            generated_report_data = json.load(f)

        filtered_reports = get_reports_in_date_range(generated_report_data, from_date, to_date)

        self.assertEqual(len(filtered_reports), 0)




if __name__ == '__main__':
    unittest.main()
