import json

from websocket import create_connection

ws = create_connection(
    "ws://localhost:8000/wc/stone_activation_status/",
    headers={
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk4OTMxODcxLCJpYXQiOjE2OTg4NDU0NzEsImp0aSI6IjAxNDI0ZDgyOTE2YzQwNTg5MTZlZWZlYTBhOTFiMmEyIiwidXNlcl9pZCI6MX0.yAMBB03EaYkPvyKHmboyctg0WjYCvTH52gKGbYe3k78"
    }
)
print("Checking status'...")
ws.send('{"username": "john"}')
print("Sent")
print("Receiving...")

result = json.loads(ws.recv())

while len(result['data']) > 0:
    results = json.loads(ws.recv())['data']
    is_pending = False

    for res in results:
        print(res)

        if res['remaining_duration'] > 0:
            is_pending = True

    if not is_pending:
        break

    print("................................")

if len(result['data']) == 0:
    print("data: ", result['data'])

print("Closing connection")
ws.close()
