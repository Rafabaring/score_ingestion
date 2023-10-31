INSERT INTO public.events (
    event_type, 
    student_id, 
    exam_id, 
    score,
    inserted_at
)
VALUES (
    INSERT_EVENT_TYPE,
    INSERT_STUDENT_ID,
    INSERT_EXAM,
    INSERT_SCORE,
    NOW()
);