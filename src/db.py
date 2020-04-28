from datetime import datetime
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key


def load_send_nas_num(user_id, ref_timestamp):
    try:
        dynamoDB = boto3.resource('dynamodb')
        table = dynamoDB.Table('NAS')

        send_nas_data_this_week = table.query(
            KeyConditionExpression=Key('tip_user_id').eq(user_id) & Key('time_stamp').gt(ref_timestamp)
        )
        send_nas_num = send_nas_data_this_week['Count']
        return send_nas_num
    except Exception as e:
        print(e)
        return 0


def scan_nas_records(ref_timestamp):
    try:
        dynamoDB = boto3.resource('dynamodb')
        table = dynamoDB.Table('NAS')

        response = table.scan(
            FilterExpression=Key('time_stamp').gt(ref_timestamp)
        )
        nas_records = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(
                FilterExpression=Key('time_stamp').gt(ref_timestamp),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            nas_records.extend(response['Items'])
        return nas_records
    except Exception as e:
        print(e)
        return []


def create_nas_record(nas_user_id, nas_user_name, receive_user_id, receive_user_name, nas_type, team_id):
    try:
        dynamoDB = boto3.resource('dynamodb')
        nas_table = dynamoDB.Table('NAS')

        nas_table.put_item(
            Item={
                'tip_user_id': nas_user_id,
                'time_stamp': Decimal(datetime.now().timestamp()),
                'tip_user_name': nas_user_name,
                'receive_user_id': receive_user_id,
                'receive_user_name': receive_user_name,
                'tip_type': nas_type,
                'team_id': team_id
            }
        )
        return True
    except Exception as e:
        print(e)
        return False


def create_nas_gacha_record(gacha_user_id, time_stamp, has_nas_num, used_nas_num, has_tickets):
    try:
        dynamoDB = boto3.resource('dynamodb')
        nas_gacha_table = dynamoDB.Table('NAS_GACHA')

        nas_gacha_table.put_item(
            Item={
                'user_id': gacha_user_id,
                'time_stamp': time_stamp,
                'has_nas_num': has_nas_num,
                'used_nas_num': used_nas_num,
                'has_tickets': has_tickets
            }
        )
        return True
    except Exception as e:
        print(e)
        return False
