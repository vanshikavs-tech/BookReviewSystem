from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("book/<int:pk>/", views.book_detail, name="book_detail"),

    path("book/<int:pk>/review/", views.add_review, name="add_review"),

    path("book/add/", views.add_book, name="add_book"),

    path("review/<int:pk>/delete/", views.delete_review, name="delete_review"),

    path("signup/", views.signup, name="signup"),
]