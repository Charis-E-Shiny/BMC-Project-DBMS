#!/usr/bin/env python
# Simple script to run the application in development mode

import os
from app import app

if __name__ == "__main__":
    # Set development mode
    os.environ['FLASK_ENV'] = 'development'
    
    # Run the application in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)