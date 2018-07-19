# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from .models import *


def index(request):
	return render(request, "reviewer/index.html.")

def register(request):
	errors = Users.objects.validate_user(request.POST)

	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error)
			return redirect('/')
	else:
		#assigns post data to a variable. 
		name = request.POST['name']
		alias = request.POST['alias']
		email = request.POST['email']
		password = request.POST['password']

		#generates a hashed password and generates a salt before being saved into the database. 
		#.encode turns it into a usable string
		hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

		#Saves password as the hashed password! not the password itself. 
		Users.objects.create(name=name, alias=alias, email=email, password=hashed_pw)

		#gets email, where email is request.POST['email'], stores new entry to the variable.
		user = Users.objects.get(email=email)
		#sets said entries id to a session id.
		#Django has the id field set to Autofield. No need to declare one in the model.
		request.session['id'] = user.id

		return redirect('/')

def login(request):

	email = request.POST['email']
	password = request.POST['password']
	
	#gets email where email 
	user = Users.objects.filter(email=email)

	
	
	if len(user) > 0:
		this_password = bcrypt.checkpw(password.encode(), user[0].password.encode())
		if this_password:
			request.session['id'] = user[0].id
			return redirect('/books')
		else:
			messages.error(request, "Incorrect username/password combination.")
			return redirect('/')

	else:
		messages.error(request, "User does not exist.")
		return redirect('/')		

def books(request):
	return render(request, 'reviewer/books.html')

