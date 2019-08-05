from flask import Response
from flask_restful import Resource
from pymongo.errors import PyMongoError
import json
from bson import json_util
from datetime import datetime
from mongoutils.mongoclient import MongoClient
from resources.baseresource import ApiResource


class DateActiveCars(ApiResource):
    """rest resource for active cars during date ordered by distance from x,y point"""

    db = MongoClient("maincontainer", "cars").connect()

    def get(self, date, x, y):
        try:
            cdate = datetime.strptime(date, "%Y-%m-%d")
            float(x)
            float(y)
        except ValueError as e:
            print(e)
            return {"executed": False}

        query = {
            "inuso": False, "sharing.inizio": {"$lte": cdate}, "sharing.fine": {"$gte": cdate},
            "posizione": {
                "$near": {
                    "$geometry": {
                        "type": "Point", "coordinates": [float(x), float(y)]
                    }
                }
            }
        }
        try:
            results = self.db.find(query)
        except PyMongoError as e:
            print(e)
            return {"executed": False}

        return Response(
            json.dumps({"data": list(results)}, default=json_util.default),
            mimetype="application/json"
        )
