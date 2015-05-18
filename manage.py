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
    
from flask.ext.migrate import Migrate, MigrateCommand
from blog.database import Base

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)    
    
from blog.models import User
from getpass import getpass
from werkzeug.security import generate_password_hash
@manager.command
def adduser():
  name = raw_input("Name: ")
  email = raw_input("Email: ")
  if session.query(User).filter_by(email=email).first():
    print "User email already exists"
    return
  
  password=""
  password2=""
  
  while not (password and password2 ) or (password != password2):
    password = getpass("Password: ")
    password2 = getpass("Please type it again: ")
    
  user = User(name=name, email=email, password =generate_password_hash(password))
  session.add(user)
  session.commit()
    
    
if __name__ == "__main__":
  manager.run()

  