# ops-py-slack-alert

---

## Description
Post a message to a Slack webhook.

Note: In the example code below a Slack Automation Worklow has already been built. The message part of the Slack Workflow has been defined to receive a `header` and a `msg` variable.

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
sa = SlackAlert(WEBHOOK)
sa.set_payload(heading=heading, msg=message)
sa.post_payload()
response_code = sa.get_response_code()
print(response_code)
```
