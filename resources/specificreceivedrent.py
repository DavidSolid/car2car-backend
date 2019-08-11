from flask_restful import Resource, abort, reqparse
from resources.baseresource import ApiResource
from bson.objectid import ObjectId
from mongoutils.mongoclient import MongoClient
from pymongo.errors import PyMongoError
from bson.errors import InvalidId
from datetime import datetime
import math


class SpecificReceivedRent(ApiResource):
    """rest resource for rent identified by objId"""

    db = MongoClient("maincontainer", "transactions").connect()
    db_cars = MongoClient("maincontainer", "cars").connect()
    db_game = MongoClient("maincontainer", "gameinfo").connect()
    db_miss = MongoClient("maincontainer", "missions").connect()

    def updateMissions(self, user, var, amount):
        missions = self.db_miss.find({"vref": var})
        info = self.db_game.find_one({"user": user})
        if "missions" not in info:
            info["missions"] = {}
        for m in missions:
            mid = str(m["_id"])
            if mid in info["missions"]:
                # update status
                if info["missions"][mid]["value"] + amount >= m["threshold"]:
                    info["missions"][mid]["complete"] = True
                    info["exp"] += m["prize"]
                else:
                    info["missions"][mid]["value"] += amount
            else:
                # insert status
                info["missions"][mid] = {
                    "value": amount,
                    "complete": False
                }
                if amount >= m["threshold"]:
                    info["missions"][mid]["complete"] = True
                    info["exp"] += m["prize"]
        self.db_game.update_one({"user": user}, {"$set": info})

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

                    # update points # what if doesn't exists?
                    last_rent = self.db.find_one({"_id": ObjectId(objId)})
                    receiver = {"user": userId}
                    sender = {"user": last_rent["author"]}
                    hours = math.ceil((last_rent["endDate"].timestamp() - last_rent["startDate"].timestamp()) / 3600)
                    self.db_game.update_one(sender, {"$inc": {"nHours": hours, "nSent": 1, "exp": 20*hours}})
                    self.db_game.update_one(receiver, {"$inc": {"nReceived": 1, "exp": 40*hours}})

                    # update missions
                    # sender
                    sender = last_rent["author"]
                    self.updateMissions(sender, "nHours", hours)
                    self.updateMissions(sender, "nSent", 1)
                    self.updateMissions(sender, "exp", 20*hours)
                    # receiver
                    self.updateMissions(userId, "nReceived", 1)
                    self.updateMissions(userId, "exp", 40*hours)

            except PyMongoError as e:
                print(e)
                return {"executed": False}

            return {"executed": True}

# if __name__ == "__main__":
    # SpecificReceivedRent().updateMissions("test", "nHours", 100)