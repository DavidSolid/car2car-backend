from unittest import TestCase
from unittest.mock import patch
from unittest .mock import Mock
from resources.receivedrents import ReceivedRents
import json
from bson import json_util
from pymongo.errors import PyMongoError
#@patch('parsers.carsparser.CarSchema.parse', new=Mock(return_value=carsample))
#patch('resources.usercars.UserCars.db.insert', Mock(return_value=""))


@patch('mongoutils.mongoclient.MongoClient.connect', new=Mock())
class TestReceivedRents(TestCase):
    """test class for receivedrents resource"""
    dbmock = [{
        "_id": {"$oid": "5d0a05e5987bbf80555a8a09"}, "carId": "5cc6dd4075ec6d0610e1aec2", "author": "pear",
        "addressedto": "pearpear", "isAccepted": True, "date": {"$date": 1557784800000}, "isEnded": False
    }]

    #@patch('resources.receivedrents.ReceivedRents.db.find', new=Mock(side_effect=PyMongoError("db error")))
    def test_get_db_error(self):
        to_use = ReceivedRents()
        to_use.db.find = Mock(side_effect=PyMongoError("db error"))
        result = ReceivedRents().get("nouser")
        self.assertEqual({"executed": False}, result)

    #@patch('resources.receivedrents.ReceivedRents.db.find', new=Mock(return_value=dbmock))
    def test_get_read_success(self):
        to_use = ReceivedRents()
        to_use.db.find = Mock(return_value=self.dbmock)
        result = ReceivedRents().get("nouser")
        self.assertEqual({"data": self.dbmock}, result.json)
