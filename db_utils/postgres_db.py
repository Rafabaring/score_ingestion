import psycopg2
import json
import os
import sys

class PostgresDB():
    def __init__(self):

        script_directory = os.path.dirname(os.path.abspath(__file__))
        db_config_path = os.path.join(script_directory, 'db_config.json')

        with open(db_config_path, 'r') as db_config:
            db_params = json.load(db_config)['db_params']
        self.connection = psycopg2.connect(**db_params)
        self.cursor = self.connection.cursor()
        
    def build_query(self, query_file_path, sql_statement_to_replace, new_sql_statement):
        """
        Builds a SQL query by replacing placeholders in a SQL file with new values.

        Args:
            query_file_path (str): The path to the SQL file.
            sql_statement_to_replace (str): The placeholder to replace in the SQL file.
            new_sql_statement (str): The new SQL statement to replace the placeholder.

        Returns:
            str: The constructed SQL query.
        """
        sql_file = open(query_file_path, 'r')
        query = sql_file.read()
        sql_file.close()
        query_statement = query.\
            replace(sql_statement_to_replace, new_sql_statement)
        return query_statement

    def execute_query(self, query):
        """
        Executes a SQL query on the database.

        Args:
            query (str): The SQL query to execute.

        Returns:
            None
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            self.cursor.close()
            self.connection.close()


    def fetch_single_row_from_query(self, query):
        """
        Executes a SQL query and fetches a single row of data from the result.

        Args:
            query (str): The SQL query to execute.

        Returns:
            tuple or None: A tuple containing data from the query result, or None if no data is found.
        """
        try:
            self.cursor.execute(query)
            data_from_query = self.cursor.fetchone()
        except Exception as e:
            self.connection.rollback()
            self.cursor.close()
            self.connection.close()
        return data_from_query
        
    

    def fetch_from_query(self, query):
        """
        Executes a SQL query and fetches all rows of data from the result.

        Args:
            query (str): The SQL query to execute.

        Returns:
            list of tuples: A list of tuples, each containing data from a row in the query result.
        """
        try:
            self.cursor.execute(query)
            data_from_query = self.cursor.fetchall()
        except Exception as e:
            self.connection.rollback()
            self.cursor.close()
            self.connection.close()
        return data_from_query
        