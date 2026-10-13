import pymysql

# Patch MySQLdb with PyMySQL for seamless MySQL connection in Django
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()

# Compatibility patches for local MySQL / MariaDB instances
from django.db.backends.mysql.base import DatabaseWrapper  # noqa: E402
from django.db.backends.mysql.features import DatabaseFeatures  # noqa: E402

DatabaseWrapper.check_database_version_supported = lambda self: None
DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)
DatabaseFeatures.can_return_rows_from_bulk_insert = property(lambda self: False)
