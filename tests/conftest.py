import os

import boto3
import pytest
from moto import mock_dynamodb2


@pytest.fixture
def nas_db():
    with mock_dynamodb2():
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

        nas_db = dynamoDB.Table('NAS')
        yield nas_db


@pytest.fixture
def nas_gacha_db():
    with mock_dynamodb2():
        os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-1'
        dynamoDB = boto3.resource('dynamodb')
        dynamoDB.create_table(
            TableName='NAS_GACHA',
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'time_stamp',
                    'AttributeType': 'N'
                }
            ],
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'time_stamp',
                    'KeyType': 'RANGE'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            }
        )

        nas_gacha_db = dynamoDB.Table('NAS_GACHA')
        yield nas_gacha_db
