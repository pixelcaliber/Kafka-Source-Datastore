from custom_exception import FormNotFoundError, QuestionNotFoundError
from flask import jsonify
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import Form, Question, Response, Answer, question_form_association
from utils import DB_URL

engine = create_engine(DB_URL, echo=True)

def create_response(form_id, response_id, questions_data):
    try:
        # Create a session to interact with the database
        session = Session(engine)

        # Check if the response already exists
        response = session.query(Response).get(response_id)
        if response:
            return jsonify({"error": "Response already exists"}), 400

        # Check if the form exists
        form = session.query(Form).get(form_id)
        if not form:
            raise FormNotFoundError("Invalid form_id")

        for question_data in questions_data:
            question_id = question_data.get("question_id")
            
            # Query the database to get the question
            question = session.query(Question).get(question_id)
            
            # Check if the question do not exists
            if not question:    
                raise QuestionNotFoundError("Invalid question_id")

       
        # Create a new response for the form
        response = Response(form=form)
        session.add(response)
        session.commit()

        for question_data in questions_data:
            question_id = question_data.get("question_id")
            answer_text = question_data.get("answer")

            question = (
                session.query(Question)
                .join(question_form_association)
                .join(Form)
                .filter(Question.id == question_id, Form.id == form_id)
                .first()
            )

            answer = Answer(text=answer_text, question=question, response=response)
            session.add(answer)

        session.commit()
        session.close()

        return jsonify({"message": "Responses submitted successfully"}), 200

    except FormNotFoundError as e:
        raise e

    except QuestionNotFoundError as e:
        raise e
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
