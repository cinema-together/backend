from flask import Flask
from flask_restplus import Api

from api.v1 import namespace

api = Api(
    title="Auth API",
    version="1.0",
    doc="/auth/doc"
)

api.add_namespace(namespace)


def init_api(app: Flask):
    api.init_app(app)
