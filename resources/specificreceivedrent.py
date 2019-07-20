from flask_restful import Resource, abort, reqparse
from bson.objectid import ObjectId
from mongoutils.mongoclient import MongoClient
from pymongo.errors import PyMongoError
from bson.errors import InvalidId
from datetime import datetime


class SpecificReceivedRent(Resource):
    """rest resource for rent identified by objId"""

    def __init__(self):
        self.db = MongoClient("maincontainer", "transactions").connect()
        self.db_cars = MongoClient("maincontainer", "cars").connect()

    def put(self, userId, objId):  # confirm transaction
        # RentSchema

        try:
            cursor = self.db.find_one(
                {"_id": ObjectId(objId), "addressedto": userId, "isAccepted": False, "isEnded": False}
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
                self.db.update_one({"_id": ObjectId(objId)}, {"$set": {"isAccepted": True}})
                self.db.update_many(
                    {"carId": cursor["carId"], "_id": {"$not": {"$eq": ObjectId(objId)}}},
                    {"$set": {"isEnded": True, "reason": "denied"}}  # maybe add end date?
                )
                self.db_cars.update_one({"_id": ObjectId(cursor["carId"])}, {"$set": {"inuso": True}})
            except PyMongoError as e:
                print(e)
                return {"executed": False}

            return {"executed": True}

    # def put(self, userId, objId):  # close used transaction # to copy and move
    # try:
    # cursor = self.db.find_one(
    # {"_id": ObjectId(objId), "author": userId, "isAccepted": True, "isEnded": False}
    # )
    # except PyMongoError as e:
    # print(e)
    # return {"executed": False}
    # except InvalidId as e:
    # print(e)
    # return abort(400)

    # if cursor is None:
    # abort(404)
    # else:
    # try:
    # self.db.update_one({"_id": ObjectId(objId)}, {"$set": {"isEnded": True}})
    # self.db_cars.update_one({"_id": ObjectId(cursor["carId"])}, {"$set": {"inuso": False}})
    ## update points
    # except PyMongoError as e:
    # print(e)
    # return {"executed": False}

    # return {"executed": True}

    def delete(self, userId, objId):  # deny transaction or close # maybe add end date?
        preq = reqparse.RequestParser()
        preq.add_argument("command", required=True, location="json")
        command = preq.parse_args()

        if command["command"] == "deny":
            query = {"_id": ObjectId(objId), "addressedto": userId, "isAccepted": False, "isEnded": False}
        else:
            query = {"_id": ObjectId(objId), "addressedto": userId, "isAccepted": True, "hasKey": True, "isEnded": False}

        try:
            cursor = self.db.find_one(
                query
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
                now_time = datetime.utcnow()
                if command["command"] == "deny":
                    self.db.update_one(
                        {"_id": ObjectId(objId)}, {"$set": {"isEnded": True, "reason": "denied"}}
                    )
                else:
                    self.db.update_one(
                        {"_id": ObjectId(objId)}, {"$set": {"isEnded": True, "endDate": now_time}}
                    )
                    self.db_cars.update_one(
                        {"_id": ObjectId(cursor["carId"])}, {"$set": {"inuso": False}}
                    )
                    # update points
            except PyMongoError as e:
                print(e)
                return {"executed": False}

            return {"executed": True}
