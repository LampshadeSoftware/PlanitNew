from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Section, WishList
import json

import API.Interface as Interface

last_get = None


# Create your views here.
def home(request):
	global last_get

	if request.POST:
		if request.GET.get('rem_id', None) is not None:
			rem_id = request.GET.get('rem_id', None)
			rem_subj = request.GET.get('rem_subj', None)
			WishList.objects.all().filter(course_id=rem_id, subject=rem_subj).delete()
		else:
			wish_subject = request.GET.get('wish_subject', None)
			wish_course_id = request.GET.get('wish_course_id', None)
			new_wish_item = WishList()
			setattr(new_wish_item, "course_id", wish_course_id)
			setattr(new_wish_item, "subject", wish_subject)
			new_wish_item.save()
			request = last_get
	else:
		last_get = request

	wishlist = WishList.objects.all()
	sections = {}

	subject = request.GET.get('term_subj', None)
	course_id = request.GET.get('course_id', None)
	if subject:  # if we got a valid GET request
		sections = Section.objects.all()

		# deals with getting a specified subject
		if subject != "0":
			sections = sections.filter(subject=subject)

		# deals with getting a specified course_id
		if course_id != "":
			sections = sections.filter(course_id=course_id)

		# gets rid of repeats
		already_added = set()
		no_repeats = []
		for section in sections:
			if section.title not in already_added:
				no_repeats.append({"subject": section.subject, "course_id": section.course_id, "title": section.title})
			already_added.add(section.title)
		sections = no_repeats

	index = 1
	if request.GET:
		index = request.GET.get("schedulenum", 1)

	schedules = Interface.compute_schedules()
	indices = [i + 1 for i in range(len(schedules))]
	schedule = []
	try:
		schedule = schedules[int(index) - 1]
	except:
		pass

	# sends the response
	return render(request, 'boot.html', {'sections': sections, "schedule": schedule, "num_schedules": len(schedules), "wishlist": wishlist, "indices": indices, "index": index})


def index(request):
	return render(request, 'scheduler.html', {"sections": Section.objects.all()})


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
				filters[key[key.find("[")+1: key.find("]")]] = data[key]

		print(filters)
		# if there was a request it sends back the response
		if wishList:
			data = Interface.compute_schedules(list(wishList.values()))
			print("possible schedules:", data)
			if len(data) > 0:
				return JsonResponse(data, safe=False)
			else:
				return JsonResponse([[{}]], safe=False)
		else:
			# returns a default value
			return JsonResponse([[{}]], safe=False)
	else:
		return HttpResponse("You shouldn't be here... 0.0")
