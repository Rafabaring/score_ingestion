SELECT
    student_id,
    exam_id,
    score
FROM
    events
ORDER BY
    inserted_at DESC
LIMIT
    INSERT_LIMIT