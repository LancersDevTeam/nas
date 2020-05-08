# coding: utf-8
import os
import threading
import requests

from utils import parse_lambda_event_str, bring_slack_id_from_slack_name
from nas import Nas
from send_message import post_public_message_to_slack, post_private_message_to_slack

NAS_LIMIT = int(os.environ['NAS_LIMIT'])
PUBLIC_NAS_CHANNEL_ID = os.environ['PUBLIC_NAS_CHANNEL_ID']


def lambda_handler(event, content):
    threading.Thread(target=main_func(event, content))  # main process
    threading.Thread(target=main_func(event, content))  # apparent process


# If the response is slow, Slack will throw an error, so return 200 codes instantly.
def return_200():
    print("return 200")
    return requests.codes.ok


def main_func(event, content):
    # Ignore the retry process from Slack
    if 'X-Slack-Retry-Num' in event['params']['header']:
        print("this is redirect requests!")
        return 204

    content_type = type(event['body'])

    if content_type is str:
        parsed_event = parse_lambda_event_str(event)

        # setup all need informations
        nas_user_id = parsed_event['user_id']
        nas_user_name = parsed_event['user_name']
        sended_message = parsed_event['text'].split()
        receive_user_name = sended_message[0].lstrip('@')
        receive_user_id = bring_slack_id_from_slack_name(receive_user_name)
        team_id = parsed_event['team_id']
        sent_channel_id = parsed_event['channel_id']
        commend = parsed_event['command']

    if commend == '/nas':
        # check can send nas message
        nas_obj = Nas(nas_user_id, nas_user_name, team_id)
        if nas_obj.chack_self_portrait(receive_user_id) is True:
            print('self portrait')
            send_user_slack_text = '自画自賛乙'
            post_private_message_to_slack(send_user_slack_text, sent_channel_id, nas_user_id)  # for send user
            return requests.codes.ok

        if nas_obj.check_can_send_nas() is False:
            print('nas send limit')
            send_user_slack_text = '今週はもうnasを送れないよ！'
            post_private_message_to_slack(send_user_slack_text, sent_channel_id, nas_user_id)  # for send user
            return requests.codes.ok

        if receive_user_id == '':
            print('the user not exist.')
            send_user_slack_text = 'そのユーザは存在しないよ！'
            post_private_message_to_slack(send_user_slack_text, sent_channel_id, nas_user_id)  # for send user
            return requests.codes.ok

        # forming message
        message = ""
        for word in sended_message[1:]:
            message += word

        # setup slack text for send user
        sended_nas_num = nas_obj.sended_nas_num()
        remain_nas = NAS_LIMIT - sended_nas_num
        nas_bonus = nas_obj.nas_bonus()
        nas_status = nas_obj.nas_status()
        send_user_slack_text = "コマンドからnasを送れたよ!\n今週の残りnas数: {0}\n先週からのボーナス: {1}\nあなたの残りnasは{2}です.".format(remain_nas, nas_bonus, nas_status)

        # setup slack text for receive user
        receive_user_slack_text = "<@{0}> {1}さんからのメッセージです。\n {2}".format(receive_user_name, nas_user_name, message)

        # send nas message
        post_public_message_to_slack(receive_user_slack_text, PUBLIC_NAS_CHANNEL_ID)  # for receive user
        post_private_message_to_slack(send_user_slack_text, sent_channel_id, nas_user_id)  # for send user

        # create nas record
        nas_obj.nas_message(receive_user_id, receive_user_name)
        return requests.codes.ok
