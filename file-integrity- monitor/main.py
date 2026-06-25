import os
import hashlib
import time

# Folder to monitor
FOLDER_TO_MONITOR = "monitored_folder"

# Log file
LOG_FILE = "log.txt"


# 🔹 Function to write logs
def write_log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")


# 🔹 Function to generate file hash
def get_file_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return None


# 🔹 Scan files and store hashes
def scan_files():
    file_hashes = {}

    for file_name in os.listdir(FOLDER_TO_MONITOR):
        file_path = os.path.join(FOLDER_TO_MONITOR, file_name)

        if os.path.isfile(file_path):
            file_hashes[file_name] = get_file_hash(file_path)

    return file_hashes


# 🔹 Start Program
print("=" * 50)
print("🔐 FILE INTEGRITY MONITOR (FINAL)")
print("=" * 50)

# Initial scan
old_hashes = scan_files()

print("Monitoring started...\n")
write_log("Monitoring started...\n")

# 🔁 Continuous Monitoring
while True:
    time.sleep(5)

    new_hashes = scan_files()

    # ✅ Check CREATED files
    for file_name in new_hashes:
        if file_name not in old_hashes:
            msg = f"[CREATED] {file_name}"
            print(msg)
            write_log(msg)

    # ❌ Check DELETED files
    for file_name in old_hashes:
        if file_name not in new_hashes:
            msg = f"[DELETED] {file_name}"
            print(msg)
            write_log(msg)

    # 🔄 Check MODIFIED files
    for file_name in old_hashes:
        if file_name in new_hashes:
            if old_hashes[file_name] != new_hashes[file_name]:
                msg = f"[MODIFIED] {file_name}"
                print(msg)
                write_log(msg)

    # Update old hashes
    old_hashes = new_hashes