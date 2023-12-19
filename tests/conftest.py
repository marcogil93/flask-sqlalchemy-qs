import pytest
import json
from flask import jsonify
from flask_sqlalchemy_qs import get_url_query_ctx
from tests import app, db, User, Person, Email

@pytest.fixture(scope="session")
def client():
  app.config['TESTING'] = True
  
  with app.app_context():
    if 'qs_parser' not in app.view_functions:
      @app.route('/endpoint', methods=['GET'])
      def qs_parser():
        ctx = get_url_query_ctx()
        return jsonify({"ctx":ctx})
    
    if 'users' not in app.view_functions:
      @app.route('/users', methods=['GET'])
      def get_users():
        ctx = get_url_query_ctx()
        users = User.query.filter_by_ctx(filters=ctx["filters"]).all()
        results = []

        for user in users:
          user_dict = {}
          user_dict['username'] = user.username
          user_dict['person'] = dict()
          user_dict['person']['name'] = user.person.name
          user_dict['person']['age'] = user.person.age
          user_dict['person']['age'] = user.person.age
          results.append(user_dict)

        return jsonify({"users": results})
  
  with app.test_client() as client:
    yield client

@pytest.fixture(scope="session")
def sqlalchemy():
  app.config['TESTING'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

  with app.app_context():
    db.create_all()
    yield db
    db.drop_all()

@pytest.fixture(scope='session')
def setup_entities(sqlalchemy):
  user   = User(username="alex_username@example.com", json_data={'foo': 'bar', 'num': 10, 'a': {'b': 10}} )
  person = Person(name="Alex", age=20)
  user.person = person
  user.emails.append(Email(address="alex_email_1@example.com"))
  user.emails.append(Email(address="ALEX_email_2@example.com"))

  user2   = User(username="marco_username@example.com")
  person2 = Person(name="Marco", age=25)
  user2.person = person2
  user2.emails.append(Email(address="marco_email_1@example.com"))
  user2.emails.append(Email(address="MARCO_email_2@example.com"))

  user3 = User(username="ivan_username@example.com")
  person3 = Person(name="Ivan", age=20)
  user3.person = person3
  user3.emails.append(Email(address="ivan_email_1@example.com"))

  user4 = User(username="david_username@example.com")
  person4 = Person(name="David L.", age=22)
  user4.person = person4
  user4.emails.append(Email(address="DAVID_email_1@example.com"))

  sqlalchemy.session.add(user)
  sqlalchemy.session.add(user2)
  sqlalchemy.session.add(user3)
  sqlalchemy.session.add(user4)
  sqlalchemy.session.commit()