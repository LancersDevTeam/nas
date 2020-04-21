import sys

import requests

from src.main import main_func, return_200

sys.path.append('../')


def test_return_200():
    """
    If the response is slow, Slack will throw an error, so return 200 codes instantly.
    Slack will spit out an error if you don't return a response within 3 seconds.
    It takes more than 3 seconds to process the database.
    For this reason, I try to return 200 responses immediately.

    Returns:
        int : 200
    """

    assert return_200() == 200


def test_main_func():
    """Methods to be executed directly by lambda.
    Parsing the request sent from the slack and controlling the processing by it.

    command list
    - nas st : Check the number of nas you have
    - nas message : Sending a NAS with a message
    - nas stamp : Sending a NAS using a stamp
    - nas rank : Get the number of rankings received for the week
    - nas gacha : You can use your own nas to play gacha

    Args:
        event: passed from the lambda function. containing the contents of the request.
        content: passed from the lambda function. maybe didn't use this.

    Returns:
        int : Return the exit code.

    Note:
        If the response is slow, multiple requests are sent by Slack.
        In some cases, this causes the process to be executed many times.
        To prevent that, I try to look at the request first and eliminate the redirection process.
    """

    event = {'params': {'header': ''}}
    content = {}
    assert main_func(event, content) == requests.codes.ok

    event = {'params': {'header': 'X-Slack-Retry-Num'}}
    content = {}
    assert main_func(event, content) == 204
