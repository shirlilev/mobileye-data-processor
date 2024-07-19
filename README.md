# Mobileye Data Processing System
This system processes JSON files containing object detection events and vehicle status updates, storing the data in a PostgreSQL database.

## Prerequisites
- Python 3.7+
- PostgreSQL 12+

## Installation
1. Clone this repository:
git clone https://github.com/shirlilev/mobileye-data-processor.git
cd mobileye-data-processor
2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate
3. Install the required packages:
pip install -r requirements.txt
4. Set up the PostgreSQL database: Create a new database named `mobileye_db`
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
## Options to Reduce CPU and Memory Usage
## If data are Not Large-Scale:
1. Load Files in Chunks with 'ijson':
   - Reduces memory usage by not loading the entire file into memory.
2. Concurrent Processing:
   - Multi-threading: For I/O-bound tasks, utilizes the same CPU core.
   - Multi-processing: For CPU-bound tasks, utilizes multiple CPU cores.
3. Batch Insertions:
   - Reduce overhead by inserting multiple rows into the database in one batch.
   - Store data temporarily in Python Pandas DataFrames for efficient manipulation.
4. Garbage Collection:
   - Manually trigger garbage collection to free up memory with the `gc` library.
## If data are Large-Scale:
1. Distributed Processing with Spark:
   - Process large-scale data across multiple nodes.
2. Data Streaming:
   - Use technologies like Apache Kafka for real-time data processing.
3. Optimized Storage Formats:
   - Use formats like Parquet for efficient storage and retrieval.
4. Horizontal Scaling:
   - Add more machines to distribute the load.
5. Cloud-Based Solutions:
   - Use cloud services like AWS S3 and AWS Lambda for scalable storage and processing.

## Assumptions
- Files are valid JSON and follow the specified format.
- The watch directory is accessible and has appropriate permissions.
- The PostgreSQL database is properly configured and accessible.
- The system has sufficient disk space to handle incoming files.
