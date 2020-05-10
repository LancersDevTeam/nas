import os
from datetime import datetime, timedelta
from decimal import Decimal
from db import scan_nas_records
from collections import Counter
import requests

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


def parse_lambda_event_str(lambda_event_obj):
    content_body = lambda_event_obj['body'].split('&')
    parsed_dict = {}
    for param in content_body:
        content_separate_index = param.find('=')
        content_key = param[:content_separate_index]
        content_value = param[content_separate_index+1:]
        parsed_dict[content_key] = content_value
    return parsed_dict


def bring_slack_id_from_slack_name(user_name):
    try:
        slack_api_url = "https://slack.com/api/users.list"
        slack_oauth_token = os.environ["SLACK_OAUTH_ACCESS_TOKEN"]

        params = {'token': slack_oauth_token}
        user_list = requests.get(slack_api_url, params=params).json()

        for user in user_list["members"]:
            if user_name == user["name"]:
                user_id = user['id']
                break
        return user_id
    except Exception as e:
        print(e)
        return ''


def bring_slack_name_from_slack_id(user_id):
    try:
        slack_api_url = "https://slack.com/api/users.list"
        slack_oauth_token = os.environ["SLACK_OAUTH_ACCESS_TOKEN"]

        params = {'token': slack_oauth_token}
        user_list = requests.get(slack_api_url, params=params).json()

        for user in user_list["members"]:
            if user_id == user['id']:
                user_name = user['name']
                break
        return user_name
    except Exception as e:
        print(e)
        return ''
