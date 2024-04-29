# WebSocketChat

Need to:

```
add virtialenv and activate

pip install -r requirements.txt

./manage.py migrate

./manage.py createsuperuser
(add user data for next stages)
```

* add superuser again

and you can check all with postman or alternative

Login URL: 
* {{base_url}}/api/user/login

Socket: 
* ws://{{base_url}}/ws/chat
(need to add 'token' to headers)

connect two users to ws

then you can send data from first user: 
```
{
    "action": "chat.send_message",
    "data": {
        "receiver_id": receiver_id,
        "text": "message text"
    }
}
```

- receiver_id which is you created second user for chech websocket, it must be connected socket to receive live data



# extra:

you can see chats list with http(rest API):
{{base_url}}/api/chat/chat/

and you can see messages list of a chat:
{{base_url}}/api/chat/chat/22/messages

must to required add Bearer Token which is you get from login API(only access token) to these two request

***used Simple JWT for auth***
