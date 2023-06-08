# flask-sqlalchemy-qs

flask-sqlalchemy-qs is a Python library that enables processing of query strings and its usage in conjunction with Flask and SQLAlchemy. The library provides tools for generating and manipulating SQLAlchemy filters and sorts from query strings in the URL, making it easier to build robust and flexible RESTful APIs. 

`/users?filters[username][eq]=awesomeuser@example.com`
where model User has a username column attribute

`/users?filters[person][age][gte]=22&sorts[0][person][age]=DESC&limit=10&offset=0`
where model User has a person relationship attribute

## Installation

Install flask-sqlalchemy-qs with pip:

```bash
pip install flask-sqlalchemy-qs
```

## Usage

To get the filters, sorts, limit, and offset from the query string is necesarry to follow the next syntaxis: 


### For the "filters" parameter
Filter your list result by column and relationship model properties.

`GET /api/endpoint?filters[field][operator]=value`

The following operators are available:

| Operator    | Description                        |
| ----------- | ---------------------------------- |
| eq          | Equal                              |
| ne          | Not equal                          |
| lt          | Less than                          |
| lte         | Less than or equal to              |
| gt          | Greater than                       |
| gte         | Greater than or equal to           |
| in          | Included in an array               |
| nin         | Not included in an array           |
| contains    | Contains                           |
| ncontains   | Does not contain                   |
| icontains   | Contains (case-insensitive)        |
| like        | Like                               |
| ilike       | Like (case-insensitive)            |
| not_like    | Not Like                           |
| not_ilike   | Not Like (case-insensitive)        |
| nicontains  | Does not contain (case-insensitive)|
| startswith  | Starts with                        |
| istartswith | Starts with (case-insensitive)     |
| endswith    | Ends with                          |
| iendswith   | Ends with (case-insensitive)       |
| or          | Joins the filters in an "or" expression  |
| and         | Joins the filters in an "and" expression |
| not         | Joins the filters in an "not" expression |

Examples:


```python
#Simple usage
/users?filters[username][eq]=username@example.com
```

```python
#Relationship usage (User has a person)
/users?filters[person][name][eq]=Marco
```

```python
#Complex usage
/users?filters[username][contains]=awesome.com&filters[person][age][gte]=25
```

```python
# in and nin usage
/users?filters[person][age][in][0]=20&filters[person][age][in][1]=25&filters[person][age][in][2]=30
```

```python
# boolean usage
/users?filters[person][age][in][0]=20&filters[person][age][in][1]=25&filters[person][age][in][2]=30
```

```python
# boolean usage
/users?filters[or][0][username][eq]=username1&filters[or][1][username][eq]=username2
```

```python
# Complex boolean usage
/users?filters[or][0][username][contains]=awesome.com&filters[or][1][not][0][and][0][person][age][gte]=20&filters[or][1][not][0][and][1][person][age][lte]=30
```

### For the "sorts" parameter
Sort your list result by column and relationship model properties.

`GET /api/endpoint?sorts[priority_index][field]=order`

Examples:

```python
# Single sort usage
/users?sorts[0][username]=DESC
```

```python
# Multiple and relationship sort usage
/users?sorts[0][username]=DESC&sorts[1][person][age]=ASC
```

### For the "limit" and "offset" parameter 
Limt (amount of elements) and set an offset (skip elements) for your list result. 

`GET /api/endpoint?limit=10&offset=2`

Example:
```python
# Single sort usage
/users?limit=100&offset=5
```

First, import the function get_url_query_ctx

```python
#This function can be used to process query strings 
# from the current URL in Flask
from flask_sqlalchemy_qs import get_url_query_ctx

#ctx is a dictionary that contains processed filters, sorts, limits, and offsets from the query string.
# type filters: dict()
#type offset: integer
#type limit: integer
#type sorts: list(dict())
ctx = get_url_query_ctx()
```

In order to use it in the sqlalchemy query object. The BaseQuery needs to be imported and set as the query_class

```python
from flask_sqlalchemy_qs import BaseQuery

# In this case, a Base Model is defined with its query_class attribute set to BaseQuery
class Base(db.Model):
  __abstract__ = True
  query_class = BaseQuery

class User(Base):
  id       = db.Column(db.Integer, primary_key=True)
  ...


...
#Then, you can query your models as follows:
ctx = get_url_query_ctx()
query = User.query.filter_by_ctx(filters=ctx["filters"]) \
                  .sort_by_ctx(sorts=ctx["sorts"]) \
                  .offset(ctx["offset"]) \
                  .limit("limit")

results = query.all()
```


## Version
1.0.0

## Requirements 
SQLALCHEMYSQLAlchemy~=2.0

flask~=2.2

flask-sqlalchemy~=3.0

## Contribution
Contributions to this project are welcome. Please open an issue or make a pull request.

## License
This project is licensed under the terms of the MIT license.

## Support
If you have any issues or suggestions, please open an issue on this repository.

## Authors
Marco Gil, marcogil93@gmail.com