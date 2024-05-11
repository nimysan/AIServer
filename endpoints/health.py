class Actuator:
    def __init__(self):
        print("hello")

    def health(self):
        return {
            'health': True
        }


from flask import (
    Blueprint, g, redirect, request, url_for
)

bp = Blueprint('user', __name__, url_prefix='/user')
