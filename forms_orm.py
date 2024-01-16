from flask import jsonify
from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.orm import Session, declarative_base, relationship
from custom_exception import FormNotFoundError, QuestionNotFoundError

DB_URL = "postgresql://postgres:12345@localhost:5432/postgres"

engine = create_engine(DB_URL, echo=True)

# Create a base class for declarative models
Base = declarative_base()

# Association Table for the many-to-many relationship
question_form_association = Table(
    "question_form_association",
    Base.metadata,
    Column("question_id", Integer, ForeignKey("questions.id")),
    Column("form_id", Integer, ForeignKey("forms.id")),
)


# Define the Form model
class Form(Base):
    __tablename__ = "forms"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    questions = relationship(
        "Question", secondary=question_form_association, back_populates="forms"
    )
    responses = relationship("Response", back_populates="form")


# Define the Question model
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    forms = relationship(
        "Form", secondary=question_form_association, back_populates="questions"
    )
    answers = relationship("Answer", back_populates="question")


# Define the Response model
class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey("forms.id"))
    form = relationship("Form", back_populates="responses")
    answers = relationship("Answer", back_populates="response")


# Define the Answer model
class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="answers")
    response_id = Column(Integer, ForeignKey("responses.id"))
    response = relationship("Response", back_populates="answers")


def create_form_template():
    # Create the PostgreSQL database engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    session = Session(engine)

    # Creating forms

    form1 = Form(title="Form 1")
    form2 = Form(title="Form 2")
    session.add_all([form1, form2])
    session.commit()

    question1 = Question(text="What's your name?")
    question2 = Question(text="What's your age?")
    session.add_all([question1, question2])
    session.commit()

    # Associating questions with forms
    form1.questions.extend([question1, question2])
    form2.questions.extend([question1, question2])
    session.commit()

    session.close()
    return f"Tables successfully created!"


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

        # Check if the questions exists
        for question_data in questions_data:
            question_id = question_data.get("question_id")
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

        return jsonify({"message": "Responses submitted successfully"}), 200

    except FormNotFoundError as e:
        raise e

    except QuestionNotFoundError as e:
        raise e
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
