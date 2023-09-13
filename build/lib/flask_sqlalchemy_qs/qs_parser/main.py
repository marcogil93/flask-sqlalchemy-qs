from typing import Dict, List, Tuple, Union
from flask import request

#Types
FilterType = Dict[str, Union[bool, str, Dict]]
SortType = Dict[str, Union[str, Dict]]

def parse_filters(items: List[Tuple[str, str]]) -> FilterType:
  filters = {}
  
  for key, value in items:
    if key.startswith("filters"):
      parts = key.split("[")
      target_dict = filters
      ##Remove first index: filters
      parts.pop(0)

      for i, part in enumerate(parts):
        #remove ] char
        part = part[:-1]

        #is final condition (eq, contains, ...)   index in
        if i == len(parts) -1:
          if value == 'true':
            target_dict[part] = True
          elif value == 'false':
            target_dict[part] = False
          elif value == 'null':
            target_dict[part] = None
          else:
            if part.isdigit(): #Case in, nin
              target_dict[int(part)] = value
            else:
              target_dict[part] = value
        
        elif part in ["in", "nin"]:
          if part not in target_dict:
            target_dict[part] = []

          #Get the index of the clause: ex. or[idx] ... and[idx]
          idx = int(parts[i + 1][:-1])

          #got index out of limit, so create empty dicts 
          # (can happen due to the order of getting filters)
          if idx >= len(target_dict[part]):
            target_dict[part].extend([None] * (idx + 1 - len(target_dict[part])))
            
          target_dict = target_dict[part]
          

        elif part in ['and', 'or', 'not']:
          if part not in target_dict:
            target_dict[part] = []
          
          #Get the index of the clause: ex. or[idx] ... and[idx]
          idx = int(parts[i + 1][:-1])

          #got index out of limit, so create empty dicts 
          # (can happen due to the order of getting filters)
          if idx >= len(target_dict[part]):
            target_dict[part].extend([{}] * (idx + 1 - len(target_dict[part])))
        
          #set the (nested) dict as the one to be modified
          target_dict = target_dict[part][idx]
        
        #is a prop or relationship
        elif not part.isdigit(): #Relationship case
          if part not in target_dict:
            target_dict[part] = {}
          #set the (nested) dict as the one to be modified
          target_dict = target_dict[part]

  return filters
  
def parse_sort(items: List[Tuple[str, str]]) -> List[SortType]:
  sorts = []
  
  for key, value in items:
    if key.startswith("sorts"):
      parts = key.split("[")
      target_dict = {}
      ##Remove first index: filters
      parts.pop(0)
      print(parts)

      for i, part in enumerate(parts):
        #remove ] char
        part = part[:-1]

        if part.isdigit():
          idx = int(part)
          len_sort = len(sorts)

          if(idx >= len_sort):
            sorts.extend([{}] * (idx + 1 - len_sort))

          target_dict = sorts[idx]
        #is final property
        elif i == len(parts) -1:
          target_dict[part] = value

        #is relationship name
        elif i < len(parts) - 1:
          field = part

          if field not in target_dict:
            target_dict[field] = {}

          #set the (nested) dict as the one to be modified
          target_dict = target_dict[field]

  return sorts
  
def get_url_query_ctx() -> Dict[str, Union[FilterType, int, List[SortType]]]:
  filters = parse_filters(request.args.items(multi=True))
  offset  = request.args.get("offset", default=0, type=int)
  limit   = request.args.get("limit", default=10, type=int)
  sorts   = parse_sort(request.args.items(multi=True))

  ctx = {
    "filters": filters,
    "offset": offset,
    "limit": limit,
    "sorts": sorts
  }

  return ctx