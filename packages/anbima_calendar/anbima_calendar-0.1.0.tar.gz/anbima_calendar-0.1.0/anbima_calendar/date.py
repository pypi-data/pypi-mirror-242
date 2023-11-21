"""
This module, part of the Anbima Calendar package, provides functionality for determining
 business days, adding business days to dates, checking if a given date is past due,
 and identifying public holidays in Brazil.

The module's functions leverage a dataset of Brazilian holidays to make calculations
relevant to financial and scheduling applications. These utilities are especially
useful for applications that need to consider Brazilian banking holidays and business
days for date calculations and scheduling.

Functions:
    - is_business_day: Determine if a given date is a business day in Brazil.
    - add_business_days: Add a specific number of business days to a given date.
    - is_past_due: Check if a given due date has already passed compared to a current
        date.
    - get_holiday: Retrieve the name of the holiday for a given date, if it is a
        holiday.
    - _parse_date: Internal utility function to parse a date from a string or date
        object.

Each function takes into account Brazilian public holidays and weekends while
performing its calculations. The module raises `InvalidDateError` if an input date is
not in a valid format or cannot be parsed correctly.
"""

from datetime import date, timedelta
from typing import Optional, Union

from anbima_calendar.errors import InvalidDateError
from anbima_calendar.holidays import HOLIDAYS


def is_business_day(check_date: Union[str, date]) -> bool:
    """
    Check if the given date is a business day.

    :param check_date: The date to check, can be a string or `datetime.date` object.
    :type check_date: Union[str, datetime.date]
    :return: `True` if the date is a business day, `False` otherwise.
    :rtype: bool
    :raises InvalidDateError: If the input is not a valid date string or date object.
    """
    date_param = _parse_date(check_date)
    weekend = [5, 6]  # Sat, Sun
    wday = date_param.weekday()
    year = str(date_param.year)

    return not (wday in weekend or date_param in HOLIDAYS[year].values())


def add_business_days(number_of_days: int, since_date: Union[str, date]) -> date:
    """
    Add a specified number of business days to a given date.

    :param number_of_days: The number of business days to add.
    :type number_of_days: int
    :param since_date: The starting date for adding business days, can be a string or
        `datetime.date` object.
    :type since_date: Union[str, datetime.date]
    :return: The date obtained after adding the business days.
    :rtype: datetime.date
    :raises InvalidDateError: If the input is not a valid date string or date object.
    """
    since = _parse_date(since_date)

    last_date = None
    counter = 1
    while number_of_days > 0:
        last_date = since + timedelta(days=counter)
        counter += 1

        if not is_business_day(last_date):
            continue

        number_of_days -= 1

    return last_date


def is_past_due(due_date: Union[str, date], current_date: Union[str, date]) -> bool:
    """
    Determine if a due date has passed relative to the current date.

    :param due_date: The due date to check, can be a string or `datetime.date` object.
    :type due_date: Union[str, datetime.date]
    :param current_date: The current date for comparison, can be a string or
        `datetime.date` object.
    :type current_date: Union[str, datetime.date]
    :return: `True` if the due date is past the current date, `False` otherwise.
    :rtype: bool
    :raises InvalidDateError: If any input is not a valid date string or date object.
    """
    due_date = _parse_date(due_date)
    current_date = _parse_date(current_date)

    if not is_business_day(due_date):
        due_date = add_business_days(1, due_date)

    return current_date > due_date


def get_holiday(check_date: Union[str, date]) -> Optional[str]:
    """
    Retrieve the holiday name for a given date, if it is a holiday.

    :param check_date: The date to check for a holiday, can be a string or
        `datetime.date` object.
    :type check_date: Union[str, datetime.date]
    :return: The name of the holiday if the date is a holiday, `None` otherwise.
    :rtype: Optional[str]
    :raises InvalidDateError: If the input is not a valid date string or date object.
    """
    date_param = _parse_date(check_date)
    year = str(date_param.year)

    for holiday, hdate in HOLIDAYS[year].items():
        if hdate == date_param:
            return holiday

    return None


def _parse_date(param: Union[str, date]) -> date:
    """
    Parse a date from a string or date object.

    :param param: The date parameter to parse.
    :type param: Union[str, datetime.date]
    :return: The parsed date object.
    :rtype: datetime.date
    :raises InvalidDateError: If the input is not a valid date string or date object.
    """
    if isinstance(param, date):
        return param

    if not isinstance(param, str):
        raise InvalidDateError(f"{param} is not a valid date")

    try:
        if param.find("/") != -1:
            str_date = "-".join(reversed(param.split("/")))
        else:
            str_date = param

        return date.fromisoformat(str_date)
    except ValueError:
        raise InvalidDateError(f"{param} is not a valid date format")
