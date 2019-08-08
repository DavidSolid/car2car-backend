from resources.usercars import *
from resources.specificusercar import *
from resources.useractivecars import *
from resources.dateactivecars import *
from resources.userstats import *
from resources.userrents import *
from resources.receivedrents import *
from resources.specificuserrent import *
from resources.specificreceivedrent import *
from resources.globalstats import *
from resources.usermissionstats import *


class EntrypointsMapper:
    """mapper for resources to api"""

    def __init__(self, api):
        self.api = api

    def bind(self):
        # cars
        # api.add_resource(ListofCarsinRange, "/cars")
        self.api.add_resource(UserCars, "/cars/<string:userId>")
        self.api.add_resource(SpecificUserCar, "/cars/<string:userId>/<string:objId>")
        self.api.add_resource(UserActiveCars, "/cars/activebyuser/<string:userId>/<x>/<y>")
        self.api.add_resource(DateActiveCars, "/cars/activebydate/<string:date>/<x>/<y>")

        # gamification
        self.api.add_resource(UserStats, "/gamification/<string:userId>")
        self.api.add_resource(GlobalStats, "/gamification")
        self.api.add_resource(UserMissionStats, "/gamification/<string:userId>/missions")

        # transactions
        self.api.add_resource(UserRents, "/rents/<string:userId>")
        self.api.add_resource(ReceivedRents, "/rents/received/<string:userId>")
        self.api.add_resource(SpecificUserRent, "/rents/<string:userId>/<string:objId>")
        self.api.add_resource(SpecificReceivedRent, "/rents/received/<string:userId>/<string:objId>")