import pymysql
import os
from flask import Flask, request, render_template, g, redirect, Response, session

###Define default LIMIT and OFFSET
LIMIT = 25
OFFSET = 0
class CourseResource:
    @classmethod
    def __init__(self):
        pass

    @staticmethod
    def _get_connection():
        #user = "admin"
        #password = "han990219"
        #h = 'e5156-database-1.coxz1yzswsen.us-east-1.rds.amazonaws.com'
        user = "admin"
        password = "1234567890"
        h = "e6156.coxz1yzswsen.us-east-1.rds.amazonaws.com"
        conn = pymysql.connect(
            user = user,
            password = password,
            host = h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_courses():
        sql = "SELECT * FROM courseswork_6156.Courses"
        conn = CourseResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        records = cur.fetchall()
        return records

    @staticmethod
    def get_course_name(course_name):
        sql = "SELECT * FROM courseswork_6156.Courses where Course_Name=%s LIMIT %s";
        course_name = course_name.strip()
        conn = CourseResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args = (course_name, LIMIT))
        records = cur.fetchall()
        #result = cur.fetchone()
        return records

    @staticmethod
    def add_course(course_name, department, introduction):
        if not (course_name and department):
            return False
        course_name, department = course_name.strip(), department.strip()
        conn = CourseResource._get_connection()
        cur = conn.cursor()
        #####judge if the course exists#####
        sql1 = """
        SELECT * From courseswork_6156.Courses 
        WHERE course_name = %s and department = %s
        """
        cur.execute(sql1, args=(course_name, department))
        records = cur.fetchall()
        if len(records) >= 1:
            return False
        #####################################
        sql2 = """
         insert into courseswork_6156.Courses (Course_Name, Department, CourseIntroduction)
         values (%s, %s, %s);
        """
        cur.execute(sql2, args = (course_name, department, introduction))
        result = cur.rowcount
        return True if result == 1 else False

    @staticmethod
    def add_student_preference(uni, course_id, timezone, dept, message):
        if not (uni and course_id and timezone and dept and message):
            return False, "Please fill in all blanks!"
        conn = CourseResource._get_connection()
        uni, course_id, timezone, dept, message = uni.strip(), course_id.strip(), timezone.strip(), dept.strip(), message.strip()
        cur = conn.cursor()
        #####judge if the preference exists#####
        sql1 = """
        SELECT * From courseswork_6156.student_preferences 
        WHERE uni = %s and Course_id = %s
        """
        cur.execute(sql1, args=(uni, int(course_id)))
        records = cur.fetchall()
        if len(records) >= 1:
            return False, "The course has been created!"
        ########################################
        sql2 = """
             insert into courseswork_6156.student_preferences 
             (uni, Course_id, prefered_Dept, prefered_Timezone, prefered_message)
             values (%s, %s, %s, %s, %s);
            """
        try:
            cur.execute(sql2, args=(uni, int(course_id), dept, timezone, message))
            return True, "Success"
        except:
            return False, "The course does not exist, please create course first!"

    @staticmethod
    def edit_student_preference(uni, course_id, timezone, dept, message):
        if not (uni and course_id and timezone and dept and message):
            return False
        sql1 = """
        SELECT * FROM courseswork_6156.student_preferences where Course_id = %s and uni = %s
        """
        conn = CourseResource._get_connection()
        uni, course_id, timezone, dept, message = uni.strip(), course_id.strip(), timezone.strip(), dept.strip(), message.strip()
        cur = conn.cursor()
        res = cur.execute(sql1, args=(course_id, uni))
        records = cur.fetchall()
        if len(records) < 1:
            return False
        sql2 = """
        UPDATE courseswork_6156.student_preferences 
        set prefered_Dept = %s, prefered_Timezone = %s, prefered_message = %s
        where uni = %s and Course_id = %s
        """;
        cur.execute(sql2, args=(dept, timezone, message, uni, int(course_id)))
        return True


    @staticmethod
    def get_course_preference_by_uni(uni, limit, offset):
        sql1 = "SELECT * FROM courseswork_6156.student_preferences where uni = %s";
        sql2 = "SELECT * FROM courseswork_6156.student_preferences where uni = %s LIMIT %s OFFSET %s";
        conn = CourseResource._get_connection()
        uni = uni.strip()
        cur = conn.cursor()
        res = cur.execute(sql1, args=(uni))
        records = cur.fetchall()
        length = len(records)
        res = cur.execute(sql2, args=(uni, int(limit), int(offset)))
        records = cur.fetchall()
        # result = cur.fetchone()
        return length, records


    @staticmethod
    def get_all_preference(uni):
        sql1 = "SELECT * FROM courseswork_6156.student_preferences where uni = %s";
        conn = CourseResource._get_connection()
        uni = uni.strip()
        cur = conn.cursor()
        res = cur.execute(sql1, args=(uni))
        records = cur.fetchall()
        return records


    @staticmethod
    def delete_course_preference_by_id_and_uni(uni, course_id):
        if not (course_id and uni):
            return False
        sql1 = """
        SELECT * FROM courseswork_6156.student_preferences where Course_id = %s and uni = %s
        """
        conn = CourseResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql1, args=(course_id, uni))
        records = cur.fetchall()
        if len(records) < 1:
            return False
        sql2 = "DELETE FROM courseswork_6156.student_preferences where Course_id = %s and uni = %s";
        cur.execute(sql2, args=(course_id, uni))
        return True
