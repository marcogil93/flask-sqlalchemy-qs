from sqlalchemy import asc, desc, or_, and_, not_
from sqlalchemy.orm import Query

# BaseQuery class to extend Query class and make use
# of filtering, sorting features

class BaseQuery(Query):
  # Helper function to handle filters
  def filter_helper(self, filters, mapper, sqlalchemy_condition, query):
    conditions = []
    column_names = [column.key for column in mapper.columns]
    relation_names = [relationship.key for relationship in mapper.relationships]
    
    for filter in filters:
      for key, value in filter.items():
        # If the key refers to a column property
        if key in column_names:
          idx = column_names.index(key)
          column = mapper.columns[idx]

          #Set all the property filters
          for condition, filter_value in value.items():
            # Supported conditions
            if condition in {
              "eq",          # Equal
              "ne",          # Not equal
              "lt",          # Less than
              "lte",         # Less than or equal to
              "gt",          # Greater than
              "gte",         # Greater than or equal to
              "in",          # Included in an array
              "nin",         # Not included in an array
              "contains",    # Contains
              "ncontains",   # Does not contain
              "icontains",   # Contains (case-insensitive)
              "like",
              "ilike",
              "not_like",
              "not_ilike",
              "nicontains",  # Does not contain (case-insensitive)
              "startswith",  # Starts with 
              "istartswith", # Starts with (case-insensitive)
              "endswith",    # Ends with 
              "iendswith"    # Ends with (case-insensitive)
            }:
              if condition == "eq":
                if filter_value == "null":
                  conditions.append(column.is_(None))
                else:
                  conditions.append(column.__eq__(filter_value))
              elif condition == "ne":
                if filter_value == "null":
                  conditions.append(column.is_not(None))
                else:
                  conditions.append(column.__ne__(filter_value))
              elif condition == "lt":
                conditions.append(column.__lt__(filter_value))
              elif condition == "lte":
                conditions.append(column.__le__(filter_value))
              elif condition == "gt":
                conditions.append(column.__gt__(filter_value))
              elif condition == "gte":
                conditions.append(column.__ge__(filter_value))
              elif condition == "in":
                conditions.append(column.in_(filter_value))
              elif condition == "nin":
                conditions.append(column.notin_(filter_value))
              elif condition == "like":
                conditions.append(column.like(filter_value))
              elif condition == "not_like":
                conditions.append(column.not_like(filter_value))
              elif condition == "ilike":
                conditions.append(column.ilike(filter_value))
              elif condition == "not_ilike":
                conditions.append(column.not_ilike(filter_value))
              elif condition == "contains":
                conditions.append(column.contains(filter_value))
              elif condition == "ncontains":
                conditions.append(not_(column.contains(filter_value)))
              elif condition == "icontains":
                conditions.append(column.icontains(f"%{filter_value}%"))
              elif condition == "nicontains":
                conditions.append(not_(column.icontains(filter_value)))
              elif condition == "startswith":
                conditions.append(column.startswith(filter_value))
              elif condition == "istartswith":
                conditions.append(column.istartswith(filter_value))
              elif condition == "endswith":
                conditions.append(column.endswith(filter_value))
              elif condition == "iendswith":
                conditions.append(column.iendswith(filter_value))

        # If the key refers to a relationship
        elif key in relation_names:
          relationship = mapper.relationships[key]
          joins = query._setup_joins 
          joined_tables = set()

          for join in joins:
            joined_tables.add(join[0])
          
          #If relationship is not present in query already, join it.
          if key not in joined_tables:
            query = query.join(relationship.mapper.entity, getattr(mapper.entity, key))
          
          r_condition, query = self.filter_helper([value], relationship.mapper, and_, query)
          conditions.append(r_condition)
        
        # If the key is a boolean operator
        elif key in {"and", "or", "not"}:
          if key == 'and':
            condition, query = self.filter_helper(value, mapper, and_, query)
          elif key == 'or':
            condition, query = self.filter_helper(value, mapper, or_, query)
          elif key == 'not':
            condition, query = self.filter_helper(value, mapper, not_, query)

          conditions.append(condition)
        
        else:
          raise Exception(f"'{key}' is not a column property, nor a relationship name, nor a boolean function of (and, or, not).")
    return (sqlalchemy_condition(*conditions), query)
    
  # Function to generate filters based on the context
  def filter_by_ctx(self, filters):
    mapper = self._entity_from_pre_ent_zero()
    (conditions, query) = self.filter_helper([filters], mapper, and_, self)

    #Generate filter by conditions
    return query.filter(conditions)
  
  # Helper function to handle sorting
  def sort_hepler(self, sort, mapper, query):
    column_names = [column.key for column in mapper.columns]
    relation_names = [relationship.key for relationship in mapper.relationships]

    for key, value in sort.items():
      # If the key refers to a column property
      if key in column_names:
        idx = column_names.index(key)
        column = mapper.columns[idx]

        if value.lower() == "desc":
          query = query.order_by(desc(column))
        else:
          query = query.order_by(asc(column))

      # If the key refers to a relationship
      elif key in relation_names:
        relationship = mapper.relationships[key]
        joins = query._setup_joins 
        joined_tables = set()

        for join in joins:
          joined_tables.add(join[0])
        
        #If relationship is not present in query already, join it.
        if key not in joined_tables:
          query = query.join(relationship.mapper.entity, getattr(mapper.entity, key))
          
        query = self.sort_hepler(value, relationship.mapper, query)

    return query

  # Function to generate sorting based on the context
  def sort_by_ctx(self, sorts):
    mapper = self._entity_from_pre_ent_zero()
    query = self

    for sort in sorts:
      query = self.sort_hepler(sort, mapper, self)

    return query