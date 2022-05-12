import sentry_sdk
import uvicorn
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app import app
from settings import get_settings

current_settings = get_settings()

app.add_middleware(SessionMiddleware, secret_key=current_settings.auth0_client_secret)

if current_settings.environment == 'production':
    sentry_sdk.init(dsn=current_settings.sentry_dsn)
    app = SentryAsgiMiddleware(app)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=current_settings.project_host,
        port=current_settings.project_port,
        reload=True,
        debug=True,
    )
