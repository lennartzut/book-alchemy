from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    birth_date = db.Column(db.DateTime)
    date_of_death = db.Column(db.DateTime)

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20))
    title = db.Column(db.String(200))
    publication_year = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    author = db.relationship("Author", backref="books")

    def __repr__(self):
        return f"Book(id={self.id}, title={self.title})"
