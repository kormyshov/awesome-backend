import os
import hmac
import hashlib


class Config:
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    SECRET_KEY = hmac.new('WebAppData'.encode(), BOT_TOKEN.encode(), hashlib.sha256).digest()

    USER_STORAGE_URL = os.environ.get('USER_STORAGE_URL')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
