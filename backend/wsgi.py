# Entry point for running the Flask app using the app factory pattern
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
