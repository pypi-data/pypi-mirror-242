# -*- coding: utf-8 -*-
import random
from typing import Any, Optional, List, TypeVar

from pip_services4_commons.convert import LongConverter
from pip_services4_commons.errors import ConnectionException, InvalidStateException, ApplicationException
from pip_services4_commons.reflect import PropertyReflector
from pip_services4_components.config import IConfigurable, ConfigParams
from pip_services4_components.context import IContext, ContextResolver
from pip_services4_components.refer import IReferenceable, IUnreferenceable, IReferences, DependencyResolver
from pip_services4_components.run import IOpenable, ICleanable
from pip_services4_data.query import PagingParams, DataPage
from pip_services4_observability.log import CompositeLogger

from pip_services4_mysql.connect.MySqlConnection import MySqlConnection

T = TypeVar('T')  # Declare type variable


class MySqlPersistence(IReferenceable, IUnreferenceable, IConfigurable, IOpenable, ICleanable):
    """
    Abstract persistence component that stores data in MySQL using plain driver.

    This is the most basic persistence component that is only
    able to store data items of any type. Specific CRUD operations
    over the data items must be implemented in child classes by
    accessing **self._db** or **self._collection** properties.

    ### Configuration parameters ###
        - table:                  (optional) MySQL table name
        - schema:                 (optional) MySQL schema name
        - connection(s):
            - discovery_key:             (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services4_components.connect.IDiscovery.IDiscovery>`
            - host:                      host name or IP address
            - port:                      port number (default: 27017)
            - uri:                       resource URI or connection string with all parameters in it
        - credential(s):
            - store_key:                 (optional) a key to retrieve the credentials from :class:`ICredentialStore <pip_services4_components.auth.ICredentialStore.ICredentialStore>`
            - username:                  (optional) user name
            - password:                  (optional) user password
        - options:
            - connect_timeout:      (optional) number of milliseconds to wait before timing out when connecting a new client (default: 0)
            - idle_timeout:         (optional) number of milliseconds a client must sit idle in the pool and not be checked out (default: 10000)
            - max_pool_size:        (optional) maximum number of clients the pool should contain (default: 10)

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>` components to pass log messages components to pass log messages
        - `*:discovery:*:*:1.0`        (optional) :class:`IDiscovery <pip_services4_components.connect.IDiscovery.IDiscovery>` services
        - `*:credential-store:*:*:1.0` (optional) :class:`ICredentialStore <pip_services4_components.auth.ICredentialStore.ICredentialStore>` stores to resolve credentials

    Example:

    .. code-block:: python

        class MyMySqlPersistence(MySqlPersistence):
            def __init__(self):
                super(MyMySqlPersistence, self).__init__('mydata')

            def get_by_name(self, context, name):
                criteria = {'name':name}
                return self._model.find_one(criteria)

            def set(self,context, item):
                criteria = {'name': item['name']}
                options = {'upsert': True, 'new': True}
                return self._model.find_one_and_update(criteria, item, options)

        persistence =MyMySqlPersistence()
        persistence.configure(ConfigParams.from_tuples(
            "host", "localhost",
            "port", 27017
        ))
        persistence.open(context)
        persistence.set(context, {'name':'ABC'})
        item = persistence.get_by_name(context, 'ABC')
        print(item) # Result: { name: "ABC" }
    """

    _default_config = ConfigParams.from_tuples(
        "table", None,
        "schema", None,
        "dependencies.connection", "*:connection:mysql:*:1.0",

        # connections.*
        # credential.*

        "options.max_pool_size", 2,
        "options.keep_alive", 1,
        "options.connect_timeout", 5000,
        "options.auto_reconnect", True,
        "options.max_page_size", 100,
        "options.debug", True
    )

    def __init__(self, table_name: str = None, schema_name: str = None):
        """
        Creates a new instance of the persistence component.

        :param table_name: (optional) a table name.
        :param schema_name: (optional) a schema name.
        """
        self.__config: ConfigParams = None
        self.__references: IReferences = None
        self.__opened: bool = None
        self.__local_connection: bool = None

        self.__schema_statements = []

        # The dependency resolver.
        self._dependency_resolver: DependencyResolver = DependencyResolver(self._default_config)
        # The logger.
        self._logger: CompositeLogger = CompositeLogger()
        # The MySQL connection component.
        self._connection: MySqlConnection = None
        # The MySQL connection pool object.
        self._client: Any = None
        # The MySQL database name.
        self._database_name: str = None
        # The MySQL table object.
        self._table_name: str = None
        # Max number of objects in data pages
        self._max_page_size: int = 100

        self._table_name = table_name
        self._schema_name = schema_name

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        config = config.set_defaults(MySqlPersistence._default_config)
        self.__config = config

        self._dependency_resolver.configure(config)

        self._table_name = config.get_as_string_with_default('collection', self._table_name)
        self._table_name = config.get_as_string_with_default('table', self._table_name)
        self._schema_name = config.get_as_string_with_default('schema', self._schema_name)
        self._max_page_size = config.get_as_integer_with_default('options.max_page_size', self._max_page_size)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self.__references = references
        self._logger.set_references(references)

        # Get connection
        self._dependency_resolver.set_references(references)
        self._connection = self._dependency_resolver.get_one_optional('connection')
        # Or create a local one
        if not self._connection:
            self._connection = self.__create_connection()
            self.__local_connection = True
        else:
            self.__local_connection = False

    def unset_references(self):
        """
        Unsets (clears) previously set references to dependent components.
        """
        self._connection = None

    def __create_connection(self) -> MySqlConnection:
        connection = MySqlConnection()

        if self.__config:
            connection.configure(self.__config)
        if self.__references:
            connection.set_references(self.__references)

        return connection

    def _ensure_index(self, name: str, keys: Any, options: Any = None):
        builder = 'CREATE'
        options = options or {}

        if options.get('unique'):
            builder += ' UNIQUE'

        index_name = self._quote_identifier(name)
        if self._schema_name is not None:
            index_name = self._quote_identifier(self._schema_name) + '.' + index_name

        builder += " INDEX " + index_name + " ON " + self._quoted_table_name()
        if options.get('type'):
            builder += " " + options['type']

        fields = ''
        for key in keys:
            if fields != '':
                fields += ', '
            fields += self._quote_identifier(key)
            asc = keys[key]
            if not asc:
                fields += ' DESC'

        builder += '(' + fields + ')'

        self._ensure_schema(builder)

    def _ensure_schema(self, schema_statement: str):
        """
        Adds a statement to schema definition

        :param schema_statement: a statement to be added to the schema
        """
        self.__schema_statements.append(schema_statement)

    def _clear_schema(self):
        """
        Clears all auto-created objects
        """
        self.__schema_statements.clear()

    def _define_schema(self):
        # Todo: override in chile classes
        self._clear_schema()

    def _convert_to_public(self, value: Any) -> Any:
        """
        Converts object value from internal to public format.

        :param value: an object in internal format to convert.
        :return:  converted object in public format.
        """
        if value is None:
            return

        return type('object', (object,), value)

    def _convert_from_public(self, value: Any) -> Any:
        """
        Convert object value from public to internal format.

        :param value: an object in public format to convert.
        :return: converted object in internal format.
        """
        if isinstance(value, dict):
            return value
        props = PropertyReflector.get_properties(value)

        # remove protected and private keys
        if isinstance(props, dict):
            keys = list(props.keys())
            for k in keys:
                if k.startswith('_'):
                    del props[k]

        return props

    def _quote_identifier(self, value: str) -> str:
        if value is None or value == '':
            return ''
        if value[0] == '`':
            return value
        return '`' + value + '`'

    def _quoted_table_name(self) -> Optional[str]:
        if self._table_name is None:
            return None

        builder = self._quote_identifier(self._table_name)
        if self._schema_name is not None:
            builder = self._quote_identifier(self._schema_name) + '.' + builder

        return builder

    def is_open(self):
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self.__opened

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        :return: raise error or null no errors occured.
        """
        if self.__opened:
            return

        if self._connection is None:
            self._connection = self.__create_connection()
            self.__local_connection = True

        if self.__local_connection:
            self._connection.open(context)

        if not self._connection.is_open():
            self.__opened = False
            raise ConnectionException(ContextResolver.get_trace_id(context), "CONNECT_FAILED",
                                      "MySQL connection is not opened")
        else:
            self._client = self._connection.get_connection()
            self._database_name = self._connection.get_database_name()

            # Define database schema
            self._define_schema()

            # Recreate objects
            try:
                self._create_schema(context)
                self.__opened = True
                self._logger.debug(context, "Connected to mysql database %s, collection %s",
                                   self._database_name,
                                   self._table_name)
            except Exception as err:
                raise ConnectionException(ContextResolver.get_trace_id(context), "CONNECT_FAILED",
                                          "Connection to mysql failed").with_cause(err)

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        :return: raise error or None no errors occured.
        """
        if not self.__opened:
            return

        if self._connection is None:
            raise InvalidStateException(ContextResolver.get_trace_id(context), 'NO_CONNECTION',
                                        'MySql connection is missing')

        if self.__local_connection:
            self._connection.close(context)

        self.__opened = False
        self._client = None

    def _request(self, query: str, params: List[str] = None) -> dict:
        """
        Performs a request to the database.

        :param query: string with sql query to database
        :param params: optional list of query parameters
        :return: result of the query
        """
        result = {'rowcount': None,
                  'items': [],
                  'column_names': None,
                  'statement': None
                  }

        conn = self._client.get_connection()
        cursor = conn.cursor()

        for response in cursor.execute(query, params=params, multi=True):
            response = response.fetchall()
            for val in response:
                result['items'].append(dict(zip(cursor.column_names, val)))

        # affected rows
        result.update({'rowcount': cursor.rowcount,
                       'column_names': cursor.column_names,
                       'statement': cursor.statement})

        conn.commit()
        cursor.close()
        conn.close()
        return result

    def clear(self, context: Optional[IContext]):
        """
        Clears component state.

        :param context: (optional) transaction id to trace execution through call chain.
        :return: raise error or None no errors occured.
        """

        # Return error if collection is not set
        if self._table_name is None:
            raise ApplicationException(ContextResolver.get_trace_id(context), message='Table name is not defined')

        query = "DELETE FROM " + self._quoted_table_name()

        try:
            self._request(query)
        except Exception as err:
            ConnectionException(ContextResolver.get_trace_id(context), "CONNECT_FAILED",
                                "Connection to mysql failed").with_cause(err)

    def _create_schema(self, context: Optional[IContext]):
        if not self.__schema_statements or len(self.__schema_statements) == 0:
            return

        # Check if table exist to determine weither to auto create objects
        # Todo: include schema
        query = "SHOW TABLES LIKE '" + self._table_name + "'"

        result = self._request(query)

        # If table already exists then exit
        if result['items'] and len(result['items']) > 0:
            return

        self._logger.debug(context,
                           'Table ' + self._table_name + ' does not exist. Creating database objects...')

        # Run all DML commands
        try:
            for dlm in self.__schema_statements:
                self._request(dlm)
        except Exception as err:
            self._logger.error(context, err, 'Failed to autocreate database object')

    def _generate_columns(self, values: Any) -> str:
        """
        Generates a list of column names to use in SQL statements like: "column1,column2,column3"

        :param values: an array with column values or a key-value map
        :return: a generated list of column names
        """
        # values = [val for val in values.__dict__ if
        #           not val.startswith('_') and
        #           not callable(getattr(values, val))] \
        #     if not isinstance(values, dict) else values.keys()

        values = values.keys()

        result = ''
        for value in values:
            if result != '':
                result += ','
            result += self._quote_identifier(value)

        return result

    def _generate_parameters(self, values: Any) -> str:
        """
        Generates a list of value parameters to use in SQL statements like: "$1,$2,$3"

        :param values: an array with values or a key-value map
        :return: a generated list of value parameters
        """
        values = values if not isinstance(values, dict) else values.keys()

        result = ''
        for val in values:
            if result != '':
                result += ','
            result += '%s'  # "$" + index;

        return result

    def _generate_set_parameters(self, values: Any) -> str:
        """
        Generates a list of column sets to use in UPDATE statements like: column1=$1,column2=$2

        :param values: a key-value map with columns and values
        :return: a generated list of column sets
        """
        result = ''
        index = 1
        for column in values.keys():
            if result != '':
                result += ','
            result += self._quote_identifier(column) + '=%s'  # "=$" + index;
            index += 1

        return result

    def _generate_values(self, values: Any) -> List[Any]:
        return list(values.values())

    def get_page_by_filter(self, context: Optional[IContext], filter: Any, paging: PagingParams,
                           sort: Any, select: Any) -> DataPage:
        """
        Gets a page of data items retrieved by a given filter and sorted according to sort parameters.
        This method shall be called by a public getPageByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param context: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter JSON object
        :param paging: (optional) paging parameters
        :param sort: (optional) sorting JSON object
        :param select: (optional) projection JSON object
        :return: a data page or raise error
        """
        select = select if select and len(select) > 0 else '*'
        query = "SELECT " + select + " FROM " + self._quoted_table_name()

        # Adjust max item count based on configuration
        paging = paging or PagingParams()
        skip = paging.get_skip(-1)
        take = paging.get_take(self._max_page_size)
        paging_enabled = paging.total

        if filter and filter != '':
            query += " WHERE " + filter

        if sort:
            query += " ORDER BY " + sort

        query += " LIMIT " + str(take)

        if skip >= 0:
            query += " OFFSET " + str(skip)

        result = self._request(query)
        items = result['items']

        if items is not None:
            self._logger.trace(context, "Retrieved %d from %s", len(items), self._table_name)

        items = list(map(self._convert_to_public, items))

        if paging_enabled:
            query = 'SELECT COUNT(*) AS count FROM ' + self._quoted_table_name()
            if filter is not None and filter != '':
                query += " WHERE " + filter
            result = self._request(query)
            count = LongConverter.to_long(len(result['items'][0])) if result and len(result['items']) == 1 else 0

            return DataPage(items, count)
        else:
            return DataPage(items)

    def get_count_by_filter(self, context: Optional[IContext], filter: Any) -> int:
        """
        Gets a number of data items retrieved by a given filter.
        This method shall be called by a public getCountByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param context: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter JSON object
        :return: a data page or error
        """
        query = 'SELECT COUNT(*) AS count FROM ' + self._quoted_table_name()

        if filter and filter != '':
            query += " WHERE " + filter

        result = self._request(query)
        count = LongConverter.to_long(len(result['items'][0])) if result and len(result['items']) == 1 else 0

        if count:
            self._logger.trace(context, "Counted %d items in %s", count, self._table_name)

        return count

    def get_list_by_filter(self, context: Optional[IContext], filter: Any, sort: Any, select: Any) -> List[T]:
        """
        Gets a list of data items retrieved by a given filter and sorted according to sort parameters.
        This method shall be called by a public getListByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param context: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter JSON object
        :param sort: (optional) sorting JSON object
        :param select: (optional) projection JSON object
        :return: a data list
        """

        select = select if select and len(select) > 0 else '*'
        query = "SELECT " + select + " FROM " + self._quoted_table_name()
        if filter and filter != '':
            query += " WHERE " + filter

        if sort:
            query += " ORDER BY " + sort

        result = self._request(query)
        items = result['items']

        if items:
            self._logger.trace(context, "Retrieved %d from %s", len(items), self._table_name)

        items = list(map(self._convert_to_public, items))

        return items

    def get_one_random(self, context: Optional[IContext], filter: Any) -> T:
        """
        Gets a random item from items that match to a given filter.
        This method shall be called by a public getOneRandom method from child class that
        receives FilterParams and converts them into a filter function.

        :param context: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter JSON object
        :return: a random item
        """
        query = 'SELECT COUNT(*) AS count FROM ' + self._quoted_table_name()

        if filter and filter != '':
            query += " WHERE " + filter

        result = self._request(query)

        query = "SELECT * FROM " + self._quoted_table_name()

        if filter and filter != '':
            query += " WHERE " + filter

        count = result['items'][0].get('count') if result['items'] and len(result['items']) == 1 else 0
        count = 0 if count == 0 else count - 1

        pos = random.randint(0, count)
        query += f" LIMIT 1 OFFSET {pos}"

        result = self._request(query)
        item = result['items'][0] if result['items'] is not None and len(result['items']) > 0 else None

        if item:
            self._logger.trace(context, "Random item wasn't found from %s", self._table_name)
        else:
            self._logger.trace(context, "Retrieved random item from %s", self._table_name)

        return self._convert_to_public(item)

    def create(self, context: Optional[IContext], item: T) -> Optional[T]:
        """
        Creates a data item.

        :param context: (optional) transaction id to trace execution through call chain.
        :param item: an item to be created.
        :return: created item
        """
        if not item:
            return
        row = self._convert_from_public(item)
        columns = self._generate_columns(row)
        params = self._generate_parameters(row)
        values = self._generate_values(row)

        query = "INSERT INTO " + self._quoted_table_name() + " (" + columns + ") VALUES (" + params + ")"
        # query += "; SELECT * FROM " + self._quoted_table_name()
        self._request(query, values)

        self._logger.trace(context, "Created in %s with id = %s", self._quoted_table_name(),
                           item.id)
        # new_item = self._convert_to_public(result['items'][0]) if result['items'] and len(result['items']) == 1 else None

        new_item = item

        return new_item

    def delete_by_filter(self, context: Optional[IContext], filter: Any):
        """
        Deletes data items that match to a given filter.

        :param context: (optional) transaction id to trace execution through call chain.
        :param filter: (optional) a filter JSON object.
        :return: null for success
        """
        query = "DELETE FROM " + self._quoted_table_name()
        if filter and filter != '':
            query += " WHERE " + filter

        result = self._request(query)

        count = result['rowcount'] if result['rowcount'] else 0

        self._logger.trace(context, "Deleted %d items from %s", count, self._table_name)
