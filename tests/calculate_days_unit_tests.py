import unittest
from unittest.mock import patch, MagicMock
import data_procession
from datetime import datetime

class TestCalculateOnlineTime(unittest.TestCase):
    def test_Should_ReturnTotalSecondsOnline_When_CalculateOnlineTimeCalled(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17']]}
        result = data_procession.calculate_online_time(user)
        self.assertEqual(result, 3600)
    def test_Should_ReturnOne_When_CalculateDaysCalledWithSameDay(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17']]}
        result = data_procession.calculate_days(user)
        self.assertEqual(result, 1)

    def test_Should_ReturnTwo_When_CalculateDaysCalledWithDifferentDays(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-10T15:14:17']]}
        result = data_procession.calculate_days(user)
        self.assertEqual(result, 2)

unittest.main()