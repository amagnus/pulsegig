from twilio.rest import TwilioRestClient
from django.conf import settings


twilio_account = settings.TWILIO_ACCOUNT
twilio_token = settings.TWILIO_TOKEN


def send_text(twilio_to, msg):
    TwilioRestClient(twilio_account, twilio_token).sms.messages.create(
        to = twilio_to,
        from_ = '15103799849',
        body = msg
    )
