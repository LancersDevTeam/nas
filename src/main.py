# coding: utf-8
import threading

import requests


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
    # write a handler for each process below.
    return requests.codes.ok
