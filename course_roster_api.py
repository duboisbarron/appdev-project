"""

FIle lto abstract away Cornell's Course Roster API

"""

import requests

def get_course_numbers(roster, subject):

    base_url = 'https://classes.cornell.edu/api/2.0/search/classes.json?'
    roster = 'roster=' + roster
    subject = 'subject=' + subject
    url = base_url + roster + '&' + subject

    resp = requests.get(url)
    data = resp.json()
    courses = data['data']['classes']

    course_numbers = []
    for course in courses:
        print(course['catalogNbr'])
        course_numbers.append(int(course['catalogNbr']))

    return course_numbers


def get_subjects(roster):
    base_url = 'https://classes.cornell.edu/api/2.0/config/subjects.json?roster='
    url = base_url + roster
    print(url)
    resp = requests.get(url)
    data = resp.json()
    return data['data']


