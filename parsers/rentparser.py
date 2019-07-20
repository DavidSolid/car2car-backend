from flask_restful import reqparse


class RentSchema:
    """schema for rent json validation"""

    def __init__(self):  # to modify
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("author", required=True, location="json")
        self.parser.add_argument("addressedto", required=True, location="json")
        self.parser.add_argument("date", type=dict, required=True, location="json")
        self.parser.add_argument("carId", required=True, location="json")
        self.parser.add_argument("isAccepted", type=bool, required=True, location="json")
        self.parser.add_argument("hasKey", type=bool, required=True, location="json")
        self.parser.add_argument("isEnded", type=bool, required=True, location="json")

    def parse(self):
        return self.parser.parse_args()
