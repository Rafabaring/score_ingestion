from db_utils.postgres_db import PostgresDB

pg = PostgresDB()

def insert_event_type_identification(event_type_idenfication, pg):
    """
    Inserts an event type identification into the database.

    Args:
        event_type_idenfication (str): The event type identification to insert.
        pg (PostgresDB): An instance of the PostgresDB class used for database operations.

    Returns:
        int: The ID of the inserted event type identification.
    """
    insert_event_type_query = pg.build_query(
        query_file_path = 'sql/event_type/insert_event_type_identification.sql',
        sql_statement_to_replace = 'INSERT_EVENT_TYPE_IDENTIFICATION',
        new_sql_statement = f"'{event_type_idenfication}'"
    )
    pg.execute_query(insert_event_type_query)

    event_type_id = search_event_type_identification(event_type_idenfication, pg)
    return event_type_id


def search_event_type_identification(event_type_idenfication, pg):
    """
    Searches for an event type identification in the database.

    Args:
        event_type_idenfication (str): The event type identification to search for.
        pg (PostgresDB): An instance of the PostgresDB class used for database operations.

    Returns:
        int or None: The ID of the event type identification if found, None if not found.
    """
    fetch_event_type_query = pg.build_query(
        query_file_path = 'sql/event_type/fetch_event_type_identification.sql',
        sql_statement_to_replace = 'INSERT_EVENT_TYPE_IDENTIFICATION',
        new_sql_statement = f"'{event_type_idenfication}'"
    )
    data_from_query = pg.fetch_single_row_from_query(fetch_event_type_query)
    if not data_from_query:
        return
    else:
        event_type_id = data_from_query[0]
        return event_type_id
    

def execute_event_type_handler(msg_payload):
    """
    Executes the event type handler by searching for or inserting an event type identification.

    Args:
        msg_payload (dict): A dictionary containing message payload data, including 'eventType'.
        pg (PostgresDB): An instance of the PostgresDB class used for database operations.

    Returns:
        int: The ID of the event type identification.
    """
    event_type_id = search_event_type_identification(msg_payload['eventType'], pg)
    if event_type_id:
        return event_type_id
    else:
        event_type_id = insert_event_type_identification(msg_payload['eventType'], pg)
        return event_type_id