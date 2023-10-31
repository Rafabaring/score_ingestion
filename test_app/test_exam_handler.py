import unittest
from schema_handler import exam_handler
from unittest.mock import Mock, call


class TestExamHandler(unittest.TestCase):
    def setUp(self):
        self.mock_pg = Mock()
        self.mock_pg.build_query.return_value = 'mocked_query'
        self.mock_pg.fetch_single_row_from_query.return_value = (1, )

    def test_insert_exam_identification(self):
        exam_idenfication = 3
        result = exam_handler.insert_exam_identification(exam_idenfication, self.mock_pg)

        expected_calls = [
            call(
                query_file_path='sql/exam/insert_exam_identification.sql',
                sql_statement_to_replace='INSERT_EXAM_IDENTIFICATION',
                new_sql_statement=f"'{exam_idenfication}'"
            ),
            call(
                query_file_path='sql/exam/fetch_exam_identification.sql',
                sql_statement_to_replace='INSERT_EXAM_IDENTIFICATION',
                new_sql_statement=f"'{exam_idenfication}'"
            )
        ]
        self.mock_pg.build_query.assert_has_calls(expected_calls)
        self.mock_pg.execute_query.assert_called_once_with('mocked_query')
        self.assertEqual(result, 1)


    def test_search_exam_identification(self):
        exam_idenfication = 2
        result = exam_handler.search_exam_identification(exam_idenfication, self.mock_pg)

        self.mock_pg.build_query.assert_called_once_with(
            query_file_path='sql/exam/fetch_exam_identification.sql',
            sql_statement_to_replace='INSERT_EXAM_IDENTIFICATION',
            new_sql_statement=f"'{exam_idenfication}'"
        )

        self.mock_pg.fetch_single_row_from_query.assert_called_once_with('mocked_query')
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()