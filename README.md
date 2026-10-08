# ☕📚 Brew & Books — Book Review Website (Django)

A warm, cafe-themed book review site built with Django. Coffee-cup logo,
cream + espresso-brown palette, serif fonts, a subtle coffee-bean/book
background pattern, and a real dataset of ~4,700 books to browse.

## Features
- Browse books in a card grid with cover image, star rating, and review count
- **Real dataset**: ~4,766 books imported from `book.csv` (title, author,
  publication year, cover image, description, and public rating)
- Pagination (24 books per page) so the full catalog stays fast and tidy
- Search by title/author and filter by genre
- User sign up / log in / log out (Django auth)
- Logged-in users can add new books and leave one star rating + review per book
- Django admin for managing genres, books, and reviews
- Custom coffee-cup-and-book SVG logo used as both the navbar brand and favicon

## Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Import the book dataset (reviews/data/book.csv ships with the project)
python manage.py import_books
#    Tip: add --limit 200 to import only the first 200 rows for a quick demo

# 5. (Optional) Create an admin user
python manage.py createsuperuser

# 6. Run the dev server
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser.
Admin panel: http://127.0.0.1:8000/admin/

> **Note:** a `db.sqlite3` with the dataset already imported ships in this
> zip, so `runserver` alone will show a fully populated site immediately.
> Run `import_books` again only if you delete the database and start fresh.

## Project structure

```
bookreview_project/
├── manage.py
├── requirements.txt
├── db.sqlite3                     # pre-populated with the imported dataset
├── bookreview/                    # Project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
└── reviews/                       # Main app
    ├── data/book.csv              # source dataset
    ├── models.py                  # Genre, Book, Review
    ├── forms.py                   # SignUpForm, ReviewForm, BookForm
    ├── views.py                   # home (paginated), book_detail, add_book, signup
    ├── urls.py
    ├── admin.py
    ├── management/commands/
    │   ├── import_books.py        # loads reviews/data/book.csv into the DB
    │   └── seed_data.py           # small hand-written sample set (optional)
    ├── templates/
    │   ├── base.html              # navbar logo + favicon
    │   └── reviews/                # home, book_detail, add_book, signup, login
    └── static/reviews/
        ├── css/style.css          # cafe theme (colors, hero, cards, pagination)
        └── img/
            ├── favicon.svg        # coffee-cup-and-book logo
            └── cafe-pattern.svg   # subtle tiled background texture
```

## Notes for your project write-up
- **Models**: `Genre` (1) → `Book` (many), `Book` (1) → `Review` (many),
  `User` (1) → `Review` (many). A user can only review a given book once
  (`unique_together` constraint).
- **Rating logic**: `Book.average_rating()` uses real Brew & Books user
  reviews if any exist; otherwise it falls back to `external_rating`, the
  public rating imported from the dataset, so freshly imported books don't
  all show up as unrated.
- **Dataset import** (`import_books` management command) parses the CSV,
  skips rows with a missing title/author or an already-imported duplicate,
  converts the publication year to an int (allowing negative years for
  classical works like *Agamemnon*, ~458 BCE), and treats the dataset's
  generic "no cover" placeholder image as "no cover" so the site's own
  cover placeholder is shown instead.
- **Theme**: colors and fonts are CSS variables at the top of `style.css`,
  so you can retheme the whole site by editing a handful of lines. The logo
  and background pattern are hand-drawn inline SVG — no external image
  files or licensing concerns.
- The dataset has no genre column, so imported books have no genre by
  default; add genres via the admin panel and assign them to showcase the
  filter, or use "Add a Book" to create new entries with a genre.

## Ideas to extend further
- User profile pages showing a user's own reviews
- Edit/delete your own review
- "Top rated" / "Most reviewed" sections
- Image upload for covers instead of a URL field
- Auto-tag genres for imported books using keyword matching on description
