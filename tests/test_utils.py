# -*- coding: utf-8 -*-
import time
from datetime import datetime
from decimal import Decimal
import json

from src.utils import get_last_week_ref_timestamp, get_ref_timestamp,\
    calc_nas_ranking_this_week, bring_slack_id_from_slack_name, bring_slack_name_from_slack_id


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


def test_calc_nas_ranking_this_week(nas_db):
    """Create a NAS ranking from a NAS record
    Get the ranking of those who received NAS from NAS records scanned from dynamo db.
    scan_nas_records() is used for the scan of dynamo db.

    Returns:
        dict : nas ranking data
    """

    estimate_nas_ranking = {}
    assert calc_nas_ranking_this_week() == {}

    for i in range(3):
        now = datetime.now()
        nas = {
            'tip_user_id': 'test_user_A_id',
            'time_stamp': Decimal(now.timestamp()),
            'receive_user_id': 'test_user_B_id',
            'receive_user_name': 'test_user_B_name',
            'tip_type': 'stamp',
            'tip_user_name': 'test_user_A_name',
            'team_id': 'test_team_id'
        }
        nas_db.put_item(Item=nas)
    estimate_nas_ranking = {
        'test_user_B_name': 3
    }
    assert calc_nas_ranking_this_week() == estimate_nas_ranking

    for i in range(2):
        now = datetime.now()
        nas = {
            'tip_user_id': 'test_user_A_id',
            'time_stamp': Decimal(now.timestamp()),
            'receive_user_id': 'test_user_C_id',
            'receive_user_name': 'test_user_C_name',
            'tip_type': 'stamp',
            'tip_user_name': 'test_user_A_name',
            'team_id': 'test_team_id'
        }
        nas_db.put_item(Item=nas)
    estimate_nas_ranking = {
        'test_user_B_name': 3,
        'test_user_C_name': 2
    }
    assert calc_nas_ranking_this_week() == estimate_nas_ranking


def test_bring_slack_id_from_slack_name(mocker):
    """Get the slack_user_name from the slack_user_id
    There are cases in which it is not possible to get enough information about the destination party, etc., in running the NAS.
    In that case, use the slack api to get the user_name directly from the group's user list.

    Return:
        str: slack user name
    """
    # Create fake response
    responseMock = mocker.Mock()
    responseMock.status_code = 200
    responseMock.text = json.dumps({'test_user_B_id': 'test_user_B_name'})

    mocker.patch('requests.get').return_value = responseMock
    assert bring_slack_id_from_slack_name('test_user_Z_id') == ''


def test_bring_slack_name_from_slack_id(mocker):
    """Get the slack_user_id from the slack_user_name
    There are cases in which it is not possible to get enough information about the destination party, etc., in running the NAS.
    In that case, use the slack api to get the user_id directly from the group's user list.

    Return:
        str: slack user name
    """
    # Create fake response
    responseMock = mocker.Mock()
    responseMock.status_code = 200
    responseMock.text = json.dumps({'test_user_B_id': 'test_user_B_name'})

    mocker.patch('requests.get').return_value = responseMock
    assert bring_slack_name_from_slack_id('test_user_Z_id') == ''
