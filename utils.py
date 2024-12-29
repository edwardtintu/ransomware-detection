import math
import shutil

def calculate_entropy(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    if not data:
        return 0
    entropy = 0
    for byte in range(256):
        prob = data.count(byte) / len(data)
        if prob > 0:
            entropy -= prob * math.log(prob, 2)
    return entropy

def quarantine_file(file_path):
    quarantine_path = "/path/to/quarantine"  # Create this directory
    shutil.move(file_path, quarantine_path)
    print(f"Quarantined {file_path}")
