from flask_restful import Resource
from resources.baseresource import ApiResource
from flask import Response
from mongoutils.mongoclient import MongoClient
from pymongo.errors import PyMongoError
import json
from bson import json_util
from datetime import datetime


class UserMissionStats(ApiResource):
    """rest resource for gamification stats of a user"""

    db = MongoClient("maincontainer", "gameinfo").connect()
    db_missions = MongoClient("maincontainer", "missions").connect()

    def get(self, userId):
        try:
            missions = self.db_missions.find({})
            stats = self.db.find_one({"user": userId})
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        if stats:
            missions = list(missions)
            for mission in missions:
                if "missions" in stats and mission["_id"] in stats["missions"]:
                    to_merge = stats["missions"][mission["_id"]]
                    mission["value"] = to_merge["value"]
                    mission["complete"] = to_merge["complete"]
                else:
                    mission["value"] = 0
                    mission["complete"] = False
            return Response(
                json.dumps(missions, default=json_util.default),
                mimetype="application/json"
            )
        else:
            return {"executed": False}
