"""
This file is to integrate constants
"""
from typing import Dict, Union
from sqlalchemy import or_, and_, not_

# Types
FilterType = Dict[str, Union[bool, str, Dict]]
SortType = Dict[str, Union[str, Dict]]
BooleanExpression = Union[or_, and_, not_]

CONDITIONS = {
    "eq": "__eq__",
    "ne": "__ne__",
    "lt": "__lt__",
    "lte": "__le__",
    "gt": "__gt__",
    "gte": "__ge__",
    "in": "in_",
    "nin": "notin_",
    "contains": "contains",
    "ncontains": "ncontains",
    "icontains": "icontains",
    "like": "like",
    "ilike": "ilike",
    "not_like": "not_like",
    "not_ilike": "not_ilike",
    "nicontains": "nicontains",
    "startswith": "startswith",
    "istartswith": "istartswith",
    "endswith": "endswith",
    "iendswith": "iendswith"
}