from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm, ReviewForm, SignUpForm
from .models import Book, Review


def home(request):
    query = request.GET.get("q", "").strip()

    books = Book.objects.all().order_by("-created_at")

    if query:
        books = books.filter(
            title__icontains=query
        ) | books.filter(
            author__icontains=query
        )

    return render(
        request,
        "reviews/home.html",
        {
            "books": books,
            "query": query,
        },
    )


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    reviews = Review.objects.filter(book=book).select_related("user")

    form = ReviewForm()

    return render(
        request,
        "reviews/book_detail.html",
        {
            "book": book,
            "reviews": reviews,
            "form": form,
        },
    )


@login_required
def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()

            messages.success(request, "Your review was posted.")
            return redirect("book_detail", pk=book.pk)

    else:
        form = ReviewForm()

    reviews = Review.objects.filter(book=book).select_related("user")

    return render(
        request,
        "reviews/book_detail.html",
        {
            "book": book,
            "reviews": reviews,
            "form": form,
        },
    )


@login_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()

            messages.success(request, "Book added successfully.")
            return redirect("book_detail", pk=book.pk)

    else:
        form = BookForm()

    return render(
        request,
        "reviews/add_book.html",
        {"form": form},
    )


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, "Account created successfully.")
            return redirect("home")

    else:
        form = SignUpForm()

    return render(
        request,
        "reviews/signup.html",
        {"form": form},
    )


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == "POST":
        if review.user == request.user or request.user.is_staff:
            review.delete()
            messages.success(request, "Review deleted.")

    return redirect("book_detail", pk=review.book.pk)