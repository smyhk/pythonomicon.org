import os
from app import create_app

app = create_app(os.getenv("DEPLOYMENT_ENV") or "default")

if __name__ == '__main__':
    app.run()
