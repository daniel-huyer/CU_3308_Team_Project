# app.py
from app import create_app
import prefix

app = create_app()

# Insert the wrapper for handling PROXY when using csel.io virtual machine
# Calling this routine will have no effect if running on local machine
prefix.use_PrefixMiddleware(app)   

if __name__ == '__main__':
    app.run(host='localhost', port=3308, debug=True)