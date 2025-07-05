# app/metrics/system_collector.py

import psutil
import asyncio
from .prometheus_exporter import CPU_USAGE_PERCENT, MEMORY_USAGE_PERCENT, PROCESS_CPU_USAGE_PERCENT, PROCESS_MEMORY_USAGE_BYTES

async def collect_system_metrics(interval: int = 5):
    """
    Asynchronous background task to collect and update system and process metrics.
    Updates Prometheus gauges periodically.
    """
    process = psutil.Process() # Get the current process

    while True:
        # System-wide metrics
        CPU_USAGE_PERCENT.set(psutil.cpu_percent(interval=None)) # Non-blocking call
        MEMORY_USAGE_PERCENT.set(psutil.virtual_memory().percent)

        # Process-specific metrics
        PROCESS_CPU_USAGE_PERCENT.set(process.cpu_percent(interval=None)) # Non-blocking call
        PROCESS_MEMORY_USAGE_BYTES.set(process.memory_info().rss) # Resident Set Size

        await asyncio.sleep(interval) # Wait for the specified interval

