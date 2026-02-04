"""Utilities for date manipulation"""

from datetime import date, datetime, timedelta
from typing import Tuple


def get_week_dates(year: int, week: int) -> Tuple[date, date]:
    """Get start and end dates for a given week number"""
    # The %V format considers week 1 as the first week with a Thursday in it
    first_day = datetime.strptime(f"{year}-W{week:02d}-1", "%Y-W%W-%w").date()
    last_day = first_day + timedelta(days=6)
    return first_day, last_day


def get_month_dates(year: int, month: int) -> Tuple[date, date]:
    """Get start and end dates for a given month"""
    first_day = date(year, month, 1)
    # Getting last day by getting first day of next month and subtracting one day
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    return first_day, last_day
