import requests
import time
from jose import jwt, jwk
from jose.utils import base64url_decode
from flask import abort


class CognitoAuth:
    """authorizer for user pool access token"""

    def __init__(self):
        region = 'us-east-1'
        pool_id = 'us-east-1_BwaIFOt0m'
        self.client_id = '4i747a0beip81otfr4s9k363q1'
        keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, pool_id)

        # getting public keys from provider
        response = requests.get(keys_url)
        if response.status_code != 200:
            abort(401)

        self.keys = response.json()["keys"]

    def auth(self, jwt_token, **kwargs):

        headers = jwt.get_unverified_headers(jwt_token)
        kid = headers['kid']

        chosen_key = None
        for i in self.keys:
            if kid == i['kid']:
                chosen_key = i
                break
        if chosen_key is None:
            print('Public key not found in jwks.json')
            return False
        # constructing the right public key
        public_key = jwk.construct(chosen_key)

        message, encoded_signature = str(jwt_token).rsplit('.', 1)
        decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

        # signature verification
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            print('Signature verification failed')
            return False
        print('Signature successfully verified')

        claims = jwt.get_unverified_claims(jwt_token)

        # token expire time check
        if time.time() > claims['exp']:
            print('Token is expired')
            return False

        # client_id check
        if claims['client_id'] != self.client_id:
            print('Token was not issued for this audience')
            return False

        # if present, check user_id
        if "userId" in kwargs and kwargs["userId"]:
            return kwargs["userId"] == claims["username"]
        # print(claims)
        return True
