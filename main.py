from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    """Creates Book Database"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    date = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


db.create_all()


@app.route('/')
def home():
    """Display Library of Books and Total Pages Read"""
    all_books = db.session.query(Book).all()
    total_pages = 0
    for book in all_books:
        if all_books != []:
            total_pages += int(book.pages)
        else:
            pass
    return render_template("index.html", all_books=all_books, pages=total_pages)


@app.route("/add", methods=["POST", "GET"])
def add():
    """Add New Book to Library"""
    if request.method == "POST":
        new_book = Book(title=request.form["title"],
                        author=request.form["author"],
                        pages=request.form["pages"],
                        rating=request.form["rating"],
                        date=request.form["date"]
                        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["POST", "GET"])
def edit():
    """Edit Selected Book Information"""
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        book_to_update.title = request.form["title"]
        book_to_update.author = request.form["author"]
        book_to_update.pages = request.form["pages"]
        book_to_update.date = request.form["date"]
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit.html", book=book_selected)


@app.route("/delete", methods=["POST", "GET"])
def delete():
    """Delete Book From Library"""
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    db.session.delete(book_selected)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

