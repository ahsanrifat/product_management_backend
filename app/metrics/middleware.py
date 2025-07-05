# app/metrics/middleware.py

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match
from prometheus_client import generate_latest

from .prometheus_exporter import REQUESTS_TOTAL, REQUEST_DURATION_SECONDS

class PrometheusMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware to collect HTTP request metrics for Prometheus.
    It records total requests and request duration, categorized by method, path, and status code.
    """
    async def dispatch(self, request: Request, call_next):
        method = request.method
        path_template = self._get_path_template(request)

        # Record request start time
        start_time = time.time()

        response = await call_next(request)

        # Record request duration
        process_time = time.time() - start_time

        # Update Prometheus metrics
        REQUESTS_TOTAL.labels(method=method, path=path_template, status_code=response.status_code).inc()
        REQUEST_DURATION_SECONDS.labels(method=method, path=path_template).observe(process_time)

        return response

    def _get_path_template(self, request: Request) -> str:
        """
        Attempts to find the path template for the given request.
        This is important for grouping metrics by endpoint, not by specific URL parameters.
        """
        for route in request.app.routes:
            match, scope = route.matches(request.scope)
            if match == Match.FULL:
                return route.path
        return request.url.path # Fallback to actual path if no route template found

