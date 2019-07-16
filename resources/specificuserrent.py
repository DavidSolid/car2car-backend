from flask_restful import Resource, abort
from mongoutils.mongoclient import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from bson.errors import InvalidId


class SpecificUserRent(Resource):
    """rest resource for rent identified by objId"""

    def __init__(self):
        self.db = MongoClient("maincontainer", "transactions").connect()
        self.db_cars = MongoClient("maincontainer", "cars").connect()

    def put(self, userId, objId):  # close used transaction
        try:
            cursor = self.db.find_one(
                {"_id": ObjectId(objId), "author": userId, "isAccepted": True, "isEnded": False}
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
                self.db.update_one({"_id": ObjectId(objId)}, {"$set": {"isEnded": True}})
                self.db_cars.update_one({"_id": ObjectId(cursor["carId"])}, {"$set": {"inuso": False}})
                # update points
            except PyMongoError as e:
                print(e)
                return {"executed": False}

        return {"executed": True}

    def delete(self, userId, objId):  # delete transaction i made
        pass
