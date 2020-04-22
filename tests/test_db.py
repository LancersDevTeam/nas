# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime
from decimal import Decimal

import boto3
from moto import mock_dynamodb2

from src.db import load_send_nas_num
from src.utils import get_ref_timestamp

sys.path.append('../')


@mock_dynamodb2
def test_load_send_nas_num():
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

    nas = {
        'tip_user_id': 'test_user_A',
        'time_stamp': Decimal(now.timestamp()),
        'receive_user_id': 'test_user_B',
        'receive_user_name': 'test_user_B',
        'tip_type': 'stamp',
        'tip_user_name': 'test_user_A',
        'team_id': 'test_team'
    }
    nas_table.put_item(Item=nas)
    ref_timestamp = get_ref_timestamp()

    assert load_send_nas_num('test_user_A', ref_timestamp) == 1
    assert load_send_nas_num('test_user_B', ref_timestamp) == 0
