# -*- coding: utf-8 -*-
import sys

from src.send_message import post_public_message_to_slack, post_private_message_to_slack

sys.path.append('../')


def test_post_public_message_to_slack(mocker):
    """Sending a public message to a specific channel in Slack
    You can send a message to the specified Slack channel.
    You need a slack token to send it. These settings should be done in advance.
    If you want to have a canary environment in addition to the production environment,
    you can prepare another room for testing and do a transmission test.

    Args:
        send_message: slack send message
        slack_channel_name: send message distination channel name

    Return:
        bool: send success is True. send failer is False.
    """

    # Create fake response
    responseMock = mocker.Mock()
    responseMock.status_code = 200
    responseMock.text = 'success'

    mocker.patch('requests.post').return_value = responseMock
    assert post_public_message_to_slack('sample_massage!', 'sample_channel') is True


def test_post_private_message_to_slack(mocker):
    """Sending a private message to a specific channel in Slack
    Send a private message that only the target user can see.
    You need a slack token to send it. These settings should be done in advance.
    If you want to have a canary environment in addition to the production environment,
    you can prepare another room for testing and do a transmission test.

    Args:
        send_message: slack send message
        slack_channel_name: send message distination channel name
        distdist_user_id_user: destination user id

    Return:
        bool: send success is True. send failer is False.
    """
    # Create fake response
    responseMock = mocker.Mock()
    responseMock.status_code = 200
    responseMock.text = 'success'

    mocker.patch('requests.post').return_value = responseMock
    assert post_private_message_to_slack('sample_massage!', 'sample_channel', 'test_user_A_id') is True

    responseMock.status_code = 404
    responseMock.text = 'error'

    mocker.patch('requests.post').return_value = responseMock
    assert post_private_message_to_slack('sample_massage!', 'sample_channel', 'test_user_A_id') is False
