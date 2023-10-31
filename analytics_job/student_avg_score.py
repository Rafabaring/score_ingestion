from collections import defaultdict
from statistics import mean
import sys
import os
path = os.path.dirname(os.path.dirname(__file__)) 
sys.path.append(path)

from db_utils.postgres_db import PostgresDB
pg = PostgresDB()

def insert_or_update(average_scores_final):
    """
    Inserts or updates records in the student_average_score table based on average scores.

    Args:
        average_scores_final (list): A list of tuples, each containing student data including student ID, scores, and average.

    Returns:
        None
    """
    for record in average_scores_final:
        student_id_to_search = record[0]
        search_student_id = f'SELECT student_id FROM student_average_score WHERE student_id = {student_id_to_search}'
        student_id_data = pg.fetch_single_row_from_query(search_student_id)
        if student_id_data:
            update_sql_statement = f'\
                scores_all = {record[1]},\
                average_score = {record[2]},\
                last_update_at = NOW()\
            WHERE\
                student_id = {student_id_to_search}\
            '

            update_student_average_score_query = pg.build_query(
            query_file_path = '/sql/analytics_query/student_average_score_job/update_student_average_score.sql',
            sql_statement_to_replace = 'INSERT_VALUES_TO_UPDATE',
            new_sql_statement = update_sql_statement
            )
            pg.execute_query(update_student_average_score_query)
        else:
            insert_sql_statement = f"\
            (\
            {student_id_to_search},\
            {record[1]},\
            {record[2]},\
            'NOW()'\
            )\
            "

            insert_student_average_score_query = pg.build_query(
            query_file_path = '/sql/analytics_query/student_average_score_job/insert_student_average_score.sql',
            sql_statement_to_replace = 'INSERT_STUDENT_AVERAGE_SCORE',
            new_sql_statement = insert_sql_statement
            )
            pg.execute_query(insert_student_average_score_query)


def build_payload_from_sample(data_from_query):
    """
    Builds a payload from sample data for insertion or update.

    Args:
        data_from_query (list of tuples): A list of tuples containing data from a database query.

    Returns:
        None
    """
    student_scores = defaultdict(list)

    for student_id, _, score in data_from_query:
        student_scores[student_id].append(score)
    average_scores_final = [(student_id, f'ARRAY{student_scores[student_id]}', mean(scores), 'NOW()') for student_id, scores in student_scores.items()]

    insert_or_update(average_scores_final)


def execute_analytics_job():
    """
    Executes an analytics job to calculate and update average scores for students.

    Returns:
        None
    """
    fetch_all_data_query = pg.build_query(
        query_file_path = '/sql/analytics_query/fetch_student_exam_score.sql',
        sql_statement_to_replace = 'LIMIT\n    INSERT_LIMIT',
        new_sql_statement = ''
    )
    data_from_query = pg.fetch_from_query(fetch_all_data_query)
    build_payload_from_sample(data_from_query)


if __name__ == '__main__':
    execute_analytics_job()
