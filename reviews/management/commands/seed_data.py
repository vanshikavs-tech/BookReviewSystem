from django.core.management.base import BaseCommand

from reviews.models import Book, Genre


class Command(BaseCommand):
    help = 'Seeds the database with sample genres and books.'

    def handle(self, *args, **options):
        genres_data = ['Fiction', 'Fantasy', 'Mystery', 'Romance', 'Non-Fiction', 'Sci-Fi']
        genres = {}
        for name in genres_data:
            genre, _ = Genre.objects.get_or_create(name=name)
            genres[name] = genre

        books_data = [
            {
                'title': 'The Silent Orchard',
                'author': 'Marianne Cole',
                'genre': 'Fiction',
                'description': 'A quiet family drama set in an old orchard town, exploring memory and belonging.',
                'published_year': 2018,
            },
            {
                'title': 'Ashes of the Ember Crown',
                'author': 'Devon Hart',
                'genre': 'Fantasy',
                'description': 'A dethroned prince must reclaim his kingdom with the help of an ancient dragon.',
                'published_year': 2021,
            },
            {
                'title': 'The Clockmaker\'s Riddle',
                'author': 'Priya Anand',
                'genre': 'Mystery',
                'description': 'A detective unravels a decades-old disappearance hidden inside an antique clock shop.',
                'published_year': 2016,
            },
            {
                'title': 'Letters from the Coast',
                'author': 'Elise Fontaine',
                'genre': 'Romance',
                'description': 'Two pen pals fall in love across a stormy Atlantic coastline.',
                'published_year': 2020,
            },
            {
                'title': 'A Brief History of Small Things',
                'author': 'Thomas Reyes',
                'genre': 'Non-Fiction',
                'description': 'An engaging look at the overlooked inventions that shaped everyday life.',
                'published_year': 2019,
            },
            {
                'title': 'Beyond the Ion Drift',
                'author': 'Kaela Storm',
                'genre': 'Sci-Fi',
                'description': 'A salvage crew discovers a derelict ship carrying a secret that could end the war.',
                'published_year': 2023,
            },
        ]

        created = 0
        for data in books_data:
            genre = genres[data.pop('genre')]
            _, was_created = Book.objects.get_or_create(
                title=data['title'], author=data['author'],
                defaults={**data, 'genre': genre},
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {len(genres)} genres and {created} new book(s).'
        ))
