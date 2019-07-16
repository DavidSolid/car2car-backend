from flask import Response
from flask_restful import Resource
from pymongo.errors import PyMongoError
import json
from bson import json_util
from mongoutils.mongoclient import MongoClient
from parsers.carsparser import CarSchema


class UserCars(Resource):
    """rest resource for cars owned by a specific user"""

    def __init__(self):
        self.db = MongoClient("maincontainer", "cars").connect()

    def get(self, userId):
        query = {"proprietarioID": userId}
        try:
            results = self.db.find(query)
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        return Response(
            json.dumps({"data": list(results)}, default=json_util.default),
            mimetype="application/json"
        )

    def post(self, userId):
        car = CarSchema().parse()
        toinsert = {"produttore": car["produttore"]}

        for k in ["modello", "targa", "posizione", "inuso"]:
            toinsert[k] = car[k]

        toinsert["proprietarioID"] = userId
        toinsert["dataIm"] = json_util.loads(json.dumps(car["dataIm"]))
        toinsert["sharing"] = json_util.loads(json.dumps(car["sharing"]))
        try:
            self.db.insert(toinsert)
        except PyMongoError as e:
            print(e)
            return {"executed": False}
        # return Response(json.dumps({"executed": True}, default=json_util.default), mimetype="application/json")
        return {"executed": True}
