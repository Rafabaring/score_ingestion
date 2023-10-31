from db_utils.postgres_db import PostgresDB

pg = PostgresDB()

def insert_exam_identification(exam_idenfication, pg):
    """
    Inserts an exam identification into the database.

    Args:
        exam_idenfication (str): The exam identification to insert.
        pg (PostgresDB): An instance of the PostgresDB class used for database operations.

    Returns:
        int: The ID of the inserted exam identification.
    """
    insert_exam_query = pg.build_query(
        query_file_path = 'sql/exam/insert_exam_identification.sql',
        sql_statement_to_replace = 'INSERT_EXAM_IDENTIFICATION',
        new_sql_statement = f"'{exam_idenfication}'"
    )
    pg.execute_query(insert_exam_query)

    exam_id = search_exam_identification(exam_idenfication, pg)
    return exam_id


def search_exam_identification(exam_idenfication, pg):
    """
    Searches for an exam identification in the database.

    Args:
        exam_idenfication (str): The exam identification to search for.
        pg (PostgresDB): An instance of the PostgresDB class used for database operations.

    Returns:
        int or None: The ID of the exam identification if found, None if not found.
    """
    fetch_exam_query = pg.build_query(
        query_file_path = 'sql/exam/fetch_exam_identification.sql',
        sql_statement_to_replace = 'INSERT_EXAM_IDENTIFICATION',
        new_sql_statement = f"'{exam_idenfication}'"
    )
    data_from_query = pg.fetch_single_row_from_query(fetch_exam_query)
    if not data_from_query:
        return
    else:
        exam_id = data_from_query[0]
        return exam_id


def execute_exam_handler(msg_payload):
    """
    Executes the exam handler by searching for or inserting an exam identification.

    Args:
        msg_payload (dict): A dictionary containing message payload data, including 'exam'.
        pg (PostgresDB): An instance of the PostgresDB class used for database operations.

    Returns:
        int: The ID of the exam identification.
    """
    exam_id = search_exam_identification(msg_payload['exam'], pg)
    if exam_id:
        return exam_id
    else:
        exam_id = insert_exam_identification(msg_payload['exam'], pg)
        return exam_id