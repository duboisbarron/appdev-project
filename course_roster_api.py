"""

FIle lto abstract away Cornell's Course Roster API

"""

import requests


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
        arr = []
        if int(course['catalogNbr']) == course_no:
            try:
                arr.append(course['catalogDistr'])
            except Exception as e:
                arr.append("")
            try:
                arr.append(course['catalogSatisfiesReq'])
            except Exception as e:
                arr.append("")
            try:
                arr.append(course['catalogBreadth'])
            except Exception as e:
                arr.append("")

            return arr

    return ["Invalid Course"]


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

    print(resp.json())
    data = resp.json()

    subjects = []
    for subject in data['data']['subjects']:
        subjects.append(subject['value'])
    return subjects


