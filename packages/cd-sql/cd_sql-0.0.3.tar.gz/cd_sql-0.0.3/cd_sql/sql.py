from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

class SQL:
    def __init__(self, connection_string):
        """
        Initialize the SQL class with a connection string.

        :param connection_string: The connection string for the database.
        """
        self.connection_string = connection_string
        self.engine = None
        self.connection = None

    def connect(self):
        """
        Establish a connection to the database using SQLAlchemy.

        This method creates an engine and connects to the database.
        """
        try:
            self.engine = create_engine(self.connection_string)
            self.connection = self.engine.connect()
        except SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            raise

    def disconnect(self):
        """
        Disconnect from the database.

        This method closes the connection to the database.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
        if self.engine:
            self.engine.dispose()

    def execute_query(self, query):
        """
        Execute a given SQL query using SQLAlchemy.

        :param query: The SQL query to be executed.
        :return: The result of the query execution.
        """
        try:
            return self.connection.execute(query)
        except SQLAlchemyError as e:
            print(f"Error executing query: {e}")
            raise

    def fetch_all(self, query):
        """
        Fetch all results from a given SQL query using SQLAlchemy.

        :param query: The SQL query for which the results are to be fetched.
        :return: A list of all rows fetched from the query.
        """
        try:
            return self.connection.execute(query).fetchall()
        except SQLAlchemyError as e:
            print(f"Error fetching data: {e}")
            raise

    def fetch_one(self, query):
        """
        Fetch a single result from a given SQL query using SQLAlchemy.

        :param query: The SQL query for which the result is to be fetched.
        :return: A single row or None if no row is found.
        """
        try:
            return self.connection.execute(query).fetchone()
        except SQLAlchemyError as e:
            print(f"Error fetching data: {e}")
            raise
