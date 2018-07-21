# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from .models import *
from django.contrib import messages


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
		print user

		return redirect('/')

def login(request):

	email = request.POST['email']
	password = request.POST['password']
	
	#filters and gets the email that is the request.POST
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
	#Basically if there is no session, which means there is no logged in user. This page cannot be accessed. So redirect to the index.
	#Where the user can login/register
	if not request.session['id']:
		return redirect ('/')

	context = {
		#User in the context of this template is to grab the user id of this session.
		#Books in this context is to grab all the books to be displayed in a list. 
		"user": Users.objects.get(id=request.session['id']),
		"books": Books.objects.all()
	}
	return render(request, 'reviewer/books.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')

def book_add(request):
	context = {
		"authors": Authors.objects.all()
	}
	return render(request, 'reviewer/book_add.html', context)

def save_book(request):
	Books.objects.validate_book(request.POST)

	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error)
			return redirect('/book_add')
	else:
		title = request.POST['title']
		if request.POST['author_name'] == "":
			author = Authors.objects.get(id=request.POST['author_menu'])
		else:
			errors = Authors.objects.validate_author(request.POST)
			author = Authors.objects.create(author=request.POST['author_name'])
		
		rating = request.POST['rating']
		review = request.POST['review']

		#takes the title/author post fields and saves them as a book to the database and assigns it to book.
		#then takes review,rating and the session id of user, as user and the book we just created and creates a review.
		book = Books.objects.create(title=title, author=author)
		Review.objects.create(content=review, rating=rating, user=Users.objects.get(id=request.session['id']), book=book)

		return redirect('/books/book.id')



