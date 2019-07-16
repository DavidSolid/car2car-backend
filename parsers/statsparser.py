from flask_restful import reqparse


class StatsSchema:
    """schema for user stats json validation"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("user", required=True, location="json")
        self.parser.add_argument("exp", type=int, required=True, location="json")

    def parse(self):
        return self.parser.parse_args()
