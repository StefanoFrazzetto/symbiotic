from unittest import TestCase

import pytest
from freezegun import freeze_time

from symbiotic.schedule import Day, Schedule, ScheduleConfigurationError


class Test_Schedule_Unit(TestCase):

    @freeze_time("2021-02-17")  # Wednesday
    def test_schedule_one_day(self):
        schedule = Schedule()
        schedule.every(Day.WEDNESDAY)
        self.assertTrue(schedule.is_active_today())

    def test_empty_schedule(self):
        schedule = Schedule()
        with pytest.raises(ScheduleConfigurationError):
            schedule.is_active_today()

    def test_schedule_between_days_exception(self):
        schedule = Schedule()
        with pytest.raises(ScheduleConfigurationError):
            schedule.between()

    def test_schedule_between_two_days(self):
        schedule = Schedule()
        schedule.between(Day.TUESDAY, Day.THURSDAY)
        expected_days = {Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY}
        self.assertEqual(expected_days, schedule.weekdays)

    def test_schedule_between_two_days_with_rollover(self):
        schedule = Schedule()
        schedule.between(Day.SATURDAY, Day.TUESDAY)
        expected_days = {Day.SATURDAY, Day.SUNDAY, Day.MONDAY, Day.TUESDAY}
        self.assertEqual(expected_days, schedule.weekdays)

    def test_schedule_between_and_exclude_one_day(self):
        schedule = Schedule()
        schedule.between(Day.SATURDAY, Day.TUESDAY).exclude(Day.MONDAY)
        expected_days = {Day.SATURDAY, Day.SUNDAY, Day.TUESDAY}
        self.assertEqual(expected_days, schedule.weekdays)

    def test_schedule_between_and_exclude_day_not_in_schedule(self):
        schedule = Schedule()
        schedule.between(Day.SATURDAY, Day.TUESDAY).exclude(Day.THURSDAY)
        expected_days = {Day.SATURDAY, Day.SUNDAY, Day.MONDAY, Day.TUESDAY}
        self.assertEqual(expected_days, schedule.weekdays)

    def test_schedule_between_same_day(self):
        schedule = Schedule()
        schedule.between(Day.SATURDAY, Day.SATURDAY)
        expected_days = {Day.SATURDAY, Day.SUNDAY, Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY}
        self.assertEqual(expected_days, schedule.weekdays)
