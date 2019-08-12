from resources.cars.usercars import *
from resources.cars.specificusercar import *
from resources.cars.useractivecars import *
from resources.cars.dateactivecars import *
from resources.stats.userstats import *
from resources.rents.userrents import *
from resources.rents.receivedrents import *
from resources.rents.specificuserrent import *
from resources.rents.specificreceivedrent import *
from resources.stats.globalstats import *
from resources.stats.usermissionstats import *


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