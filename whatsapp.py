from twilio.rest import Client

account_sid = 'AC124ddf4971a179a0c4e50d5c4a688d3f'
auth_token = 'dda019f4401cc9a7cff933d0c798bc55'
client = Client(account_sid, auth_token)
whatsappmsg = "sahan chathura perera"
message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=whatsappmsg,
    to='whatsapp:+94713730870'
)

print(message.sid)