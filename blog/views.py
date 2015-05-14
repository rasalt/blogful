from flask import render_template

from blog import app
from .database import session,connection
from .models import Post
import mistune
from flask import request, redirect, url_for
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
def add_post_get():
    return render_template("add_post.html")

@app.route("/post/add", methods=["POST"])
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=request.form["content"],
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
def post_id_edit(id=1):
   posts = session.query(Post).get(id)
   return render_template("edit_post.html", posts=posts)

@app.route("/post/<int:id>/edit", methods=["POST"])
def post_id_edit_post(id=1):
  print "Here in post_id_edit_post"
#    posts = session.query(Post).get(id)
#    print "New post and title are {} {}".format(posts.title, posts.content)
  print "Form title {}".format(request.form["title"])
  print "Form content {}".format(request.form["content"])
    
#  posts.title = request.form["title"]
#  posts.content = request.form["content"]
#  print "New post and title are {} {}".format(posts.title, posts.content)
#      content=mistune.markdown(request.form["content"]),
#    )
  cursor = connection.cursor()
  
  command = "update posts set title=%s, content=%s where id=%d"
  cursor.execute(command, (request.form["title"], request.form["content"], 27))
  
 # session.commit()
  return redirect(url_for("posts"))


@app.route("/post/<int:id>/delete", methods=["POST"])
def post_id_delete(id=1):
  return True
#  posts = session.query(Post).get(id)
#  return render_template("post_id.html", posts=posts)


