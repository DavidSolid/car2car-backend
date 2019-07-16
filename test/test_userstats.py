from unittest import TestCase
from unittest.mock import patch
from unittest .mock import Mock
from resources.userstats import UserStats
import json
from pymongo.errors import PyMongoError
#@patch('parsers.carsparser.CarSchema.parse', new=Mock(return_value=carsample))
#patch('resources.usercars.UserCars.db.insert', Mock(return_value=""))


class TestUserStats(TestCase):
    """test class for userstats resource"""
    dbmock = {
        "_id": "hash", "user": "pippo", "exp": 200
    }

    @patch('resources.userstats.UserStats.db.find', new=Mock(side_effect=PyMongoError("db error")))
    def test_get_db_error_read(self):
        response = UserStats().get("nomeacaso")
        self.assertEqual({"executed": False}, response)

    @patch('resources.userstats.UserStats.db.find_one', new=Mock(return_value=dbmock))
    def test_get_read_successful(self):
        response = UserStats().get("pippo")
        self.assertEqual({"data": self.dbmock}, response)

    @patch('resources.userstats.UserStats.db.find_one', new=Mock(return_value=None))
    @patch('resources.userstats.UserStats.db.insert', new=Mock(side_effect=PyMongoError("db error")))
    def test_get_db_error_creation(self):
        response = UserStats().get("notpippo")
        self.assertEqual({"executed": False}, response)

    @patch('resources.userstats.UserStats.db.find_one', new=Mock(return_value=None))
    @patch('resources.userstats.UserStats.db.insert', new=Mock())
    def test_get_insert_successful(self):
        response = UserStats().get("notpippo")
        self.assertEqual({"data": {"user": "notpippo", "exp": 0}}, response.json)
