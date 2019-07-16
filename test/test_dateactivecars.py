from unittest import TestCase
from unittest.mock import patch
from unittest .mock import Mock
from resources.dateactivecars import DateActiveCars
import json
from pymongo.errors import PyMongoError


@patch('mongoutils.mongoclient.MongoClient.connect', new=Mock())
class TestDateActiveCars(TestCase):
    """test class for dateactivecars resource"""
    dbmock = [{
            "inuso": {"$ne": "true"}, "sharing.inizio": {"$lte": 123213131}, "sharing.fine": {"$gte": 121313123},
            "posizione": {
                "$near": {
                    "$geometry": {
                        "type": "Point", "coordinates": [1.34, 3.45]
                    }
                }
            }
        }]

    def test_get_invalid_date(self):
        response = DateActiveCars().get("invalid date", 0, 0)
        self.assertEqual({"executed": False}, response)

    def test_get_badformat_date(self):
        response = DateActiveCars().get("2019-7-27 23:23", 0, 0)
        self.assertEqual({"executed": False}, response)

    def test_get_invalid_position(self):
        response = DateActiveCars().get("2019-7-27", "0-", 0)
        self.assertEqual({"executed": False}, response)

    #@patch('resources.dateactivecars.DateActiveCars.db.find', new=Mock(side_effect=PyMongoError("db error")))
    def test_get_db_error(self):
        to_use = DateActiveCars()
        to_use.db.find = Mock(side_effect=PyMongoError("db error"))
        response = DateActiveCars().get("2019-7-27", 0, 0)
        self.assertEqual({"executed": False}, response)

    #@patch('resources.dateactivecars.DateActiveCars.db.find', new=Mock(return_value=[]))
    def test_get_emptydb(self):
        to_use = DateActiveCars()
        to_use.db.find = Mock(return_value=[])
        response = DateActiveCars().get("2019-7-27", 0, 0)
        self.assertEqual({"data": []}, response.json)

    #@patch('resources.dateactivecars.DateActiveCars.db.find', new=Mock(return_value=dbmock))
    def test_get_query_successful(self):
        to_use = DateActiveCars()
        to_use.db.find = Mock(return_value=self.dbmock)
        response = DateActiveCars().get("2019-7-27", 0, 0)
        self.assertEqual({"data": self.dbmock}, response.json)
