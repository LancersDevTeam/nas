# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from decimal import Decimal

from src.db import create_nas_record, load_send_nas_num, scan_nas_records, create_nas_gacha_record, load_latest_nas_gacha_record
from src.utils import get_ref_timestamp

sys.path.append('../')


def test_load_send_nas_num(nas_db):
    """Retrieve the NAS records of the week created by the target user
    The NAS uses a week as a basic unit.
    The NAS, which can be sent every week, is reset and a ranking for the week is created.
    The user_id is created based on the slack's user_id.

    Args:
        user_id : slack user_id
        ref_timestamp : Criteria for obtaining a timestamp greater than this

    Returns:
        int : target user sended nas in this week
    """

    now = datetime.now()

    nas = {
        'tip_user_id': 'test_user_A',
        'time_stamp': Decimal(now.timestamp()),
        'receive_user_id': 'test_user_B',
        'receive_user_name': 'test_user_B',
        'tip_type': 'stamp',
        'tip_user_name': 'test_user_A',
        'team_id': 'test_team'
    }
    nas_db.put_item(Item=nas)
    ref_timestamp = get_ref_timestamp()

    assert load_send_nas_num('test_user_A', ref_timestamp) == 1
    assert load_send_nas_num('test_user_B', ref_timestamp) == 0


def test_scan_nas_records(nas_db):
    """Use SCAN to retrieve all NAS records created prior to the specified period.
    The query function can only get the hash key and the set, so we use scan.
    In addition, as a characteristic of scanning dynamo db,
    the upper limit of one acquisition is 1MB.
    For this reason, it is not possible to obtain all the data in just one acquisition.
    Therefore, the process is such that it starts the next acquisition from
    the last key acquired last time and does not finish until all the keys have been acquired.

    Args:
        ref_timestamp : Criteria for obtaining a timestamp greater than this

    Return:
        list : nas record list
    """
    now = datetime.now()

    nas = {
        'tip_user_id': 'test_user_A',
        'time_stamp': Decimal(now.timestamp()),
        'receive_user_id': 'test_user_B',
        'receive_user_name': 'test_user_B',
        'tip_type': 'stamp',
        'tip_user_name': 'test_user_A',
        'team_id': 'test_team'
    }
    nas_db.put_item(Item=nas)
    ref_timestamp = get_ref_timestamp()

    assert scan_nas_records(ref_timestamp)[0] == nas


def test_create_nas_record(nas_db):
    """Create a new NAS record
    When a user grants a NAS, a new record is added to the Dynamo DB.
    A record is written with information about both the user who sent it and the user who was sent it.
    It also measures how that NAS was added in the way it was. (ex, message, stamp)

    Args:
        nas_user_id: slack user id
        nas_user_name: slack user name
        receive_user_id: slack user id
        receive_user_name: slack user name
        nas_type: sended nas type. message or stamp
        team_id: slack team id
    """

    assert create_nas_record('test_user_A_id', 'test_user_A_name', 'test_user_B_id', 'test_user_B_name', 'stamp', 'test_team_id')

    ref_timestamp = get_ref_timestamp()
    assert load_send_nas_num('test_user_A_id', ref_timestamp) == 1

    assert load_send_nas_num('test_user_B_id', ref_timestamp) == 0


def test_load_latest_nas_gacha_record(nas_gacha_db):
    """Retrieve the latest record of the target user.
    The user record in nas_gacha is the most recent record representing the most recent state.
    Along with that, when creating a new record or wanting to know the status of the user,
    it is necessary to get the latest record.
    This function does not return the contents of the record, but gets all the latest records.

    Args:
        gacha_user_id : The id of the user who wants to retrieve the latest record.

    Return:
        dict : latest record.
    """

    assert load_latest_nas_gacha_record('test_user_A_id') == {}

    now = datetime.now()
    create_nas_gacha_record('test_user_A_id', Decimal(now.timestamp()), 10, 0, {})
    nas_gacha_record = {
        'user_id': 'test_user_A_id',
        'time_stamp': Decimal(now.timestamp()),
        'has_nas_num': 10,
        'used_nas_num': 0,
        'has_tickets': {}
    }
    assert load_latest_nas_gacha_record('test_user_A_id') == nas_gacha_record

    now = datetime.now()
    create_nas_gacha_record('test_user_A_id', Decimal(now.timestamp()), 0, 10, {})
    nas_gacha_record = {
        'user_id': 'test_user_A_id',
        'time_stamp': Decimal(now.timestamp()),
        'has_nas_num': 0,
        'used_nas_num': 10,
        'has_tickets': {}
    }
    assert load_latest_nas_gacha_record('test_user_A_id') == nas_gacha_record


def test_create_nas_gacha_record(nas_gacha_db):
    """Create a nas_gacha record
    The ability to turn the Gacha using the NAS you received.
    A record is created each time, and the latest record of the target user indicates the current status.
    Using a dynamo db called NAS_GACHA, which is separate from NAS.
    Each gacha prize is saved in dictionary format.

    Args:
        gacha_user_id: executed nas gacha user id
        time_stamp: the record created time stamp.
        has_nas_num: Total value of the NAS we received.
        used_nas_num: Already used nas for gacha.
        has_tickets: The list of freebies that the user has at that time.
    """
    now = datetime.now()
    assert create_nas_gacha_record('test_user_A_id', Decimal(now.timestamp()), 10, 0, {}) is True
