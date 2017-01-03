from django.shortcuts import render, redirect, HttpResponse
from .models import User, Trip
import bcrypt
from django.contrib import messages, sessions
# Create your views here.
def index(request):
	if "id" not in request.session:
		request.session['id'] = ""
	return render(request, 'belt_app/index.html')

def register(request):
	if request.method == "POST":
		valid_fields = User.objects.register(request.POST)
		if valid_fields[0] == "valid":
			request.session['id'] = valid_fields[1].id
			return redirect('/homepage')
		else:
			for i in valid_fields[1]:
				messages.error(request, i)
			return redirect('/')

def login(request):
	valid_login = User.objects.login(request.POST)
	if valid_login[0] == "valid":
		request.session['id'] = valid_login[1][0].id
		return redirect('/homepage')
	else:
		for i in valid_login[1]:
			messages.error(request, i)
		return redirect('/')

def logout(request):
	request.session.clear()
	return redirect('/')

def home(request):
	return redirect('/homepage')

def homepage(request):
	if not request.session['id']:
		return render('/')
	user = User.objects.filter(id = request.session['id'])
	context = {
		'my_trips': Trip.objects.filter(user = request.session['id']),
		'new_trips': Trip.objects.all().exclude(user = request.session['id']),
		'user': user,
		'all_trips': Trip.objects.all()
	}
	return render(request, 'belt_app/homepage.html', context)

def newtrip(request):
	return render(request, 'belt_app/new_trip.html')

def add_trip(request):
	valid_trip = Trip.objects.new_trip(request.POST, request.session['id'])
	if valid_trip[0] == True:
		return redirect('/homepage')
	else:
		for i in valid_trip[1]:
			messages.error(request, i)
		return redirect('/newtrip')

def join(request, id):
	Trip.objects.join_trip(user_id = request.session['id'], trip_id = id)
	return redirect('/homepage')

def viewtrip(request, id):
	trip = Trip.objects.get(id = id)
	context = {
	'trips': trip,
	}
	return render(request, 'belt_app/trip.html', context)


	




