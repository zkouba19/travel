from __future__ import unicode_literals
from django import forms
from django.db import models
import re
import bcrypt
import datetime
# Create your models here.
class UserManager(models.Manager):
	def register(self, postData):
		errors = []
		email_taken = User.objects.filter(email = postData['email'])
		if email_taken:
			errors.append("Email is already in use. Please sign in or use a different email address")
		if len(postData['email']) < 1:
			errors.append('Email cannot be blank')
		elif not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', postData['email']):
			errors.append('email invalid')
		if len(postData['password']) < 1: 
			errors.append('Password cannot be empty')
		if not re.match(r'^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{8,32}$', postData['password']):
			errors.append('Password must be at least 8 characters, have atleast one capital letter, one number, and one special character')
		elif postData['confirm_password'] != postData['password']:
			errors.append('The passwords you entered do not match')
		if len(postData['first_name']) < 1:
			errors.append('First Name cannot be blank')
		if len(postData['last_name']) < 1:
			errors.append('Last Name cannot be blank')
		if errors == []:
			encrypt_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = encrypt_pw)
			user_valid = User.objects.get(email = postData['email'])
			return ["valid", user_valid]
		else: 
			return ["invalid", errors]

	def login(self, postData):
		errors = []
		user_exists = User.objects.filter(email = postData['email'])
		if not user_exists:
			errors.append('Email does not exist, please register above')
		if len(postData['email']) < 1:
			errors.append('Email cannot be blank')
		elif not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', postData['email']):
			errors.append('email invalid')
		if len(postData['password']) < 1: 
			errors.append('Password cannot be empty')
		if errors == []:
			user = User.objects.filter(email = postData['email'])
			hashed = user[0].password
			if bcrypt.hashpw(postData['password'].encode(), hashed.encode()) == hashed:
				return ["valid", user]
			else: 
				errors.append('Invalid Password, please try again!')
				return ["invalid", errors]
		else:
			return ["invalid", errors]


class TripManager(models.Manager):
	def new_trip(self, postData, id):
		errors = []
		if len(postData['destination']) < 1:
			errors.append('Destination cannot be empty')
		if len(postData['plan']) < 1:
			errors.append('Description cannot be empty')
		if len(postData['start_date']) < 1:
			errors.append('Start Date cannot be empty')
		if len(postData['end_date']) < 1:
			errors.append('End Date cannot be empty')
		if postData['end_date'] < postData['start_date']:
			errors.append('End Date must be after Start Date')
		if errors == []:
			users = User.objects.get(id = id)
			trip = Trip.objects.create(destination = postData['destination'], creator = id, start_date = postData['start_date'], end_date = postData['end_date'], plan = postData['plan'])
			trip.user.add(users)
			return [True, errors]
		else: 
			return [False, errors]

	def join_trip(self, user_id, trip_id):
		user = User.objects.get(id = user_id)
		trip = Trip.objects.get(id = trip_id)
		trip.user.add(user)
		return True



class User(models.Model):
	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	email = models.CharField(max_length = 100)
	password = models.CharField(max_length = 250)
	created_on = models.DateTimeField(auto_now_add = True)
	objects = UserManager()


class Trip(models.Model):
	creator = models.DecimalField(max_digits=7, decimal_places=0)
	destination = models.CharField(max_length = 100)
	start_date = models.CharField(max_length = 10)
	end_date = models.CharField(max_length = 10)
	plan = models.CharField(max_length = 250)
	user = models.ManyToManyField(User)
	created_on = models.DateTimeField(auto_now_add = True)
	objects = TripManager()






