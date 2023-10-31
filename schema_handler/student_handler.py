from db_utils.postgres_db import PostgresDB
from utils.hash import create_student_entity_id

pg = PostgresDB()

def insert_student_identification(student_idenfication, pg):
    """
    Inserts a student identification into the database.

    Args:
        student_idenfication (str): The student identification to insert.
        pg (PostgresDB): An instance of the PostgresDB class used for database operations.

    Returns:
        int: The ID of the inserted student identification.
    """
    insert_student_query = pg.build_query(
        query_file_path = 'sql/student/insert_student_identification.sql',
        sql_statement_to_replace = 'INSERT_STUDENT_IDENTIFICATION',
        new_sql_statement = f"'{student_idenfication}'"
    )
    pg.execute_query(insert_student_query)
    
    student_id = search_student_identification(student_idenfication, pg)
    return student_id


def search_student_identification(student_idenfication, pg):
    """
    Searches for a student identification in the database.

    Args:
        student_idenfication (str): The student identification to search for.
        pg (PostgresDB): An instance of the PostgresDB class used for database operations.

    Returns:
        int or None: The ID of the student identification if found, None if not found.
    """
    fetch_student_query = pg.build_query(
        query_file_path = 'sql/student/fetch_student_identification.sql',
        sql_statement_to_replace = 'INSERT_STUDENT_IDENTIFICATION',
        new_sql_statement = f"'{student_idenfication}'"
    )
    data_from_query = pg.fetch_single_row_from_query(fetch_student_query)
    if not data_from_query:
        return
    else:
        student_id = data_from_query[0]
        return student_id


def execute_student_handler(msg_payload,):
    """
    Executes the student handler by searching for or inserting a student identification.

    Args:
        msg_payload (dict): A dictionary containing message payload data, including 'studentId'.
        pg (PostgresDB): An instance of the PostgresDB class used for database operations.

    Returns:
        int: The ID of the student identification.
    """
    student_id = search_student_identification(msg_payload['studentId'], pg)
    if student_id:
        hashed_student_id = create_student_entity_id(student_id)
        return hashed_student_id
    else:
        hashed_student_id = create_student_entity_id(msg_payload['studentId'])
        student_id = insert_student_identification(hashed_student_id, pg)
        return hashed_student_id