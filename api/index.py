import os
import sys
import traceback
from pathlib import Path

print("=== STARTING VERCEL DEPLOYMENT ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

try:
    # Add project to Python path
    BASE_DIR = Path(__file__).resolve().parent.parent
    print(f"BASE_DIR: {BASE_DIR}")
    sys.path.append(str(BASE_DIR))
    
    # Check if we can find the project
    settings_path = BASE_DIR / "bkbookingtrucks" / "settings.py"
    print(f"Looking for settings at: {settings_path}")
    print(f"Settings exists: {settings_path.exists()}")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bkbookingtrucks.settings')
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    
    # Initialize Django
    print("Attempting to import django...")
    import django
    print(f"Django version: {django.__version__}")
    
    print("Calling django.setup()...")
    django.setup()
    print("django.setup() successful!")
    
    # Use WSGI instead of ASGI
    print("Importing WSGI application...")
    from django.core.wsgi import get_wsgi_application
    from asgiref.wsgi import WsgiToAsgi
    
    print("Creating WSGI application...")
    wsgi_app = get_wsgi_application()
    print("WSGI application created!")
    
    print("Converting WSGI to ASGI...")
    asgi_app = WsgiToAsgi(wsgi_app)
    print("ASGI application created!")
    
    # Export the handler
    handler = asgi_app
    app = asgi_app
    
    print("=== SUCCESS: handler and app variables created ===")
    print(f"handler type: {type(handler)}")
    print(f"app type: {type(app)}")
    
except Exception as e:
    print(f"\n=== ERROR OCCURRED ===")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print(f"\nFull traceback:")
    traceback.print_exc()
    
    # Create a simple fallback handler that shows the error
    async def error_handler(scope, receive, send):
        if scope['type'] == 'http':
            await send({
                'type': 'http.response.start',
                'status': 500,
                'headers': [
                    (b'content-type', b'text/plain; charset=utf-8'),
                ],
            })
            error_msg = f"Setup Error: {type(e).__name__}: {str(e)}".encode('utf-8')
            await send({
                'type': 'http.response.body',
                'body': error_msg,
            })
    
    # Still export handler and app even on error
    handler = error_handler
    app = error_handler
    print("\n=== Fallback handler created ===")