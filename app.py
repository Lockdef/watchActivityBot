import os

from router import app

port = os.environ.get('PORT', 8080)
host = '0.0.0.0'
app.run(host=host, port=port)
