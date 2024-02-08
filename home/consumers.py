# home/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import base64
import numpy as np
import cv2
import face_recognition

class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Convert bytes data to numpy array
            nparr = np.frombuffer(bytes_data, np.uint8)
            # Decode image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Here, you can process the image with face_recognition
            # For simplicity, this example will just echo back the received image
            # Convert the image back to bytes and send it back
            _, img_encoded = cv2.imencode('.jpg', img)
            await self.send(bytes_data=img_encoded.tobytes())
