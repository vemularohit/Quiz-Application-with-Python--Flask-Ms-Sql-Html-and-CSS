from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import urllib

params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=ROHITVEMULA;"
                                 "DATABASE=quiz;"
                                 "Trusted_Connection=yes;")

engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

metadata = MetaData()

metadata.reflect(engine)

courseadd = metadata.tables["course"]

usersData = metadata.tables["Users"]

################################

# quiz_questions = metadata.tables["Questions"]

# quiz_options = metadata.tables["options"]

# quiz_answers = metadata.tables["answers"]

#######################

questions = metadata.tables['t_questions']

answers =  metadata.tables['t_answers']

quiznames = metadata.tables['QuizNames']

studentcourses = metadata.tables['student_interest']


Sessionlocal = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False))
