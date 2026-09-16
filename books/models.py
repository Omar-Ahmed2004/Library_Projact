from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_year = models.PositiveIntegerField()
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books"
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )


    def __str__(self):
            return self.title



class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    returned = models.BooleanField(default=False)
    returned_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_overdue(self):
        return not self.returned and self.due_date < timezone.now().date()

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

