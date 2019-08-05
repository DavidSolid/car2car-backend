from flask import Response
from flask_restful import Resource
from resources.baseresource import ApiResource
from pymongo.errors import PyMongoError
import json
from bson import json_util
from mongoutils.mongoclient import MongoClient


class UserActiveCars(ApiResource):
    """rest resource for active cars owned by a user ordered by distance from x,y point"""

    db = MongoClient("maincontainer", "cars").connect()

    def get(self, userId, x, y):
        try:
            float(x), float(y)
        except ValueError as e:
            print(e)
            return {"executed": False}

        query = {
            "inuso": {"$ne": "true"}, "proprietarioID": userId, "sharing": {"$exists": "true"},
            "posizione": {
                "$near": {
                    "$geometry": {
                        "type": "Point", "coordinates": [float(x), float(y)]
                    }
                }
            }
        }
        try:
            results = self.db.find(query)
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        return Response(
            json.dumps({"data": list(results)}, default=json_util.default),
            mimetype="application/json"
        )
