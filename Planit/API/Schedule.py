from Planit.API.TimeBlock import *

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
		out = dict()

		for section in self._sections:
			crn = section.get_crn()
			out[crn] = dict()

			out[crn]['subject'] = section.get_course().get_subject()
			out[crn]['course_id'] = section.get_course().get_course_id()
			out[crn]['section_num'] = section.get_section_number()


			out[crn]['times'] = dict()
			k = 0
			for block in section.get_time_blocks():
				out[crn]['times'][k] = block.get_as_dict()
				k += 1

			out[crn]['total_credits'] = self._num_credits


		return out