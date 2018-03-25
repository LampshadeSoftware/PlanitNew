
import os
import sys

import django

sys.path.append('..')
# you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Planit.Planit.settings")

django.setup()

from Planit.API.User import *

# your imports, e.g. Django models
from courses_database.models import WishList

from Planit.API.Section import *
from Planit.API.TimeBlock import *

def compute_schedules():
	user = API_User()

	wish_list = WishList.objects.all()
	for course in wish_list:
		user.add_to_wish_list(str(course.subject), str(course.course_id))

	# apply filters

	return user.get_all_schedules_as_dict()
