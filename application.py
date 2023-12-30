import os

from app import app as application

if __name__ == "__main__":
    if 'nt' in os.name:
        application.run(debug=True)
    else:
        application.run()