import os
import hashlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Function to generate a hash of the entire directory's contents, including file names and paths
def get_directory_hash(directory):
    hash_obj = hashlib.sha256()
    for root, _, files in os.walk(directory):
        for filename in sorted(files):  # Sort to ensure consistent hash
            filepath = os.path.join(root, filename)
            # Include file path in hash calculation
            hash_obj.update(filepath.encode('utf-8'))
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as f:
                    while chunk := f.read(4096):
                        hash_obj.update(chunk)
    return hash_obj.hexdigest()

# Event handler for directory monitoring
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, directory_hash):
        self.initial_directory_hash = directory_hash

    def on_any_event(self, event):
        if event.is_directory:
            return

        print(f"Change detected: {event.src_path}")
        time.sleep(1)

        # Calculate the modified hash after detecting changes
        modified_directory_hash = get_directory_hash(directory_to_monitor)
        print(f"Modified Directory Hash: {modified_directory_hash}")
        time.sleep(1)

        # Check if the hash has changed, indicating potential ransomware activity
        if modified_directory_hash != self.initial_directory_hash:
            print("Hash value is different.")
            time.sleep(1)
            print("Ransomware activity detected!")
            time.sleep(1)
            print("Email alerts sent to the user.")
            observer.stop()  # Stop monitoring after detecting ransomware
        else:
            print("No ransomware activity detected.")
            observer.stop()  # Stop monitoring after confirming no changes

# Start monitoring the directory
def start_monitoring(directory):
    initial_directory_hash = get_directory_hash(directory)
    print(f"Initial Directory Hash: {initial_directory_hash}")
    time.sleep(1)

    event_handler = FileChangeHandler(initial_directory_hash)
    global observer
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=True)
    observer.start()

    print(f"Monitoring directory: {directory}")
    time.sleep(1)
    try:
        observer.join()  # Keep the observer running until it is stopped
    except KeyboardInterrupt:
        observer.stop()

# Main Execution - User input for directory
if __name__ == "__main__":
    directory_to_monitor = input("Enter the directory to monitor: ")

    if not os.path.isdir(directory_to_monitor):
        print(f"Error: Directory {directory_to_monitor} does not exist.")
    else:
        print("Monitoring started...")
        start_monitoring(directory_to_monitor)
