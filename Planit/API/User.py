from Planit.API.Course import *
from Planit.API.TimeBlock import *
from Planit.API.Schedule import *


class API_User:

	def __init__(self):

		# list of API_Course objects that the user might like to take
		self._wish_list = dict()

		# dictionary of filters for the possible schedules
		self._filters = dict()

		self._filters['earliest_time'] = None
		self._filters['latest_time'] = None

		self._filters['credit_min'] = 5
		self._filters['credit_max'] = 18

		self._filters['forbidden_days'] = set()

		self._filters['desired_attributes'] = set()



	def set_filter_earliest_time(self, time):
		self._filters['earliest_time'] = TimeBlock.convert_string(time)

	def set_filter_latest_time(self, time):
		self._filters['latest_time'] = TimeBlock.convert_string(time)

	def set_filter_credit_min(self, amount):
		self._filters['credit_min'] = amount

	def set_filter_credit_max(self, amount):
		self._filters['credit_max'] = amount

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


	def add_to_wish_list(self, subject, course_id):
		key = str(subject) + str(course_id)
		if key not in self._wish_list:
			course = API_Course(subject, course_id)
			self._wish_list[key] = [course, True]
		else:
			print(key + " already in wish list")

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

	def get_all_schedules_as_dict(self):
		out = dict()
		i = 1
		for sched in self.get_all_schedules():
			out[i] = sched.convert_to_dict()
			i += 1

		return out

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
				# if the new schedule also passes the final filters, it is technically a valid schedule, even though
				# we might be able to add more to it
				if self.schedule_passes_final_filters(locked_schedule):
					possible_schedules.append(locked_schedule)
				return self._get_all_schedules_recursive(locked_schedule, self.get_want_list(), True)
			else:
				if self.schedule_passes_final_filters(locked_schedule):
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







