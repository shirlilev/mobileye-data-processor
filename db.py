import psycopg2
from config import DB_CONFIG

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_tables():
    conn = get_db_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        # Create schema if it does not exist
        create_schema = """
        CREATE SCHEMA IF NOT EXISTS mobileye_data;
        """
        cur.execute(create_schema)

        create_objects_detection_events_table = """
        CREATE TABLE IF NOT EXISTS mobileye_data.objects_detection_events (
            vehicle_id VARCHAR(255),
            detection_time TIMESTAMP,
            object_type VARCHAR(50),
            object_value INT,
            PRIMARY KEY (vehicle_id, detection_time, object_type)
        );
        """
        create_vehicle_status_table = """
        CREATE TABLE IF NOT EXISTS mobileye_data.vehicle_status (
            vehicle_id VARCHAR(255) PRIMARY KEY,
            report_time TIMESTAMP,
            status VARCHAR(50)
        );
        """
        cur.execute(create_objects_detection_events_table)
        cur.execute(create_vehicle_status_table)

        # Create indexes for common queries
        create_indexes = """
        CREATE INDEX IF NOT EXISTS idx_objects_detection_detection_time ON mobileye_data.objects_detection_events(detection_time); 
        CREATE INDEX IF NOT EXISTS idx_vehicles_status_report_time ON mobileye_data.vehicle_status(report_time); 
        CREATE INDEX IF NOT EXISTS idx_vehicles_status_status ON mobileye_data.vehicle_status(status);
        """
        cur.execute(create_indexes)

        conn.commit()
    except Exception as e:
        print(f"Error creating tables or indexes: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
