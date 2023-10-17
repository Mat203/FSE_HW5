import unittest
from unittest.mock import patch, MagicMock
import data_procession
from datetime import datetime

class TestDeleteUserData(unittest.TestCase):
    @patch('json.dump')
    @patch('json.load')
    @patch('builtins.open')
    def test_Should_DeleteUserData_When_DeleteUserDataCalled(self, mock_open, mock_load, mock_dump):
        mock_load.return_value = [{'userId': '1'}, {'userId': '2'}]
        data_procession.delete_user_data('1')
        mock_dump.assert_called_once_with([{'userId': '2'}], mock_open.return_value.__enter__.return_value)
        
    @patch('json.dump')
    @patch('json.load')
    @patch('builtins.open')
    def test_Should_NotChangeData_When_DeleteUserDataCalledWithNonExistingUserId(self, mock_open, mock_load, mock_dump):
        mock_load.return_value = [{'userId': '1'}, {'userId': '2'}]
        data_procession.delete_user_data('3')
        mock_dump.assert_called_once_with([{'userId': '1'}, {'userId': '2'}], mock_open.return_value.__enter__.return_value)

    @patch('json.dump')
    @patch('json.load')
    @patch('builtins.open')
    def test_Should_NotChangeData_When_DeleteUserDataCalledWithNoUserId(self, mock_open, mock_load, mock_dump):
        mock_load.return_value = [{'userId': '1'}, {'userId': '2'}]
        data_procession.delete_user_data(None)
        mock_dump.assert_called_once_with([{'userId': '1'}, {'userId': '2'}], mock_open.return_value.__enter__.return_value)

    @patch('json.dump')
    @patch('json.load')
    @patch('builtins.open')
    def test_Should_NotChangeData_When_DeleteUserDataCalledWithEmptyData(self, mock_open, mock_load, mock_dump):
        mock_load.return_value = []
        data_procession.delete_user_data('1')
        mock_dump.assert_called_once_with([], mock_open.return_value.__enter__.return_value)

unittest.main()