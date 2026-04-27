CREATE TABLE SysLogs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action VARCHAR(255),
    performed_by VARCHAR(50)
);


-- # stale code , used for initial dataset generation