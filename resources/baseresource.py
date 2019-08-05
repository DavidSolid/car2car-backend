from flask_restful import Resource, abort, reqparse
from functools import wraps
from authorizerutils.cognitoauth import CognitoAuth


class ApiResource(Resource):
    """base resource for auth support"""

    def __init__(self):
        self.authorizer = CognitoAuth()

        def authenticate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not getattr(func, 'authenticated', True):
                    return func(*args, **kwargs)

                parser = reqparse.RequestParser()
                parser.add_argument('Authorization', required=True, location='headers', dest="auth")
                token = parser.parse_args()["auth"]

                acct = self.authorizer.auth(token, **kwargs)  # custom account lookup function

                if acct:
                    return func(*args, **kwargs)

                abort(401)

            return wrapper

        self.method_decorators = {'post': [authenticate], 'put': [authenticate], 'delete': [authenticate]}
