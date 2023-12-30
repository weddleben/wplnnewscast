import os

from app import app as application

if 'nt' in os.name:
    application.run(debug=True)
else:
    application.run()