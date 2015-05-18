from flask import render_template
import datetime
from blog import app
from .database import session
from .models import Post
import mistune
from flask import request, redirect, url_for

from flask import flash
from flask.ext.login import login_user, login_required, current_user, logout_user

from werkzeug.security import check_password_hash
from .models import User

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")


@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():  
  post = Post(
     title=request.form["title"],
     content=request.form["content"],
     author = current_user
#      content=mistune.markdown(request.form["content"]), 
  )
    
  session.add(post)
  session.commit()
  return redirect(url_for("posts"))

@app.route("/post/<int:id>")
def post_id(id=1):
  posts = session.query(Post).get(id)
  return render_template("post_id.html", posts=posts)

@app.route("/post/<int:id>/edit", methods=["GET"])
@login_required
def post_id_edit(id=1):
  posts = session.query(Post).get(id)
  if (current_user.email == posts.author.email):
   return render_template("edit_post.html", posts=posts)
  else:
    flash("Cannot edit a post you have not authored")
    return redirect(url_for("posts"))    

  

@app.route("/post/<int:id>/edit", methods=["POST"])
@login_required
def post_id_edit_post(id=1):
  print "Here in post_id_edit_post"

    
#  posts.title = request.form["title"]
#  posts.content = request.form["content"]
#  print "New post and title are {} {}".format(posts.title, posts.content)
#      content=mistune.markdown(request.form["content"]),
#    )
#  cursor = connection.cursor()
#  session.
#  command = "update posts set title=%s, content=%s where id=%s"
#  command = "update posts set title='hello there', content='violet' where id=27;"
#  cursor.execute(command, (request.form["title"], request.form["content"], 27))
#  if cursor:
#     cursor.execute(command) 
#     print "cursor is valid"
  post = session.query(Post).get(id)
  
  print "Form title {}".format(request.form["title"])
  print "Form content {}".format(request.form["content"])
  post.title = request.form["title"]
  post.content = request.form["content"]
  post.datetime = datetime.datetime.now()
  session.commit()
  return redirect(url_for("posts"))    



@app.route("/post/<int:id>/delete", methods=["GET"])
@login_required
def post_id_delete(id=id):
  post = session.query(Post).get(id)
  if (current_user.email == post.author.email):
   return render_template("delete_post.html", posts=post)
  else:
    flash("Cannot delete a post you have not authored")
    return redirect(url_for("posts"))    
  
@app.route("/post/<int:id>/delete", methods=["POST"])
@login_required
def post_id_delete_post(id=id):
  post = session.query(Post).get(id)
  
  if request.form["button"]=="Yes":
    print "Yes Button"
    session.delete(post)
    session.commit()
  elif request.form["button"]=="Cancel":
    print "No Button"
  return redirect(url_for("posts"))

#  posts = session.query(Post).get(id)
#  return render_template("post_id.html", posts=posts)


@app.route("/register", methods=["GET"])
def register_get():
  return render_template("register.html")
from getpass import getpass
from werkzeug.security import generate_password_hash
@app.route("/register", methods=["POST"])
def register_post():
  print "In method post"
  name = request.form["username"]
  email = request.form["emailaddr"]
  if session.query(User).filter_by(email=email).first():
    flash("User email exists, please login")
    return redirect(url_for("login_get"))
  print "Checking passwords"
  password1=request.form["password1"]
  password2=request.form["password2"]
  print "Checking passwords{} and {}".format(password1, password2)
  if not (password1 and password2 ) or (password1 != password2):
    flash("passwords do not match please attempt again")
    print "Passwords do not match"
    return redirect(url_for("register"))
    
  user = User(name=name, email=email, password =generate_password_hash(password1))
  session.add(user)
  session.commit()
  print "Redirecting to posts"
  return redirect(url_for("login_get"))



@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
  email = request.form["email"]
  print "{}".format(email)
  
  password = request.form["password"]
  print "{}".format(password)
  user = session.query(User).filter_by(email = email).first()
  if not user or not check_password_hash(user.password, password):
    flash("Incorrect email or password","danger")
    print "user non existent"
    return redirect(url_for("login_get"))

  login_user(user)  
  return redirect(request.args.get('next') or url_for("posts"))

    




#  posts = session.query(Post).get(id)
#  return render_template("post_id.html", posts=posts)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    print "Logging out"
    logout_user()
    return redirect(url_for("posts"))


