import unittest
from unittest.mock import Mock, patch
from data_procession import get_data 
from data_procession import update_user_data
from data_procession import fetch_and_update_data
import requests

class TestGetDataFunction(unittest.TestCase):
    @patch('data_procession.requests.get')
    def test_Should_GetData_When_Success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'data': 'mocked_data'}
        mock_get.return_value = mock_response

        result = get_data(1)

        self.assertEqual(result, 'mocked_data')

    @patch('data_procession.requests.get')
    def test_Should_ReturnException_When_Failure(self, mock_get):
        mock_get.side_effect = Exception("Mocked error")

        with self.assertRaises(Exception):
            get_data(1) 

class TestUpdateUserData(unittest.TestCase):

    def test_Should_Update_UserData_of_ExistingUser(self):
        previous_state = {'user123': {'userId': 'user123', 'isOnline': True}}
        user = {'userId': 'user123', 'nickname': 'John', 'isOnline': False}

        updated_user = update_user_data(user, previous_state)

        expected_user = {
            'userId': 'user123',
            'isOnline': False,
            'nickname': 'John'
        }

        self.assertEqual(updated_user, expected_user)

    def test_Should_Update_UserSata_When_NewUser(self):
        previous_state = {'user123': {'userId': 'user123', 'isOnline': True}}
        user = {'userId': 'user456', 'nickname': 'Alice', 'isOnline': True}

        updated_user = update_user_data(user, previous_state)

        expected_user = {
            'userId': 'user456',
            'isOnline': True,
            'nickname': 'Alice'
        }

        self.assertEqual(updated_user, expected_user)   


class TestFetchAndUpdateData(unittest.TestCase):
    @patch('data_procession.get_data')  
    @patch('data_procession.update_user_data')  
    @patch('data_procession.save_user_data_to_json') 
    def test_Should_fetch_and_update_data(self, mock_save, mock_update, mock_get):
        mock_get.side_effect = [
            [{'userId': 1, 'isOnline': True, 'lastSeenDate': '2023-11-02', 'nickname': 'test', 'lastName': 'user', 'registrationDate': '2023-11-01'}],
            []
        ]
        mock_update.return_value = {'userId': 1, 'isOnline': True, 'lastSeenDate': '2023-11-02', 'nickname': 'test', 'lastName': 'user', 'registrationDate': '2023-11-01', 'firstDetectionTime': None}
        
        fetch_and_update_data()

        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(mock_update.call_count, 1)
        self.assertEqual(mock_save.call_count, 1)
if __name__ == '__main__':
    unittest.main()


