# routes.py
from flask import jsonify, request
from database import create_form_template
from form_orm2 import create_response
from custom_exception import FormNotFoundError, QuestionNotFoundError

def health():
    return f"Server is listening to port 5000"

def create_form():
    create_form_template()
    return f"Form created successfully."

def route_create_response():
    try:
        data = request.get_json()
        form_id = data.get("form_id")
        response_id = data.get("response_id")
        questions_data = data.get("questions")
        create_response(form_id, response_id, questions_data)
        return jsonify({"message": "Response successfully created"}), 200

    except FormNotFoundError as e:
        return jsonify({"error": str(e)}), 400

    except QuestionNotFoundError as e:
        return jsonify({"error": str(e)}), 400
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
