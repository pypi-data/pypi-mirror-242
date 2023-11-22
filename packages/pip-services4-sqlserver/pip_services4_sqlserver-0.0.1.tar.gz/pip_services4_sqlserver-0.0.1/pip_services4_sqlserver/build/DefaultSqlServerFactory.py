# -*- coding: utf-8 -*-

from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from pip_services4_sqlserver.connect.SqlServerConnection import SqlServerConnection


class DefaultSqlServerFactory(Factory):
    """
    Creates SqlServer components by their descriptors.

    See: :class:`SqlServerConnection <pip_services4_sqlserver.persistence.SqlServerConnection.SqlServerConnection>`,
    :class:`Factory <pip_services4_components.build.Factory.Factory>`
    """

    SqlServerConnectionDescriptor = Descriptor("pip-services", "connection", "sqlserver", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultSqlServerFactory, self).__init__()
        self.register_as_type(
            DefaultSqlServerFactory.SqlServerConnectionDescriptor, SqlServerConnection)
