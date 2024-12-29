import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Function to check if a file is likely encrypted
def is_encrypted(filepath):
    encrypted_extensions = ['.enc', '.locked', '.crypt', '.encrypted']
    _, extension = os.path.splitext(filepath)

    # Check for known encrypted extensions
    if extension in encrypted_extensions:
        return True

    # Attempt to read the file and check if it's readable text (optional)
    try:
        with open(filepath, 'rb') as f:
            content = f.read(256)  # Read a small part of the file
            if any(b > 127 for b in content):  # Check for non-text characters
                return True
    except Exception:
        return True  # Treat as encrypted if unreadable

    return False

# Function to scan the directory for existing encrypted files
def scan_directory_for_encrypted_files(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if is_encrypted(filepath):
                return True  # Stop if any encrypted file is found
    return False

# Event handler for monitoring new file changes
class FileChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        if is_encrypted(event.src_path):
            print("Ransomware detected: Encrypted file created during monitoring.")
            observer.stop()  # Stop monitoring after detecting ransomware
        else:
            print("File change detected, but no ransomware activity.")

# Start monitoring the directory
def start_monitoring(directory):
    event_handler = FileChangeHandler()
    global observer
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=True)
    observer.start()
    print("Monitoring directory for changes...")
    try:
        observer.join()  # Keep the observer running until it is stopped
    except KeyboardInterrupt:
        observer.stop()

# Main Execution - User input for directory
if __name__ == "__main__":
    directory_to_monitor = input("Enter the directory to monitor: ")

    if not os.path.isdir(directory_to_monitor):
        print("Error: Directory does not exist.")
    else:
        # Initial scan for existing encrypted files
        if scan_directory_for_encrypted_files(directory_to_monitor):
            print("Ransomware detected: Encrypted files exist in the directory.")
        else:
            print("No ransomware detected: No encrypted files found in the directory.")
            start_monitoring(directory_to_monitor)
