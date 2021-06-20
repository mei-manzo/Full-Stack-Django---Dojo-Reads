from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from django.db.models import Count

def index(request):
    return render(request, "index.html")

def check_registration(request):
    errors = User.objects.basic_validator(request.POST)
    email = request.POST['email']
    if request.method == "GET":
        return redirect('/')
    elif len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    #changed to check len of dictionary
    elif len(User.objects.filter(email=email)) >= 1:
        messages.error(request, "Email is already in use")
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name = request.POST['first-name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed_pw)
        request.session['user_id'] = new_user.id
        return redirect('/books')

def check_login(request):
    if request.method == "GET":
        return redirect ("/")
    else:
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/books')

def check_review(request):
    if request.method == "GET":
        return redirect ("/books/add") #add id parameter
    else:
        errors = Book.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books/add')
        #if no issues, create a book
        if len(request.POST['author']) < 1:
            this_user = User.objects.get(id = request.session['user_id'])
            Book.objects.create(title=request.POST['title'], author=request.POST['author2'], review=request.POST['review'], rating=request.POST['rating'], who_reviewed=this_user)
            new_review = Book.objects.last() #might need to refine this, change to get request.session
            new_review.users_reviewed.add(this_user)
            return redirect(f"/books/{new_review.id}") 
        this_user = User.objects.get(id = request.session['user_id'])
        Book.objects.create(title=request.POST['title'], author=request.POST['author'], review=request.POST['review'], rating=request.POST['rating'], who_reviewed=this_user)
        new_review = Book.objects.last() #might need to refine this, change to get request.session
        new_review.users_reviewed.add(this_user)
        return redirect(f"/books/{new_review.id}") 

def check_new_review(request, id):
    if request.method == "GET":
        return redirect (f"/books/{id}") #add id parameter
    else:
        errors = Review.objects.new_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/books/{id}")
        this_user = User.objects.get(id = request.session['user_id'])
        book = Book.objects.get(id=id) #not fetching id?
        Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], user = this_user, book = Book.objects.get(id=id))
        new_review = Book.objects.last() #might need to refine this, change to get request.session
        return redirect(f"/books/{id}") 


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    all_users= User.objects.all()
    all_books=Book.objects.all()
    #make all_unique_books
    recent_reviews=Review.objects.all().order_by("-created_at")
    recent_three=[recent_reviews[0],recent_reviews[1], recent_reviews[2]]
    context = {
        "current_user" : this_user[0], #grabs from session rather than database to prevent refreshing into login
        "all_users": all_users,
        "all_books": all_books,
        "recent_three":recent_three,#changed to be recent reviews, not books
        }
    return render(request, "success.html", context)

def logout(request):
    request.session.flush()
    return redirect('/')

def add(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    all_users= User.objects.all()
    all_books = Book.objects.all()
    context = {
        "current_user" : this_user[0], #grabs from session rather than database to prevent refreshing into login
        "all_users": all_users,
        "all_books": all_books,
        }
    return render(request, "add_book_and_review.html", context)

def new_review(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    clicked_book = Book.objects.get(id=id)
    all_books = Book.objects.all()
    all_users= User.objects.all()
    context = {
        "current_user" : this_user[0], #grabs from session rather than database to prevent refreshing into login
        "all_users": all_users,
        "clicked_book": clicked_book,
        "all_books": all_books,
        }
    return render(request, "view_and_review.html", context)

def user(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=id)
    all_users= User.objects.all()
    total_reviews = Review.objects.filter(user_id=id).count()
    all_their_reviews = Review.objects.filter(user_id=id)
    context = {
        "current_user" : current_user, #grabs from session rather than database to prevent refreshing into login
        "all_users": all_users,
        "total_reviews": total_reviews,
        "all_their_reviews": all_their_reviews,
        }
    return render(request, "user_page.html", context)

def check_both(request):
    if request.method == "GET":
        return redirect ("/books/add") #add id parameter
    else:
        errors = Book.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books/add')
        errors = Review.objects.new_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books/add')
        title = request.POST['title']
        if len(Book.objects.filter(title=title)) >= 1:
            messages.error(request, "Book already exists")
            return redirect('/books/add')
        #if no issues, create a book
        this_user = User.objects.get(id = request.session['user_id'])
        new_book = Book.objects.create(title=request.POST['title'], author=request.POST['author'])
        # new_review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'])
        poster = User.objects.get(id=request.session['user_id'])
        book = Book.objects.get(id = new_book.id)
        Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], user = poster, book = book)
        new_review = Book.objects.last() #might need to refine this, change to get request.session
        # new_review.users_reviewed.add(this_user)
        return redirect(f"/books/{new_review.id}") 

def delete(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    review = Review.objects.get(id=id)
    this_user = User.objects.filter(id = request.session['user_id'])
    current_user = this_user[0]
    if current_user.id != review.user_id: #need to doctor this to match review owner
        return redirect('/')
    d = Review.objects.get(id=id)
    d.delete()
    book = review.book
    # return redirect(f"/books/{}")
    return redirect(f"/books/{book.id}")
