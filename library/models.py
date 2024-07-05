from datetime import datetime, timedelta
from django.db import models
from django.forms import ValidationError

from courses.models import Course
from student_profile.models import StudentProfile


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_number = models.CharField(max_length=100, unique=True)
    borrowed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title}({self.book_number})"


class BorrowRecord(models.Model):
    book_instance = models.ForeignKey(BookInstance, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.book_instance.borrowed:
            raise ValidationError("The book is already borrowed!")

        previous_return_records = ReturnRecord.objects.filter(
            borrow_record__book_instance=self.book_instance,
            borrow_record__student=self.student,
        ).order_by("-return_date")

        if previous_return_records.exists():
            latest_return_record = previous_return_records.first()
            if latest_return_record.return_date and latest_return_record.return_date > datetime.now().date():  # type: ignore
                raise ValidationError("The book has not been returned by the student.")

        super().save(*args, **kwargs)
        self.book_instance.borrowed = True
        self.book_instance.save()

    def __str__(self):
        return f"{self.book_instance.book.title} - {self.student.first_name}({self.book_instance.book_number})"


class ReturnRecord(models.Model):
    borrow_record = models.OneToOneField(BorrowRecord, on_delete=models.CASCADE)
    return_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.borrow_record.book_instance.borrowed = False
        self.borrow_record.returned = True
        self.borrow_record.book_instance.save(update_fields=["borrowed"])
        self.borrow_record.save(update_fields=["returned"])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.borrow_record.book_instance.book_number} - {self.borrow_record.student.full_name}"
