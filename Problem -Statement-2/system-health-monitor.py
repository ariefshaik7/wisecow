import psutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define thresholds
CPU_THRESHOLD = 80.0
MEM_THRESHOLD = 80.0
DISK_THRESHOLD = 80.0

def check_system_health():
    """Monitors system health and logs alerts if thresholds are exceeded."""
    
    # Check CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        logging.warning(f"High CPU usage detected: {cpu_usage}%")
    
    # Check memory usage
    memory_info = psutil.virtual_memory()
    if memory_info.percent > MEM_THRESHOLD:
        logging.warning(f"High Memory usage detected: {memory_info.percent}%")
        
    # Check disk space
    disk_info = psutil.disk_usage('/')
    if disk_info.percent > DISK_THRESHOLD:
        logging.warning(f"Low Disk Space detected: {disk_info.percent}% used")
        
    # Check running processes
    process_count = len(psutil.pids())
    logging.info(f"Number of running processes: {process_count}")

if __name__ == "__main__":
    check_system_health()