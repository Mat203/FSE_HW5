import unittest
from datetime import datetime, timedelta
from data_procession import fetch_and_update_data, delete_user_data, previous_state, calculate_days, calculate_min_max, calculate_average_times, calculate_online_time, generate_report, get_reports_in_date_range
import json
from unittest.mock import patch, MagicMock,mock_open
from dateutil.parser import parse

class TestIntegration(unittest.TestCase):
    @patch('data_procession.get_data')
    def test_Should_FetchAndUpdateUserData_When_DataDeleted(self, mock_get_data):
        user_id = '1'
        user = {'userId': user_id, 'isOnline': True, 'lastSeenDate': datetime.now().isoformat()}
        mock_get_data.return_value = [user]

        fetch_and_update_data()
        self.assertTrue(previous_state)
        self.assertIn(user_id, previous_state)

        delete_user_data(user_id)
        self.assertNotIn(user_id, previous_state)

        fetch_and_update_data()
        self.assertNotIn(user_id, previous_state)

    @patch('data_procession.get_data')
    def Should_FetchAndUpdateDeletedData_When_MultipleUsers(self, mock_get_data):
        user1_id = '1'
        user1 = {'userId': user1_id, 'isOnline': True, 'lastSeenDate': datetime.now().isoformat()}
        user2_id = '2'
        user2 = {'userId': user2_id, 'isOnline': True, 'lastSeenDate': datetime.now().isoformat()}
        mock_get_data.return_value = [user1, user2]

        fetch_and_update_data()
        self.assertTrue(previous_state)

        delete_user_data(user1_id)
        self.assertNotIn(user1_id, previous_state)

        fetch_and_update_data()
        self.assertNotIn(user1_id, previous_state)
        self.assertIn(user2_id, previous_state)

    @patch('data_procession.get_data')
    def Should_CalculateTimeAndDeleteUser_Properly(self, mock_get_data):
        user_id = '1'
        user = {'userId': user_id, 'isOnline': True, 'lastSeenDate': datetime.now().isoformat(), 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17']]}
        mock_get_data.return_value = [user]

        self.assertEqual(calculate_days(user), 1)
        self.assertEqual(calculate_online_time(user), 3600.0)
        weekly_avg, daily_avg = calculate_average_times(user)
        self.assertEqual(weekly_avg, 3600.0 * 7)
        self.assertEqual(daily_avg, 3600.0)

        delete_user_data(user_id)
        self.assertNotIn(user_id, previous_state)

        fetch_and_update_data()
        self.assertNotIn(user_id, previous_state)

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

class TestIntegrationGenerateAndFilterReport(unittest.TestCase):
    def test_integration_generate_and_filter_report(self):
        all_data = [
            {
                "userId": "user1",
                "metrics": [
                    {"date": "2023-10-15", "dailyAverage": 100},
                    {"date": "2023-10-16", "dailyAverage": 150},
                    {"date": "2023-10-17", "dailyAverage": 200},
                ]
            },
            {
                "userId": "user2",
                "metrics": [
                    {"date": "2023-10-15", "dailyAverage": 50},
                    {"date": "2023-10-16", "dailyAverage": 80},
                    {"date": "2023-10-17", "dailyAverage": 120},
                ]
            },
        ]

        with open("all_data.json", "w") as f:
            json.dump(all_data, f)
        generate_report("integration_test_report", ["dailyAverage"], ["user1", "user2"])

        from_date = parse("2023-10-16")
        to_date = parse("2023-10-17")

        with open("integration_test_report.json", "r") as f:
            generated_report_data = json.load(f)

        filtered_reports = get_reports_in_date_range(generated_report_data, from_date, to_date)
        self.assertEqual(len(filtered_reports), 2)

unittest.main()

