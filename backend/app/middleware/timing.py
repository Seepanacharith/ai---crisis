import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("crisis_companion.middleware.timing")

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = (time.perf_counter() - start_time) * 1000
        response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
        
        # Log slow requests
        if process_time > 2000:
            logger.warning(f"SLOW REQUEST: {request.method} {request.url.path} took {process_time:.2f}ms")
            
        return response
