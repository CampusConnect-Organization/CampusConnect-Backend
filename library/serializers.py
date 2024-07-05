from rest_framework import serializers

from library.models import Book, BookInstance, BorrowRecord, ReturnRecord


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ["course"]


class BookInstanceSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source="book.title")

    class Meta:
        model = BookInstance
        exclude = ["book"]


class BorrowRecordSerializer(serializers.ModelSerializer):
    book_code = serializers.CharField(source="book_instance.book_number")
    book_name = serializers.CharField(source="book_instance.book.title")
    borrower = serializers.CharField(source="student.full_name")

    class Meta:
        model = BorrowRecord
        exclude = ["book_instance", "student"]


class ReturnRecordSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source="borrow_record.book_instance.book.title")
    borrowed_date = serializers.CharField(source="borrow_record.borrow_date")
    borrower = serializers.CharField(source="borrow_record.student.full_name")

    class Meta:
        model = ReturnRecord
        exclude = ["borrow_record"]
