# coding: utf-8
import threading


def lambda_handler(event, content):
    main_process = threading.Thread(target=main_func(event, content))
    sub_process = threading.Thread(target=main_func(event, content))

# If the response is slow, Slack will throw an error, so return 200 codes instantly.
def return_200():
    print("return 200")
    return 200

def main_func(event, content):
    # Ignore the retry process from Slack
    if 'X-Slack-Retry-Num' in event['params']['header']:
        print("this is redirect requests!")
        return 200
    
    # write a handler for each process below.
    return 200