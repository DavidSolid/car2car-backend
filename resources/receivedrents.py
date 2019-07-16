from flask_restful import Resource
from flask import Response
from mongoutils.mongoclient import MongoClient
from pymongo.errors import PyMongoError
from bson import json_util
import json


class ReceivedRents(Resource):
    """rest resource for rents received by a user"""

    def __init__(self):
        self.db = MongoClient("maincontainer", "transactions").connect()

    def get(self, userId):  # get received not ended transactions
        query = {"addressedto": userId, "isEnded": False}
        try:
            results = self.db.find(query)
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        return Response(
            json.dumps({"data": list(results)}, default=json_util.default),
            mimetype="application/json"
        )
