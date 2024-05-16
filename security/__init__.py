import base64
import logging

from flask import current_app
from model import get_user_repository

logger = logging.getLogger(__name__)


def is_authenticated(auth_header=""):
    auth_token = auth_header.split(' ')[1]
    logger.debug(f"auth_token {auth_token}")
    try:
        decoded_token = base64.b64decode(auth_token).decode('utf-8')
        username, password = decoded_token.split(':')
        user_repository = get_user_repository()
        logger.info(f"Username {username} and password *** - {current_app}")
        user_item = user_repository.load_user_by_username(username)
        if user_item:
            if user_item['password'] == password:
                return True, ""
            else:
                return False, "Password wrong"
        else:
            return False, f"User does not exist"
        logger.info(f"---- {item} ------")

    except:
        return False, f"auth_token is invalid"

    return False;
