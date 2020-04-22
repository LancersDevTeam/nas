# -*- coding: utf-8 -*-
import sys
import time

from src.utils import get_last_week_ref_timestamp, get_ref_timestamp

sys.path.append('../')


def test_get_ref_timestamp():
    """Get a time stamp at the start of the week
    The week starts at midnight on Monday, Japan time.
    Use this function to get a timestamp that is the starting point for the week.
    This function is converted to Decimal at the end to store the value in Dynamo DB,
    which uniquely recognizes nas by the combination of user ID and timestamp.

    In the test case, the function is used to get a reference timestamp and check if it matches.

    Returns:
        Decimal : ref timestamp
    """

    ref_timestamp_1 = get_ref_timestamp()
    time.sleep(1)
    ref_timestamp_2 = get_ref_timestamp()
    assert ref_timestamp_1 == ref_timestamp_2


def test_get_last_week_ref_timestamp():
    """Get last week's reference time stamp
    A basic feature of NAS is the BONUS feature, which increases the number of NAS
    you can send in a week according to the number of NAS you sent last week.
    To calculate that, I created a function to get a reference timestamp for the last week

    In the test case, the function is used to get a reference timestamp and check if it matches.

    Returns:
        Decimal : ref timestamp
    """

    ref_timestamp_1 = get_last_week_ref_timestamp()
    time.sleep(1)
    ref_timestamp_2 = get_last_week_ref_timestamp()
    assert ref_timestamp_1 == ref_timestamp_2
