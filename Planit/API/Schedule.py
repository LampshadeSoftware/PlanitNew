from API.TimeBlock import *
from random import randint

class API_Schedule:

	def __init__(self):
		self._sections = set()
		self._num_credits = 0


	def add_section(self, new_section):
		if new_section in self._sections:
			print(str(new_section) + " already exists in schedule")
			return False

		for existing_section in self._sections:
			if existing_section.overlaps(new_section):
				print("Not adding " + str(new_section) + ". Overlaps with " + str(existing_section))
				return False

		self._sections.add(new_section)
		self._num_credits += new_section.get_course().num_credits()
		return True

	def total_credits(self):
		return self._num_credits

	def get_sections(self):
		return list(self._sections)

	def equals(self, other_schedule):
		if len(self._sections) != len(other_schedule._sections):
			return False

		for section in self._sections:
			if section not in other_schedule._sections:
				return False

		return True

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

	def convert_to_dict(self):
		out = []

		r = randint(50, 255)
		g = randint(50, 255)
		b = randint(50, 255)

		for section in self._sections:
			for block in section.get_time_blocks():
				block = block.get_as_dict()
				class_dict = dict()

				"""
				class_dict['crn'] = section.get_crn()
				class_dict['subject'] = section.get_course().get_subject()
				class_dict['course_id'] = section.get_course().get_course_id()
				class_dict['section_num'] = section.get_section_number()
				"""

				subject = section.get_course().get_subject()
				course_id = section.get_course().get_course_id()
				section_num = section.get_section_number()
				start = "2018-01-0{}T{}:{}".format(block["day"], block["start_hour"], block["start_minute"])
				end = "2018-01-0{}T{}:{}".format(block["day"], block["end_hour"], block["end_minute"])

				class_dict['title'] = subject + " " + course_id + " " + section_num
				class_dict['start'] = start
				class_dict['end'] = end

				out.append(class_dict)

		return out
