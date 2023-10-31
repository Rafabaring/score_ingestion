import unittest
from schema_handler import student_handler
from unittest.mock import Mock, call


class TestStudentHandler(unittest.TestCase):
    def setUp(self):
        self.mock_pg = Mock()
        self.mock_pg.build_query.return_value = 'mocked_query'
        self.mock_pg.fetch_single_row_from_query.return_value = (1, )

    def test_insert_student_identification(self):
        student_idenfication = "Karli35"
        result = student_handler.insert_student_identification(student_idenfication, self.mock_pg)

        expected_calls = [
            call(
                query_file_path='sql/student/insert_student_identification.sql',
                sql_statement_to_replace='INSERT_STUDENT_IDENTIFICATION',
                new_sql_statement=f"'{student_idenfication}'"
            ),
            call(
                query_file_path='sql/student/fetch_student_identification.sql',
                sql_statement_to_replace='INSERT_STUDENT_IDENTIFICATION',
                new_sql_statement=f"'{student_idenfication}'"
            )
        ]
        self.mock_pg.build_query.assert_has_calls(expected_calls)
        self.mock_pg.execute_query.assert_called_once_with('mocked_query')
        self.assertEqual(result, 1)


    def test_search_student_identification(self):
        student_idenfication = "Karli35"
        result = student_handler.search_student_identification(student_idenfication, self.mock_pg)

        self.mock_pg.build_query.assert_called_once_with(
            query_file_path='sql/student/fetch_student_identification.sql',
            sql_statement_to_replace='INSERT_STUDENT_IDENTIFICATION',
            new_sql_statement=f"'{student_idenfication}'"
        )

        self.mock_pg.fetch_single_row_from_query.assert_called_once_with('mocked_query')
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()