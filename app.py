import json
from flask import Flask, request
from db import db, Assignment, Class, User
import requests
import course_roster_api as api

app = Flask(__name__)

# pretty sure the db stuff here is trash for now
# db_filename = 'cms.db'
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
#
# db.init_app(app)
# with app.app_context():
#     db.create_all()
#


@app.route('/')
def root():
    return 'Hello world!'


def get_reqs(roster, subject, course_no):

    base_url = 'https://classes.cornell.edu/api/2.0/search/classes.json?'
    roster = 'roster=' + roster
    subject = 'subject=' + subject

    url = base_url + roster + '&' + subject

    r = requests.get(url)

    data = r.json()

    courses = data['data']['classes']

    # need to find the course number in the very long list
    for course in courses:
        # print(course['catalogNbr'])
        # print(course_no)
        if int(course['catalogNbr']) == course_no:
            return course['catalogDistr']

    return "class was not found.. probably user error"


@app.route('/api/dust/', methods=['POST'])
# @app.route('/api/classes/', methods=['POST'])
def create_class():
    post_body = json.loads(request.data)
    print(post_body)

    requirements_fulfilled = []

    for req in post_body:
        print(req)
        roster = req['semester'] + str(req['year'])
        subject = req['subject']
        course_no = req['number']
        requirement = get_reqs(roster, subject, course_no)
        requirements_fulfilled.append({roster + ' ' + subject + ' ' + str(course_no): requirement})
    return json.dumps({'success': True, 'data': requirements_fulfilled}), 201


@app.route('/api/numbers/', methods=['POST'])
def get_numbers():

    post_body = json.loads(request.data)
    roster = post_body['semester'] + str(post_body['year'])
    subject = post_body['subject']

    return json.dumps({'success': True, 'data': api.get_course_numbers(roster, subject)})


@app.route('/api/subjects/', methods=['POST'])
def get_subjects():

    post_body = json.loads(request.data)
    roster = post_body['semester'] + str(post_body['year'])
    return json.dumps({'success': True, 'data': api.get_subjects(roster)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
