import boto3
from boto3.dynamodb.conditions import Key

from .utils import get_ref_timestamp


def load_send_nas_num(user_id):
    ref_timestamp = get_ref_timestamp()
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
