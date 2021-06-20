from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('books', views.success),
    path('check_registration', views.check_registration),
    path('check_login', views.check_login),
    path('logout', views.logout),
    path('books/add', views.add),
    path('books/<int:id>', views.new_review), #add parameter id
    path('users/<int:id>', views.user), #add parameters
    path('check_review', views.check_review),
    path('check_book_and_review', views.check_both),
    path('check_new_review/<int:id>', views.check_new_review),
    path('delete/<int:id>', views.delete),
]