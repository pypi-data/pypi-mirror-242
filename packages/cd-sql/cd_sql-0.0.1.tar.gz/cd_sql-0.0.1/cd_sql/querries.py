class CommonQueries:
    def __init__(self, db_instance):
        """
        Initialize the CommonQueries class with a database instance.

        :param db_instance: An instance of a database class.
        """
        self.db = db_instance

    def select_all(self, table_name):
        """
        Select all records from a specified table.

        :param table_name: Name of the table to select from.
        :return: All records from the table.
        """
        query = f"SELECT * FROM {table_name}"
        return self.db.fetch_all(query)

    def select_where(self, table_name, conditions):
        """
        Select records from a table with specific conditions.

        :param table_name: Name of the table to select from.
        :param conditions: Conditions for the selection query.
        :return: Records matching the conditions.
        """
        query = f"SELECT * FROM {table_name} WHERE {' AND '.join(conditions)}"
        return self.db.fetch_all(query)

    def insert(self, table_name, columns, values):
        """
        Insert a record into a specified table.

        :param table_name: Name of the table to insert into.
        :param columns: List of column names.
        :param values: Corresponding values for the columns.
        """
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        self.db.execute_query(query, values)

    def update(self, table_name, set_columns, set_values, where_column, where_value):
        """
        Update a record in a specified table.

        :param table_name: Name of the table to update.
        :param set_columns: Columns to be updated.
        :param set_values: New values for the specified columns.
        :param where_column: Column to match for the update.
        :param where_value: Value to match for the update.
        """
        set_clause = ', '.join([f"{col} = ?" for col in set_columns])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_column} = ?"
        self.db.execute_query(query, set_values + [where_value])

    def delete(self, table_name, where_column, where_value):
        """
        Delete a record from a specified table.

        :param table_name: Name of the table to delete from.
        :param where_column: Column to match for the deletion.
        :param where_value: Value to match for the deletion.
        """
        query = f"DELETE FROM {table_name} WHERE {where_column} = ?"
        self.db.execute_query(query, [where_value])

    def count_rows(self, table_name):
        """
        Count the number of rows in a specified table.

        :param table_name: Name of the table to count rows in.
        :return: Number of rows in the table.
        """
        query = f"SELECT COUNT(*) FROM {table_name}"
        return self.db.fetch_one(query)[0]

    def create_table_if_not_exists(self, table_name, columns_with_datatypes):
        """
        Create a table if it does not already exist.

        :param table_name: Name of the table to be created.
        :param columns_with_datatypes: List of columns with their data types.
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_with_datatypes)})"
        self.db.execute_query(query)

    def create_table(self, table_name, columns_with_datatypes):
        """
        Create a table.

        :param table_name: Name of the table to be created.
        :param columns_with_datatypes: List of columns with their data types.
        """
        query = f"CREATE TABLE {table_name} ({', '.join(columns_with_datatypes)})"
        self.db.execute_query(query)

    def delete_table(self, table_name):
        """
        Delete a table.

        :param table_name: Name of the table to be deleted.
        """
        query = f"DROP TABLE {table_name}"
        self.db.execute_query(query)

    def truncate_table(self, table_name):
        """
        Truncate a table (remove all records).

        :param table_name: Name of the table to be truncated.
        """
        query = f"TRUNCATE TABLE {table_name}"
        self.db.execute_query(query)

    def custom_query(self, query, values=[]):
        """
        Execute a custom SQL query.

        :param query: The SQL query to execute.
        :param values: Optional values for parameterized queries.
        :return: The result of the query execution.
        """
        return self.db.execute_query(query, values)
