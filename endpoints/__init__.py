from flask import Flask

from endpoints.api import api_bp
from endpoints.statistics import bp as log_bp
from endpoints.bedrock import bp as bedrock_bp

print("hello --- api ---")


def register_api_endpoints(app: Flask):
    api_bp.register_blueprint(log_bp)
    app.register_blueprint(bedrock_bp)

    app.register_blueprint(api_bp)
