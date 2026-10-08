from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='books'
    )
    description = models.TextField(blank=True)
    cover_url = models.URLField(blank=True, help_text="Link to a cover image (optional)")
    # Signed, not PositiveIntegerField: the dataset includes classical works
    # published before year 0 (e.g. The Odyssey, ~ -720).
    published_year = models.IntegerField(null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Pre-existing public rating (e.g. imported from a dataset like Goodreads).
    # Shown until the book has real reviews from Brew & Books users, so freshly
    # imported books don't all show up as an unrated 0.
    external_rating = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[self.pk])

    def published_year_display(self):
        if self.published_year is None:
            return ''
        if self.published_year < 0:
            return f'{abs(self.published_year)} BCE'
        return str(self.published_year)

    def average_rating(self):
        ratings = self.reviews.values_list('rating', flat=True)
        if ratings:
            return round(sum(ratings) / len(ratings), 1)
        if self.external_rating is not None:
            return round(self.external_rating, 1)
        return 0

    def review_count(self):
        return self.reviews.count()

    def full_stars(self):
        return range(round(self.average_rating()))

    def empty_stars(self):
        return range(5 - round(self.average_rating()))


class Review(models.Model):
    RATING_CHOICES = [(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('book', 'user')

    def __str__(self):
        return f'{self.user.username} rated "{self.book.title}" {self.rating}/5'

    def full_stars(self):
        return range(self.rating)

    def empty_stars(self):
        return range(5 - self.rating)
