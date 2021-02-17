from datetime import time, datetime
from enum import IntEnum
from typing import Set, Union


class Day(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class ScheduleConfigurationError(Exception):
    pass


class Schedule(object):

    def __init__(self):
        self.weekdays: Set[Day] = set()
        self.time: Union[time, None] = None

    def __repr__(self):
        return f'{self.__class__.__qualname__}, {self.weekdays}'

    def at(self, time_string: str):
        self.time = self._time_string_to_datetime(time_string)

    @staticmethod
    def _time_string_to_datetime(time_string: str):
        split_string = time_string.split(':')
        if 1 < len(split_string) > 3:
            e = f'Invalid time string provided, {time_string}'
            raise ScheduleConfigurationError(e)

        # get correct time format string depending on params provided
        time_format = {1: '%H', 2: '%H:%M', 3: '%H:%M:%S'}
        schedule_datetime = datetime.strptime(time_string, time_format[len(split_string)])
        return schedule_datetime.time()

    def between(self, *days) -> 'Schedule':
        """
        Sets the schedule to be active between the specified days (inclusive).
        @param days: the extremes of the interval
        """
        if len(days) != 2:
            e = f'Schedules between days require exactly two days, got {days}'
            raise ScheduleConfigurationError(e)

        start_day, end_day = days[0], days[1]
        self.weekdays = self._weekdays_between(start_day, end_day)
        return self

    def every(self, *days) -> 'Schedule':
        """
        Sets the schedule to be active on the specified days.
        @param days: the exact days when the schedule will be active
        """
        weekdays = set(days)
        self.weekdays = weekdays
        return self

    def every_day(self) -> 'Schedule':
        """
        Sets the schedule to be active every day of the week.
        """
        self.weekdays = [day for day in Day]
        return self

    def exclude(self, *days) -> 'Schedule':
        """
        Excludes the specified days from the schedule.

        Example:
        >>> schedule = Schedule().between(Day.Monday, Day.FRIDAY)
        >>> schedule.exclude(Day.THURSDAY)
        >>> print(schedule)
        @param days: the days to remove from the schedule
        """
        weekdays = set(days)
        self.weekdays = self.weekdays - weekdays
        return self

    @staticmethod
    def _weekdays_between(start_day: Day, end_day: Day) -> Set[Day]:
        if start_day == end_day:  # e.g. Friday to Friday
            end_day += 6
        if start_day > end_day:  # e.g. Saturday to Tuesday
            end_day += 7

        weekdays = [Day(index % 7) for index in range(start_day, end_day + 1)]
        return set(weekdays)

    def is_active_today(self) -> bool:
        """
        Returns true if the schedule is set to be active today.
        """
        if len(self.weekdays) == 0:
            e = 'Schedules must have at least one day.'
            raise ScheduleConfigurationError(e)

        today = datetime.now()
        weekday = Day(today.weekday())
        return weekday in self.weekdays
