"""FastAPI app entrypoint (stub)."""
from apps.api.config import settings
from apps.api.routers import billing
from apps.api.routers import members
from apps.api.routers import sessions
from apps.api.routers import webhooks
from apps.api.routers import auth
from apps.api.routers import notifications
from apps.api.routers import reports
from apps.api.routers import audit
from apps.api.routers import exports
from apps.api.routers import integrations

class App:
    """Minimal app stub."""
    def __init__(self):
        self.routers = []

def create_app():
    """Factory."""
    app = App()
    app.routers.append(billing.ROUTES)
    app.routers.append(members.ROUTES)
    app.routers.append(sessions.ROUTES)
    app.routers.append(webhooks.ROUTES)
    app.routers.append(auth.ROUTES)
    app.routers.append(notifications.ROUTES)
    app.routers.append(reports.ROUTES)
    app.routers.append(audit.ROUTES)
    app.routers.append(exports.ROUTES)
    app.routers.append(integrations.ROUTES)
    return app

app = create_app()
