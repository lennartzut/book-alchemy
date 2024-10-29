import os
from flask import Flask, redirect, render_template, request, url_for, \
    flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from data_models import db, Author, Book

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath('data/library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Needed for flash messages
db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birthdate_str = request.form['birthdate']
        date_of_death_str = request.form['date_of_death']

        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d')
        date_of_death = datetime.strptime(date_of_death_str,
                                          '%Y-%m-%d') if date_of_death_str else None

        new_author = Author(name=name, birth_date=birthdate,
                            date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()

        flash(
            "Author successfully added!")  # Flash the success message

        return redirect(url_for('add_author'))

    return render_template('add_author.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
