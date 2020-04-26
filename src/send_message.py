import json
import os

import requests


def post_public_message_to_slack(send_message, slack_channel_name):
    slack_bot_token = "Bearer {0}".format(os.environ['SLACK_BOT_USER_ACCESS_TOKEN'])
    slack_oauth_token = os.environ["SLACK_OAUTH_ACCESS_TOKEN"]

    slack_api_url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": slack_bot_token
    }
    data = {
        "token": slack_oauth_token,
        "channel": slack_channel_name,
        "text": send_message
    }
    try:
        response = requests.post(slack_api_url, data=json.dumps(data).encode("utf-8"), headers=headers)
        if response.status_code != requests.codes.ok:
            return False
    except Exception as e:
        print(e)
        return False
    return True


def post_private_message_to_slack(send_message, slack_channel_name, dist_user_id):
    slack_bot_token = "Bearer {0}".format(os.environ['SLACK_BOT_USER_ACCESS_TOKEN'])
    slack_oauth_token = os.environ["SLACK_OAUTH_ACCESS_TOKEN"]

    slack_api_url = "https://slack.com/api/chat.postEphemeral"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": slack_bot_token
    }
    data = {
        "token": slack_oauth_token,
        "channel": slack_channel_name,
        "text": send_message,
        "user": dist_user_id
    }
    try:
        response = requests.post(slack_api_url, data=json.dumps(data).encode("utf-8"), headers=headers)
        if response.status_code != requests.codes.ok:
            return False
    except Exception as e:
        print(e)
        return False
    return True
