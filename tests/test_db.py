# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from decimal import Decimal

from src.db import create_nas_record, load_send_nas_num
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
