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
