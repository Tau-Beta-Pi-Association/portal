import os
from twilio.rest import Client

account_sid = 'AC1f6967d88bca8a29969f84f3c50f3c04'
auth_token = 'da01d37131bfc676b79585292edbc93a'
client = Client(account_sid, auth_token)

def send_sms(user_code, phone_number):
    message = client.messages.create(
        body=f'Hi! Your verification code is {user_code}',
        from_='+18559343310',
        to=f'{phone_number}'
    )
    print(message.sid)