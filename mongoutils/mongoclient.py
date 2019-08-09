import pymongo


class MongoClient:
    """client for Mongo cluster"""
    URI = "mongodb+srv://Api_app:swe2019@clusterdiprova-prsqj.mongodb.net/test?retryWrites=true"
    instance = pymongo.MongoClient(URI, connect=False)

    def __init__(self, db, collection):
        self.db = db
        self.collection = collection

    def connect(self):
        return self.instance[self.db][self.collection]
