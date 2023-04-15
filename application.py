from flask import Flask, Response, request
from flask import Flask, request, render_template, g, redirect, Response, session
from datetime import datetime
import json
from courses_resource import CourseResource
from flask_cors import CORS
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# TODO: INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'longer-secret-is-better'
CORS(app)

@app.route("/", methods = ['GET'])
def init():
    return "hello world"

@app.route("/courses/", methods=["GET"])
def get_courses():
    result = CourseResource.get_courses()
    print(result)
    rsp = Response(json.dumps(result), status=200, content_type="application.json")
    return rsp



@app.route("/course/", methods=["GET"])
def get_course_by_name(course_name = ""):
    if "course_name" in request.args:
        course_name = request.args["course_name"]
    result = CourseResource.get_course_name(course_name)
    print(result)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/course/add", methods=["POST"])
def insert_courses():
    if request.is_json:
        try:
            request_data = request.get_json()
        except ValueError:
            return Response("[COURSE] UNABLE TO RETRIEVE REQUEST", status=400, content_type="text/plain")
    else:
        return Response("[COURSE] INVALID POST FORMAT: SHOULD BE JSON", status=400, content_type="text/plain")
    if not request_data:
        rsp = Response("[COURSE] INVALID INPUT", status=404, content_type="text/plain")
        return rsp
    course_name, department, introduction = request_data['course_name'], request_data['department'], request_data['introduction']
    result = CourseResource.add_course(course_name, department, introduction)
    if result:
        rsp = Response("COURSE CREATED", status=200, content_type="text/plain")
    else:
        rsp = Response("There already exist one course", status=404, content_type="text/plain")
    return rsp


@app.route("/course/student_preference/add",methods=["POST"])
def add_course_preference():
    if request.is_json:
        try:
            request_data = request.get_json()
        except ValueError:
            return Response("[COURSE] UNABLE TO RETRIEVE REQUEST", status=400, content_type="text/plain")
    else:
        return Response("[COURSE] INVALID POST FORMAT: SHOULD BE JSON", status=400, content_type="text/plain")
    if not request_data:
        rsp = Response("[COURSE] INVALID INPUT", status=404, content_type="text/plain")
        return rsp
    uni, course_id, timezone, dept, message = request_data['uni'], request_data['course_id'], request_data['timezone'], \
                                              request_data['Dept'], request_data['message']
    result, message = CourseResource.add_student_preference(uni, course_id, timezone, dept, message)
    if result:
        rsp = Response("Course Preferences CREATED", status=200, content_type="text/plain")
    else:
        rsp = Response(message, status=404, content_type="text/plain")
    return rsp

@app.route("/course/student_preference/edit/", methods=["GET", "POST"])
def edit_course_preference():
    if request.is_json:
        try:
            request_data = request.get_json()
        except ValueError:
            return Response("[COURSE] UNABLE TO RETRIEVE REQUEST", status=400, content_type="text/plain")
    else:
        return Response("[COURSE] INVALID POST FORMAT: SHOULD BE JSON", status=400, content_type="text/plain")
    if not request_data:
        rsp = Response("[COURSE] INVALID INPUT", status=404, content_type="text/plain")
        return rsp
    uni, course_id, timezone, dept, messages = request_data['uni'], request_data['course_id'], request_data['timezone'], request_data['Dept'], request_data['message']
    result = CourseResource.edit_student_preference(uni, course_id, timezone, dept, messages)
    if result:
        rsp = Response("Course Preferences CREATED", status=200, content_type="text/plain")
    else:
        rsp = Response("The preference does not exist", status=404, content_type="text/plain")
    return rsp


@app.route("/course/student_preference/", methods=["GET"])
def get_course_preference_by_uni(uni = "", limit = "", offset = ""):
    if "uni" in request.args and "limit" in request.args and "offset" in request.args:
        uni, limit, offset = request.args["uni"], request.args["limit"], request.args["offset"]
    result = CourseResource.get_course_preference_by_uni(uni, limit, offset)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/course/student_preferences/uni=<uni>", methods=["GET"])
def get_all_preference(uni):
    result = CourseResource.get_all_preference(uni)
    print(result)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/course/student_preference/delete/",methods=["POST", "GET"])
def delete_course_preference_by_id_and_uni():
    if request.is_json:
        try:
            request_data = request.get_json()
        except ValueError:
            return Response("[COURSE] UNABLE TO RETRIEVE REQUEST", status=400, content_type="text/plain")
    else:
        return Response("[COURSE] INVALID POST FORMAT: SHOULD BE JSON", status=400, content_type="text/plain")
    if not request_data:
        rsp = Response("[COURSE] INVALID INPUT", status=404, content_type="text/plain")
        return rsp
    uni, course_id = request_data['uni'], request_data['course_id']
    print(uni, course_id)
    result = CourseResource.delete_course_preference_by_id_and_uni(uni, course_id)
    if result:
        rsp = Response("DELETE SUCCESS", status=200, content_type="application.json")
    else:
        rsp = Response("No existed Preference is found!", status=404, content_type="text/plain")
    return rsp

app.run(host="0.0.0.0", port=5011)