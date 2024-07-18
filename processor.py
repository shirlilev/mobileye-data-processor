import json
import os
from datetime import datetime
from db import get_db_connection

def process_file(file_path):
    try:
        file_name = os.path.basename(file_path)
        with open(file_path, 'r') as file:
            data = json.load(file)
            if file_name.startswith("objects_detection_"):
                process_objects_detection(data['objects_detection_events'])
            elif file_name.startswith("vehicles_status_"):
                process_vehicle_status(data['vehicle_status'])
            else:
                print(f"Unknown file type: {file_name}")
                return  # Don't delete unknown file types
        os.remove(file_path)  # Remove the processed file
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# {
#     "vehicle_id": "ebab5f787798416fb2b8afc1340d7a4e",
#     "detection_time": "2022-06-05T21:05:20.590Z",
#     "detections": [
#         {"object_type": "cars",
#         "object_value": 4},
#     ]
# }
def process_objects_detection(events):
    conn = get_db_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        for event in events:
            vehicle_id = event['vehicle_id']
            detection_time = datetime.strptime(event['detection_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            for detection in event['detections']:
                object_type = detection['object_type']
                object_value = detection['object_value']
                cur.execute("""
                    INSERT INTO objects_detection_events (vehicle_id, detection_time, object_type, object_value)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (vehicle_id, detection_time, object_type) DO NOTHING;
                """, (vehicle_id, detection_time, object_type, object_value))
        conn.commit()
    except Exception as e:
        print(f"Error inserting objects detection events: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# {
#     "vehicle_id": "ebab5f787798416fb2b8afc1340d7a4e", 
#     "report_time": "2022-05-05T22:02:34.546Z",
#     "status": "driving",
# }
def process_vehicle_status(statuses):
    conn = get_db_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        for status in statuses:
            vehicle_id = status['vehicle_id']
            report_time = datetime.strptime(status['report_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            vehicle_status = status['status']
            cur.execute("""
                INSERT INTO vehicle_status (vehicle_id, report_time, status)
                VALUES (%s, %s, %s)
                ON CONFLICT (vehicle_id) DO UPDATE SET report_time = EXCLUDED.report_time, status = EXCLUDED.status;
            """, (vehicle_id, report_time, vehicle_status))
        conn.commit()
    except Exception as e:
        print(f"Error inserting vehicle status: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
