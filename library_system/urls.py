from django.contrib import admin
from django.urls import path
from books.views import book_list, book_detail, add_book , edit_book , delete_book , borrow_book , return_book , my_loans , dashboard
from accounts.views import login_view, logout_view, register_view





urlpatterns = [

    path('admin/', admin.site.urls),

    path("books/", book_list, name="book_list"),
    path("books/<int:book_id>/", book_detail, name="book_detail"),

    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),

    path("books/add/", add_book, name="add_book"),
    path("books/<int:book_id>/edit/", edit_book, name="edit_book"),
    path("books/<int:book_id>/delete/", delete_book, name="delete_book"),

    path(
        "books/<int:book_id>/borrow/",
        borrow_book,
        name="borrow_book"
    ),

    path(
        "loans/",
        my_loans,
        name="my_loans"
    ),

    path(
        "loans/<int:loan_id>/return/",
        return_book,
        name="return_book"
    ),

    path(
        "dashboard/",
        dashboard,
        name="dashboard"
    ),
    
]
