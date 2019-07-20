from unittest import TestCase
from unittest.mock import patch, create_autospec
from unittest.mock import Mock, MagicMock
from resources.specificreceivedrent import SpecificReceivedRent
import json
from bson import json_util
from bson.errors import InvalidId
from pymongo.errors import PyMongoError
from werkzeug.exceptions import NotFound, BadRequest
from mongoutils.mongoclient import MongoClient
#@patch('parsers.carsparser.CarSchema.parse', new=Mock(return_value=carsample))
#patch('resources.usercars.UserCars.db.insert', Mock(return_value=""))


@patch('mongoutils.mongoclient.MongoClient.connect', new=Mock())
class TestSpecificReceivedRent(TestCase):
    """test class for specificreceivedrent resource"""
    db_mock = {"author": "user",
               "carId": "5d0a05e5987bbf80555a8a06"}

    def test_put_invalid_objid(self):
        with self.assertRaises(BadRequest):
            SpecificReceivedRent().put("user", "ehehe")

    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.find_one', new=Mock(side_effect=PyMongoError))
    def test_put_db_error_on_find(self):
        touse = SpecificReceivedRent()
        touse.db.find_one = Mock(side_effect=PyMongoError)
        response = touse.put("user", "5d0a05e5987bbf80555a8a06")
        self.assertEqual({"executed": False}, response)

    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.find_one', new=Mock(return_value=None))
    def test_put_rent_not_found(self):
        touse = SpecificReceivedRent()
        touse.db.find_one = Mock(return_value=None)
        with self.assertRaises(NotFound):
            response = SpecificReceivedRent().put("user", "5d0a05e5987bbf80555a8a06")

    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.find_one', new=Mock(return_value=db_mock))
    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.update_one', new=Mock(side_effect=PyMongoError))
    def test_put_db_error_on_first_update(self):
        to_use = SpecificReceivedRent()
        to_use.db.find_one = Mock(return_value=self.db_mock)
        to_use.db.update_one = Mock(side_effect=PyMongoError)
        response = SpecificReceivedRent().put("user", "5d0a05e5987bbf80555a8a06")
        self.assertEqual({"executed": False}, response)

    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.find_one', new=Mock(return_value=db_mock))
    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.update_one', new=Mock())
    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.delete_many', new=Mock(side_effect=PyMongoError))
    def test_put_db_error_on_delete(self):
        to_use = SpecificReceivedRent()
        to_use.db.find_one = Mock(return_value=self.db_mock)
        to_use.db.update_one = Mock()
        to_use.db.delete_many = Mock(side_effect=PyMongoError)
        response = SpecificReceivedRent().put("user", "5d0a05e5987bbf80555a8a06")
        self.assertEqual({"executed": False}, response)

    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.find_one', new=Mock(return_value=db_mock))
    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.update_one', new=Mock())
    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.delete_many', new=Mock())
    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db_cars.update_one', new=Mock(side_effect=PyMongoError))
    def test_put_db_error_on_second_update(self):
        to_use = SpecificReceivedRent()
        to_use.db.find_one = Mock(return_value=self.db_mock)
        to_use.db.update_one = Mock()
        to_use.db.delete_many = Mock()
        to_use.db_cars.update_one = Mock(side_effect=PyMongoError)
        response = SpecificReceivedRent().put("user", "5d0a05e5987bbf80555a8a06")
        self.assertEqual({"executed": False}, response)

    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.find_one', new=Mock(return_value=db_mock))
    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.update_one', new=Mock())
    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db.delete_many', new=Mock())
    #@patch('resources.specificreceivedrent.SpecificReceivedRent.db_cars.update_one', new=Mock())
    def test_put_success(self):
        to_use = SpecificReceivedRent()
        to_use.db.find_one = Mock(return_value=self.db_mock)
        to_use.db.update_one = Mock()
        to_use.db.delete_many = Mock()
        to_use.db_cars.update_one = Mock()
        response = SpecificReceivedRent().put("user", "5d0a05e5987bbf80555a8a06")
        self.assertEqual({"executed": True}, response)
