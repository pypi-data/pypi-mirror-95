# Slackertpy

A simple way to create and send Slack messages through a webhook.

Especially useful for logging and alerting, supports three logging levels `Error, Info, Debug` and templates to simplify sending the same layout message with different content.

This is a port from a Ruby library [Slackert](https://github.com/braze-inc/braze-growth-shares-slackert). Follow Slackert's documnetation for in depth description of classes and methods.

## Installation

Install using pip

    pip install slackertpy

## Usage

Slackert sends message through an incoming webhook.

Initialize alerr client that will handle sending out your messages

    from slackertpy import Alerter
    alerter = Alerter('your-webhook-url)

Create a message with templates

    from slackertpy import templates
    simple_message = templates.notification(
        text="Hello from Slackert!"
    )

Send it on its way with alerter

    alerter.info(simple_message)

You can use richer templates or compose messages from scratch using `MessageBuilder`. Consult the documentation for more information.

    alert = templates.notification(text='Incoming debug info!', title='Silly Little Job')
    alerter.debug(alert)


    alert = templates.job_executed(
        title='Process ABC',
        result='Success',
        overview={
            'Start Time': process_start_time,
            'Server Location': 'US'
        },
        stats={
            'Records': 12345,
            'Retries': 3
        }
    )
    alerter.info(alert)

Tag users to notify them an exception was raised

    error_alert = templates.job_error(
        title='Process ABC',
        error=error_output,
        notify_user_ids=['MemberID1', 'MemberID2'],
        extra={
            'Retries': num_retries
        }
    )
