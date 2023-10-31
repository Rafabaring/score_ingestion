import json
from sseclient import SSEClient
from data_quality_check import data_quality_check
from schema_handler import events_handler, student_handler, exam_handler, event_type_handler


messages = SSEClient('https://live-test-scores.herokuapp.com/scores')

for msg in messages:
    if msg.data:
        msg_payload = json.loads(msg.data)
        msg_payload['eventType'] = msg.event
        
        # Pre-check
        check_pass = data_quality_check.execute_data_quality_check(msg_payload)
        if check_pass:

            # Data normalization
            student_id = student_handler.execute_student_handler(msg_payload)
            msg_payload['studentId'] = student_id

            exam_id = exam_handler.execute_exam_handler(msg_payload)
            msg_payload['exam'] = exam_id

            event_type_id = event_type_handler.execute_event_type_handler(msg_payload)
            msg_payload['eventType'] = event_type_id

            events_handler.insert_payload_into_event_table(msg_payload)