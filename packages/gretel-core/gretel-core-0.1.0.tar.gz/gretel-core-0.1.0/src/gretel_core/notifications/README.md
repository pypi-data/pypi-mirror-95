# Gretel Notifications

The `gretel_core.notifications` library is a lightweight, opinionated library for creating generally formatted messages and sending them to providers.  There are two components of the library:

- `BaseMessage` sub-classes
- `Provider` sub-classes

These two can be used to constract and craft messages. Built-in providers have default message parsing rules to create pre-formatted messages for you.

Sending a Slack message:

```python
from gretel_core.notifications import DefaultMessage, SlackProvider, ProviderError, MessageError

slack = SlackProvider("https://hooks.slack.com/...")

try:
    msg = DefaultMessage(
        title="Test Message",
        body={"Message": "This is a message"},
        footer={"Trace-ID": 86753098}
    )
except MessageError as err:
    print(str(err))

try:
    slack.notify(msg)
except ProviderError as err:
    print(str(err))
```

## Built In Messages

```python
msg = DefaultMessage("...")
```

## Providers

All providers should have a `notify()` method. By default, the method should have
opinionated handling for all messages that inherit from the ``BaseMessage`` type.

### Slack

Uses Slack App webhooks:

```python
slack = SlackProvider("https://hooks.slack.com/...")
```