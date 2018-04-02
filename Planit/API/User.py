from API.Course import *
from API.TimeBlock import *
from API.Schedule import *


class API_User:

	def __init__(self):

		# list of API_Course objects that the user might like to take
		self._wish_list = dict()

		# dictionary of filters for the possible schedules
		self._filters = dict()

		self._filters['earliest_time'] = None
		self._filters['latest_time'] = None

		self._filters['credit_min'] = 1
		self._filters['credit_max'] = 18

		self._filters['forbidden_days'] = set()
		#self.set_filter_forbidden_days('F', True)

		self._filters['desired_attributes'] = set()
		#self.set_filter_desired_attributes('CSI', True)

		# keeps track of all of the courses that actually end up in a possible schedule
		self._used_courses = set()


	def apply_filter(self, filter, value):
		if filter == 'startTime':
			self.set_filter_earliest_time(TimeBlock.get_readable_time(int(value)))

		elif filter == 'endTime':
			self.set_filter_latest_time(TimeBlock.get_readable_time(int(value)))

		elif filter == 'minCredits':
			self.set_filter_credit_min(value)

		elif filter == 'maxCredits':
			self.set_filter_credit_max(value)

		elif filter == 'daysOff':
			days = value.split(',')
			for day in days:
				self.set_filter_forbidden_days(day, True)

		elif filter == 'attr':
			attributes = value.split(',')
			for attr in attributes:
				self.set_filter_desired_attributes(attr, True)


	def set_filter_earliest_time(self, time):
		# print("Setting earliest time to: " + str(time))
		self._filters['earliest_time'] = str(time)

	def set_filter_latest_time(self, time):
		self._filters['latest_time'] = str(time)

	def set_filter_credit_min(self, amount):
		self._filters['credit_min'] = int(amount)

	def set_filter_credit_max(self, amount):
		self._filters['credit_max'] = int(amount)

	'''
	day in 'MTWRF'
	value = True or False
	'''
	def set_filter_forbidden_days(self, day, value):
		if value:
			self._filters['forbidden_days'].add(day)
		elif day in self._filters['forbidden_days']:
			self._filters['forbidden_days'].remove(day)

	def set_filter_desired_attributes(self, attribute, value):
		if value:
			self._filters['desired_attributes'].add(attribute)
		else:
			self._filters['desired_attributes'].remove(attribute)


	def add_to_wish_list(self, subject, course_id, optional=True):
		key = str(subject) + str(course_id)
		if key not in self._wish_list:
			course = API_Course(subject, course_id)
			self._wish_list[key] = [course, optional]
		else:
			pass
			# print(key + " already in wish list")

	def set_course_optional(self, subject, course_id, value):
		key = str(subject) + str(course_id)
		if key in self._wish_list:
			self._wish_list[key][1] = value

	def get_need_list(self):
		need_list = []

		for course in self._wish_list:
			if not self._wish_list[course][1]:
				need_list.append(self._wish_list[course][0])

		return need_list

	def get_want_list(self):
		want_list = []

		for course in self._wish_list:
			if self._wish_list[course][1]:
				want_list.append(self._wish_list[course][0])

		return want_list

	def get_all_schedules(self):

		# start with an empty schedule
		schedule = API_Schedule()

		# start recursive function
		return self._get_all_schedules_recursive(schedule, self.get_need_list(), False)

	def _get_all_schedules_recursive(self, locked_schedule, course_list, optional):
		possible_schedules = []
		# if we have added all our required courses, we can begin to add optional courses
		if len(course_list) == 0:
			if not optional:
				return self._get_all_schedules_recursive(locked_schedule, self.get_want_list(), True)
			else:
				if self.schedule_passes_final_filters(locked_schedule):
					# update used courses set
					self._used_courses.update(locked_schedule.get_course_set())
					return [locked_schedule]
				else:
					return []



		if optional:
			# add all derivative schedules that do not contain the top class on the wish list
			all_schedules_without = self._get_all_schedules_recursive(locked_schedule, course_list[1:], True)
			possible_schedules += all_schedules_without

		course = course_list[0]
		sections = course.get_sections()

		# for each potential section of this course...
		for section in sections:
			# if this section adheres to the filters...
			if self.section_passes_intermediate_filters(section):
				# make a copy of the previous schedule
				new_schedule = locked_schedule.copy()

				# try to add the new section. if it fails, ignore it and continue
				if not new_schedule.add_section(section):
					continue

				# if this new schedule passes the intermediate filters...
				if self.schedule_passes_intermediate_filters(new_schedule):

					# add all derivative schedules that DO contain this section
					all_schedules_with = self._get_all_schedules_recursive(new_schedule, course_list[1:], optional)
					possible_schedules += all_schedules_with

		return possible_schedules


	'''
	returns true if the given section is allowed through the filters
	'''
	def section_passes_intermediate_filters(self, section):
		# time interval is correct and doesn't occur on forbidden days
		for time_block in section.get_time_blocks():

			if self._filters['earliest_time'] is not None and not time_block.starts_after(self._filters['earliest_time']):
				return False

			if self._filters['latest_time'] is not None and not time_block.ends_before(self._filters['latest_time']):
				return False

			if time_block.get_day_char() in self._filters['forbidden_days']:
				return False
		return True

	'''
	returns true if the given schedule is allowed through the filters,
	returns false if the given schedule and all its derivative schedules are not allowed through the filters
	'''
	def schedule_passes_intermediate_filters(self, schedule):
		return True

	'''
	returns true if the given schedule is allowed through the filters,
	returns false if the given schedule is not allowed through the filters,
	however a derivative of this schedule MAY pass the filters
	'''
	def schedule_passes_final_filters(self, schedule):
		# check that schedule has more than min credits
		if self._filters['credit_min'] is not None and schedule.total_credits() < self._filters['credit_min']:
			return False

		# check that schedule has less than max credits
		if self._filters['credit_max'] is not None and schedule.total_credits() > self._filters['credit_max']:
			return False

		# check for all desired attributes
		for a in self._filters['desired_attributes']:
			for section in schedule.get_sections():
				if section.get_course().has_attribute(a):
					break
			else:
				return False

		return True

	def get_all_schedules_as_dicts(self):
		out = []
		for sched in self.get_all_schedules():
			out.append(sched.convert_to_dict())

		return out

	def get_interface_output(self, colors_dict):
		schedules = self.get_all_schedules_as_dicts()
		print(schedules)
		used_courses = dict()
		for key in self._used_courses:
			used_courses[key] = dict()
			used_courses[key]['color'] = colors_dict[key]

		return {'schedules': schedules, 'coursesInfo': used_courses}





