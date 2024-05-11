from flask import Flask

from endpoints.api import api_bp
from endpoints.statistics import bp as log_bp
from endpoints.bedrock import bp as bedrock_bp
from endpoints.config_item import bp as config_bp
from endpoints.user import bp as user_bp

print("hello --- api ---")


def register_api_endpoints(app: Flask):
    api_bp.register_blueprint(log_bp)
    api_bp.register_blueprint(bedrock_bp)
    api_bp.register_blueprint(config_bp)

    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)
