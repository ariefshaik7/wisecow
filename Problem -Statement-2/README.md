# Shell Scripts

This collection includes scripts for system administration and monitoring tasks. Each script is designed to be a standalone tool for a specific purpose.

## 📜 Table of Contents

* [Backup Script (`backup.sh`)](./backup.sh)
    
* [Health Check Script (`health_check.sh`)](./health_check.sh)
    
* [System Health Monitor (`system_health_monitor.py`)](./system_health_monitor.py)
    

---

## 💾 Backup Script (`backup.sh`)

This script creates a compressed `tar.gz` archive of a specified source directory.

### Description

The script takes a source directory path as an argument and creates a timestamped backup of its contents. The backups are stored in a `~/backups` directory, and a log file (`~/backups/backup.log`) is maintained to record the success or failure of each backup operation.

### Usage

To run the script, make it executable and provide the path to the directory you want to back up.

Bash

```plaintext
chmod +x backup.sh
./backup.sh /path/to/your/directory
```

### Example

To back up the contents of a directory named `images` located on your desktop:

Bash

```plaintext
./backup.sh /home/desktop/images
```

Upon successful execution, a message will be printed to the console indicating the location of the archive file, and a success entry will be added to the log file. If it fails, a failure message will be logged.

---

## 🔗 URL Health Check Script (`health_check.sh`)

This script performs a simple health check on a given URL by examining its HTTP status code.

### Description

The script uses `curl` to send a request to the specified URL and checks the HTTP response code. If the status code is in the 2xx range (e.g., 200 OK), it reports that the application is "UP". Otherwise, it reports that the application is "DOWN".

### Usage

Make the script executable and pass the URL you want to check as an argument.

Bash

```plaintext
chmod +x health_check.sh
./health_check.sh <URL_TO_CHECK>
```

### Example

Bash

```plaintext
./health_check.sh https://example.com
```

### Exit Codes

* **0**: The application is UP (the script received a 2xx status code).
    
* **1**: The application is DOWN (the script received a non-2xx status code).
    

---

## 🖥️ System Health Monitor (`system_health_monitor.py`)

This Python script monitors basic system health metrics, including CPU, memory, and disk usage.

### Description

The script checks the system's current CPU usage, memory usage, and disk space usage. If any of these metrics exceed a predefined threshold (80%), it logs a warning message. It also logs the total number of currently running processes.

### Prerequisites

You need to have the `psutil` library installed.

Bash

```plaintext
pip install psutil
```

### Usage

Run the script using the Python interpreter.

Bash

```plaintext
python3 system_health_monitor.py
```

### Thresholds

The script uses the following thresholds, which can be modified within the script:

* **CPU Usage**: 80%
    
* **Memory Usage**: 80%
    
* **Disk Usage**: 80%