from API.TimeBlock import *
from random import choice

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
				#print("Not adding " + str(new_section) + ". Overlaps with " + str(existing_section))
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

	def convert_to_dict(self, colors_dict, colors):
		"""
		:param colors_dict: maps subject+course_id to a color
		:param colors: returns colors in order
		:return: 
		"""
		out = []

		for i, section in enumerate(self._sections):
			subject = section.get_course().get_subject()
			course_id = section.get_course().get_course_id()
			title = section.get_title()
			section_num = section.get_section_number()

			# sets the colors
			if subject+course_id not in colors_dict:
				color = next(colors)
				colors_dict[subject+course_id] = color

			color = colors_dict[subject + course_id]

			for block in section.get_time_blocks():
				block = block.get_as_dict()
				class_dict = dict()

				"""
				class_dict['crn'] = section.get_crn()
				class_dict['subject'] = section.get_course().get_subject()
				class_dict['course_id'] = section.get_course().get_course_id()
				class_dict['section_num'] = section.get_section_number()
				"""

				start = "2018-01-0{}T{}:{}".format(block["day"], block["start_hour"], block["start_minute"])
				end = "2018-01-0{}T{}:{}".format(block["day"], block["end_hour"], block["end_minute"])

				class_dict['title'] = subject + " " + course_id + " " + section_num + " - " + title
				class_dict['start'] = start
				class_dict['end'] = end
				class_dict['color'] = color

				out.append(class_dict)

		return out, colors_dict, colors
