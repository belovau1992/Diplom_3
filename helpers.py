import json
import requests
from data import TestData


class Helpers:
    @staticmethod
    def register_new_user():
        payload = {
            "email": TestData.VALID_EMAIL,
            "password": TestData.VALID_PASSWORD,
            "name": TestData.NEW_USER_NAME
        }
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/register", data=payload)
        return response.json()

    @staticmethod
    def delete_user(access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        requests.delete("https://stellarburgers.nomoreparties.site/api/auth/user", headers=headers)