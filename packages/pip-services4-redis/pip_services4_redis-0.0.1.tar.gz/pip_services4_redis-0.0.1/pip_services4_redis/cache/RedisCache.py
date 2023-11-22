# -*- coding: utf-8 -*-
from typing import Optional, Any

import redis
from pip_services4_commons.errors import ConfigException, InvalidStateException
from pip_services4_components.config import ConfigParams, IConfigurable
from pip_services4_components.context import IContext, ContextResolver
from pip_services4_components.refer import IReferences, IReferenceable
from pip_services4_components.run import IOpenable
from pip_services4_config.auth import CredentialResolver
from pip_services4_config.connect import ConnectionResolver
from pip_services4_logic.cache import ICache


class RedisCache(ICache, IConfigurable, IReferenceable, IOpenable):
    """
    Distributed cache that stores values in Redis in-memory database.

    ### Configuration parameters ###

    - connection(s):
        - discovery_key:         (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services4_components.connect.IDiscovery.IDiscovery>`
        - host:                  host name or IP address
        - port:                  port number
        - uri:                   resource URI or connection string with all parameters in it
    - credential(s):
        - store_key:             key to retrieve parameters from credential store
        - username:              user name (currently is not used)
        - password:              user password
    - options:
        - retries:               number of retries (default: 3)
        - timeout:               default caching timeout in milliseconds (default: 1 minute)
        - max_size:              maximum number of values stored in this cache (default: 1000)

    ### References ###

    - `*:discovery:*:*:1.0`        (optional) :class:`IDiscovery <pip_services4_components.connect.IDiscovery.IDiscovery>` services to resolve connection
    - `*:credential-store:*:*:1.0` (optional) Credential stores to resolve credential


    Example:

    .. code-block:: python

        cache = RedisCache()
        cache.configure(ConfigParams.from_tuples(
            "host", "localhost",
            "port", 6379
        ))
        cache.open(context)
        cache.store(context, "key1", "ABC", None)
        value = cache.retrieve(context, "key1") # Result: "ABC"
    """

    def __init__(self):
        """
        Creates a new instance of this cache
        """

        self.__connection_resolver: ConnectionResolver = ConnectionResolver()
        self.__credential_resolver: CredentialResolver = CredentialResolver()

        self.__timeout: int = 30000
        self.__retries: int = 3
        self.__client: redis.Redis = None

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self.__connection_resolver.configure(config)
        self.__credential_resolver.configure(config)

        self.__timeout = config.get_as_integer_with_default('options.timeout', self.__timeout)
        self.__retries = config.get_as_integer_with_default('options.retries', self.__retries)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self.__connection_resolver.set_references(references)
        self.__connection_resolver.set_references(references)

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self.__client is not None

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        connection = self.__connection_resolver.resolve(context)
        if connection is None:
            raise ConfigException(
                ContextResolver.get_trace_id(context),
                'NO_CONNECTION',
                'Connection is not configured'
            )

        credential = self.__credential_resolver.lookup(context)

        options = {
            # connect_timeout: self.__timeout,
            # max_attempts: self.__retries,
            'retry_on_timeout': True,
            # 'retry_strategy': lambda options: self.__retry_strategy(options)  # TODO add reconnect callback
        }

        if connection.get_uri():
            options['url'] = connection.get_uri()
        else:
            options['host'] = connection.get_host() or 'localhost'
            options['port'] = connection.get_port() or 6379

        if credential is not None:
            options['password'] = credential.get_password()

        self.__client = redis.Redis(**options)

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self.__client is None: return

        self.__client.close()
        self.__client = None

    def __check_opened(self, context: Optional[IContext]):
        if not self.is_open():
            raise InvalidStateException(
                ContextResolver.get_trace_id(context),
                'NOT_OPENED',
                'Connection is not opened'
            )

    def __retry_strategy(self, options: dict) -> Any:
        if options['error'] and options['error']['code'] == 'ECONNREFUSED':
            # End reconnecting on a specific error and flush all commands with
            # a individual error
            return Exception('The server refused the connection')

        if options['total_retry_time'] > self.__timeout:
            # End reconnecting after a specific timeout and flush all commands
            # with a individual error
            return Exception('Retry time exhausted')

        if options['attempt'] > self.__retries:
            # End reconnecting with built in error
            return None

        return min(int(options['attempt']) * 100, 3000)

    def retrieve(self, context: Optional[IContext], key: str) -> Any:
        """
        Retrieves cached value from the cache using its key.
        If value is missing in the cache or expired it returns `None`.

        :param context: (optional) transaction id to trace execution through call chain.
        :param key: a unique value key.
        :return: a retrieve cached value or `None` if nothing was found.
        """
        self.__check_opened(context)

        return self.__client.get(key)

    def store(self, context: Optional[IContext], key: str, value: Any, timeout: int) -> Any:
        """
        Stores value in the cache with expiration time.

        :param context: (optional) transaction id to trace execution through call chain.
        :param key: a unique value key.
        :param value: a value to store.
        :param timeout: expiration timeout in milliseconds.
        :return: the stored value.
        """
        self.__check_opened(context)

        return self.__client.set(name=key, value=value, px=timeout)

    def remove(self, context: Optional[IContext], key: str) -> Any:
        """
        Removes a value from the cache by its key.

        :param context: (optional) transaction id to trace execution through call chain.
        :param key: a unique value key.
        :return: the removed value.
        """
        self.__check_opened(context)

        return self.__client.delete(key)
