from django.urls import path

from library.views import (
    BookDetailView,
    BookInstanceListView,
    BookListView,
    BookBorrowView,
    BookReturnView,
    BookBorrowListView,
    BookReturnListView,
)


urlpatterns = [
    path("books/", BookListView.as_view(), name="books"),
    path("book/<pk>/", BookDetailView.as_view(), name="book"),
    path("book-instances/<pk>/", BookInstanceListView.as_view(), name="book-instances"),
    path("borrow-book/<pk>/", BookBorrowView.as_view(), name="borrow-book"),
    path("return-book/<pk>/", BookReturnView.as_view(), name="return-book"),
    path("borrows/", BookBorrowListView.as_view(), name="borrows"),
    path("returns/", BookReturnListView.as_view(), name="returns"),
]
