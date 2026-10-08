import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from reviews.models import Book

CSV_PATH = Path(__file__).resolve().parent.parent.parent / 'data' / 'book.csv'

# The dataset uses this generic "no cover available" image for many rows.
# We treat those the same as "no cover" so the site shows its own nice
# placeholder icon instead of a broken/ugly stock image.
NO_COVER_MARKER = 'nophoto'


class Command(BaseCommand):
    help = 'Imports books from reviews/data/book.csv into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit', type=int, default=None,
            help='Only import the first N rows (useful for a quick demo).',
        )

    def handle(self, *args, **options):
        if not CSV_PATH.exists():
            self.stderr.write(self.style.ERROR(f'CSV not found at {CSV_PATH}'))
            return

        limit = options.get('limit')
        created = 0
        skipped = 0

        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if limit is not None and i >= limit:
                    break

                title = (row.get('title') or '').strip()
                authors = (row.get('authors') or '').strip()
                if not title or not authors:
                    skipped += 1
                    continue

                if Book.objects.filter(title=title, author=authors).exists():
                    skipped += 1
                    continue

                year = None
                try:
                    year_raw = row.get('original_publication_year')
                    if year_raw:
                        year = int(float(year_raw))
                except (TypeError, ValueError):
                    year = None

                rating = None
                try:
                    rating_raw = row.get('average_rating')
                    if rating_raw:
                        rating = float(rating_raw)
                except (TypeError, ValueError):
                    rating = None

                cover_url = (row.get('image_url') or '').strip()
                if NO_COVER_MARKER in cover_url:
                    cover_url = ''

                description = (row.get('description') or '').strip()

                Book.objects.create(
                    title=title,
                    author=authors,
                    description=description,
                    cover_url=cover_url,
                    published_year=year,
                    external_rating=rating,
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Imported {created} book(s), skipped {skipped} (duplicates or missing data).'
        ))
