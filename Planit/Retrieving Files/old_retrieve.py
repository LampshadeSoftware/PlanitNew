import urllib.request
from bs4 import BeautifulSoup

import os
import django

# you have to set the correct path to you settings module
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Planit.settings")
# django.setup()

# your imports, e.g. Django models
# from catalog.models import Section

headers = ['crn', 'course_id', 'course_attr', 'title', 'instructor', 'credit_hrs', 'meet_time',
           'projected_enr', 'curr_enr', 'seats_avail', 'status']

all_classes = []


def save_course(section, subj):  # adds the course to the database
    section["subject"] = subj
    # setattr(section, "subject", subj)
    all_classes.append(section)
    # section.save()


def get_additional_info(crn, current_section, term=201910):
    url = "https://courselist.wm.edu/courselist/courseinfo/addInfo?fterm={}&fcrn={}".format(term, crn)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    descrip = soup.find_all("td")[0].text.split(" -- ")[2].strip()
    location = soup.find_all("td")[-1].text
    current_section["description"] = descrip
    current_section["location"] = location

    # setattr(current_section, "description", descrip)
    # setattr(current_section, "location", location)


def save_courses_for_subj(subj, term=201910):
    url = 'https://courselist.wm.edu/courselist/courseinfo/searchresults?term_code={}&term_subj={}&attr=' \
          '0&attr2=0&levl=0&status=0&ptrm=0&search=Search'.format(term, subj)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    entries = soup.find_all('td')
    current_section = None
    crn = None
    for i, entry in enumerate(entries):
        if i % len(headers) > 6:  # we don't need the last three column headers
            continue

        entry = entry.contents
        if i % len(headers) == 0:  # make a new section if we finished going through the last one
            entry = entry[1].string
            if current_section is not None:  # save the previous course before making a new one
                get_additional_info(crn, current_section)
                current_section
                save_course(current_section, subj)
            current_section = {}  # replace this with the Django class after testing
        else:
            entry = entry[0].replace(u'\xa0 ', '').strip()
        if headers[i % len(headers)] == "crn":
            crn = int(entry.strip("*"))
            entry = int(entry.strip("*"))

        # add the attribute
        current_section[headers[i % len(headers)]] = entry
        # setattr(current_section, headers[i % len(headers)], entry)

    if current_section is not None:
        get_additional_info(crn, current_section)
        save_course(current_section, subj)


def get_all_subject_courses():
    url = 'https://courselist.wm.edu/courselist/'
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    subj_codes = [x['value'] for x in soup.find('select', {'name': 'term_subj'}).findAll('option')[1:]]

    for subj_code in subj_codes:
        subject = Subject()
        subject.subj_id = subj_code
        subject.save()
        for course in save_courses_for_subj(subj_code):
            subject.courses.add(course)

# get_additional_info("16302", {})

save_courses_for_subj("CSCI")
print(all_classes[0].keys())
for course in all_classes:
    print(course)
    print()

