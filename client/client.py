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
print(f"Current status:")
print({json.dumps(result)})

while len(result['data']) > 0:
    result = json.loads(ws.recv())
    print(result)

print("Closing connection")
ws.close()
