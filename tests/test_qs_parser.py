def test_qs_parser_filters_1(client):
  response = client.get('/endpoint?filters[username][eq]=username@example.com')
  assert response.status_code == 200

  data = response.json
  assert data["ctx"] == {
    "filters": {"username":{"eq":"username@example.com"}},
    "offset": 0,
    "limit": 10,
    "sorts": []
  }

#Simple prop filtering
def test_qs_parser_simple_filter(client):
  response = client.get('/endpoint?filters[foo][bar][eq]=relationship_foo_value_bar')
  assert response.status_code == 200

  data = response.json
  assert data["ctx"] == {
    "filters": {"foo":{"bar":{"eq":"relationship_foo_value_bar"}}},
    "offset": 0,
    "limit": 10,
    "sorts": []
  }

#Simple nested relationship prop filtering
def test_qs_parser_simple_nested_relationship_filter(client):
  response = client.get('/endpoint?filters[foo][bar][eq]=relationship_foo_with_prop_bar')
  assert response.status_code == 200

  data = response.json
  assert data["ctx"] == {
    "filters": {"foo":{"bar":{"eq":"relationship_foo_with_prop_bar"}}},
    "offset": 0,
    "limit": 10,
    "sorts": []
  }

#Complex 3 levels filtering
def test_qs_parser_complex_3_levels_filter(client):
  response = client.get("/endpoint?" +
    "filters[baz][eq]=value_baz&" +
    "filters[foo][bar][eq]=relationship_foo_with_prop_bar&" +
    "filters[foo][abc][def][eq]=model_has_relationship_foo_then_has_abc_with_def_as_prop")
  assert response.status_code == 200

  data = response.json
  assert data["ctx"] == {
    "filters": {
      "baz": {"eq":"value_baz"},
      "foo":{
        "bar":{"eq":"relationship_foo_with_prop_bar"},
        "abc": {
          "def":{"eq":"model_has_relationship_foo_then_has_abc_with_def_as_prop"}
        }
      }
    },
    "offset": 0,
    "limit": 10,
    "sorts": []
  }

#in filtering
def test_qs_parser_in_value_filtering(client):
  response = client.get("/endpoint?filters[baz][in][0]=1&filters[baz][in][1]=2&filters[baz][in][2]=3")
  assert response.status_code == 200

  data = response.json
  print(data)
  assert data["ctx"] == {
    "filters": {
      "baz": {"in":["1","2","3"]},
    },
    "offset": 0,
    "limit": 10,
    "sorts": []
  }

#boolean value filtering
def test_qs_parser_boolean_value_filtering(client):
  response = client.get("/endpoint?filters[baz][eq]=true&filters[foo][eq]=false")
  assert response.status_code == 200

  data = response.json
  assert data["ctx"] == {
    "filters": {
      "baz": {"eq":True},
      "foo": {"eq":False}
    },
    "offset": 0,
    "limit": 10,
    "sorts": []
  }

#Test null 
def test_qs_parser_null_value_filtering(client):
  response = client.get("/endpoint?filters[baz][is]=null&filters[foo][is_not]=null")
  assert response.status_code == 200

  data = response.json
  assert data["ctx"] == {
    "filters": {
      "baz": {"is": None},
      "foo": {"is_not": None}
    },
    "offset": 0,
    "limit": 10,
    "sorts": []
  }

#Boolean expressions filtering
def test_qs_parser_boolean_expressions_filter(client):
  response = client.get("/endpoint?" +
    "filters[or][0][baz][eq]=value_baz&" +
    "filters[or][1][foo][bar][eq]=value_bar")
  assert response.status_code == 200

  data = response.json
  assert data["ctx"] == {
    "filters": {
      "or": [
        {"baz": {"eq":"value_baz"}},
        {"foo":{"bar":{"eq":"value_bar"}}}
      ]
    },
    "offset": 0,
    "limit": 10,
    "sorts": []
  }

#Nested Boolean expressions filtering
def test_qs_parser_nested_boolean_expressions_filter(client):
  response = client.get("/endpoint?" +
    "filters[or][0][baz][eq]=value_baz&" +
    "filters[or][1][and][0][foo][bar][contains]=foo&" +
    "filters[or][1][and][1][foo][bar][contains]=bar")
  assert response.status_code == 200

  data = response.json
  assert data["ctx"] == {
    "filters": {
      "or": [
        {"baz": {"eq":"value_baz"}},
        {"and":[
          {"foo":{"bar":{"contains":"foo"}}},
          {"foo":{"bar":{"contains":"bar"}}}
        ]}
      ]
    },
    "offset": 0,
    "limit": 10,
    "sorts": []
  }

#Nested Boolean expressions filtering
def test_qs_parser_nested_boolean_expressions_filter_2(client):
  response = client.get("/endpoint?" +
    "filters[or][0][baz][eq]=value_baz&" +
    "filters[or][1][not][0][and][0][foo][bar][contains]=foo&" +
    "filters[or][1][not][0][and][1][foo][bar][contains]=bar")
  assert response.status_code == 200

  data = response.json
  assert data["ctx"] == {
    "filters": {
      "or": [
        {"baz": {"eq":"value_baz"}},
        {"not": [
          {"and":[
            {"foo":{"bar":{"contains":"foo"}}},
            {"foo":{"bar":{"contains":"bar"}}}
          ]}
        ]}
      ]
    },
    "offset": 0,
    "limit": 10,
    "sorts": []
  }

#offset limit
def test_qs_parser_ofsset_limit(client):
  response = client.get("/endpoint?limit=30&offset=5")
  assert response.status_code == 200

  data = response.json
  assert data["ctx"] == {
    "filters": {},
    "offset": 5,
    "limit": 30,
    "sorts": []
  }

#sorts filtering
def test_qs_parser_complex_3_levels_sorting(client):
  response = client.get("/endpoint?" +
    "sorts[0][baz]=ASC&" +
    "sorts[1][foo][bar]=DESC&" +
    "sorts[2][foo][abc][def]=ASC")
  assert response.status_code == 200

  data = response.json

  assert data["ctx"] == {
    "filters": {},
    "offset": 0,
    "limit": 10,
    "sorts": [
      {"baz":"ASC"},
      {"foo":{"bar":"DESC"}}, 
      {"foo":{"abc":{"def":"ASC"}}}
    ]
  }

#Filtering, Sorting, Offset and Limit:
def test_qs_all_combined(client):
  response = client.get("/endpoint?" +
    "filters[abc][eq]=value_abc&" +                    
    "filters[or][0][baz][eq]=value_baz&" +
    "filters[or][1][not][0][and][0][foo][bar][contains]=foo&" +
    "filters[or][1][not][0][and][1][foo][bar][contains]=bar&" +
    "limit=30&offset=5&" +
    "sorts[0][baz]=ASC&" +
    "sorts[1][foo][bar]=DESC&" +
    "sorts[2][foo][abc][def]=ASC")
  assert response.status_code == 200

  data = response.json
  assert data["ctx"] == {
    "filters": {
      "abc": {"eq":"value_abc"},
      "or": [
        {"baz": {"eq":"value_baz"}},
        {"not": [
          {"and":[
            {"foo":{"bar":{"contains":"foo"}}},
            {"foo":{"bar":{"contains":"bar"}}}
          ]}
        ]}
      ]
    },
    "offset": 5,
    "limit": 30,
    "sorts": [
      {"baz":"ASC"},
      {"foo":{"bar":"DESC"}}, 
      {"foo":{"abc":{"def":"ASC"}}}
    ]
  }