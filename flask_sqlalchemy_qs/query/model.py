"""
BaseQuery class to extend Query class and make use of filtering and
sorting features
"""

from sqlalchemy import asc, desc, or_, and_, not_
from sqlalchemy.orm import Query, Mapper
from typing import List

from .constants import CONDITIONS, CASTS, FilterType, SortType, BooleanExpression

class BaseQuery(Query):
    """
    BaseQuery class extends the Query class and provides additional filtering and sorting features.
    """

    def filter_helper(
        self,
        filters: FilterType,
        mapper: Mapper,
        sqlalchemy_condition: BooleanExpression,
        query: Query,
    ) -> Query:
        """
        Helper function to handle filters.

        Args:
            filters: The filters to be applied.
            mapper: The mapper for the current entity.
            sqlalchemy_condition: The SQLAlchemy boolean expression (or_, and_, not_).
            query: The current Query object.

        Returns:
            A Query object with the applied filters.
        """
        conditions = []
        column_names = [column.key for column in mapper.columns]
        relation_names = [relationship.key for relationship in mapper.relationships]

        for filter in filters:
            for key, value in filter.items():
                try:
                    # If the key refers to a column property
                    if key in column_names:
                        idx = column_names.index(key)
                        column = mapper.columns[idx]

                        # Set all the property filters
                        for condition, filter_value in value.items():
                            if condition in CONDITIONS:
                                column_condition = CONDITIONS[condition]
                                condition_func = getattr(
                                    column, column_condition
                                )
                                
                                #Cast value to its necessary type if needed
                                if type(filter_value) == str and column.type.python_type in CASTS:
                                    value = column.type.python_type(filter_value)
                                else: 
                                    value = filter_value

                                if condition in {"ncontains", "nicontains"}:
                                    # No native ncontains, nor nicontains attr.
                                    # Use of a not and the contains, and 
                                    # icontains attrs.
                                    conditions.append(
                                        not_(condition_func(value))
                                    )
                                else:
                                    conditions.append(
                                        condition_func(value)
                                    )
                            else:
                                raise Exception(
                                    f"'{condition}' is not a supported condition."
                                )

                    # If the key refers to a relationship
                    elif key in relation_names:
                        relationship = mapper.relationships[key]
                        joins = query._setup_joins
                        joined_tables = set()

                        for join in joins:
                            joined_tables.add(join[0])

                        # If relationship is not present in query already, join it.
                        if key not in joined_tables:
                            query = query.join(
                                relationship.mapper.entity,
                                getattr(mapper.entity, key),
                            )

                        r_condition, query = self.filter_helper(
                            [value], relationship.mapper, and_, query
                        )
                        conditions.append(r_condition)

                    # If the key is a boolean operator
                    elif key in {"and", "or", "not"}:
                        if key == "and":
                            condition, query = self.filter_helper(
                                value, mapper, and_, query
                            )
                        elif key == "or":
                            condition, query = self.filter_helper(
                                value, mapper, or_, query
                            )
                        elif key == "not":
                            condition, query = self.filter_helper(
                                value, mapper, not_, query
                            )

                        conditions.append(condition)

                    else:
                        raise Exception(
                            f"'{key}' is not a column property, nor a relationship name, nor a boolean function of (and, or, not)."
                        )

                except Exception as e:
                    # Handle the exception here
                    print(f"Exception occurred: {str(e)}")

        return sqlalchemy_condition(*conditions), query

    def filter_by_ctx(self, filters: FilterType) -> Query:
        """
        Function to generate filters based on the context.

        Args:
            filters: The filters to be applied.

        Returns:
            A Query object with the applied filters.
        """
        try:
            mapper = self._entity_from_pre_ent_zero()
            conditions, query = self.filter_helper([filters], mapper, and_, self)

            # Generate filter by conditions
            return query.filter(conditions)

        except Exception as e:
            # Handle the exception here
            print(f"Exception occurred: {str(e)}")

    def sort_helper(
        self, sort: SortType, mapper: Mapper, query: Query
    ) -> Query:
        """
        Helper function to handle sorting.

        Args:
            sort: The sorting instructions.
            mapper: The mapper for the current entity.
            query: The current Query object.

        Returns:
            A Query object with the applied sorting.
        """
        column_names = [column.key for column in mapper.columns]
        relation_names = [relationship.key for relationship in mapper.relationships]

        for key, value in sort.items():
            try:
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

                    # If relationship is not present in query already, join it.
                    if key not in joined_tables:
                        query = query.join(
                            relationship.mapper.entity,
                            getattr(mapper.entity, key),
                        )

                    query = self.sort_helper(value, relationship.mapper, query)

            except Exception as e:
                # Handle the exception here
                print(f"Exception occurred: {str(e)}")

        return query

    def sort_by_ctx(self, sorts: List[SortType]) -> Query:
        """
        Function to generate sorting based on the context.

        Args:
            sorts: The sorting instructions.

        Returns:
            A Query object with the applied sorting.
        """
        try:
            mapper = self._entity_from_pre_ent_zero()
            query = self

            for sort in sorts:
                query = self.sort_helper(sort, mapper, self)

            return query

        except Exception as e:
            # Handle the exception here
            print(f"Exception occurred: {str(e)}")