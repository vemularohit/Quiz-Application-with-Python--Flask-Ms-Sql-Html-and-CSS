from flask import Flask, flash, render_template, request, url_for, redirect, session, abort
from logzero import logger
from sqlalchemy.sql.operators import op
import crud
import urllib
from db import courseadd
from functools import wraps
from flask import g


app = Flask(__name__)

app.secret_key = 'rohit'


def restricted(access_level):
    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):
            print(access_level)
            # uid = session.get("UID")
            user_id = session.get("UID")

            logger.warning("-----> user_id: {} st_id: {}".format(user_id))

            role = crud.getuserrole(user_id)

            if role:
                if role not in access_level:
                    abort(403)
            else:
                abort(404)

            return function(*args, **kwargs)

        return wrapper

    return decorator


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        get_UID = session.get('UID')
        logger.warning("get_UID: {}".format(get_UID))
        if not get_UID:

            return render_template('login.html')

        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------------------------------------------------------------


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

# -------------------------------------------------------------------------------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    else:
        usn = str(request.form.get('email'))
        psw = str(request.form.get('password'))

        logger.info("Username: {} Password: {}".format(usn, psw))

        error = None

        result = crud.checkUser(usn, psw)

        logger.warning("-----> Result: {}".format(result))

        if result:

            if result.role == 'student':

                flash('You were successfully logged in as Student')
                # return render_template('admin_home.html')
                return redirect(url_for('student_home'))

            elif result.role == 'teacher':

                flash('You were successfully logged in as Teacher')
                # return render_template('super_admin_home.html')
                return redirect(url_for('teacher_home'))

        else:

            error = 'Invalid credentials'
            return render_template('login.html', error=error)

# -------------------------------------------------------------------------------------------------


