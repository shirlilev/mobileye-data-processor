CREATE SCHEMA IF NOT EXISTS mobileye_data;

CREATE TABLE mobileye_data.objects_detection (
    vehicle_id VARCHAR(255),
    detection_time TIMESTAMP,
    object_type VARCHAR(50),
    object_value INT,
    PRIMARY KEY (vehicle_id, detection_time, object_type)
);

CREATE TABLE mobileye_data.vehicle_status (
    vehicle_id VARCHAR(255) PRIMARY KEY,
    report_time TIMESTAMP,
    status VARCHAR(50)
);

-- Create indexes for common queries 
CREATE INDEX idx_objects_detection_detection_time ON mobileye_data.objects_detection(detection_time); 
CREATE INDEX idx_vehicles_status_report_time ON mobileye_data.vehicles_status(report_time); 
CREATE INDEX idx_vehicles_status_status ON mobileye_data.vehicles_status(status);

