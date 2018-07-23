from django.conf.urls import url
from . import views           
urlpatterns = [
  url(r'^$', views.index),
  url(r'^register$', views.register),
  url(r'^login$', views.login),
  url(r'^books$', views.books),
  url(r'^logout$', views.logout),
  url(r'^add$', views.book_add),
  url(r'^save/book$', views.save_book),
  url(r'^books/(?P<id>\d+)$', views.show_book)


]