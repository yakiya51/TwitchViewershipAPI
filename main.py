from flask import Flask
from flask_restful import Api, Resource
from scraper import get_viewership

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self, game):
        return {
                "game": game, 
                "viewers" : get_viewership(game)
            }

api.add_resource(HelloWorld, '/get-twitch-viewership/<str:game>')


if __name__ == "__main__":
    app.run()
