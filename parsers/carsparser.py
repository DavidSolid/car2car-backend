from flask_restful import reqparse


class CarSchema:
    """schema for cars json validation"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("produttore", required=True, location="json")
        self.parser.add_argument("modello", required=True, location="json")
        self.parser.add_argument("descrizione", required=True, location="json")
        self.parser.add_argument("targa", required=True, location="json")
        self.parser.add_argument("dataIm", type=dict, required=True, location="json")
        self.parser.add_argument("posizione", type=dict, required=True, location="json")
        self.parser.add_argument("sharing", type=dict, required=True, location="json")
        self.parser.add_argument("inuso", type=bool, required=True, location="json")
        self.parser.add_argument("prezzo", type=float, required=True, location="json")

    def parse(self):
        return self.parser.parse_args()
