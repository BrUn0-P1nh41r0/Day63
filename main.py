from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
db = SQLAlchemy()
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book))
        books = result.scalars().all()
    return render_template("index.html", books=books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["book_name"]
        author = request.form["book_author"]
        rating = request.form["rating"]
        if name != "" and author != "" and rating != "":
            with app.app_context():
                db_new_book = Book(title=name, author=author, rating=rating)
                db.session.add(db_new_book)
                db.session.commit()
            return redirect(url_for('home'))
    return render_template("add.html")

@app.route(f"/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    with app.app_context():
        book = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar_one_or_none()
    if request.method == "POST":
        with app.app_context():
            rating_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar_one_or_none()
            rating_to_update.rating = request.form["rating"]
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book_id=book_id, book=book)

if __name__ == "__main__":
    app.run(debug=True)

