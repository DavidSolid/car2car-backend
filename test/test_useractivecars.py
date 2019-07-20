from unittest import TestCase
from unittest.mock import patch
from unittest .mock import Mock
from resources.useractivecars import UserActiveCars
import json
from pymongo.errors import PyMongoError
#@patch('parsers.carsparser.CarSchema.parse', new=Mock(return_value=carsample))
#patch('resources.usercars.UserCars.db.insert', Mock(return_value=""))


@patch('mongoutils.mongoclient.MongoClient.connect', new=Mock())
class TestUserActiveCars(TestCase):
    """test class for useractivecars resource"""
    dbmock = [{
            "inuso": {"$ne": "true"}, "proprietarioID": "user", "sharing": {"$exists": "true"},
            "posizione": {
                "$near": {
                    "$geometry": {
                        "type": "Point", "coordinates": [-234, -234]
                    }
                }
            }
        }]

    def test_get_invalid_position(self):
        response = UserActiveCars().get("nomeacaso", "stringx1", "stringy1")
        self.assertEqual(response, {"executed": False})

    #@patch('resources.useractivecars.UserActiveCars.db.find', new=Mock(return_value=[]))
    def test_get_empty_db(self):
        to_use = UserActiveCars()
        to_use.db.find = Mock(return_value=[])
        response = UserActiveCars().get("nomeacaso", "0.1", "-1.2")
        self.assertEqual({"data": []}, response.json)

    #@patch('resources.useractivecars.UserActiveCars.db.find', new=Mock(side_effect=PyMongoError("db error")))
    def test_get_db_error(self):
        to_use = UserActiveCars()
        to_use.db.find = Mock(side_effect=PyMongoError("db error"))
        response = UserActiveCars().get("nomeacaso", "0.1", "-1.2")
        self.assertEqual({"executed": False}, response)

    #@patch('resources.useractivecars.UserActiveCars.db.find', new=Mock(return_value=dbmock))
    def test_get_query_successful(self):
        to_use = UserActiveCars()
        to_use.db.find = Mock(return_value=self.dbmock)
        response = UserActiveCars().get("user", "0.1", "-1.2")
        self.assertEqual({"data": self.dbmock}, response.json)