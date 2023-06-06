from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_qs import BaseQuery

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

# Define a base model for other database tables to inherit
class Base(db.Model):
  __abstract__ = True
  query_class = BaseQuery

class User(Base):
  __tablename__ = "users"

  id       = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True)
  person   = db.relationship("Person", uselist=False, back_populates="user")
  emails   = db.relationship("Email", back_populates="user")

  def __repr__(self):
    return f'<User id={self.id!r}, username={self.username!r}>'
  
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Person(Base):
  __tablename__ = "persons"

  id         = db.Column(db.Integer, primary_key=True)
  name       = db.Column(db.String(120))
  age        = db.Column(db.Integer)
  user_id    = db.Column(db.Integer, db.ForeignKey('users.id'))
  user       = db.relationship("User", back_populates="person")

  def __repr__(self):
    return f'<Person id={self.id!r}, name={self.name!r}>'
  
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Email(Base):
  __tablename__ = "emails"

  id            = db.Column(db.Integer, primary_key=True)
  address       = db.Column(db.String(50), unique=True)
  user_id       = db.Column(db.Integer, db.ForeignKey('users.id'))
  user          = db.relationship("User", back_populates="emails")

  def __repr__(self) -> str:
    return f'<Email id={self.id!r}, address={self.address!r}>'
  
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

if __name__ == '__main__':
  app.run()