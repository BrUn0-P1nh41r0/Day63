from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

all_books = []

@app.route('/')
def home():
    return render_template("index.html", books=all_books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["book_name"]
        author = request.form["book_author"]
        rating = request.form["rating"]
        new_book = {
            "name": name,
            "author": author,
            "rating": rating
        }
        all_books.append(new_book)
    print(all_books)
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)

