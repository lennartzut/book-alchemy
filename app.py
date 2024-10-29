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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
