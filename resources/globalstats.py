from flask import Response
from flask_restful import Resource, abort
from resources.baseresource import ApiResource
from mongoutils.mongoclient import MongoClient
from pymongo import DESCENDING
from pymongo.errors import PyMongoError
import json
from bson import json_util


class GlobalStats(ApiResource):
    """rest resource for stats leaderboard"""

    db = MongoClient("maincontainer", "gameinfo").connect()

    def get(self):
        try:
            cursor = self.db.find({}).sort("exp", DESCENDING)
        except PyMongoError as e:
            print(e)
            return abort(404)

        if cursor.count():
            return Response(
                json.dumps({"data": list(cursor)}, default=json_util.default),
                mimetype="application/json"
            )
        else:
            return {"data": []}
