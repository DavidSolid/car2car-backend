from flask import Response, abort
from flask_restful import Resource
from pymongo.errors import PyMongoError
import json
from bson import json_util, ObjectId
from bson.errors import InvalidId
from mongoutils.mongoclient import MongoClient
from parsers.carsparser import CarSchema


class SpecificUserCar(Resource):
    """rest resource for specific car owned by a specific user"""

    def __init__(self):
        self.db = MongoClient("maincontainer", "cars").connect()

    def get(self, userId, objId):
        try:
            cursor = self.db.find_one({"proprietarioID": userId, "_id": ObjectId(objId)})
        except PyMongoError as e:
            print(e)
            return {"executed": False}
        except InvalidId as e:
            abort(400)
            return

        if cursor is None:
            abort(404)
        else:
            return Response(
                json.dumps({"data": cursor}, default=json_util.default),
                mimetype="application/json"
            )

    def delete(self, userId, objId):
        pass