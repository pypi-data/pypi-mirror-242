# ops-py-slack-alert

---

## Description
Post a message to a Slack webhook.

Note: In the example code below a Slack Automation Worklow has already been built. The message part of the Workflow has been defined to receive a `header` and a `msg` variable.

---

## Installation
`pip install ops-py-slack-alert`

---

## Usage
Export your slack webhook:   
`export WEBHOOK="12345blablabla...."`

Example code:   
```
from slack_alert import slack_alert as sa

WEBHOOK = os.getenv("WEBHOOK")
heading = "This is the heading"
message = "This is the message"
alert = sa.SlackAlert(WEBHOOK)
alert.set_payload(heading=heading, msg=message)
alert.post_payload()
```
