USE Civic_Resolve;

CREATE TABLE Complaints (
    ticket_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    created_at DATETIME,
    description TEXT,
    location VARCHAR(100),
    wing VARCHAR(50),
    priority VARCHAR(20),
    status VARCHAR(20),
    true_wing VARCHAR(50),
    scheduled_timestamp DATETIME NULL,
    calibration_timestamp DATETIME NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

LOAD DATA LOCAL INFILE '[COMPLETE-PATH]'
INTO TABLE Complaints
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(ticket_id, user_id, @timestamp_var, description, location, wing, priority, status, true_wing, @scheduled_var, @calibration_var)
SET 
    created_at = STR_TO_DATE(@timestamp_var, '%Y-%m-%d %H:%i:%s'),
    scheduled_timestamp = NULLIF(@scheduled_var, ''),
    calibration_timestamp = NULLIF(@calibration_var, '');

-- # stale code , used for initial dataset generation