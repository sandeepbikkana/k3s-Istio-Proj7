from flask import Flask
import os
app = Flask(__name__)

version = os.environ.get('APP_VERSION', 'vX')

@app.route('/')
def hello():
    hostname = os.environ.get('HOSTNAME', 'unknown')
    return f"Hello from {version} - pod: {hostname}\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
