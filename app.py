from flask import Flask, render_template, request, redirect, url_for, flash
from lib.db import init_db
from controller.librarycontroller import LibraryController
from repository.BookRepository import BookRepository
from repository.UserRepository import UserRepository

app = Flask(__name__)
app.secret_key = 'replace-with-a-secure-key'
init_db()

ctrl = LibraryController(books_repo=BookRepository(),
                         users_repo=UserRepository())

@app.route("/")
def index():
    page = int(request.args.get("page", 1))
    page_size = 10
    all_books = ctrl.books.all()
    total = len(all_books)
    total_pages = (total - 1) // page_size + 1
    start = (page - 1) * page_size
    end = start + page_size
    books = all_books[start:end]
    return render_template(
        "index.html",
        books=books,
        page=page,
        total_pages=total_pages
    )

@app.route("/action", methods=["POST"])
def action():
    cmd    = request.form["cmd"]
    user   = request.form["user"]
    title  = request.form["title"]
    method = "return_media" if cmd=="return" else cmd
    success, msg = getattr(ctrl, method)(user, title)
    flash(msg)
    return redirect(url_for("index"))

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form["title"]
    success, msg = ctrl.remove_media(title)
    flash(msg)
    return redirect(url_for("index"))

@app.route("/details/<title>")
def details(title):
    book = ctrl.books.find_by_title(title)
    if not book:
        flash("Nie znaleziono książki.")
        return redirect(url_for("index"))
    return render_template("details.html", book=book)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        media_type = request.form["media_type"]
        title = request.form["title"]
        author = request.form["author"]
        quantity = int(request.form.get("quantity", 1))
        if not title or not author:
            flash("Tytuł i autor są wymagane.")
            return redirect(url_for("add"))
        try:
            ctrl.add_media(media_type, title, author, quantity)
            flash(f"{media_type.capitalize()} '{title}' dodano.")
        except Exception as e:
            flash(f"Błąd: {e}")
        return redirect(url_for("index"))
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)