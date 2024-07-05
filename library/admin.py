from django.contrib import admin
from .models import Book, BookInstance, BorrowRecord, ReturnRecord


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "course")
    list_filter = ("category", "course")
    search_fields = ("title", "author", "category")


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "book_number")
    search_fields = ("book__title", "book__author", "book_number")


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ("book_instance", "student", "borrow_date")
    search_fields = (
        "book_instance__book__title",
        "book_instance__book__author",
        "student__first_name",
        "student__last_name",
    )


@admin.register(ReturnRecord)
class ReturnRecordAdmin(admin.ModelAdmin):
    list_display = ("borrow_record", "return_date")
    search_fields = (
        "borrow_record__book_instance__book__title",
        "borrow_record__book_instance__book__author",
        "borrow_record__student__first_name",
        "borrow_record__student__last_name",
    )

    def save_model(self, request, obj, form, change):
        obj.borrow_record.book_instance.borrowed = False
        obj.borrow_record.book_instance.save()
        super().save_model(request, obj, form, change)
