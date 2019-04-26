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
        requirement = api.get_reqs(roster, subject, course_no)
        requirements_fulfilled.append({roster + ' ' + subject + ' ' + str(course_no): requirement})
    return json.dumps({'success': True, 'data': requirements_fulfilled}), 201

    # for x in range(0, 1000):
    #     print(x)
    #     api.get_subjects("FA19")


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
