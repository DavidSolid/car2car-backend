import pymongo


class MongoClient:
    """client for Mongo cluster"""
    URI = "mongodb+srv://Api_app:swe2019@clusterdiprova-prsqj.mongodb.net/test?retryWrites=true"

    def __init__(self, db, collection):
        self.db = db
        self.collection = collection

    def connect(self):
        return pymongo.MongoClient(self.URI)[self.db][self.collection]
