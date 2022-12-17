from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *
from duckduckgo_search import ddg
import requests
import json
import geocoder
# Create your views here.

def index(request):
	tasks = Task.objects.all()

	form = TaskForm()

	if request.method =='POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/')


	context = {'tasks':tasks, 'form':form}
	return render(request, 'tasks/list.html', context)

def updateTask(request, pk):
	task = Task.objects.get(id=pk)

	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}

	return render(request, 'tasks/update_task.html', context)

def deleteTask(request, pk):
	item = Task.objects.get(id=pk)

	if request.method == 'POST':
		item.delete()
		return redirect('/')

	context = {'item':item}
	return render(request, 'tasks/delete.html', context)

def suggestions(request):
	if 'Tornado' in request.POST:
		key = "Tornado preparedness"
		supplies = ["1.Flashlight and extra batteries",
		"2.Water and food (canned food)","3.Warm clothes- coats, mittens, hats, blankets",
		"4.Cell phone, portable charger & extra batteries",
		"5.Candle",
		"6.Tools",
		"7.Battery powered radio",
		"8.First aid",
		"9.Store important documents or copies",
		"10.clothing tent, tarps"
		"11.whistle","12.sleeping gear","13.Road maps","14.Waterproof matches","15.Duct tape","16.Pet supplies","17.Fire extinguisher"
,"18.Sanitation supplies","19.Prescription Medicines (One week’s supply)","20.Mosquito repellent","21.Gloves"]
	elif 'Flood' in request.POST:
		key = "Floods preparedness"
		supplies = ["1.Flashlight and extra batteries",
		"2.Water and food (canned food)","3.Warm clothes- coats, mittens, hats, blankets",
		"4.Cell phone, portable charger & extra batteries",
		"5.Candle",
		"6.Tools",
		"7.Battery powered radio",
		"8.First aid",
		"9.Store important documents or copies",
		"10.clothing tent, tarps"
		"11.whistle","12.sleeping gear","13.Road maps","14.Waterproof matches","15.Duct tape","16.Pet supplies",
"17.Sanitation supplies","18.Prescription Medicines (One week’s supply)","19.Mosquito repellent","20.Gloves", "21. Raincoat", "22. Boots"]
	elif 'Cyclone' in request.POST:
		key = "Cyclone preparedness"
		supplies = ["1.Flashlight and extra batteries",
		"2.Water and food (canned food)","3.Warm clothes- coats, mittens, hats, blankets",
		"4.Cell phone, portable charger & extra batteries",
		"5.Candle",
		"6.Tools",
		"7.Battery powered radio",
		"8.First aid",
		"9.Store important documents or copies",
		"10.clothing tent, tarps"
		"11.whistle","12.sleeping gear","13.Road maps","14.Waterproof matches","15.Duct tape","16.Pet supplies","17.Fire extinguisher"
,"18.Sanitation supplies","19.Prescription Medicines (One week’s supply)","20.Mosquito repellent","21.Gloves"]
	else:
		key = "Disaster Management"
		supplies = ["Leave it to God :)"]

	#component = Component.objects.get(id=component_id)
	#print(component)
	#if(request.POST.get('tornado')):
		#key = "tornado preparedness"
	#elif(request.GET.get('Floods')):
		#key = "flood preparedness"
	#elif(request.GET.get('cyclones')):
		#key = "cyclone preparedness"
	context = {"result": ddg(keywords=key, max_results=5), "supplies": supplies}
	#return result
	return render(request,'tasks/suggestions.html', context)

#*args,**kwargs
def get_ip():
	response=requests.get("https://api64.ipify.org?format=json").json()
	return response["ip"]

def get_location():
	ip=geocoder.ip(get_ip())
	s=""
	for i in ip.latlng:
		s=s+", "+str(i)
	s = s[1:]
	return s

def nearby(request):
	if 'pharmacy' in request.POST:
		querystring = {"location":get_location(),"type":"pharmacy","radius":"5000","language":"en"}
	elif 'hospital' in request.POST:
		querystring = {"location":"18.60267940359643, 78.5148597206248","type":"hospital","radius":"5000","language":"en"}
	elif 'police_station' in request.POST:
		querystring = {"location":get_location(),"type":"police_station","radius":"10000","language":"en"}
	else:
		querystring = {"location":get_location(),"type":"fire_station","radius":"5000","language":"en"}
	url = "https://trueway-places.p.rapidapi.com/FindPlacesNearby"
	#querystring = {"location":"18.60267940359643, 78.5148597206248","type":type,"radius":"10000","language":"en"}
	headers = {
	"X-RapidAPI-Key": "b03ee82bbcmsh3579e3fca7285e5p1ce1a4jsnc7bb6182f40c",
	"X-RapidAPI-Host": "trueway-places.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	result = (response.text)
	jsonObject = json.loads(result)
	dicts = jsonObject['results']
	places = []
	print(dicts)
	for dict in dicts:
		place = ""
		place = place + dict["name"] + dict['address']
		places.append(place)


	context = {"places": places}
	return render(request,'tasks/nearby.html', context)
