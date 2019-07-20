from flask_restful import Resource
from flask import Response
from bson import json_util
import json
from pymongo.errors import PyMongoError
from mongoutils.mongoclient import MongoClient
from parsers.rentparser import RentSchema


class UserRents(Resource):
    """rest resource for rents sent by a user"""

    def __init__(self):
        self.db = MongoClient("maincontainer", "transactions").connect()
        self.db_cars = MongoClient("maincontainer", "cars").connect()  # to be used

    def post(self, userId):  # insert transaction #tocheck if car is not in use and is in sharing
        rent = RentSchema().parse()
        toinsert = {"author": userId}
        for k in ["addressedto", "carId", "isAccepted", "hasKey", "isEnded"]:  # aggiungere hasKey
            toinsert[k] = rent[k]
        toinsert["date"] = json_util.loads(json.dumps(rent["date"]))
        try:
            self.db.insert_one(toinsert)
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        return {"executed": True}

    def get(self, userId):  # get made not ended transactions #and all rents?
        query = {"author": userId, "isEnded": False}
        try:
            results = self.db.find(query)
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        return Response(
            json.dumps({"data": list(results)}, default=json_util.default),
            mimetype="application/json"
        )
