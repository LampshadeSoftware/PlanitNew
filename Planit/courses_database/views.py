from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Section, WishList
import json

import API.Interface as Interface


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
		print("data:", data)
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

		print("filters:", filters)
		# if there was a request it sends back the response
		if wishList:
			data = Interface.compute_schedules(list(wishList.values()), filters)
			#print("possible schedules:", data)
			if len(data) > 0:
				return JsonResponse(data, safe=False)
			else:
				return JsonResponse([[{}]], safe=False)
		else:
			# returns a default value
			return JsonResponse([[{}]], safe=False)
	else:
		return HttpResponse("You shouldn't be here... 0.0")
