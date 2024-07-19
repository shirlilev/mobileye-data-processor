from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from processor import process_file
from config import WATCH_FOLDER
from db import create_tables

class Watcher:
    def __init__(self, folder_to_watch):
        self.observer = Observer()
        self.folder_to_watch = folder_to_watch

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.folder_to_watch, recursive=False) # without subdirectories 
        self.observer.start()
        try:
            while True:                
                self.observer.join(1) # used to keep the main thread alive and give the observer time to monitor events        
        except KeyboardInterrupt:
            self.observer.stop() # when user stop the thread
        except Exception as e:
            print(f"Error in watcher: {e}")
        finally:            
            self.observer.join() # Ensures that the main thread waits for the observer thread to properly shut down before exiting

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory: # igonre directories
            return None
        elif event.event_type == 'created':
            try:
                process_file(event.src_path)
            except Exception as e:
                print(f"Error processing file {event.src_path}: {e}")

if __name__ == '__main__':
    try:
        create_tables()
        watch_folder = WATCH_FOLDER
        watcher = Watcher(watch_folder)
        watcher.run()
    except Exception as e:
        print(f"Error in main execution: {e}")
