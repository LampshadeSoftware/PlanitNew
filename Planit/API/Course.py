import os
import sys

import django

sys.path.append('..')
# you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Planit.Planit.settings")

django.setup()

# your imports, e.g. Django models
from courses_database.models import Section

from API.Section import *
from API.TimeBlock import *

class API_Course:

	def __init__(self, subject, course_id):
		self._subject = subject
		self._course_id = course_id
		self._attributes = set()

		django_obj_set = Section.objects.all().filter(subject=subject, course_id=course_id)
		if len(django_obj_set) > 0:
			self._name = django_obj_set[0].title
			self._credits = int(django_obj_set[0].credit_hrs)
			for attr in django_obj_set[0].course_attr.split(','):
				self._attributes.add(attr)


		self._sections = []
		for section in django_obj_set:
			time_blocks = TimeBlock.get_time_blocks(section.meet_time)
			sec_object = API_Section(self, section.crn, section.section_number, time_blocks, section.title)
			self._sections.append(sec_object)

	def get_subject(self):
		return self._subject

	def get_course_id(self):
		return self._course_id

	def get_sections(self):
		return self._sections

	def num_credits(self):
		return self._credits

	def has_attribute(self, attribute):
		return attribute in self._attributes

	def __str__(self):
		return str(self._subject) + " " + str(self._course_id)

