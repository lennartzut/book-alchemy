import os
from flask import (Flask, redirect, render_template, request,
                   url_for, flash)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from data_models import db, Author, Book

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath('data/library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'leo'
db.init_app(app)


@app.route('/')
def home():
    """
    Retrieves the list of books, optionally filtered by a search
    query and sorted either by book title or author name.

    GET Parameters: sort_by (str): The field by which to sort the
    books ('title' or 'author'). search_query (str): A search term
    to filter books by title or author name.

    Returns:
        Rendered HTML page displaying the list of books.
    """
    sort_by = request.args.get('sort_by', 'title')
    search_query = request.args.get('search_query', '')
    query = Book.query.join(Author)

    if search_query:
        query = query.filter(
            (Book.title.ilike(f"%{search_query}%")) |
            (Author.name.ilike(f"%{search_query}%"))
        )

    if sort_by == 'author':
        query = query.order_by(Author.name)
    else:
        query = query.order_by(Book.title)
    books = query.all()

    for book in books:
        if book.isbn:
            book.cover_image_url = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg"
        else:
            book.cover_image_url = "/static/images/default_cover.jpg"

    return render_template('home.html', books=books, sort_by=sort_by,
                           search_query=search_query)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handles both GET and POST requests. On GET, renders a form to
    add a new author. On POST, adds the new author to the database
    and redirects back to the form.

    POST Parameters: name (str): The name of the author. birthdate
    (str): The birthdate of the author in 'YYYY-MM-DD' format.
    date_of_death (str): The date of death of the author in
    'YYYY-MM-DD' format (optional).

    Returns: Redirect to the add_author page or renders the
    add_author form.
    """
    if request.method == 'POST':
        name = request.form['name']
        birthdate_str = request.form['birthdate']
        date_of_death_str = request.form['date_of_death']

        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d')
        date_of_death = datetime.strptime(date_of_death_str,
                                          '%Y-%m-%d') if date_of_death_str else None

        new_author = Author(name=name,
                            birth_date=birthdate,
                            date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()

        flash("Author successfully added!")
        return redirect(url_for('add_author'))

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handles both GET and POST requests. On GET, renders a form to
    add a new book. On POST, adds the new book to the database and
    redirects back to the form.

    POST Parameters:
        title (str): The title of the book.
        isbn (str): The ISBN of the book.
        publication_year (str): The publication year of the book.
        author_id (int): The ID of the author of the book.

    Returns:
        Redirect to the add_book page or renders the add_book form.
    """
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year_str = request.form['publication_year']
        author_id = request.form['author_id']
        publication_year = datetime.strptime(publication_year_str,
                                             '%Y')

        new_book = Book(title=title,
                        isbn=isbn,
                        publication_year=publication_year,
                        author_id=author_id)
        db.session.add(new_book)
        db.session.commit()

        flash("Book successfully added!")
        return redirect(url_for('add_book'))

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Deletes a specific book. If the author has no more books,
    deletes the author as well.

    Returns:
        Redirect to the home page after deletion.
    """
    book = Book.query.get_or_404(book_id)
    author_id = book.author_id

    db.session.delete(book)
    db.session.commit()

    remaining_books = Book.query.filter_by(
        author_id=author_id).count()
    if remaining_books == 0:
        author = Author.query.get(author_id)
        if author:
            db.session.delete(author)
            db.session.commit()

    flash(f"Book '{book.title}' was successfully deleted!")
    return redirect(url_for('home'))


@app.route('/author/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    """
    Deletes a specific author, along with all their associated books.

    Returns:
        Redirect to the home page after deletion.
    """
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()

    flash(f"Author '{author.name}' and all associated books were successfully deleted!")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
