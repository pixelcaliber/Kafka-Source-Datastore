from flask import Flask
from routes import health, create_form, route_create_response

app = Flask(__name__)

app.add_url_rule("/", "health", health)
app.add_url_rule("/create_form", "create_form", create_form, methods=["GET"])
app.add_url_rule("/create_response", "route_create_response", route_create_response, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)
