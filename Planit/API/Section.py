
class API_Section:

	'''
	crn: int representing the course registration number
	course: Course object representing the class of this section
	section_number: number of section
	time_blocks: list of TimeBlock objects representing the times that the section meets
	'''
	def __init__(self, course, crn, section_number, time_blocks, title):
		self._crn = crn
		self._course = course
		self._section_number = section_number

		self._time_blocks = time_blocks
		self._title = title


	def overlaps(self, other_section):
		for time_block in self._time_blocks:
			for other_time_block in other_section._time_blocks:
				if time_block.overlaps(other_time_block):
					return True

		return False

	def get_time_blocks(self):
		return self._time_blocks

	def get_time_blocks_on_day(self, day):
		out = []
		for time_block in self._time_blocks:
			if time_block.get_day_char() == day:
				out.append(time_block)
		return out

	def get_course(self):
		return self._course

	def get_crn(self):
		return self._crn

	def get_section_number(self):
		return self._section_number

	def get_title(self):
		return self._title

	def __str__(self):
		return str(self._course) + " " + str(self._section_number)