from dataclasses import dataclass
from typing import Union, Tuple, Optional, List, Dict, Any

from py2gds.algorithm import AlgorithmType, Algorithm
from py2gds.collection import Collection
from py2gds.connection import Connection
from py2gds.exceptions import ProjectionIsNotSetup
from py2gds.projection import NativeProjection, ProjectionIdentity, Projection
from py2gds.rank import (
    WriteArticleRank,
    WritePageRank,
    StreamPageRank,
    StreamArticleRank,
    RankConfiguration,
    RankConfigurationWithFilter,
)
from py2gds.utils import builder


@dataclass()
class QueryBuilder:
    """
    It stores the state of a query.

    """

    _graph_connection: Connection = None
    _collection: Collection = None
    _projection: Projection = None
    _algorithm: AlgorithmType = None
    _config: RankConfiguration = None
    _prepared_query: Algorithm = None
    _max_iterations: int = 20
    _damping_factor: float = 0.80
    _write_property: Optional[str] = None
    _filter_elements: Optional[List[Tuple[str, str, Dict[str, str]]]] = None
    _returned_properties: Optional[Tuple[str, ...]] = None
    _sort_by_properties: Optional[Tuple[str, ...]] = None
    _sort_descending: bool = False
    _n_rows: Optional[int] = None
    _first_row: Optional[int] = None

    @property
    def prepared_query(self):
        if self._prepared_query:
            return self._prepared_query

        if self._write_property:
            if self._algorithm == AlgorithmType.PageRank:
                self._prepared_query = WritePageRank(
                    self._graph_connection, self._projection, self._config,
                )
            else:
                self._prepared_query = WriteArticleRank(
                    self._graph_connection, self._projection, self._config,
                )
        elif self._algorithm == AlgorithmType.PageRank:
            self._prepared_query = StreamPageRank(
                self._graph_connection,
                self._projection,
                self._config,
                limit=self._n_rows,
                returned_properties=self._returned_properties,
                sort_by_properties=self._sort_by_properties,
                sort_descending=self._sort_descending,
                skip=self._first_row,
            )
        else:
            self._prepared_query = StreamArticleRank(
                self._graph_connection,
                self._projection,
                self._config,
                limit=self._n_rows,
                returned_properties=self._returned_properties,
                sort_by_properties=self._sort_by_properties,
                sort_descending=self._sort_descending,
                skip=self._first_row,
            )
        return self._prepared_query

    @builder
    def using(
        self,
        graph_connection: Optional[Connection] = None,
        collection: Optional[Collection] = None,
    ):
        self._graph_connection = graph_connection
        self._collection = collection

    @builder
    def rank(self, algorithm: AlgorithmType):
        self._algorithm = algorithm

    @builder
    def projected_by(
        self,
        labels: Union[Tuple[str, ...], str] = '"*"',
        relationships: Union[Tuple[str, ...], str] = '"*"',
        tag: Optional[str] = None,
    ):
        if tag and not self._collection:
            raise ProjectionIsNotSetup(
                "You must setup a collection in using step or instead use "
                "labels and/or relationships parameters"
            )

        if tag:
            self._projection = self._collection.get_projection_by_tag(tag)
        else:
            self._projection = NativeProjection(
                self._graph_connection,
                ProjectionIdentity(labels=labels, relationships=relationships),
            )

    @builder
    def set(self, max_iterations: int, damping_factor: float):
        self._max_iterations = max_iterations
        self._damping_factor = damping_factor

    @builder
    def select(self, *returned_properties: str):
        """
        This function allows to select the returned properties of the query.

        Args:
            returned_properties: The names of node properties that query will return.

        """
        self._returned_properties = returned_properties

    @builder
    def order_by(self, *sort_by_properties: str, descending: bool = False):
        """
        This function allows to select the returned properties of the query.

        Args:
            sort_by_properties: The names of node properties used to sort the output.
            descending: it indicates if it is sorted in descending order or not.

        """
        self._sort_by_properties = sort_by_properties
        self._sort_descending = descending

    @builder
    def skip(self, first_row: int):
        """
        SKIP defines from which row to start including the rows in the output.

        Args:
            first_row: first row from which it starts.

        """
        self._first_row = first_row

    @builder
    def limit(self, n_rows: int):
        """
         LIMIT constrains the number of rows in the output.

        Args:
            n_rows: number of rows of the output.

        """
        self._n_rows = n_rows

    @builder
    def write(self, property_name: str):
        """
        When using this function, the query will store scores in nodes' property with name property_name.

        Args:
            property_name: Name of the property where the results will be stored.

        """
        self._write_property = property_name

    def _setup_config(self):
        if self._filter_elements:
            self._config = RankConfigurationWithFilter(
                max_iterations=self._max_iterations,
                damping_factor=self._damping_factor,
                write_property=self._write_property,
                filter_elements=self._filter_elements,
            )
        else:
            self._config = RankConfiguration(
                max_iterations=self._max_iterations,
                damping_factor=self._damping_factor,
                write_property=self._write_property,
            )

    def _setup_projection(self, log: bool = True):
        if not self._projection.exists(log):
            self._projection.create(log)

    def run(self, log: bool = True) -> str:
        self._setup_config()
        self._setup_projection(log)

        return self.prepared_query.run(log)

    def __str__(self):
        self._setup_config()
        return self.prepared_query.cypher


