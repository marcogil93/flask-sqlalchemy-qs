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
    "is": "is_",
    "is_not": "is_not",
    "eq": "__eq__",
    "ne": "__ne__",
    "lt": "__lt__",
    "lte": "__le__",
    "gt": "__gt__",
    "gte": "__ge__",
    "in": "in_",
    "nin": "notin_",
    "contains": "contains",
    "ncontains": "contains",
    "icontains": "icontains",
    "nicontains": "icontains",
    "like": "like",
    "ilike": "ilike",
    "not_like": "not_like",
    "not_ilike": "not_ilike",
    "startswith": "startswith",
    "istartswith": "istartswith",
    "endswith": "endswith",
    "iendswith": "iendswith"
}

CASTS = {int, float}