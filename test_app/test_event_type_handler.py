import unittest
from schema_handler import event_type_handler
from unittest.mock import Mock, call


class TestEventTypeHandler(unittest.TestCase):
    def setUp(self):
        self.mock_pg = Mock()
        self.mock_pg.build_query.return_value = 'mocked_query'
        self.mock_pg.fetch_single_row_from_query.return_value = (1, )

    def test_insert_event_type_identification(self):
        event_type_idenfication = 'score'
        result = event_type_handler.insert_event_type_identification(event_type_idenfication, self.mock_pg)

        expected_calls = [
            call(
                query_file_path='sql/event_type/insert_event_type_identification.sql',
                sql_statement_to_replace='INSERT_EVENT_TYPE_IDENTIFICATION',
                new_sql_statement=f"'{event_type_idenfication}'"
            ),
            call(
                query_file_path='sql/event_type/fetch_event_type_identification.sql',
                sql_statement_to_replace='INSERT_EVENT_TYPE_IDENTIFICATION',
                new_sql_statement=f"'{event_type_idenfication}'"
            )
        ]
        self.mock_pg.build_query.assert_has_calls(expected_calls)
        self.mock_pg.execute_query.assert_called_once_with('mocked_query')
        self.assertEqual(result, 1)


    def test_search_event_type_identification(self):
        event_type_idenfication = 'score'
        result = event_type_handler.search_event_type_identification(event_type_idenfication, self.mock_pg)

        self.mock_pg.build_query.assert_called_once_with(
            query_file_path='sql/event_type/fetch_event_type_identification.sql',
            sql_statement_to_replace='INSERT_EVENT_TYPE_IDENTIFICATION',
            new_sql_statement=f"'{event_type_idenfication}'"
        )

        self.mock_pg.fetch_single_row_from_query.assert_called_once_with('mocked_query')
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()