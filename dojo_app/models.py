from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        email = postData['email']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first-name']) <2:
            errors["first_name"]="First name should be at least 2 characters"
        if len(postData['alias']) <2:
            errors["alias"]="Alias should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):             
            errors['email'] = ("Invalid email address!")
        if len(postData['password']) < 8:
            errors["password"]="Password must be at least 8 characters"
        if postData['password'] != postData['confirm-password']:
            errors["password"]="Passwords do not match"
        return errors
        
    def login_validator(self, postData):
        errors = {}
        email = postData['email']
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Must enter an email"
            return errors
        if len(User.objects.filter(email=email)) == 0:
            errors['email'] = "Email is not registered"
            return errors
        if len(postData['password']) < 8:
            errors['password'] = "Must enter a password 8 characters or longer"
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['password'] = "Email and password do not match"
        return errors

class BookManager(models.Manager): #title required # desc at least 5 chars
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) <1:
            errors["title"]="Must enter a title"
        if len(postData['author']) <1 and len(postData['author2']) <1:
            errors['author']="Must enter an author"
        return errors

class ReviewManager(models.Manager):
    def new_validator(self, postData):
        errors = {}
        if len(postData['review']) <5:
            errors["review"]="Review must be at least 5 characters."
        if postData['rating'] != "1" and postData['rating'] != "2" and postData['rating'] != "3" and postData['rating'] != "4" and postData['rating'] != "5":
            errors['rating'] = "Choose a rating between 1 and 5"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length= 255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # who_uploaded = models.ForeignKey(User, related_name="books", on_delete = models.CASCADE, null = True)
    # users_reviewed = models.ManyToManyField(User, related_name="Books")
    objects = BookManager()

class Review(models.Model):
    user = models.ForeignKey(User, related_name="reviews", on_delete = models.CASCADE)
    book = models.ForeignKey(Book, related_name="book_reviews", on_delete = models.CASCADE)
    review = models.TextField()
    rating = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()