

import os
import sys

import django

sys.path.append('..')
# you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Planit.Planit.settings")

django.setup()

from API.User import *

# your imports, e.g. Django models
from courses_database.models import WishList

from API.Section import *
from API.TimeBlock import *


'''
wish_list should be a list of dictionaries where each dictionary has
subject, course_id, and title as keys
'''
def compute_schedules(wish_list, filters):
	user = API_User()

	colors = ["#33B79B", "#CE5858", "#5869CE", "#BD4EAC"]
	colors_dict = {}

	for i, course in enumerate(wish_list):
		colors_dict[str(course['subject']) + str(course['course_id'])] = colors[i % len(colors)]
		user.add_to_wish_list(str(course['subject']), str(course['course_id']))

	for key in filters:
		print("Recieving filter - {" + str(key) + ": " + str(filters[key]) + "}")
		user.apply_filter(key, filters[key])
		pass

	# apply filters
	"""
	for x in user.get_all_schedules():
		print("NEW SCHEDULE")
		print(x)
		print()
	"""

	#print(user.get_all_schedules_as_dict())
	return user.get_all_schedules_as_dict(colors_dict)

