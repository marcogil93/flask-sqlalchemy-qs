# flask-sqlalchemy-qs

flask-sqlalchemy-qs is a Python library that enables processing of query strings and its usage in conjunction with Flask and SQLAlchemy. The library provides tools for generating and manipulating SQLAlchemy filters and sorts from query strings in the URL, making it easier to build robust and flexible RESTful APIs. 

A User model has a username column attribute to filter:

`/users?filters[username][eq]=awesomeuser@example.com`


A User model has a person relationship attribute, and a list of users has to be filtered and sorted by an attribute of that relationship:

`/users?filters[person][age][gte]=22&sorts[0][person][age]=DESC&limit=10&offset=0`

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
| is          | Is                                 |
| is_not      | Is not                             |
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

#### Examples:

1) Simple usage

`/users?filters[username][eq]=username@example.com`  

2) Relationship usage (User has a person)

`/users?filters[person][name][eq]=Marco`

3) Multiple usage

`/users?filters[username][contains]=awesome.com&filters[person][age][gte]=25`

4) In and nin usage

`/users?filters[person][age][in][0]=20&filters[person][age][in][1]=25&filters[person][age][in][2]=30`

5) Boolean usage

`/users?filters[or][0][username][eq]=username1&filters[or][1][username][eq]=username2`

6) Complex boolean usage

`/users?filters[or][0][username][contains]=awesome.com&filters[or][1][not][0][and][0][person][age][gte]=20&filters[or][1][not][0][and][1][person][age][lte]=30`

7) JSON support followed by dot notation

`/users?filters[json_column.foo][eq]=bar`

<!-- blank line -->  

<!-- blank line -->  


### For the "sorts" parameter
Sort your list result by column and relationship model properties.

`GET /api/endpoint?sorts[priority_index][field]=order`

#### Examples:

1) Single sort usage

`/users?sorts[0][username]=DESC`

2) Multiple order priority and relationship usage

`/users?sorts[0][username]=DESC&sorts[1][person][age]=ASC`

### For the "limit" and "offset" parameter 
Limt (amount of elements) and offset (amount of skipped elements) for your list result. 

`GET /api/endpoint?limit=10&offset=2`

#### Examples:

`/users?limit=100&offset=5`


## Implementation 
In order to use it in the sqlalchemy query object. The BaseQuery needs to be imported and set as the query_class in the model

```python
from typing import Dict, List, Tuple, Union
from flask_sqlalchemy_qs import get_url_query_ctx, BaseQuery

...

db = SQLAlchemy(app)

# In this case, a Base Model is defined with its query_class attribute set to BaseQuery
class Base(db.Model):
  __abstract__ = True
  query_class = BaseQuery

class User(Base):
  id       = db.Column(db.Integer, primary_key=True)
  ...

...

#Types
FilterType = Dict[str, Union[bool, str, Dict]]
SortType = Dict[str, Union[str, Dict]]

...

@myblueprint.route('/users', methods=['GET'])
def get_all_users():
  #Get the query string in the correct format
  ctx: Dict[str, Union[FilterType, List[SortType], int]] = get_url_query_ctx()

  filters:FilterType   = ctx["filters"]
  sorts:List[SortType] = ctx["sorts"]
  limit:int            = ctx["limit"]
  offset:int           = ctx["offset"]


  #Query the model with the extended methods
  query = User.query.filter_by_ctx(filters=filters) \
                    .sort_by_ctx(sorts=sorts) \
                    .offset(offset) \
                    .limit(limit)
  
  ...

  results = query.all()

  ...
```

## Version
1.1.4

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