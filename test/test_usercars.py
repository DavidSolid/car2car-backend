from unittest import TestCase
from unittest.mock import patch
from unittest .mock import Mock
from resources.usercars import UserCars
import json
from pymongo.errors import PyMongoError


class TestUserCars(TestCase):
    """test class for usercars resource"""
    carsample = {
        "produttore": "",
        "modello": "",
        "targa": "",
        "posizione": "",
        "inuso": "",
        "dataIm": "",
        "sharing": ""
    }

    def test_get_from_db(self):
        totest = UserCars()
        totest.db.find = Mock(return_value=[{"result": 2}])

        result = UserCars().get("nomeacaso")

        self.assertEqual({"data": [{"result": 2}]}, result.json)

    def test_get_if_empty(self):
        totest = UserCars()
        totest.db.find = Mock(return_value=[])

        result = UserCars().get("nomeacaso")

        self.assertEqual({"data": []}, result.json)

    def test_get_db_error(self):
        totest = UserCars()
        totest.db.find = Mock(side_effect=PyMongoError("server error"))

        result = UserCars().get("nomeacaso")

        self.assertEqual({"executed": False}, result)

    @patch('parsers.carsparser.CarSchema.parse', new=Mock(return_value=carsample))
    def test_post_valid_schema(self):
        with patch('resources.usercars.UserCars.db.insert', Mock(return_value="")):
            result = UserCars().post("nomeacaso")
        self.assertEqual(result, {"executed": True})

    @patch('parsers.carsparser.CarSchema.parse', new=Mock(return_value=carsample))
    def test_post_insertion_success(self, inserted=None):

        def insertfunc(insert):
            nonlocal inserted
            inserted = insert

        with patch('resources.usercars.UserCars.db.insert', Mock(side_effect=insertfunc)):
            result = UserCars().post("nomeacaso")

        updatedsample = self.carsample.copy()
        updatedsample["proprietarioID"] = "nomeacaso"
        self.assertEqual(inserted, updatedsample)

    @patch('parsers.carsparser.CarSchema.parse', new=Mock(return_value=carsample))
    def test_post_db_error(self):
        with patch('resources.usercars.UserCars.db.insert', Mock(side_effect=PyMongoError("server error"))):
            result = UserCars().post("nomeacaso")
        self.assertEqual(result, {"executed": False})
