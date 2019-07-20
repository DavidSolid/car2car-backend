from unittest import TestCase
from unittest.mock import patch
from unittest .mock import Mock
from resources.userrents import UserRents
import json
from bson import json_util
from pymongo.errors import PyMongoError
#@patch('parsers.carsparser.CarSchema.parse', new=Mock(return_value=carsample))
#patch('resources.usercars.UserCars.db.insert', Mock(return_value=""))


@patch('mongoutils.mongoclient.MongoClient.connect', new=Mock())
class TestUserRents(TestCase):
    """test class for userrents resource"""
    rentmock = {
        "_id": {"$oid": "5d0a05e5987bbf80555a8a09"}, "carId": "5cc6dd4075ec6d0610e1aec2", "author": "pear",
        "addressedto": "pearpear", "isAccepted": True, "date": {"$date": 1557784800000}, "isEnded": False
    }

    dbmock = [{
        "_id": {"$oid": "5d0a05e5987bbf80555a8a09"}, "carId": "5cc6dd4075ec6d0610e1aec2", "author": "pear",
        "addressedto": "pearpear", "isAccepted": True, "date": {"$date": 1557784800000}, "isEnded": False
    }]

    #@patch('resources.userrents.UserRents.db.insert_one', new=Mock(return_value=""))
    @patch('parsers.rentparser.RentSchema.parse', new=Mock(return_value=rentmock))
    def test_post_valid_schema(self):
        to_use = UserRents()
        to_use.db.insert_one = Mock(return_value="")
        result = UserRents().post("iron")
        self.assertEqual({"executed": True}, result)

    #@patch('resources.userrents.UserRents.db.insert_one', new=Mock(side_effect=PyMongoError))
    @patch('parsers.rentparser.RentSchema.parse', new=Mock(return_value=rentmock))
    def test_post_db_error(self):
        to_use = UserRents()
        to_use.db.insert_one = Mock(side_effect=PyMongoError)
        result = UserRents().post("iron")
        self.assertEqual({"executed": False}, result)

    @patch('parsers.rentparser.RentSchema.parse', new=Mock(return_value=rentmock))
    def test_post_inserted_correctly(self, inserted=None):
        def insertfunc(insert):
            nonlocal inserted
            del insert["date"]
            inserted = insert


        #with patch('resources.userrents.UserRents.db.insert_one', new=Mock(side_effect=insertfunc)):
        to_mock = UserRents()
        to_mock.db.insert_one = Mock(side_effect=insertfunc)
        UserRents().post("pear")
        modifiedmock = self.rentmock.copy()
        del modifiedmock["_id"]
        del modifiedmock["date"]
        self.assertEqual(modifiedmock, inserted)

    #@patch('resources.userrents.UserRents.db.find', new=Mock(side_effect=PyMongoError("db error")))
    def test_get_db_error(self):
        to_mock = UserRents()
        to_mock.db.find = Mock(side_effect=PyMongoError("db error"))
        result = UserRents().get("nouser")
        self.assertEqual({"executed": False}, result)

    #@patch('resources.userrents.UserRents.db.find', new=Mock(return_value=dbmock))
    def test_get_read_successful(self):
        to_mock = UserRents()
        to_mock.db.find = Mock(return_value=self.dbmock)
        result = UserRents().get("pear")
        self.assertEqual({"data": self.dbmock}, result.json)