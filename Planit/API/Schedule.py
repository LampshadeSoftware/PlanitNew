from API.TimeBlock import *
from random import choice

class API_Schedule:

	def __init__(self):
		self._sections = set()
		self._num_credits = 0

	'''
	:param new_section: API.Section object
	:return: True if the add was successful, false if not
	'''
	def add_section(self, new_section):
		# check that we are not adding duplicate sections
		if new_section in self._sections:
			# print(str(new_section) + " already exists in schedule")
			return False

		# check that the class we are trying to add does not overlap with
		# any sections that already exist in this schedule
		for existing_section in self._sections:
			if existing_section.overlaps(new_section):
				# print("Not adding " + str(new_section) + ". Overlaps with " + str(existing_section))
				return False

		# add section to set and increment credit count
		self._sections.add(new_section)
		self._num_credits += new_section.get_course().get_num_credits()
		return True

	def total_credits(self):
		return self._num_credits

	def get_sections(self):
		return list(self._sections)

	'''
	:param other_schedule: API.Schedule object
	:return: true if the schedules are equal, false if not
	'''
	def equals(self, other_schedule):
		if len(self._sections) != len(other_schedule._sections):
			return False

		for section in self._sections:
			if section not in other_schedule._sections:
				return False

		return True

	'''
	:return: a new API.Schedule object that has all the same sections
	'''
	def copy(self):
		new = API_Schedule()
		new._sections = self._sections.copy()
		new._num_credits = self._num_credits
		return new


	def __str__(self):
		out = ""
		for day in TimeBlock.DAYS:
			out += str(day) + "\n"
			out += "---------\n"
			for section in self._sections:
				blocks = section.get_time_blocks_on_day(day)
				if len(blocks) > 0:
					out += str(section) + " -- "
					for time_block in blocks:
						out += str(time_block) + "\n"
			out += "\n"
		return out

	'''
	:param colors_dict: Dictionary, maps subject+course_id to a color
	:return: a list of dictionaries, where each dictionary represents a meet time
	of a section, with the keys:
		title
		start
		end
		color

	TODO: fix this so that each dictionary is one section, with another list of time
	block dictionaries for meet times
	'''
	def convert_to_dict(self):
		print("test")
		sched = dict()
		sched['total_credits'] = self.total_credits()

		sections = dict()

		for section in self._sections:

			section_dict = dict()
			section_dict['subject'] = section.get_course().get_subject()
			section_dict['course_id'] = section.get_course().get_course_id()
			section_dict['title'] = section.get_title()
			section_dict['section_num'] = section.get_section_number()
			section_dict['crn'] = section.get_crn()
			section_dict['num_credits'] = section.get_course().get_num_credits()
			section_dict['times'] = [x.get_as_dict() for x in section.get_time_blocks()]

			key = section_dict['subject'] + section_dict['course_id']
			sections[key] = section_dict

		sched['sections'] = sections

		return sched