class Query:
    """
    It is used to build queries through a DSL. Its format is inspired in IGQL:
    https://ai.facebook.com/blog/powered-by-ai-instagrams-explore-recommender-system/

    """

    @classmethod
    def _builder(cls, **kwargs: Any) -> QueryBuilder:
        return QueryBuilder(**kwargs)

    @classmethod
    def using(
        cls,
        graph_connection: Connection,
        collection: Optional[Collection] = None,
        **kwargs: Any,
    ) -> QueryBuilder:
        """
        Query builder entry point. It initializes query building with graph_connection and optional collection.

        Args:
            graph_connection: Connection used to talk with the database.
            collection: If this parameter is used, projections can be used selecting it by tag in projected_by function.

        Returns:
            QueryBuilder.

        """
        return cls._builder(**kwargs).using(graph_connection, collection)

    @classmethod
    def rank(cls, algorithm: AlgorithmType, **kwargs: Any) -> QueryBuilder:
        """
        Query builder entry point. It initializes query building with the algorithm that we are going to use in that
        query.

        Args:
            algorithm: Enum string that define the used algorithm.

        Returns:
            QueryBuilder.

        """
        return cls._builder(**kwargs).rank(algorithm)

    @classmethod
    def projected_by(
        cls,
        *,
        labels: Union[Tuple[str, ...], str] = '"*"',
        relationships: Union[Tuple[str, ...], str] = '"*"',
        tag: Optional[str] = None,
        **kwargs: Any,
    ) -> QueryBuilder:
        """
        Query builder entry point. It initializes query setting the projection that query will use.

        Args:
            labels: Labels' names used to create the projection.
            relationships: Relationships' names used to create the projection.
            tag: if a collection is used (see using method), can get a projection by tag using this parameter.

        Returns:
            QueryBuilder.

        """
        return cls._builder(**kwargs).projected_by(labels, relationships, tag)

    @classmethod
    def set(
        cls, max_iterations: int, damping_factor: float, **kwargs: Any
    ) -> QueryBuilder:
        """
        Query builder entry point. It initializes query with algorithm's parameters.

        Args:
            max_iterations: The maximum number of iterations of Rank to run.
            damping_factor: The damping factor of the Rank calculation.

        Returns:
            QueryBuilder

        """
        return cls._builder(**kwargs).set(max_iterations, damping_factor)

    @classmethod
    def write(cls, property_name: str, **kwargs: Any) -> QueryBuilder:
        """
        When using this function, the query will store scores in nodes' property with name property_name.

        Args:
            property_name: The name of the property where it's going to be saved the result score.

        Returns:
            QueryBuilder.

        """
        return cls._builder(**kwargs).write(property_name)

    @classmethod
    def select(cls, *returned_properties: List[str], **kwargs: Any):
        """
        Query builder entry point. It will setup the returned properties of the resulting nodes.

        Args:
            returned_properties: The names of node properties that query will return.

        Returns:
            QueryBuilder

        """
        return cls._builder(**kwargs).select(*returned_properties)

    @classmethod
    def order_by(
        cls, *sort_by_properties: List[str], descending: bool = False, **kwargs: Any
    ):
        """
        Query builder entry point. ORDER BY is used to sort the output according to specified properties.

        Args:
            sort_by_properties: The names of node properties used to sort the output.
            descending: it indicates if it is sorted in descending order or not.

        Returns:
            QueryBuilder

        """
        return cls._builder(**kwargs).order_by(
            *sort_by_properties, descending=descending
        )

    @classmethod
    def skip(cls, first_row: int, **kwargs: Any):
        """
        Query builder entry point. SKIP defines from which row to start including the rows in the output.

        Args:
            first_row: first row from which it starts.

        Returns:
            QueryBuilder

        """
        return cls._builder(**kwargs).skip(first_row)

    @classmethod
    def limit(cls, n_rows: int, **kwargs: Any):
        """
        Query builder entry point. LIMIT constrains the number of rows in the output.

        Args:
            n_rows: number of rows of the output

        Returns:
            QueryBuilder

        """
        return cls._builder(**kwargs).limit(n_rows)
