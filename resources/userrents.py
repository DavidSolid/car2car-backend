from flask_restful import Resource
from resources.baseresource import ApiResource
from flask import Response
from bson import json_util
import json
from pymongo.errors import PyMongoError
from mongoutils.mongoclient import MongoClient
from parsers.rentparser import RentSchema


class UserRents(ApiResource):
    """rest resource for rents sent by a user"""

    db = MongoClient("maincontainer", "transactions").connect()
    db_cars = MongoClient("maincontainer", "cars").connect()  # to be used

    def post(self, userId):  # insert transaction #tocheck if car is not in use and is in sharing
        rent = RentSchema().parse()
        toinsert = {"author": userId}
        for k in ["addressedto", "carId", "isAccepted", "hasKey", "isEnded"]:  # aggiungere hasKey
            toinsert[k] = rent[k]
        toinsert["date"] = json_util.loads(json.dumps(rent["date"]))

        try:
            same_rent = self.db.find_one({"author": userId, "carId": toinsert["carId"], "isEnded": False})
            if same_rent is not None:
                return {"executed": False}
            self.db.insert_one(toinsert)
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        return {"executed": True}

    def get(self, userId):  # get made transactions
        query = {"author": userId}
        try:
            results = self.db.find(query)
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        return Response(
            json.dumps({"data": list(results)}, default=json_util.default),
            mimetype="application/json"
        )
