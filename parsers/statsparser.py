from flask_restful import reqparse


class StatsSchema:
    """schema for user stats json validation"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("user", required=True, location="json")
        self.parser.add_argument("exp", type=int, required=True, location="json")
        self.parser.add_argument("nSent", type=int, location="json")
        self.parser.add_argument("nReceived", type=int, location="json")
        self.parser.add_argument("nHours", type=int, location="json")
        self.parser.add_argument("lastReward", type=dict, location="json")

    def parse(self):
        return self.parser.parse_args()
