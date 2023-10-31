-- FEED EVENT TABLES

CREATE TABLE IF NOT EXISTS events (
    id SERIAL,
    event_type INT NOT NULL,
    student_id VARCHAR(255) NOT NULL,
    exam_id INT NOT NULL,
    score FLOAT (13) NOT NULL,
    inserted_at TIMESTAMP,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS students (
    id SERIAL,
    student_identification VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS exams (
    id SERIAL,
    exam_identification INT NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS event_type (
    id SERIAL,
    event_type_identification CHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

-- DATA QUALITY CHECK TABLES
CREATE TABLE IF NOT EXISTS data_quality_check_results (
    id SERIAL,
    message_payload JSON,
    results JSON,
    last_update_at TIMESTAMP,
    PRIMARY KEY (id)
);

-- ANALYTICS TABLES
CREATE TABLE IF NOT EXISTS student_average_score (
    id SERIAL,
    student_id INT NOT NULL,
    scores_all FLOAT ARRAY NOT NULL,
    average_score FLOAT (13) NOT NULL,
    last_update_at TIMESTAMP,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS exam_average_score (
    id SERIAL,
    exam_id INT NOT NULL,
    scores_all FLOAT ARRAY NOT NULL,
    average_score FLOAT (13) NOT NULL,
    last_update_at TIMESTAMP,
    PRIMARY KEY (id)
);