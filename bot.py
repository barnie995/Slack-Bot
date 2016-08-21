import os
import time
from slackclient import SlackClient



BOT_ID = "INSERT ME HERE"

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "greet"

def greet():
    return """

		Hello and welcome to SecTalks.	 
        Join your local chapters by clicking on these links:
        #sectalks_bne , #sectalks_syd , #sectalks_perth , #sectalks_mel , #sectalks_cbr , #sectalks_adl and #sectalks_lon (London)

        Alternative try #newbiecorner if you are new as well. Feel free to browse the other channels and join em at your lesuire. 
        We are a nice and friendly bunch.  Except @bull .  He bites.  :smile: """


slack_client = SlackClient('INSERT ME HERE')


def handle_command(command, channel):

    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = greet()

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("GreetingsBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("YOU DUN FUCKED UP WITH THE BOT API KEY OR SOMETHINGS")


