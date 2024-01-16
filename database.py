from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DB_URL = "postgresql://postgres:12345@localhost:5432/postgres"
engine = create_engine(DB_URL, echo=True)
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

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
    # Base.metadata.create_all(engine)

    # # Create a session to interact with the database
    # session = Session(engine)

    # # Creating forms

    # form1 = Form(title="Form 1")
    # form2 = Form(title="Form 2")
    # session.add_all([form1, form2])
    # session.commit()

    # question1 = Question(text="What's your name?")
    # question2 = Question(text="What's your age?")
    # session.add_all([question1, question2])
    # session.commit()

    # # Associating questions with forms
    # form1.questions.extend([question1, question2])
    # form2.questions.extend([question1, question2])
    # session.commit()

    # session.close()
    return f"Tables successfully created!"