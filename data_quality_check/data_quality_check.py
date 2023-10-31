import json
from db_utils.postgres_db import PostgresDB

pg = PostgresDB()

def check_data_types(payload):
    """
    Check if the payload contains data with the expected data types.

    Args:
        payload (dict): The data payload to be checked.

    Returns:
        bool: True if all data types match the expected types, False otherwise.
    """
    expected_types = {
        'studentId': str,
        'exam': int,
        'score': float,
        'eventType': str,
    }
    
    for field, data_type in expected_types.items():
        if not isinstance(payload.get(field), data_type):
            return False
    return True


def check_null(payload):
    """
    Check if any values in the payload are null (empty or None).

    Args:
        payload (dict): The data payload to be checked.

    Returns:
        bool: True if all values in the payload are non-null, False otherwise.
    """
    for value in payload.values():
        if not value:
            return False
    return True


def check_empty_string(payload):
    """
    Check if the 'studentId' field in the payload is an empty string.

    Args:
        payload (dict): The data payload to be checked.

    Returns:
        bool: True if the 'studentId' field is not an empty string, False otherwise.
    """
    if payload['studentId'] and len(payload['studentId']) == 0:
        return False
    else:
        return True


def check_data_ranges(payload):
    """
    Check if the values in the payload are within acceptable ranges.

    Args:
        payload (dict): The data payload to be checked.

    Returns:
        bool: True if data values are within acceptable ranges, False otherwise.
    """
    if not (0 <= payload['score'] <= 1):
        return False
    if not (payload['exam'] > 0):
        return False
    return True


def check_mandatory_fields(payload):
    """
    Check if all mandatory fields are present in the payload.

    Args:
        payload (dict): The data payload to be checked.

    Returns:
        bool: True if all mandatory fields are present, False otherwise.
    """
    mandatory_fields = ['studentId', 'exam', 'score', 'eventType']
    
    for field in mandatory_fields:
        if field not in payload:
            return False
    return True


def check_event_type(payload):
    """
    Check if the eventType is one of the valid event types.

    Args:
        payload (dict): The data payload to be checked.

    Returns:
        bool: True if eventType is valid, False otherwise.
    """
    valid_event_types = ['score', 'attendance', 'assignment']
    event_type = payload.get('eventType')
    if event_type not in valid_event_types:
        return False
    return True


def check_score_format(payload):
    """
    Check if the score has a valid format with a minimun of 2 decimal places.

    Args:
        payload (dict): The data payload to be checked.

    Returns:
        bool: True if the score format is valid, False otherwise.
    """
    score = payload.get('score')
    if score is not None:
        decimal_places = len(str(score).split('.')[-1])
        if decimal_places < 2:
            return False
    return True


def insert_data_quality_check_results(msg_payload, data_quality_check_results, pg):
    """
    Insert data quality check results and associated message payload into a database.

    This function formats the data quality check results and the original message payload
    and inserts them into a database using the provided PostgreSQL instance.

    Args:
        msg_payload (dict): The original message payload containing data to be checked.
        data_quality_check_results (dict): A dictionary containing the results of data quality checks.
        pg (PostgreSQL): An instance of a PostgreSQL database connection.

    Returns:
        None
    """
    data_quality_check_sql_statement = f"\
    (\
    '{json.dumps(msg_payload)}',\
    '{json.dumps(data_quality_check_results)}',\
    'NOW()'\
    )\
    "
    insert_data_quality_check_query = pg.build_query(
        query_file_path = 'sql/data_quality_check/insert_data_quality_check_results.sql',
        sql_statement_to_replace = 'INSERT_DATA_QUALITY_CHECK_RESULTS',
        new_sql_statement = f"{data_quality_check_sql_statement}"
    )
    pg.execute_query(insert_data_quality_check_query)


def execute_data_quality_check(msg_payload):
    """
    Execute a series of data quality checks on a given message payload and insert results into a database if any check fails.

    This function runs a set of data quality checks on the provided message payload.
    If any of the checks fail, the results are inserted into a database along with the original payload.

    Args:
        msg_payload (dict): The message payload containing data to be checked.

    Returns:
        bool: True if all data quality checks pass, False if any check fails.
    """
    data_quality_check_results = {
        'data_types_check': check_data_types(msg_payload),
        'null_check': check_null(msg_payload),
        'empty_string_check': check_empty_string(msg_payload),
        'data_ranges_check': check_data_ranges(msg_payload),
        'mandatory_fields_check': check_mandatory_fields(msg_payload),
        'event_type_check': check_event_type(msg_payload),
        'score_format_check': check_score_format(msg_payload),   
    }
    if False in data_quality_check_results.values():
        insert_data_quality_check_results(msg_payload, data_quality_check_results, pg)
        return False
    return True