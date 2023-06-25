-- Create notification_pattern table
CREATE TABLE IF NOT EXISTS notification_pattern
(
    id           SERIAL PRIMARY KEY,
    type_        SMALLINT NOT NULL,
    pattern_file VARCHAR(100) NOT NULL,
    actual_time  INTEGER,
    settings_    JSON
);

COMMENT ON COLUMN notification_pattern.type_ IS 'by event / by time / manual';
COMMENT ON COLUMN notification_pattern.pattern_file IS 'A path to the pattern file';
COMMENT ON COLUMN notification_pattern.actual_time IS 'in seconds';

ALTER TABLE notification_pattern OWNER TO app;

-- Create types table
CREATE TABLE IF NOT EXISTS types
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR  NOT NULL
);

ALTER TABLE types OWNER TO app;

-- Create notification_event table
CREATE TABLE IF NOT EXISTS notification_event
(
    pattern    INTEGER NOT NULL
        CONSTRAINT notification_event_notification_pattern_null_fk
            REFERENCES notification_pattern,
    source     JSON,
    start_time TIME NOT NULL,
    end_time   TIME
);

COMMENT ON COLUMN notification_event.pattern IS 'Link to notification_pattern';
COMMENT ON COLUMN notification_event.source IS 'A reason to launch';

ALTER TABLE notification_event OWNER TO app;

-- Insert into types
INSERT INTO types (name) VALUES ('by event');
INSERT INTO types (name) VALUES ('by time');
INSERT INTO types (name) VALUES ('manual');

INSERT INTO notification_pattern (type_, pattern_file, actual_time, settings_)
VALUES (
  1, 
  'mail.html', 
  600, 
  '{
    "event_type": "review_like", 
    "subject": "Hello there, Something interesting happened!", 
    "title": "This is a letter", 
    "image": "https://cdn.pixabay.com/photo/2014/04/03/11/52/pop-corn-312386_640.png", 
    "text": "This is a beautiful text", 
    "cta_link":"http://localhost:5000/", 
    "cta_text": "Your ticket!", 
    "special_offer": "As we dicussed", 
    "recipient_name": "Dmitriy", 
    "unsubscribe_link": "http://localhost:5000/"
  }'
);

