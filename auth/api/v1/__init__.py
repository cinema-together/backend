from flask_restplus import Namespace

namespace = Namespace("Api v1", path="/v1", description="Auth actions")
from api.v1 import users
