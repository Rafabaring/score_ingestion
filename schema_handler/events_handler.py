from db_utils.postgres_db import PostgresDB

pg = PostgresDB()

def insert_payload_into_event_table(msg_payload):
    """
    Inserts a message payload into the event table in the database.

    Args:
        msg_payload (dict): A dictionary containing message payload data including 'eventType',
            'studentId', 'exam', and 'score'.
        pg (PostgresDB): An instance of the PostgresDB class used for database operations.

    Returns:
        None
    """
    sql_file = open('sql/events/insert_events.sql', 'r')
    query = sql_file.read()
    sql_file.close()
    insert_query = query.\
        replace('INSERT_EVENT_TYPE', f"'{msg_payload['eventType']}'").\
        replace('INSERT_STUDENT_ID', f"'{msg_payload['studentId']}'").\
        replace('INSERT_EXAM', f"{int(msg_payload['exam'])}").\
        replace('INSERT_SCORE', f"{float(msg_payload['score'])}")

    pg.execute_query(insert_query)