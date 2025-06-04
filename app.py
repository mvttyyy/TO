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
    books = ctrl.books.all()
    return render_template("index.html", books=books)

@app.route("/action", methods=["POST"])
def action():
    cmd    = request.form["cmd"]
    user   = request.form["user"]
    title  = request.form["title"]
    method = "return_media" if cmd=="return" else cmd
    success, msg = getattr(ctrl, method)(user, title)
    flash(msg)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)