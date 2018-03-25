
class TimeBlock:

	DAYS = ['M', 'T', 'W', 'R', 'F']

	'''
	returns a list of time blocks, repeating the start/end times for the given days
	ex: time_str = 'MWF:1000-1050'
	'''
	@classmethod
	def get_time_blocks(cls, time_str):
		colon_index = time_str.index(':')
		days = time_str[:colon_index]

		start_time = time_str[-9:-5]
		end_time = time_str[-4:]

		blocks = []
		for day in days:
			blocks.append(TimeBlock(start_time, end_time, day))

		return blocks

	@classmethod
	def convert_string(cls, time_str):
		hour = int(time_str[:2])
		minute = int(time_str[2:])
		time = hour * 60 + minute

		return time

	@classmethod
	def get_readable_time(cls, time):
		return format((time // 60), '02d') + format((time % 60), '02d')


	def __init__(self, start_str, end_str, day):

		self._start = TimeBlock.convert_string(start_str)
		self._end = TimeBlock.convert_string(end_str)

		self._day_index = TimeBlock.DAYS.index(day)

	def __str__(self):
		out = TimeBlock.DAYS[self._day_index]
		out += ": " + TimeBlock.get_readable_time(self._start)
		out += "-" + TimeBlock.get_readable_time(self._end)
		return out


	def get_start(self):
		return self._start

	def get_end(self):
		return self._end

	def get_day_char(self):
		return TimeBlock.DAYS[self._day_index]

	def get_day_index(self):
		return self._day_index

	def get_as_list(self):
		return [self.get_day_char(), self._start, self._end]

	def get_as_dict(self):
		out = dict()
		out['day'] = self.get_day_index()
		out['start'] = TimeBlock.get_readable_time(self._start)
		out['end'] = TimeBlock.get_readable_time(self._end)
		return out

	def overlaps(self, other_block):
		if self._day_index != other_block._day_index:
			return False

		if self._start < other_block._start:
			if self._end < other_block._start:
				return False
			else:
				return True
		else:
			if self._start < other_block._end:
				return True
			else:
				return False

	def starts_after(self, time_str):
		return self._start >= TimeBlock.convert_string(time_str)

	def ends_before(self, time_str):
		return self._end <= TimeBlock.convert_string(time_str)
