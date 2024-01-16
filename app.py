# from flask import Flask, jsonify, request
# from forms_orm import create_form_template, create_response
# from custom_exception import FormNotFoundError, QuestionNotFoundError

# app = Flask(__name__)

# @app.route("/")
# def health():
#     return f"Server is listening to port 5000"


# @app.route("/create_form", methods=["GET"])
# def create_form():
#     create_form_template()
#     return f"Form created successfullly."


# @app.route("/create_response", methods=["POST"])
# def route_create_response():
#     try:
#         data = request.get_json()
#         form_id = data.get("form_id")
#         response_id = data.get("response_id")
#         questions_data = data.get("questions")
#         create_response(form_id, response_id, questions_data)
#         return f"Response succesfully created", 200

#     except FormNotFoundError as e:
#         return jsonify({"error": str(e)}), 400

#     except QuestionNotFoundError as e:
#         return jsonify({"error": str(e)}), 400
    
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(debug=True)

# app.py
from flask import Flask
from routes import health, create_form, route_create_response

app = Flask(__name__)

app.add_url_rule("/", "health", health)
app.add_url_rule("/create_form", "create_form", create_form, methods=["GET"])
app.add_url_rule("/create_response", "route_create_response", route_create_response, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)
