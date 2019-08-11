from flask_restful import reqparse
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
                if "missions" in stats and str(mission["_id"]) in stats["missions"]:
                    to_merge = stats["missions"][str(mission["_id"])]
                    mission["value"] = to_merge["value"]
                    mission["complete"] = to_merge["complete"]
                else:
                    mission["value"] = 0
                    mission["complete"] = False
            return Response(
                json.dumps({"data": missions}, default=json_util.default),
                mimetype="application/json"
            )
        else:
            return {"executed": False}

    def post(self, userId):
        try:
            stats = self.db.find_one({"user": userId})
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        p = reqparse.RequestParser()
        p.add_argument("mission", required=True, location="json")
        command = p.parse_args()

        if "missions" not in stats:
            stats["missions"] = {}

        if command["mission"] == "tutorial":
            # tutorial
            if "5d4dd80975c90b34b4a85d80" not in stats["missions"]:
                stats["missions"]["5d4dd80975c90b34b4a85d80"] = {
                    "value": 1,
                    "complete": True
                }
                gained = 100
                stats["exp"] += gained
                stats["tutorial"] = True
            else:
                return {"executed": False}

        if command["mission"] == "first_auto":
            # auto
            if "5d4d8f4c984d5d350c264be4" not in stats["missions"]:
                stats["missions"]["5d4d8f4c984d5d350c264be4"] = {
                    "value": 1,
                    "complete": True
                }
                gained = 40
                stats["exp"] += gained
            else:
                return {"executed": False}

        try:
            self.db.update_one({"user": userId}, {"$set": stats})
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        return {"executed": True, "gained": gained}
