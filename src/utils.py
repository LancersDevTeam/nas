from datetime import datetime, timedelta
from decimal import Decimal
from .db import scan_nas_records
from collections import Counter

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


def calc_nas_ranking_this_week():
    ref_timestamp = get_ref_timestamp()
    nas_records = scan_nas_records(ref_timestamp)

    if nas_records == []:
        return {}

    receive_user_list = []
    for item in nas_records:
        receive_user_list.append(item['receive_user_name'])

    ranking_source = Counter(receive_user_list)
    receive_users, nas_counts = zip(*ranking_source.most_common())
    return dict(zip(receive_users, nas_counts))