@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'GET':

        return render_template('student_signup.html')

    else:
        fname = str(request.form.get('fname'))
        lname = str(request.form.get('lname'))
        uname = str(request.form.get('uname'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        role = str(request.form.get('role'))
        # course_id = request.form.getlist('course_id')

        logger.info("Fname: {} LName: {} UNamee: {} Email: {} password: {} role : {} ".format(
            fname, lname, uname, email, password, role))

        crud.createUser(fname, lname, uname, email, password, role)

        # return render_template('login.html')
        return redirect(url_for("student_signup_courses"))

# -------------------------------------------------------------------------------------------------


@app.route('/student_signup_courses', methods=['GET', 'POST'])
def student_signup_courses():
    if request.method == 'GET':

        result = crud.getallcourses()
        logger.info("result{}".format(result))
        if result:
            data = result
        else:
            data = None

        return render_template('student_signup_courses.html', courseadd=data)

    else:

        course_Names = request.form.getlist('course_id')

        logger.info("course_id: {} ".format(course_Names))

        crud.insertcourse(course_Names)

        return render_template('login.html')

# -------------------------------------------------------------------------------------------------


@app.route('/teacher_signup', methods=['GET', 'POST'])
def teacher_signup():
    if request.method == 'GET':
        return render_template('teacher_signup.html')

    else:
        fname = str(request.form.get('fname'))
        lname = str(request.form.get('lname'))
        uname = str(request.form.get('uname'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        role = str(request.form.get('role'))

        logger.info("Fname: {} LName: {} UNamee: {} Email: {} password: {} role : {}".format(
            fname, lname, uname, email, password, role))

        crud.createUser(fname, lname, uname, email, password, role)

        return render_template('login.html')

# -------------------------------------------------------------------------------------------------


@app.route('/teacher_home')
def teacher_home():

    return render_template('teacher_home.html')

# -------------------------------------------------------------------------------------------------


@app.route('/student_home')
def student_home():

    return render_template('student_home.html')

# -------------------------------------------------------------------------------------------------


@app.route('/add', methods=['GET', 'POST'])
# @login_required
# @restricted(['teacher'])
def add():
    if request.method == 'GET':
        result = crud.getcourse()

        if result:
            data = result
        else:
            data = None

        return render_template('add.html', courses=data)
    else:
        course = str(request.form.get('course'))

    logger.info("course: {}".format(course))

    crud.addcourse(course)

    return redirect('/add')

# -------------------------------------------------------------------------------------------------


@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'GET':

        result = crud.getcourse()

        if result:
            data = result
        else:
            data = None

        result1 = crud.get_Quiznames()

        if result1:
            data1 = result1
        else:
            data1 = None

        return render_template('add_quiz.html', courseadd=data, QuizNames=data1)

    else:

        course_id = request.form.get('course_id')
        quiz_name = str(request.form.get('quiz_name'))

        crud.add_quiz(quiz_name, course_id)

        logger.info("course_id: {} quiz name: {}".format(course_id, quiz_name))

        return redirect('/add_quiz')

# -------------------------------------------------------------------------------------------------


@app.route('/add_quiz_questions', methods=['GET', 'POST'])
def add_quiz_questions():
    if request.method == 'GET':

        result = crud.getcourse()

        if result:
            data = result
        else:
            data = None

        result1 = crud.get_Quiznames()

        if result1:
            data1 = result1
        else:
            data1 = None

        return render_template('add_quiz_questions.html', courseadd=data, QuizNames=data1)

    else:

        course_id = request.form.get('course_id')
        quiz_id = request.form.get('quiz_id')
        question = str(request.form.get('question'))
        option1 = str(request.form.get('option1'))
        option2 = str(request.form.get('option2'))
        option3 = str(request.form.get('option3'))
        option4 = str(request.form.get('option4'))
        correct_answer = [int(i)
                          for i in (request.form.getlist('correct_answer'))]

        final_options = [option1, option2, option3, option4]
        final_correct_answer = []

        logger.info(str(correct_answer))

        for i in range(1, len(final_options) + 1):
            if i in correct_answer:
                final_correct_answer.append(1)
            else:
                final_correct_answer.append(0)

        logger.info(str(final_correct_answer))

        crud.insertQuestionandAnswer(
            question, course_id,  final_options, final_correct_answer, quiz_id)

        logger.info("course_id: {} question: {} option1: {} option2: {} option3: {} option4 : {} correct_answer: {} quiz_id: {}".format(
            course_id, question, option1, option2, option3, option4, final_correct_answer, quiz_id))

        return render_template('add_quiz_questions.html')

# -------------------------------------------------------------------------------------------------


@app.route('/view_quiz', methods=['GET', 'POST'])
def view_quiz():

    if request.method == 'GET':
        # --------------- Course Dropdown--------
        result = crud.getcourse()
        logger.info("result{}".format(result))
        if result:
            data = result
        else:
            data = None
# --------------- Quiznames Dropdown----------
        result1 = crud.get_Quiznames()
        if result1:
            data3 = result1
        else:
            data3 = None

        return render_template('view_quiz.html', courseadd=data, QuizNames=data3, quizes='',  ans='')

    else:

        cid = request.form.get('course_id')
        qu_id = request.form.get('quiz_id')

        logger.info("course_id {} quiz_id {}".format(cid, qu_id))

        result = crud.getcourse()
        logger.info("result{}".format(result))
        if result:
            data = result
        else:
            data = None

        result1 = crud.get_Quiznames()

        if result1:
            data3 = result1
        else:
            data3 = None

        ques, answ = crud.getquizquestion(cid, qu_id)
        logger.info("query {}".format(ques))

        if ques:
            data1 = ques
        else:
            data1 = None

        if answ:
            data2 = answ
        else:
            data2 = None

        return render_template('view_quiz.html', courseadd=data, QuizNames=data3, ans=data2, quizes=data1)

# -------------------------------------------------------------------------------------------------


@app.route('/show_studentquiz', methods=['GET', 'POST'])
def show_studentquiz():

    if request.method == 'GET':

        # --------------- Course Dropdown--------
        result = crud.getcoursesdropdown()

        if result:
            data = result
        else:
            data = None

        logger.info("result:{}".format(result))

        return render_template('show_studentquiz.html', courseadd=data, quizes='',  ans='')

    else:

        
        c_id = request.form.get('course_id')
        qu_id = request.form.get('quiz_id')

        result = crud.getcoursesdropdown()

        if result:
            data = result
        else:
            data = None

        result1 = crud.get_QuiznamesStudent(c_id)

        if result1:
            data3 = result1
        else:
            data3 = None

        logger.info("result1{}".format(result1))

        ques, answ = crud.studentQuizQuestions(qu_id, c_id)
        logger.info("ques:{}, answ:{}".format(ques, answ))

        if ques and answ:
            data1, data2 = ques, answ
            session['C_ID'] = c_id
            session['QU_ID'] = qu_id
        else:
            data1, data2 = None, None

        return render_template('show_studentquiz.html', courseadd=data,  QuizNames=data3, quizes=data1, ans=data2)

# -------------------------------------------------------------------------------------------------


@app.route('/result_studentquiz', methods=['GET', 'POST'])
def result_studentquiz():

    if request.method == 'POST':
        selected_ans = []
        c_id = session.get('C_ID')
        qu_id = session.get('QU_ID')
        logger.info("cid: {} quiz_id: {} ".format(c_id, qu_id))

        qauestion_count = crud.get_question_count(courseid=c_id, quizid=qu_id)
        logger.info("qauestion_count: {} ".format(qauestion_count))

        question_id = crud.get_question_id(courseid=c_id, quizid=qu_id)
        logger.info("question_id: {} ".format(str(question_id)))

        for i in question_id:
            a = request.form.getlist(i)
            print("a:", str(a))

            if len(a) < 1:
                selected_ans.append(("False"))
            else:

                if 'False' in a:
                    selected_ans.append(("False"))

                else:
                    selected_ans.append("True")


        logger.info("Final set: {}".format(selected_ans))

        score = round((len([i for i in selected_ans if i == 'True']) / qauestion_count) * 100.0, 2)

        logger.info("Final Score: {}".format(score))

        return render_template('results.html', score=score)


# -------------------------------------------------------------------------------------------------


@app.route('/my_courses', methods=['GET', 'POST'])
# @login_required
# @restricted(['teacher'])
def my_courses():
    if request.method == 'GET':

        # -----------Opted courses------
        result = crud.getstudentcourse()
        if result:
            data = result
        else:
            data = None
# ---------To add more courses-------
        result1 = crud.getallcourses()
        logger.info("result{} result1{}".format(result, result1))
        if result1:
            data1 = result1
        else:
            data1 = None

        return render_template('my_courses.html', courses=data, courseadd=data1)

    else:
        course_Names = request.form.getlist('course_id')

        logger.info("course_id: {} ".format(course_Names))

        crud.insertcourseafterlogin(course_Names)

        return redirect(url_for("my_courses"))

# -------------------------------------------------------------------------------------------------


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
