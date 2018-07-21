# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.db import models

class UserManager(models.Manager):
	def validate_user(request, postData):
		errors = []

		#Name validation
		if len(postData['name']) < 2:
			errors.append("Name must be 2 characters or more in length")

		#Email validation
		if len(postData['email']) < 4:
			errors.append("Email must be more than 8 characters in length")


		#Password Validation
		if len(postData['password']) < 8:
			errors.append("Password must be at least 8 characters")

		#Password match validation
		if postData['password'] != postData['cnfrm_password']:
			errors.append("Passwords do not match")

		return errors

class BooksManager(models.Manager):
	def validate_book(request, postData):
		errors = []

		#Title validation
		if len(postData['title']) < 2:
			errors.append("Title name is too short")

		if len(postData['author']) < 2:
			errors.append("The summary must be more than 10 characters long")

		return errors

class ReviewManager(models.Manager):
	def validate_review(request, postData):
		errors = []

		if len(postData['title']) < 2:
			errors.append("The title is too short")

		if len(postData['content']) < 10:
			errors.append("Content must be more than 10 characters long")

		return errors

class AuthorManager(models.Manager):
	def validate_author(request, postData):
		errors = []

		if len(postData['author_name']) < 2:
			errors.append("The name must be longer than 2 characters long")

		return errors




class Users(models.Model):
	#Django has the id field set to Autofield. No need to declare one in the model.
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Books(models.Model):
	#Django has the id field set to Autofield. No need to declare one in the model.
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = BooksManager()

class Review(models.Model):
	#Django has the id field set to Autofield. No need to declare one in the model.
	title = models.CharField(max_length=255)
	content = models.CharField(max_length=255)
	rating = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	book = models.ForeignKey(Books, related_name="reviews")
	user = models.ForeignKey(Users, related_name="reviews")
	objects = ReviewManager()

class Authors(models.Model):
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = AuthorManager()

