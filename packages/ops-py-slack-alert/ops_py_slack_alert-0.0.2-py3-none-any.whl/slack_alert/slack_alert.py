#!/usr/bin/env python

import os
import requests
import logging
import json


###############################################################################


class SlackAlert(object):
    """
    Post a message to Slack using webhook.

    ...

    Attributes
    ----------
    webhook : str
        Where the payload will be posted
    payload : dict
        The payload which will be posted

    Methods
    -------
    set_payload()
        Combine heading and message to a dict
    post_payload()
        Post the payload as json to webhook
    """

    def __init__(self, webhook: str):
        """
        Parameters
        ----------
        webhook : str
            Where the payload will be posted
        """

        self.webhook = webhook
        self.payload = {}

    def set_payload(self, **kwargs: str):
        """Create a payload of the heading and the message

        Parameters
        ----------
        kwargs : dict
            key-value pairs which will be the payload
        """

        self.payload = {}

        # Parse through every provided key-value pair and add to payload
        # Also ensure the value is converted to string before added to payload
        for k, v in kwargs.items():
            self.payload[k] = str(v).rstrip("\n")

    def post_payload(self):
        """Post the payload to the webhook

        The payload must be structured as you have designed for the specific Slack Workflow in
        Slack Workflow Builder.

        Or like data payload is handled by your app: {"text":"Hello, World!"}
        More info: https://api.slack.com/messaging
        """

        if not self.webhook:
            logging.error("No webhook specified.")
            return

        if not self.payload:
            error_msg = "Payload not set"
            logging.error(error_msg)
            raise ValueError(error_msg)

        response = requests.post(
            self.webhook, data=json.dumps(self.payload),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            error_msg = f"Response status code: {response.status_code}. - Response text: {response.text}"
            logging.error(error_msg)
            raise ValueError(response.status_code, response.text)
        else:
            logging.info(f"{response.status_code} - slack message sent.")


###############################################################################


if __name__ == '__main__':
    WEBHOOK = os.getenv("WEBHOOK")
    heading = "This is the heading"
    message = "This is the message"
    sa = SlackAlert(WEBHOOK)
    sa.set_payload(heading=heading, msg=message)
    sa.post_payload()
