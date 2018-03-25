import urllib.request
from bs4 import BeautifulSoup

import os
import django
import sys

# you have to set the correct path to you settings module
sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Planit.Planit.settings")
django.setup()

# import the django module
from courses_database.models import Section


"""
WARNING, This code is sloppy... The tables we're not neatly arranged on the WAM website.
"""

headers = ['crn', 'course_id', 'course_attr', 'title', 'instructor', 'credit_hrs', 'meet_time',
	'projected_enr', 'curr_enr', 'seats_avail', 'status']


def save_course(section, subj):
	"""
	One save method in case we change the way that we're saving objects
	"""
	setattr(section, "subject", subj)
	section.save()


def get_additional_info(crn, current_section, term=201910):
	"""
	:param crn: the crn of the section we want the additional info from
	:param current_section: the Section object to which add the extra info
	:param term: the current term to search
	:return: None, it simply updates the mutable object "current_section"
	We do this in a separate function because the additional info comes from a different url
	"""
	url = "https://courselist.wm.edu/courselist/courseinfo/addInfo?fterm={}&fcrn={}".format(term, crn)
	html = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')
	descrip = soup.find_all("td")[0].text.split(" -- ")[2].strip()
	location = soup.find_all("td")[-1].text

	setattr(current_section, "description", descrip)
	setattr(current_section, "location", location)


def save_courses_for_subj(subj, term=201910):
	"""
	:param subj: The 4-character subject code as defined by WAM! example: CSCI
	:param term: the year/term
	:return: None, updates the database only
	"""
	url = 'https://courselist.wm.edu/courselist/courseinfo/searchresults?term_code={}&term_subj={}&attr=0&attr2=0&levl=0&status=0&ptrm=0&search=Search'.format(term, subj)
	html = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')

	entries = soup.find_all('td')
	current_section = None
	crn = None
	for i, entry in enumerate(entries):  # goes through every entry in the table. Every 11 entries is 1 section
		if i % len(headers) > 6:  # we don't need the any of the remaining columns
			continue

		entry = entry.contents
		if i % len(headers) == 0:  # When we get here, we need to create a new section to add entries into
			entry = entry[1].string
			if current_section is not None:  # save the previous section before making a new one
				get_additional_info(crn, current_section)
				save_course(current_section, subj)
			current_section = Section()  # creates a blank Section
		else:
			entry = entry[0].replace(u'\xa0 ', '').strip()  # string formatting
		if headers[i % len(headers)] == "crn":  # converts the crn to an int
			crn = int(entry.strip("*"))
			entry = int(entry.strip("*"))
		elif headers[i % len(headers)] == "course_id":  # converts the crn to an int
			course_id, section_number = entry.strip().split(" ")[1:]
			setattr(current_section, "course_id", course_id)
			setattr(current_section, "section_number", section_number)
			continue

		# add the attribute to the current_section that we're on
		setattr(current_section, headers[i % len(headers)], entry)

	if current_section is not None:  # this just adds the last section since the for loop doesn't save the last one
		get_additional_info(crn, current_section)
		save_course(current_section, subj)


def get_all_subject_courses():
	url = 'https://courselist.wm.edu/courselist/'
	html = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')
	subj_codes = [x['value'] for x in soup.find('select', {'name': 'term_subj'}).findAll('option')[1:]]

	for subj_code in subj_codes:  # all the subjects are at different urls so this just goes through them all
		save_courses_for_subj(subj_code)

get_all_subject_courses()
