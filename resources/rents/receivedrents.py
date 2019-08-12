from flask_restful import Resource
from resources.baseresource import ApiResource
from flask import Response
from mongoutils.mongoclient import MongoClient
from pymongo.errors import PyMongoError
from bson import json_util
import json


class ReceivedRents(ApiResource):
    """rest resource for rents received by a user"""

    db = MongoClient("maincontainer", "transactions").connect()

    def get(self, userId):  # get received transactions
        query = {"addressedto": userId}
        try:
            results = self.db.find(query)
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        return Response(
            json.dumps({"data": list(results)}, default=json_util.default),
            mimetype="application/json"
        )
