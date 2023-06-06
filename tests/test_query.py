from tests import User

def test_eq(setup_entities):
  filters = {
    "person": {"age": {"eq": "20"}}
  }

  users = User.query.filter_by_ctx(filters=filters)
  users = users.all()

  assert len(users) == 2

  for user in users:
    assert user.person.age == 20
  
def test_neq(setup_entities):
  filters = {
    "person": {"age": {"ne": "20"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 2

  for user in users:
    assert user.person.age != 20

def test_lt(setup_entities):
  filters = {
    "person": {"age": {"lt": "22"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 2

  for user in users:
    assert user.person.age < 21

def test_lte(setup_entities):
  filters = {
    "person": {"age": {"lte": "22"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 3

  for user in users:
    assert user.person.age <= 22

def test_gt(setup_entities):
  filters = {
    "person": {"age": {"gt": "22"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 1

  for user in users:
    assert user.person.age > 22

def test_gte(setup_entities):
  filters = {
    "person": {"age": {"gte": "22"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 2

  for user in users:
    assert user.person.age >= 22

def test_in(setup_entities):
  filters = {
    "person": {"age": {"in": [20, 22]}}
  }

  users = User.query.filter_by_ctx(filters=filters)
  users = users.all()

  for user in users:
    assert user.person.age == 20 or user.person.age == 22

def test_nin(setup_entities):
  filters = {
    "person": {"age": {"nin": [20, 22]}}
  }

  users = User.query.filter_by_ctx(filters=filters)
  users = users.all()

  for user in users:
    assert not (user.person.age == 20 or user.person.age == 22)

def test_contains(setup_entities):
  filters = {
    "emails": {"address": {"contains": "alex_email"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 1

  emails_with_string = 0
  for email in users[0].emails:
    if(email.address.find("alex_email") > -1):
      emails_with_string += 1
  
  assert emails_with_string == 1

def test_icontains(setup_entities):
  filters = {
    "emails": {"address": {"icontains": "david_EMAIL"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 1
  assert users[0].emails[0].address == "DAVID_email_1@example.com"

def test_not_contains(setup_entities):
  filters = {
    "emails": {"address": {"ncontains": "alex_email"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 3

  for user in users:
    for email in user.emails:
      assert email.address.find("alex_email") == -1

def test_not_icontains(setup_entities):
  filters = {
    "emails": {"address": {"nicontains": "david_EMAIL"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 3

  for user in users:
    for email in user.emails:
      assert email.address.lower().find("david_email") == -1

def test_like(setup_entities):
  filters = {
    "emails": {"address": {"like": "%alex_email%"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 1

  emails_with_string = 0
  for email in users[0].emails:
    if(email.address.find("alex_email") > -1):
      emails_with_string += 1
  
  assert emails_with_string == 1

def test_ilike(setup_entities):
  filters = {
    "emails": {"address": {"ilike": "%david_EMAIL%"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 1
  assert users[0].emails[0].address == "DAVID_email_1@example.com"

def test_not_like(setup_entities):
  filters = {
    "emails": {"address": {"not_like": "%alex_email%"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 3

  for user in users:
    for email in user.emails:
      assert email.address.find("alex_email") == -1

def test_not_ilike(setup_entities):
  filters = {
    "emails": {"address": {"not_ilike": "%david_EMAIL%"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 3

  for user in users:
    for email in user.emails:
      assert email.address.lower().find("david_email") == -1

def test_startswith(setup_entities):
  filters = {
    "emails": {"address": {"startswith": "ivan"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 1
  assert users[0].emails[0].address.find("ivan") == 0

def test_istartswith(setup_entities):
  filters = {
    "emails": {"address": {"istartswith": "dAvId"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 1
  assert users[0].emails[0].address.find("DAVID_email_1") == 0

def test_endswith(setup_entities):
  filters = {
    "person": {"name": {"iendswith": "ex"}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 1
  assert users[0].person.name == "Alex"

def test_iendswith(setup_entities):
  filters = {
    "person": {"name": {"iendswith": "l."}}
  }

  users = User.query.filter_by_ctx(filters=filters).all()

  assert len(users) == 1
  assert users[0].person.name == "David L."

#Test de or
def test_or(setup_entities):
  filters = {
    "or": [
      {"person": {"age": {"eq": "20"}}},
      {"person": {"name": {"eq": "David L."}}},
    ]
  }

  users = User.query.filter_by_ctx(filters=filters)
  users = users.all()

  for user in users:
    assert user.person.age == 20 or user.person.name == "David L."
    
#Test de and
def test_and(setup_entities):
  filters = {
    "and": [
      {"person": {"age": {"eq": "20"}}},
      {"emails": {"address": {"eq": "ivan_email_1@example.com"}}},
    ]
  }

  users = User.query.filter_by_ctx(filters=filters)
  users = users.all()

  assert len(users) == 1
  assert (users[0].person.age == 20 and 
          users[0].emails[0].address == "ivan_email_1@example.com")

#Test de not
def test_not(setup_entities):
  filters = {
    "emails": {"address": {"contains": "email_2"}},
    "not": [{"person": {"age": {"eq": "20"}}}]
  }

  users = User.query.filter_by_ctx(filters=filters)
  users = users.all()

  assert len(users) == 1
  emails_with_string = 0

  for email in users[0].emails:
    if(email.address.find("email_2") > -1):
      emails_with_string += 1
  
  assert emails_with_string > 0

  assert users[0].person.age != 20

#Test sort
def test_sort(setup_entities):
  sorts = [
    {"person":{"age":"DESC"}}
  ]

  users = User.query.sort_by_ctx(sorts=sorts)
  users = users.all()
  age = 99

  for user in users:
    assert age >= user.person.age
    age = user.person.age

  assert age == 20