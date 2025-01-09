import hmac
import hashlib
from urllib.parse import unquote
from config import Config


def validate_telegram_data(data: str) -> bool:
    sorted_params = []
    hash = ''
    auth_date = -1
    for param in sorted(unquote(data).split('&')):
        if param.startswith('hash='):
            hash = param[5:]
            continue
        if param.startswith('auth_date='):
            auth_date = int(param[10:])
        sorted_params.append(param)
    print('sorted_params:', '\n'.join(sorted_params).encode())
    if hash == '' or auth_date == -1:
        return False
    print('hmac:', hmac.new(Config.SECRET_KEY, '\n'.join(sorted_params).encode(), hashlib.sha256))
    print('hmac.hex', hmac.new(Config.SECRET_KEY, '\n'.join(sorted_params).encode(), hashlib.sha256).hexdigest())
    return hmac.new(Config.SECRET_KEY, '\n'.join(sorted_params).encode(), hashlib.sha256).hexdigest() == hash
