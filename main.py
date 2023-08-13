from flask import Flask
from routes.common_routes import common_blueprint


app = Flask(__name__)

app.register_blueprint(common_blueprint)

if __name__ == '__main__':
    app.run(debug=True)