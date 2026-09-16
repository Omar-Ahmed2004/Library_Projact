from django.shortcuts import render , get_object_or_404 , redirect
from .models import Book , Category , Author , Loan
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from accounts.decorators import librarian_required
from datetime import date, timedelta
from django.utils import timezone
from django.contrib import messages

# Create your views here.


@login_required
def book_list(request):
    search_query = request.GET.get("search")
    category_id = request.GET.get("category")
    author_id = request.GET.get("author")

    books = Book.objects.all()

    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query)
            | Q(author__name__icontains=search_query)
            | Q(category__name__icontains=search_query)
            | Q(isbn__icontains=search_query))



    if category_id:
        books = books.filter(category_id=category_id)

    if author_id:
        books = books.filter(author_id=author_id)

    categories = Category.objects.all()
    authors = Author.objects.all()

    return render(request, "books/book_list.html", {
        "books": books,
        "search_query": search_query,
        "categories": categories,
        "selected_category": category_id,
        "authors": authors,
        "selected_author": author_id,

    })

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book , id=book_id)

    return render(request, "books/book_detail.html", {
        "book": book
    })


@login_required
@librarian_required
def add_book(request):

    if request.method == "POST":

        title = request.POST.get("title")
        isbn = request.POST.get("isbn")
        publication_year = request.POST.get("publication_year")
        total_copies = request.POST.get("total_copies")
        category = request.POST.get("category")
        author = request.POST.get("author")

        if not all([
            title,
            isbn,
            publication_year,
            total_copies,
            category,
            author
        ]):
            messages.error(
                request,
                "Please fill in all fields."
            )

        elif Book.objects.filter(isbn=isbn).exists():
            messages.error(
                request,
                "A book with this ISBN already exists."
            )

        else:
            Book.objects.create(
                title=title,
                isbn=isbn,
                publication_year=publication_year,
                total_copies=total_copies,
                available_copies=total_copies,
                category_id=category,
                author_id=author,
            )

            messages.success(
                request,
                "Book added successfully."
            )

            return redirect("book_list")

    categories = Category.objects.all()
    authors = Author.objects.all()

    return render(request, "books/add_book.html", {
        "categories": categories,
        "authors": authors,
    })


@login_required
@librarian_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        title = request.POST.get("title")
        isbn = request.POST.get("isbn")
        publication_year = request.POST.get("publication_year")
        total_copies = request.POST.get("total_copies")
        category = request.POST.get("category")
        author = request.POST.get("author")

        if not all([
            title,
            isbn,
            publication_year,
            total_copies,
            category,
            author
        ]):
            messages.error(request, "Please fill in all fields.")

        elif Book.objects.filter(isbn=isbn).exclude(id=book.id).exists():
            messages.error(request, "This ISBN already exists.")

        else:
            old_total = book.total_copies
            old_available = book.available_copies

            new_total = int(total_copies)

            borrowed_copies = old_total - old_available

            if new_total < borrowed_copies:
                messages.error(
                    request,
                    "Total copies cannot be less than borrowed copies."
                )
            else:
                book.title = title
                book.isbn = isbn
                book.publication_year = publication_year
                book.total_copies = new_total
                book.available_copies = new_total - borrowed_copies
                book.category_id = category
                book.author_id = author

                book.save()

                messages.success(
                    request,
                    "Book updated successfully."
                )

                return redirect(
                    "book_detail",
                    book_id=book.id
                )

    return render(request, "books/edit_book.html", {
        "book": book,
        "categories": Category.objects.all(),
        "authors": Author.objects.all(),
    })

@login_required
@librarian_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.delete()

        messages.success(
            request,
            "Book deleted successfully."
        )

        return redirect("book_list")

    return render(request, "books/delete_book.html", {
        "book": book
    })



@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.available_copies <= 0:
        messages.error(request, "This book is not available.")
        return redirect("book_detail", book_id=book.id)

    if Loan.objects.filter(
        user=request.user,
        book=book,
        returned=False
    ).exists():
        messages.warning(
            request,
            "You already borrowed this book."
        )
        return redirect("book_detail", book_id=book.id)

    Loan.objects.create(
        user=request.user,
        book=book,
        due_date=date.today() + timedelta(days=7)
    )

    book.available_copies -= 1
    book.save()

    messages.success(
        request,
        "Book borrowed successfully."
    )

    return redirect("book_detail", book_id=book.id)



@login_required
def return_book(request, loan_id):
    loan = get_object_or_404(
        Loan,
        id=loan_id,
        user=request.user,
        returned=False
    )

    loan.returned = True
    loan.returned_at = timezone.now()
    loan.save()

    loan.book.available_copies += 1
    loan.book.save()

    messages.success(
        request,
        "Book returned successfully."
    )

    return redirect("my_loans")


@login_required
def my_loans(request):
    loans = Loan.objects.filter(
        user=request.user
    ).select_related("book")

    return render(request, "books/my_loans.html", {
        "loans": loans
    })


@login_required
def dashboard(request):
    total_books = Book.objects.count()

    available_books = sum(
        book.available_copies
        for book in Book.objects.all()
    )

    active_loans = Loan.objects.filter(
        returned=False
    ).count()

    overdue_loans = Loan.objects.filter(
        returned=False,
        due_date__lt=date.today()
    ).count()

    return render(request, "books/dashboard.html", {
        "total_books": total_books,
        "available_books": available_books,
        "active_loans": active_loans,
        "overdue_loans": overdue_loans,
    })