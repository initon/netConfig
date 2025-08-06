import asyncio
import json

import requests
from nio import AsyncClient, LoginResponse


class MatrixBot:

    def __init__(self, matrix_server: str, username: str, password: str, room: str):
        self.matrix_server = matrix_server
        self.username = username
        self.password = password
        self.room = room
        self.token = None
        self.initialize_bot()

    def initialize_bot(self):
        try:
            self.token = MatrixBot.load_token()
        except FileNotFoundError:
            self.token = self.login()
            self.save_token()

    # Функция для входа и получения токена
    def login(self):
        response = requests.post('https://matrix.ru/_matrix/client/r0/login', json={
            'type': 'm.login.password',
            'user': self.username,
            'password': self.password,
        })
        self.token = response.json().get('access_token')
        return self.token

    # Функция для сохранения токена в файл
    def save_token(self):
        with open('token.json', 'w') as f:
            json.dump({'access_token': self.token}, f)

    @staticmethod
    def load_token():
        with open('token.json', 'r') as f:
            return json.load(f)['access_token']

    # Функция для отправки сообщения
    def send_message_with_code(self, messages):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }
        for message in messages:
            data = {
                'msgtype': 'm.text',
                "format": "org.matrix.custom.html",
                'body': message,
                'formatted_body': message
            }
            response = requests.post(f'https://matrix.ru/_matrix/client/r0/rooms/{self.room}/send/m.room.message',
                                     headers=headers, json=data)

            if response.status_code == 200:
                print("Сообщение отправлено успешно!")
            else:
                print("Ошибка при отправке сообщения:", response.json())

    @staticmethod
    def get_formatted_message_diff(message, code):
        formatted_message = f"{message}<br><br> <code> {code}</code>"
        return formatted_message

