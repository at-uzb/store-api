import requests
from django.conf import settings
from django.core.cache import cache

TOKEN_CACHE_KEY = "eskiz_token"
TOKEN_TIMEOUT = settings.ESKIZ_TOKEN_LIFETIME

class EskizClient:
    LOGIN_URL = "https://notify.eskiz.uz/api/auth/login"
    SEND_SMS_URL = "https://notify.eskiz.uz/api/message/sms/send"
    
    def __init__(self):
        self.email = settings.ESKIZ_EMAIL
        self.password = settings.ESKIZ_PASSWORD
        self.token = self.get_token()
    
    def login(self):
        response = requests.post(self.LOGIN_URL, data={
            "email": self.email,
            "password": self.password
        })

        if response.status_code == 200:
            token = response.json()["data"]["token"]
            cache.set(TOKEN_CACHE_KEY, token, timeout=TOKEN_TIMEOUT)
            return token
        else:
            raise Exception("Eskiz login failed: " + response.text)
    
    def get_token(self):
        token = cache.get(TOKEN_CACHE_KEY)
        if token:
            return token
        return self.login()
    
    def is_valid_uz_phone(self, phone):
        return phone.startswith('+998') and len(phone) == 13

    def send_sms(self, phone, message):
        if not self.is_valid_uz_phone(phone):
            raise ValueError("Invalid Uzbek phone number")

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        payload = {
            "mobile_phone": phone[1:],
            "message": "Bu Eskiz dan test",
            "from": "Store Project",  
            "callback_url": "http://store.uz/callback"
        }

        response = requests.post(self.SEND_SMS_URL, headers=headers, data=payload)

        if response.status_code == 401:
            self.token = self.login()
            headers["Authorization"] = f"Bearer {self.token}"
            response = requests.post(self.SEND_SMS_URL, headers=headers, data=payload)

        return response.json()
