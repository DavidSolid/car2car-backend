from flask import Flask
from flask_restful import Api
from entrypoints import EntrypointsMapper

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

# resource binding
EntrypointsMapper(api).bind()

if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0")
