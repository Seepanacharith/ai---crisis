import time
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
from app.config import settings

class SimpleRateLimiter:
    def __init__(self, requests_per_minute: int = None):
        self.rpm = requests_per_minute or settings.RATE_LIMIT_PER_MINUTE
        # ip -> (count, reset_timestamp)
        self.clients: Dict[str, Tuple[int, float]] = {}

    def check(self, request: Request):
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()
        
        if client_ip in self.clients:
            count, reset_time = self.clients[client_ip]
            if now > reset_time:
                # Window expired, reset
                self.clients[client_ip] = (1, now + 60.0)
            else:
                if count >= self.rpm:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail={
                            "success": False,
                            "error": {
                                "code": "RATE_LIMIT_EXCEEDED",
                                "message": f"Rate limit of {self.rpm} requests per minute exceeded. Please try again shortly."
                            }
                        }
                    )
                self.clients[client_ip] = (count + 1, reset_time)
        else:
            self.clients[client_ip] = (1, now + 60.0)

rate_limiter = SimpleRateLimiter()
