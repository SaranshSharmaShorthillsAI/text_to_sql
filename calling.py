from twilio.rest import Client

# Twilio Account SID and Auth Token
account_sid = 'XXXXXXX'
auth_token = 'XXXXXX'

# Twilio phone number
twilio_phone_number = '+1-XXXXXXX'

# Recipient's phone number
recipient_phone_number = '+91-XXXXXX'

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Create TwiML for the call
twiml = f"""
<Response>
    <Say>Hello anuj, how you doing today ?</Say>
</Response>
"""

# Make a call

call = client.calls.create(
        twiml=twiml,
        to=recipient_phone_number,
        from_=twilio_phone_number
    )
print("Call SID:", call.sid)

