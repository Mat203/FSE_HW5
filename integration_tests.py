import unittest
from datetime import datetime, timedelta
import data_procession

from unittest.mock import patch, MagicMock

class TestIntegration(unittest.TestCase):
    @patch('data_procession.get_data')
    def test_Should_FetchAndUpdateUserData_When_DataDeleted(self, mock_get_data):
        user_id = '1'
        user = {'userId': user_id, 'isOnline': True, 'lastSeenDate': datetime.now().isoformat()}
        mock_get_data.return_value = [user]

        data_procession.fetch_and_update_data()
        self.assertTrue(data_procession.previous_state)
        self.assertIn(user_id, data_procession.previous_state)

        data_procession.delete_user_data(user_id)
        self.assertNotIn(user_id, data_procession.previous_state)

        data_procession.fetch_and_update_data()
        self.assertNotIn(user_id, data_procession.previous_state)


    @patch('data_procession.get_data')
    def Should_FetchAndUpdateDeletedData_When_MultipleUsers(self, mock_get_data):
        user1_id = '1'
        user1 = {'userId': user1_id, 'isOnline': True, 'lastSeenDate': datetime.now().isoformat()}
        user2_id = '2'
        user2 = {'userId': user2_id, 'isOnline': True, 'lastSeenDate': datetime.now().isoformat()}
        mock_get_data.return_value = [user1, user2]

        data_procession.fetch_and_update_data()
        self.assertTrue(data_procession.previous_state)

        data_procession.delete_user_data(user1_id)
        self.assertNotIn(user1_id, data_procession.previous_state)

        data_procession.fetch_and_update_data()
        self.assertNotIn(user1_id, data_procession.previous_state)
        self.assertIn(user2_id, data_procession.previous_state)

    @patch('data_procession.get_data')
    def Should_CalculateTimeAndDeleteUser_Properly(self, mock_get_data):
        user_id = '1'
        user = {'userId': user_id, 'isOnline': True, 'lastSeenDate': datetime.now().isoformat(), 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17']]}
        mock_get_data.return_value = [user]

        self.assertEqual(data_procession.calculate_days(user), 1)
        self.assertEqual(data_procession.calculate_online_time(user), 3600.0)
        weekly_avg, daily_avg = data_procession.calculate_average_times(user)
        self.assertEqual(weekly_avg, 3600.0 * 7)
        self.assertEqual(daily_avg, 3600.0)

        data_procession.delete_user_data(user_id)
        self.assertNotIn(user_id, data_procession.previous_state)

        data_procession.fetch_and_update_data()
        self.assertNotIn(user_id, data_procession.previous_state)


unittest.main()

