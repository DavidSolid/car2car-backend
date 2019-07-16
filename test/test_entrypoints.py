from unittest import TestCase
from unittest.mock import patch
from unittest .mock import Mock
from resources.usercars import UserCars
import json
from pymongo.errors import PyMongoError


class TestEntrypoints(TestCase):
    """test class for resource entrypoints"""

    def test_unused_method(self):
        pass

    def test_usercars_post_invalid_schema(self):
        pass
