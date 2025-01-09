import os
import hmac
import hashlib


class Config:
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    SECRET_KEY = hmac.new('WebAppData'.encode(), BOT_TOKEN.encode(), hashlib.sha256).digest()
