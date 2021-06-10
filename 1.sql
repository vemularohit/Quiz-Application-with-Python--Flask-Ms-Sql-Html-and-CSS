create table course(
ID int not null primary key identity(1,1),
userId int not null,
course varchar(100) Unique not null)


create table QuizNames(
id int primary key identity(1,1),
quiz_name varchar(50) not null,
course_id int foreign key references course(ID),
user_id int foreign key references Users(Id))


create table t_questions(
id int primary key identity(1,1),
question varchar(100),
course_id int foreign key references course(ID),
quiz_id int foreign key references QuizNames(id),
user_id int foreign key references Users(Id))


create table t_answers(
id int primary key identity(1,1),
answer varchar(100),
correct_ans bit,
q_id int foreign key references t_questions(id),
quiz_id int foreign key references QuizNames(id),
user_id int foreign key references Users(Id))


create table student_interest(
id int primary key identity(1,1),
user_id int foreign key references Users(ID),
student_interest int);


select * from course
select * from QuizNames
select * from t_questions
select *from Users
select * from student_interest
select * from QuizNames
select * from course
select * from t_answers


select quiz_name from QuizNames
inner join student_interest
on student_interest.student_interest = QuizNames.course_id
where course_id = 7

select quiz_name from QuizNames where course_id = 7

select answer from t_answers
where q_id = 41 




delete Users
where Id = 1050;

declare @user_id int = 2

insert into student_interest values(
@user_id, '1')

insert into student_interest values(
@user_id, '2')

insert into student_interest values(
@user_id, '3')