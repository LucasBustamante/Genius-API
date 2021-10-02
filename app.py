from controllers.default import GeniusConsume
from flask_restful import Api
from flask import Flask


app = Flask(__name__)
api = Api(app)

app.config.from_object('config')

api.add_resource(GeniusConsume, '/artist/<string:artist>')

if __name__ == "__main__":
    app.run()