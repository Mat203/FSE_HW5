import unittest
from unittest.mock import patch, MagicMock
from data_procession import fetch_and_update_data, get_data, update_user_data, save_user_data_to_json, print_json_file  # replace with your actual module

class TestIntegration(unittest.TestCase):
    @patch('data_procession.get_data')  
    @patch('data_procession.update_user_data')  
    @patch('data_procession.save_user_data_to_json') 
    def test_Should_fetch_and_update_data_using_AllThePreviousFunctions(self, mock_save, mock_update, mock_get):
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
