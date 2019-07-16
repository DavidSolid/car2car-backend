from flask_restful import Resource, abort
from bson.objectid import ObjectId
from mongoutils.mongoclient import MongoClient
from pymongo.errors import PyMongoError


class SpecificReceivedRent(Resource):
    """rest resource for rent identified by objId"""

    def __init__(self):
        self.db = MongoClient("maincontainer", "transactions").connect()
        self.db_cars = MongoClient("maincontainer", "cars").connect()

    def put(self, userId, objId):  # confirm or deny transaction #only confirm for the moment
        # RentSchema

        try:
            cursor = self.db.find_one(
                {"_id": ObjectId(objId), "addressedto": userId, "isAccepted": False}
            )
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        if cursor is None:
            abort(404)
        else:
            try:
                self.db.update_one({"_id": ObjectId(objId)}, {"$set": {"isAccepted": True}})
                self.db.delete_many(
                    {"carId": cursor["carId"], "_id": {"$not": ObjectId(objId)}}
                )
                self.db_cars.update_one({"_id": ObjectId(cursor["carId"])}, {"$set": {"inuso": True}})
            except PyMongoError as e:
                print(e)
                return {"executed": False}

            return {"executed": True}
