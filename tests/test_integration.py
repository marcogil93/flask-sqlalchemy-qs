def test_users_integration(client, setup_entities):
  response = client.get("/users?" +
    "filters[username][eq]=alex_username@example.com")
  
  assert response.status_code == 200
  data = response.json
  
  assert data["users"][0]["username"] == "alex_username@example.com"


def test_users_integration_2(client, setup_entities):
  response = client.get("/users?" +
    "filters[person][age][gte]=22&sorts[0][person][age]=DESC&limit=10&offset=0")
  
  assert response.status_code == 200
  data = response.json
  users = data["users"]
               
  assert len(users) == 2
  age = 100

  for user in users:
    assert user["person"]["age"] >= 22
    assert user["person"]["age"] < age
    age = user["person"]["age"]