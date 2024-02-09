# home/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import base64
import numpy as np
import cv2
import face_recognition
import pickle


class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if text_data == 'PING':
            # print("hello world")
            await self.send('PONG')
        if bytes_data:
            import face_recognition

            # Convert bytes data to numpy array
            name_of_students = ['Jatin', 'Tatin', 'Arryuann']
            nparr = np.frombuffer(bytes_data, np.uint8)
            # Decode image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            with open('EncodeFile.p', 'rb') as file:
                encodeList = pickle.load(file)
            encodelistknown, student_id = encodeList

            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Detect faces and their encodings in the current frame
            face_positions = face_recognition.face_locations(imgS)
            encoding_frame = face_recognition.face_encodings(imgS, face_positions)

            for encface, facepos in zip(encoding_frame, face_positions):
                matches = face_recognition.compare_faces(encodelistknown, encface)
                face_dist = face_recognition.face_distance(encodelistknown, encface)
                best_match_index = np.argmin(face_dist)

            print(name_of_students[best_match_index])
            # Here, you can process the image with face_recognition
            # For simplicity, this example will just echo back the received image
            # Convert the image back to bytes and send it back
            _, img_encoded = cv2.imencode('.jpg', img)
            # print(img)
            # print("hello world")
            await self.send(bytes_data=img_encoded.tobytes())
