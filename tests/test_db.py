# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal

import boto3
from moto import mock_dynamodb2

from src.db import load_send_nas_num

sys.path.append('../')


@mock_dynamodb2
def test_load_send_nas_num():
    """Retrieve the NAS records of the week created by the target user
    The NAS uses a week as a basic unit.
    The NAS, which can be sent every week, is reset and a ranking for the week is created.
    The user_id is created based on the slack's user_id.

    Args:
        user_id : slack user_id

    Returns:
        int : target user sended nas in this week
    """

    os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-1'
    dynamoDB = boto3.resource('dynamodb')
    dynamoDB.create_table(
        TableName='NAS',
        AttributeDefinitions=[
            {
                'AttributeName': 'tip_user_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'time_stamp',
                'AttributeType': 'N'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'tip_user_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'time_stamp',
                'KeyType': 'RANGE'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 15,
            'WriteCapacityUnits': 5,
        }
    )
    nas_table = dynamoDB.Table('NAS')

    # create sample timestamp
    now = datetime.now()
    format_ref_date = datetime(now.year, now.month, now.day, 0, 0, 0)
    add_one_day = timedelta(days=1)
    test_time_stamp = format_ref_date + add_one_day

    nas = {
        'tip_user_id': 'test_user_A',
        'time_stamp': Decimal(test_time_stamp.timestamp()),
        'receive_user_id': 'test_user_B',
        'receive_user_name': 'test_user_B',
        'tip_type': 'stamp',
        'tip_user_name': 'test_user_A',
        'team_id': 'test_team'
    }
    nas_table.put_item(Item=nas)

    assert load_send_nas_num('test_user_A') == 1
    assert load_send_nas_num('test_user_B') == 0
