import os
import sys
import traceback
from pathlib import Path
from asgiref.wsgi import WsgiToAsgi


def create_app():
    print("=== STARTING VERCEL DEPLOYMENT ===")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")

    try:
        # BASE_DIR should be index.py's parent (api/) parent if Django is at root
        BASE_DIR = Path(__file__).resolve().parent.parent
        print(f"BASE_DIR: {BASE_DIR}")

        sys.path.insert(0, str(BASE_DIR))

        # Confirm settings file exists
        settings_path = BASE_DIR / "bkbookingtrucks" / "settings.py"
        print(f"Looking for settings at: {settings_path}")
        print(f"Settings exists: {settings_path.exists()}")

        # Django settings
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bkbookingtrucks.settings")
        print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

        # Django init
        print("Attempting to import django...")
        import django
        print(f"Django version: {django.__version__}")

        print("Calling django.setup()...")
        django.setup()
        print("django.setup() successful!")

        # Use WSGI → ASGI wrapper
        print("Importing WSGI application...")
        from django.core.wsgi import get_wsgi_application

        print("Creating WSGI application...")
        wsgi_app = get_wsgi_application()
        print("WSGI application created!")

        print("Converting WSGI to ASGI...")
        asgi_app = WsgiToAsgi(wsgi_app)
        print("ASGI application created!")

        print("=== SUCCESS: handler and app variables created ===")
        print(f"handler type: {type(asgi_app)}")
        print(f"app type: {type(asgi_app)}")

        return asgi_app

    except Exception as e:
        print("\n=== ERROR OCCURRED ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()

        # Fallback ASGI handler so Vercel still works
        async def error_handler(scope, receive, send):
            if scope["type"] == "http":
                await send({
                    "type": "http.response.start",
                    "status": 500,
                    "headers": [(b"content-type", b"text/plain; charset=utf-8")],
                })
                msg = f"Setup Error: {type(e).__name__}: {str(e)}".encode()
                await send({"type": "http.response.body", "body": msg})

        print("\n=== Fallback handler created ===")
        return error_handler


# MUST exist at module import time
app = create_app()
handler = app
