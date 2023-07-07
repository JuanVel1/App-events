import jwt
import os
import datetime

secret_key = os.getenv('SECRET_KEY')


def generate_token(nombre: str, email: str):
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        'nombre': nombre,
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    print(token)
    return token


def validate_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
