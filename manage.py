import os
from flask.ext.script import Manager

from blog import app
manager = Manager(app)


from blog.models import Post
from blog.database import session

@manager.command
def run():
  port = int(os.environ.get('PORT',8080))
  app.run(host='0.0.0.0', port=port)
  


@manager.command
def seed():
  content = """ Hello there this is seed content """
  for i in range(25):
    post = Post(
            title="Seed post {}".format(i),
            content = content
            )
    session.add(post)
  session.commit()  
    
if __name__ == "__main__":
  manager.run()

  