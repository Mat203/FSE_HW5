import unittest
from unittest.mock import patch, MagicMock
import data_procession
from datetime import datetime


class TestCalculateDays(unittest.TestCase):
    def test_Should_ReturnTotalDays_When_CalculateDaysCalled(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-10T15:14:17']]}
        result = data_procession.calculate_days(user)
        self.assertEqual(result, 2)

    def test_Should_ReturnOne_When_CalculateDaysCalledWithSameDayAndNoneEnd(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', None]]}
        result = data_procession.calculate_days(user)
        self.assertEqual(result, 1)


class TestCalculateAverageTimes(unittest.TestCase):
    def test_Should_ReturnWeeklyAndDailyAverage_When_CalculateAverageTimesCalled(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-10T15:14:17']]}
        weekly_average, daily_average = data_procession.calculate_average_times(user)
        self.assertEqual(weekly_average, 315000.0)
        self.assertEqual(daily_average, 45000.0)

    def test_Should_ReturnZero_When_CalculateAverageTimesCalledWithNoOnlinePeriods(self):
        user = {'userId': '1', 'isOnline': False, 'onlinePeriods': []}
        weekly_average, daily_average = data_procession.calculate_average_times(user)
        self.assertEqual(weekly_average, 0.0)
        self.assertEqual(daily_average, 0.0)

    def test_Should_ReturnCorrectValues_When_CalculateAverageTimesCalledWithMultipleOnlinePeriods(self):
        user = {'userId': '1', 'isOnline': True, 'onlinePeriods': [['2023-10-09T14:14:17', '2023-10-09T15:14:17'], ['2023-10-10T14:14:17', '2023-10-10T15:14:17']]}
        weekly_average, daily_average = data_procession.calculate_average_times(user)
        self.assertEqual(weekly_average, 25200.0)
        self.assertEqual(daily_average, 3600.0)

unittest.main()