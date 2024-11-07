from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Any
import json
import time
import asyncio
app = FastAPI()

# Dictionary to store WebSocket connections for each user
connections: Dict[str, WebSocket] = {}
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Any
import json

app = FastAPI()

# Dictionary to store WebSocket connections for each user
connections: Dict[str, WebSocket] = {}

# WebSocket Endpoint for user connection
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connections[user_id] = websocket
    print(f"User {user_id} connected")

    try:
        while True:  # Keep the connection open to receive multiple messages
            message_json = await websocket.receive_text()  # Wait for a message from the client
            await asyncio.sleep(10)  # Non-blocking sleep
            data = json.loads(message_json)  # Parse the JSON message
            print(f"Received from {user_id}: {data}")  # Log the received message

    except WebSocketDisconnect:
        del connections[user_id]  # Remove the connection from the dictionary
        print(f"User {user_id} disconnected")



# Endpoint to send a message to a specific user
@app.post("/send_message/{user_id}")
async def send_message(user_id: str, message: Dict[str, Any]):
    if user_id in connections:
        websocket = connections[user_id]
        await websocket.send_text(json.dumps(message))  # Send message as JSON
        return {"status": "success", "msg": f"Message sent to {user_id}"}
    else:
        return {"status": "error", "msg": f"User {user_id} not connected"}

# Endpoint to broadcast a message to all users
@app.post("/broadcast_message/")
async def broadcast_message(message: Dict[str, Any]):
    for user_id, websocket in connections.items():
        await websocket.send_text(json.dumps(message))  # Send message as JSON
    return {"status": "success", "msg": "Message broadcasted to all users"}
