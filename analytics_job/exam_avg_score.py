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
    Inserts or updates records in the exam_average_score table based on average scores.

    Args:
        average_scores_final (list): A list of tuples, each containing exam data including exam ID, scores, and average.

    Returns:
        None
    """
    for record in average_scores_final:
        exam_id_to_search = record[0]
        search_exam_id = f'SELECT exam_id FROM exam_average_score WHERE exam_id = {exam_id_to_search}'
        exam_id_data = pg.fetch_single_row_from_query(search_exam_id)
        if exam_id_data:
            update_sql_statement = f'\
                scores_all = {record[1]},\
                average_score = {record[2]},\
                last_update_at = NOW()\
            WHERE\
                exam_id = {exam_id_to_search}\
            '

            update_exam_average_score_query = pg.build_query(
            query_file_path = '/sql/analytics_query/exam_average_score_job/update_exam_average_score.sql',
            sql_statement_to_replace = 'INSERT_VALUES_TO_UPDATE',
            new_sql_statement = update_sql_statement
            )
            pg.execute_query(update_exam_average_score_query)
        else:
            insert_sql_statement = f"\
            (\
            {exam_id_to_search},\
            {record[1]},\
            {record[2]},\
            'NOW()'\
            )\
            "

            insert_exam_average_score_query = pg.build_query(
            query_file_path = '/sql/analytics_query/exam_average_score_job/insert_exam_average_score.sql',
            sql_statement_to_replace = 'INSERT_STUDENT_AVERAGE_SCORE',
            new_sql_statement = insert_sql_statement
            )
            pg.execute_query(insert_exam_average_score_query)


def build_payload_from_sample(data_from_query):
    """
    Builds a payload from sample data for insertion or update.

    Args:
        data_from_query (list of tuples): A list of tuples containing data from a database query.

    Returns:
        None
    """
    exam_scores = defaultdict(list)

    for _, exam_id, score in data_from_query:
        exam_scores[exam_id].append(score)
    average_scores_final = [(exam_id, f'ARRAY{exam_scores[exam_id]}', mean(scores), 'NOW()') for exam_id, scores in exam_scores.items()]

    insert_or_update(average_scores_final)


def execute_analytics_job():
    """
    Executes an analytics job to calculate and update average scores for exams.

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