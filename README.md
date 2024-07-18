# Mobileye Data Processing System
This system processes JSON files containing object detection events and vehicle status updates, storing the data in a PostgreSQL database.

## Prerequisites
- Python 3.7+
- PostgreSQL 12+
- pip (Python package manager)

## Installation
1. Clone this repository:
git clone https://github.com/shirlilev/mobileye-data-processor.git
cd mobileye-data-processor
2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate
3. Install the required packages:
pip install -r requirements.txt
4. Set up the PostgreSQL database: Create a new database named `mobileye_data`
5. Update the `config.py` file with your database credentials and the folder to watch for new files.

## Usage
1. Run the script:
python main.py
2. The script will now watch for new files in the specified directory and process them automatically.
3. To stop the script, press Ctrl+C.

## Design Considerations
- Code reuse: The Handler, Watcher, and process_file functions are designed to be reusable and easily extensible.
- Flexibility for changes: The modular design allows for easy modifications to file processing logic or database operations.
- Cloud readiness: The solution can be deployed to cloud environments by updating the DB_CONFIG and WATCH_FOLDER accordingly.
- Resilience: The script uses a file watcher to ensure no files are missed, and processed files are removed to prevent duplication.
- Scalability: While PostgreSQL can handle moderate volumes of data efficiently, for extremely large datasets, consider using a more scalable solution like Snowflake 
            (A cloud native data warehousing solution that offers excellent scalability, performance, and support for complex queries.)

## Performance Considerations
- CPU usage: The script uses minimal CPU when idle and processes files efficiently.
- Memory usage: Files are processed one at a time to minimize memory consumption.
- Execution time: Bulk inserts are used to minimize database roundtrips and improve performance.

## Assumptions
- Files are valid JSON and follow the specified format.
- The watch directory is accessible and has appropriate permissions.
- The PostgreSQL database is properly configured and accessible.
- The system has sufficient disk space to handle incoming files.
