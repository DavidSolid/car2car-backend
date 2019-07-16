from flask_restful import Resource
from flask import Response
from mongoutils.mongoclient import MongoClient
from pymongo.errors import PyMongoError
import json
from bson import json_util


class UserStats(Resource):
    """rest resource for gamification stats of a user"""

    def __init__(self):
        self.db = MongoClient("maincontainer", "gameinfo").connect()

    def get(self, userId):
        query = {"user": userId}
        projection = {"_id": 0}
        try:
            results = self.db.find_one(query, projection)
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        if results is not None:  # is present user stats?
            return {"data": results}
        else:  # creating user stats
            obj = {"user": userId, "exp": 0}
            try:
                self.db.insert(obj)
            except PyMongoError as e:
                print(e)
                return {"executed": False}

            return Response(
                json.dumps({"data": obj}, default=json_util.default),
                mimetype="application/json"
            )

    def put(self, userId):
        pass
