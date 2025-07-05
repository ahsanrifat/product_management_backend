# app/metrics/prometheus_exporter.py

from prometheus_client import Counter, Histogram, Gauge, generate_latest

# Define custom metrics
# Counter for total requests
REQUESTS_TOTAL = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'path', 'status_code']
)

# Histogram for request duration
REQUEST_DURATION_SECONDS = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'path']
)

# Gauge for CPU usage
CPU_USAGE_PERCENT = Gauge(
    'system_cpu_usage_percent',
    'Current system CPU usage in percent'
)

# Gauge for Memory usage
MEMORY_USAGE_PERCENT = Gauge(
    'system_memory_usage_percent',
    'Current system memory usage in percent'
)

# Gauge for process CPU usage (specific to the FastAPI process)
PROCESS_CPU_USAGE_PERCENT = Gauge(
    'process_cpu_usage_percent',
    'Current process CPU usage in percent'
)

# Gauge for process Memory usage (specific to the FastAPI process)
PROCESS_MEMORY_USAGE_BYTES = Gauge(
    'process_memory_usage_bytes',
    'Current process memory usage in bytes'
)

# Function to generate Prometheus metrics in text format
def get_prometheus_metrics():
    """Generates the latest Prometheus metrics in text format."""
    return generate_latest().decode('utf-8')

