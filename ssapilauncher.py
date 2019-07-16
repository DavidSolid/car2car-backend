from flask import Flask
from flask_restful import Api
from resources.usercars import *
from resources.useractivecars import *
from resources.dateactivecars import *
from resources.userstats import *
from resources.userrents import *
from resources.receivedrents import *
from resources.specificuserrent import *
from resources.specificreceivedrent import *

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

# resource binding

# cars
# api.add_resource(ListofCarsinRange, "/cars")
api.add_resource(UserCars, "/cars/<string:userId>")
# api.add_resource(SpecificCar,"/cars/<string:objId>")
api.add_resource(UserActiveCars, "/cars/activebyuser/<string:userId>/<x>/<y>")
api.add_resource(DateActiveCars, "/cars/activebydate/<string:date>/<x>/<y>")
# gamification
api.add_resource(UserStats, "/gamification/<string:userId>")
# transactions
api.add_resource(UserRents, "/rents/<string:userId>")
api.add_resource(ReceivedRents, "/rents/received/<string:userId>")
api.add_resource(SpecificUserRent, "/rents/<string:userId>/<string:objId>")
api.add_resource(SpecificReceivedRent, "/rents/received/<string:userId>/<string:objId>")

if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0")
