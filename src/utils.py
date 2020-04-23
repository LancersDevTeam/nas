from datetime import datetime, timedelta
from decimal import Decimal

import pytz


def get_ref_timestamp():
    timezone = pytz.timezone('Asia/Tokyo')
    now = datetime.now(tz=timezone)

    diff_from_ref_day = timedelta(days=now.weekday())
    format_ref_date = datetime(now.year, now.month, now.day, 0, 0, 0)

    ref_timestamp = format_ref_date - diff_from_ref_day
    return Decimal(ref_timestamp.timestamp())


def get_last_week_ref_timestamp():
    timezone = pytz.timezone('Asia/Tokyo')
    now = datetime.now(tz=timezone)
    diff_from_ref_day_plus_a_week = timedelta(days=now.weekday()+7)

    format_ref_date = datetime(now.year, now.month, now.day, 0, 0, 0)
    ref_timestamp_past_a_week = format_ref_date - diff_from_ref_day_plus_a_week
    return Decimal(ref_timestamp_past_a_week.timestamp())
