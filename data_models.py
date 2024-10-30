from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    """
    Represents an Author entity in the database.

    Attributes:
        id (int): The primary key of the author, unique identifier.
        name (str): The name of the author, limited to 120 characters.
        birth_date (DateTime): The birth date of the author.
        date_of_death (DateTime): The date of death of the author (if applicable).
    """
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier for each author
    name = db.Column(db.String(120))  # Name of the author
    birth_date = db.Column(db.DateTime)  # Birth date of the author
    date_of_death = db.Column(db.DateTime)  # Date of death of the author

    def __repr__(self):
        """Returns a string representation of the Author object."""
        return f"Author(id={self.id}, name={self.name})"


class Book(db.Model):
    """
    Represents a Book entity in the database.

    Attributes:
        id (int): The primary key of the book, unique identifier.
        isbn (str): The ISBN of the book, limited to 20 characters.
        title (str): The title of the book, limited to 200 characters.
        publication_year (DateTime): The publication year of the book.
        author_id (int): Foreign key linking to the Author model.
        author (Author): Relationship to the Author model.
    """
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier for each book
    isbn = db.Column(db.String(20))  # ISBN of the book
    title = db.Column(db.String(200))  # Title of the book
    publication_year = db.Column(db.DateTime)  # Publication year of the book
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))  # Foreign key to link to the author
    author = db.relationship("Author", backref="books")  # Relationship definition allowing back reference from Author to Book

    def __repr__(self):
        """Returns a string representation of the Book object."""
        return f"Book(id={self.id}, title={self.title})"
