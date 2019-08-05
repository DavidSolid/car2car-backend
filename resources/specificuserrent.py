from flask_restful import Resource, abort
from resources.baseresource import ApiResource
from mongoutils.mongoclient import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from bson.errors import InvalidId
from datetime import datetime


class SpecificUserRent(ApiResource):
    """rest resource for rent identified by objId"""

    db = MongoClient("maincontainer", "transactions").connect()
    db_cars = MongoClient("maincontainer", "cars").connect()

    def put(self, userId, objId):  # confirm key received
        try:
            cursor = self.db.find_one(
                {"_id": ObjectId(objId), "author": userId, "isAccepted": True, "hasKey": False, "isEnded": False}
            )
        except PyMongoError as e:
            print(e)
            return {"executed": False}
        except InvalidId as e:
            print(e)
            return abort(400)

        if cursor is None:
            abort(404)
        else:
            now_time = datetime.utcnow()
            try:
                self.db.update_one({"_id": ObjectId(objId)}, {"$set": {"hasKey": True, "startDate": now_time}})
            except PyMongoError as e:
                print(e)
                return {"executed": False}

        return {"executed": True}

    def delete(self, userId, objId):  # delete transaction i made
        try:
            cursor = self.db.find_one(
                {"_id": ObjectId(objId), "author": userId, "isAccepted": False, "isEnded": False}
            )
        except PyMongoError as e:
            print(e)
            return {"executed": False}
        except InvalidId as e:
            print(e)
            return abort(400)

        if cursor is None:
            abort(404)
        else:
            try:
                self.db.update_one(
                    {"_id": ObjectId(objId)}, {"$set": {"isEnded": True, "reason": "aborted"}}
                )
            except PyMongoError as e:
                print(e)
                return {"executed": False}

            return {"executed": True}
