from flask_restful import Resource
from flask import Response
from mongoutils.mongoclient import MongoClient
from pymongo.errors import PyMongoError
import json
from bson import json_util
from datetime import datetime


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
            return Response(
                json.dumps({"data": results}, default=json_util.default),
                mimetype="application/json"
            )
        else:  # creating user stats
            obj = {"user": userId, "exp": 0, "nSent": 0, "nReceived": 0, "nHours": 0}
            try:
                self.db.insert(obj)
            except PyMongoError as e:
                print(e)
                return {"executed": False}

            return Response(
                json.dumps({"data": obj}, default=json_util.default),
                mimetype="application/json"
            )

    def put(self, userId):  # daily reward
        try:
            data = self.db.find_one({"user": userId})
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        if not data:
            return {"executed": False}

        if "lastReward" in data:
            delta = (datetime.utcnow().timestamp() - data["lastReward"].timestamp()) / 3600
            print(delta)
            if delta >= 24:
                self.db.update_one({"user": userId}, {"$inc": {"exp": 200}, "$set": {"lastReward": datetime.utcnow()}})
                return {"executed": True}
            else:
                return {"executed": False}
        else:
            self.db.update_one({"user": userId}, {"$inc": {"exp": 200}, "$set": {"lastReward": datetime.utcnow()}})
            return {"executed": True}
