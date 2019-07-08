import os
from twilio.rest import Client


account_sid = "ACe4ea74609a33afa972388c4a33cc453d"
auth_token = "7de09367ad23e02e78d243126318ac34"

client = Client(account_sid, auth_token)

call = client.calls.create(
    to= "+84868189506",
    from_="+84868189506",
    url="http://demo.twilio.com/docs/voice.xml"

)
print (call.sid)