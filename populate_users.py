from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *


engine = create_engine('sqlite:///tutorial.db', echo=True)


# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("test1", "password1", "someone@example.com")
session.add(user)

user = User("test2", "password2", "someone@example.com")
session.add(user)

# commit the record the database
session.commit()
