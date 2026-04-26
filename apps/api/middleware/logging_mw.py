import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"method={request.method} path={request.url.path} status=500 duration_ms={duration_ms:.2f}"
            )
            raise

        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            f"method={request.method} path={request.url.path} status={status_code} duration_ms={duration_ms:.2f}"
        )

        return response
