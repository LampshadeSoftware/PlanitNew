from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Section, WishList
import json

import API.Interface as Interface


def index(request):
	unique_sections = set()
	sections = []
	for section in Section.objects.all():
		subject, course_id = section.subject, section.course_id
		if subject + course_id not in unique_sections:
			sections.append(section)
			unique_sections.add(subject + course_id)

	return render(request, 'scheduler.html', {"sections": sections})


# Used to retrieve schedules from Daniel's code and return them to put in the calendar
def get_schedules(request):
	if request.POST:
		# processes the request
		data = request.POST
		keys = data.keys()
		wishList = {}
		filters = {}
		for key in keys:
			if "wishList" in key:
				# key format = wishList[crn#][attr] - (e.g. wishList[12712][subject])
				open_b = [pos for pos, char in enumerate(key) if char == "["]
				close_b = [pos for pos, char in enumerate(key) if char == "]"]
				crn = key[open_b[0]+1:close_b[0]]
				attr = key[open_b[1]+1:close_b[1]]
				wishList.setdefault(crn, {})[attr] = data[key]
			elif "filters" in key:
				filter_key = key[key.find("[")+1: key.find("]")]
				if filter_key == "day":
					filters.setdefault(filter_key, []).append(data[key])
				else:
					filters[filter_key] = data[key]

		default_response = {"schedules": [], "coursesInfo": {}}
		# if there was a request it sends back the response
		if wishList:
			schedules, courses_info = Interface.compute_schedules(list(wishList.values()), filters)
			return JsonResponse({"schedules": schedules, "coursesInfo": courses_info}, safe=False)
		else:
			# returns a default value
			return JsonResponse(default_response, safe=False)
	else:
		return HttpResponse("You shouldn't be here... 0.0")
