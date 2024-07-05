from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from library.models import Book, BookInstance, BorrowRecord, ReturnRecord
from core.response import CustomResponse

from library.serializers import (
    BookInstanceSerializer,
    BookSerializer,
    BorrowRecordSerializer,
    ReturnRecordSerializer,
)


class BookListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get(self, request):
        books = Book.objects.all()

        serializer = self.serializer_class(instance=books, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="Books fetched successfully!",
        )


class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get(self, request, pk: int):
        book = Book.objects.filter(id=pk).first()
        if not book:
            return CustomResponse.error(
                message=f"Book with ID {pk} doesn't exist!",
            )
        serializer = self.serializer_class(instance=book)
        return CustomResponse.success(
            data=serializer.data, message="Book fetched successfully!"
        )


class BookInstanceListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookInstanceSerializer

    def get(self, request, pk: int):
        book_instances = BookInstance.objects.filter(book__id=pk).all()
        if not book_instances:
            return CustomResponse.error(
                message=f"Book with ID {pk} doesn't have any instances"
            )
        serializer = self.serializer_class(instance=book_instances, many=True)

        return CustomResponse.success(
            data=serializer.data,
            message=f"Book instances of book with ID {pk} fetched successfully!",
        )


class BookBorrowView(APIView):
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk: int):
        book_instance = BookInstance.objects.filter(id=pk).first()
        if not book_instance:
            return CustomResponse.error("Book instance not found!")
        borrow_record = BorrowRecord.objects.create(
            book_instance=book_instance, student=request.user.studentprofile
        )

        serializer = self.serializer_class(instance=borrow_record)

        return CustomResponse.success(
            data=serializer.data, message="Book borrowed successfully!"
        )


class BookBorrowListView(APIView):
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        borrow_records = (
            BorrowRecord.objects.filter(student=request.user.studentprofile)
            .all()
            .order_by("-id")
        )

        serializer = self.serializer_class(instance=borrow_records, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Book borrows fetched succesfully!"
        )


class BookReturnView(APIView):
    serializer_class = ReturnRecordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk: int):
        borrow_record = BorrowRecord.objects.filter(id=pk).first()
        if not borrow_record:
            return CustomResponse.error("Borrow record not found!")

        return_record = ReturnRecord.objects.create(borrow_record=borrow_record)
        borrow_record.book_instance.borrowed = False
        borrow_record.book_instance.save()

        serializer = self.serializer_class(instance=return_record)

        return CustomResponse.success(
            data=serializer.data, message="Book returned successfully!"
        )


class BookReturnListView(APIView):
    serializer_class = ReturnRecordSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return_records = ReturnRecord.objects.filter(
            borrow_record__student=request.user.studentprofile
        ).order_by("-id")

        serializer = self.serializer_class(instance=return_records, many=True)

        return CustomResponse.success(
            data=serializer.data, message="Return records fetched successfully!"
        )
